import discord
from discord.ext import commands
import sys
import asyncio
import datetime
from ..utils import Embeds


class CommandErrorHandler(commands.Cog):
    """The cog that handles errors"""
    def __init__(self, client):
        self.client = client
        self.time = datetime.datetime.utcnow().strftime('%Y:%m:%d %H:%M:%S')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            error = error.original
        except Exception:
            error = error
        if isinstance(error, commands.NoPrivateMessage):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The command can not be used in private "
                                                                            "messages")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = Embeds().OnError(
                ctx.command.qualified_name,
                self.time,
                'The command is missing required arguments',
            )

            await ctx.send(embed=embed)
        elif isinstance(error, commands.DisabledCommand):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The command is currently disabled and "
                                                                            "cannot be used")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = Embeds().OnCooldown(error=str(error))
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.NotOwner):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The command is only used by the owner")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ChannelNotFound):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The channel couldn't be found")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The user couldn't be found")
            await ctx.send(embed=embed)
        elif isinstance(error, discord.Forbidden):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "I am forbidden to do this")
            await ctx.send(embed=embed)
        elif isinstance(error, discord.NotFound):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "Couldn't find what you need")
            await ctx.send(embed=embed)
        elif isinstance(error, asyncio.TimeoutError):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "You have been timed out because you "
                                                                            "didn't respond in time")
            await ctx.send(embed=embed)
        elif isinstance(error, discord.HTTPException):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "Something went wrong... Please Contact: "
                                                                            "Jerrydotpy#4249 if it keeps happening")
            await ctx.send(embed=embed)
        if not isinstance(error, discord.HTTPException):
            try:
                print(error, file=sys.stderr)
            except Exception:
                print(error, file=sys.stderr)
        else:
            print(error, file=sys.stderr)


def setup(client):
    client.add_cog(CommandErrorHandler(client))
