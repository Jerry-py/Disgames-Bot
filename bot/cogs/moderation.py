import discord
from discord.ext import commands
from ..utils import BelowMemberConverter, ToSeconds
import humanize
import datetime


class BelowMember(discord.Member):
    pass

commands.converter.BelowMemberConverter = BelowMemberConverter
BelowMember.__module__ = "discord.belowmember"


class ModerationCog(commands.Cog):
    """The cog that is for moderation commands. This is mostly from https://github.com/The-Coding-Realm/coding-bot-v4/blob/main/cogs/mod.py"""
    def __init__(self, bot):
        self.bot = bot
        
    async def _execute(self, ctx, coro):
        try:
            await coro
        except discord.errors.Forbidden:
            await ctx.send(embed=ctx.error('I do not have permission to interact with that user'))

    def mute_role(self, ctx):
        if mute_role := (
            [role for role in ctx.guild.roles if 'muted' in role.name.lower()]
        ):
            mute_role = mute_role[0],
        else:
            'I couldn\'t find a mute role'
            
    def _log_embed(self, target, color, reason, moderator, duration, icon, action_string):
        description = (f'**{icon} {action_string.title()} {target.name}**#'
                       f'{target.discriminator} *(ID: {target.id})* \n**'
                       f':page_facing_up: Reason:** {reason}') + (' \n**:clock2: Duration:** '
                                                                  f'{humanize.precisedelta(duration)}') if duration else ''
        embed = discord.Embed(description=description, color=color, timestamp=datetime.datetime.now(datetime.timezone.utc))
        embed.set_author(name=f'{moderator} (ID: {moderator.id}', icon_url=moderator.avatar.url)
        embed.set_thumbnail(url=target.avatar.url)
        return embed
        
        
    def _logging_action(self, **kwargs):
        action = kwargs.pop('action')
        moderator = kwargs.pop('moderator')
        target = kwargs.pop('target')
        undo = kwargs.get('undo')
        reason = kwargs.get('reason')
        duration = kwargs.get('duration')
        if undo:
            color = discord.Color.green()
        if action == 'kick':
            if undo:
                raise ValueError('Cannot un-kick')
            color = discord.Color.orange()
            action_string = 'kicked'
            icon = ':boot:'
        elif action == 'ban':
            if undo:
                action_string = 'unbanned'
                icon = ':unlock:'
            else:
                color = discord.Color.red()
                action_string = 'banned'
                icon = ':hammer:'
        elif action == 'warn':
            warn = kwargs.get('warn')
            if undo:
                if warn:
                    action_string = f'removed warning ({warn}) from'
                else:
                    action_string = 'removed all warnings from'
                icon = ':flag_white:'
            else:
                color = discord.Color.yellow()
                action_string = 'warned'
                icon = ':warning:'
        elif action == 'mute':
            if undo:
                action_string = 'unmuted'
                icon = ':loud_sound:'
            else:
                color = discord.Color.grey()
                action_string = 'muted'
                icon = ':mute:'
        elif action == 'timeout':
            if undo:
                action_string = 'un-timed out'
                icon = ':loud_sound:'
            else:
                color = discord.Color.grey()
                action_string = 'timeout'
                icon = ':x:'
        else:
            raise ValueError('Incorrect Type')
        return self._log_embed(target, color, reason, moderator, duration, icon, action_string)
        
 
    async def _log(self, **kwargs):
        await self.logs.send(embed=self._logging_action(**kwargs))
    
    @commands.command(name="purge", aliases=['clear', 'clean'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True, manage_messages=True)
    async def _purge(self, ctx : commands.Context, limit : int):
        """Purge messages from the channel"""
        purged = await ctx.channel.purge(limit)
        await ctx.send(f'Cleared {len(purged)} messages', delete_after=15)

    
    @commands.command(name="ban")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def _ban(self, ctx : commands.Context, target : BelowMemberConverter, reason : str):
        """Ban the user from the guild"""
        await self.log(action='ban', moderator=ctx.author, target=target, reason=reason)
        await self.execute(ctx, target.ban(reason=f'{ctx.author.id}: {reason}'))
        await ctx.send(embed=discord.Embed(title=':hammer: Member Banned :hammer:',
            description=f'{target.mention} has been banned \nReason: {reason}'))
    
    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def _unban(self, ctx : commands.Context, target : BelowMemberConverter, reason : str):
        """Ban the user from the guild"""
        await self.log(action='ban', moderator=ctx.author, target=target, reason=reason, undo=True)
        await self.execute(ctx, ctx.guild.unban(target, reason=f'{ctx.author.id}: {reason}'))
        await ctx.send(embed=discord.Embed(title=':unlock: Member Unbanned :unlock:',
            description=(f'{target.mention} has been unbanned \nReason: '
                         f'{reason}')))
    
    @commands.command(name="massban")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def _massban(self, ctx : commands.Context, *targets : commands.Greedy[BelowMember], reason : str):
        """Mass ban the users from the guild"""
        users = []
        for target in targets:
            users.append(target.name)
            await self.execute(ctx, target.ban(reason=f'{ctx.author.id}: {reason}'))
            await self.log(action='ban', moderator=ctx.author, target=target, reason=reason)

        await ctx.send(embed=discord.Embed(title=':hammer: Member Unbanned :hammer:',
            description=(f'{", ".join(users)} has been unbanned \nReason: '
                         f'{reason}')))
            
    
    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def _kick(self, ctx : commands.Context, target : BelowMemberConverter, reason : str):
        """Kicks the user from the guild"""
        await self.log(action='kick', moderator=ctx.author, target=target, reason=reason)
        await self.execute(ctx, target.kick(reason=f'{ctx.author.id}: {reason}'))
        await ctx.send(embed=discord.Embed(title=':boot: Member Kicked :boot:',
            description=f'{target.mention} has been kicked \nReason: {reason}'))
    
    @commands.command(name="mute")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_users=True)
    async def _mute(self, ctx : commands.Context, target : BelowMemberConverter, duration : ToSeconds, *, reason : str = None):
        """Mute the user from the guild"""
        await self.log(action='mute', moderator=ctx.author, target=target, duration=duration, reason=reason)
        await self.execute(ctx, target.add_roles(self.mute_role(ctx), reason=f'{ctx.author.id}: {reason}'))
        await ctx.send(embed=discord.Embed(title=':mute: Member Muted :mute:',
            description=(f'{target.mention} has been muted \nReason: {reason} \n'
                         f'**Duration**: {duration}')))
        
    @commands.command(name="unmute")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_users=True)
    async def _unmute(self, ctx : commands.Context, target : BelowMemberConverter, reason : str = None):
        """Unmute the user from the guild"""
        await self.log(action='mute', moderator=ctx.author, target=target, reason=reason, undo=True)         
        await self.execute(ctx, target.add_roles(self.mute_role, reason=f'{ctx.author.id}: {reason}'))
        await ctx.send(embed=discord.Embed(title=':loud_sound: Member Unmuted :loud_sound:',
            description=(f'{target.mention} has been unmuted \nReason: '
                         f'{reason}')))
    
    @commands.command(name="timeout")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_users=True)
    async def _timeout(self, ctx : commands.Context, target : BelowMemberConverter, duration : ToSeconds, *, reason : str = None):
        """Timeout the user from the guild"""
        await target.timeout(duration, reason)
        await self.log(action='timeout', moderator=ctx.author, target=target, reason=reason)         
        await ctx.send(embed=discord.Embed(title=':x: Member Timeout :x:',
            description=(f'{target.mention} has been timeout \nReason: {reason} \n'
                         f'**Duration**: {duration}')))
    
    @commands.command(name="untimeout")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_users=True)
    async def _untimeout(self, ctx : commands.Context, target : BelowMemberConverter, reason : str = None):
        """Untimeout the user from the guild"""
        await target.remove_timeout(reason)
        await self.log(action='timeout', moderator=ctx.author, target=target, reason=reason, undo=True)         
        await ctx.send(embed=discord.Embed(title=':loud_sound: Member Untimeout :loud_sound:',
            description=(f'{target.mention} has been untimeout \nReason: '
                         f'{reason}')))
    
    @commands.command(name="slowmode")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    async def _slowmode(self, ctx : commands.Context, delay: ToSeconds):
        """Change the slowmode of the channel"""
        if delay > 120:
            return await ctx.send('Slowmode cannot be greater than 120 seconds')
        await ctx.channel.edit(slowmode_delay=delay)
        await ctx.send(embed=ctx.embed(title='Successfully changed slowmode',
                                       description=f'Set to {delay} seconds'))        
        
        
    @commands.command(name="nickname", aliases=['rename'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_nicknames=True)
    async def _nickname(self, ctx, target: BelowMemberConverter, *, nick=None):
        """Change the nickname of the the user"""
        await target.edit(nick=nick)
        await ctx.send(embed=ctx.embed(title='Updated Nickname',
                                       description=f'Updated the nickname of {target.mention} to {nick}' if nick else f'Removed the nickname of {target.mention}'))
    
def setup(bot):
    bot.add_cog(ModerationCog(bot))
