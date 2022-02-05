import discord
import sys
from discord.ext import commands
from .utils import Config
from tortoise import Tortoise


def _prefix_callable(bot, message):
    base = ['ds!', 'Ds!', 'dS!', 'DS!', 'ds! ', 'ds! ', 'Ds! ', 'dS! ', 'DS! ']
    return commands.when_mentioned_or(*base)(bot, message)


initial_extensions = [
    'bot.cogs.evaluator',
    'bot.cogs.fun',
    #'bot.cogs.handler',
    'bot.cogs.moderation',
    'bot.cogs.tags'
]

utils_extension = [
    'bot.utils.config',
    'bot.utils.converters',
    'bot.utils.embeds',
    'bot.utils.models',
    'bot.utils.pagination',
    'bot.utils.request',
    'bot.utils.solver'
]

additional_extensions = [
    'jishaku',
    #'disgames'
]


class Bot(commands.Bot):
    def __init__(self):
        prefixes = _prefix_callable
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        super().__init__(
            command_prefix=prefixes, 
            case_insensitive=True, 
            strip_after_prefix=True, 
            intents=discord.Intents.all(),
            allowed_mentions=allowed_mentions
        )
        self.statuses = "for ds!help"
        
    @property
    def config(self):
        return Config
    
    def load_all_cogs(self):
        # for extension in initial_extensions:
            # try:
                # self.load_extension(extension)   
            # except Exception as e:
                # print(f'Failed to load extension {extension}.', file=sys.stderr)
        for extension in initial_extensions:
            self.load_extension(extension)
        for extension in additional_extensions:
            try:
                self.load_extension(extension)   
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)

    def load_cog(self, cog):
        try:
            self.load_extension(cog)
        except Exception as e:
            print(f'Failed to load extension {cog}.', file=sys.stderr)
            
    def unload_cog(self, cog):
        try:
            self.unload_extension(cog)
        except Exception as e:
            print(f'Failed to load extension {cog}.', file=sys.stderr)

    def reload_cog(self, cog):
        try:
            self.unload_cog(cog)
            self.load_cog(cog)
        except Exception as e:
            print(f'Failed to load extension {cog}.', file=sys.stderr)
        
    async def on_ready(self):
        print("Bot Online")
        await Tortoise.init(
            db_url="sqlite://bot/db/database.db", modules={"models": ["bot.utils.models"]}
        )
        await Tortoise.generate_schemas()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.statuses))
        self.load_all_cogs()
        
    async def close(self):
        print("Bot Offline")

    def run(self):
        super().run(self.config().__getitem__(item='TOKEN'), reconnect=True)
