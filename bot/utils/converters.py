import discord
import humanize
import time_str
from discord.ext import commands


def secondsToTime(seconds):
    """Convert seconds to time"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    return "%d Weeks %d Days %d Hours %d Minutes %d Seconds" % (weeks, days, hours, minutes, seconds)

def UpperCase(text : str):
    """Returns Uppercase text."""
    return text.upper()

def LowerCase(text : str):
    """Returns Lowercase text."""
    return text.lower()

def Capitalize(text : str):
    """Returns Capitalized text."""
    return text.capitalize()

class JoinDistance:
    """Returns the distance between two dates in a human readable format."""
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @classmethod
    async def convert(cls, ctx, argument):
        """Get the member's joined date and created date"""
        member = await commands.MemberConverter().convert(ctx, argument)
        return cls(member.joined_at, member.created_at)

    @property
    def delta(self):
        """Get the delta time of joined and created date"""
        return self.joined - self.created

class JoinDistanceConverter(commands.MemberConverter):
    """Find the join distance of a member"""
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return JoinDistance(member.joined_at, member.created_at)

class BelowMemberConverter(commands.MemberConverter):
    """Check if the member is below the author or higher than the author"""
    async def convert(self, ctx, *args, **kwargs):
        res = await super().convert(ctx, *args, **kwargs)
        if ctx.author.top_role.position <= res.top_role.position: raise commands.CheckFailure(
            'You do not have permissions to interact with that user')
        return res

class ToSeconds:
    """Converts time string to seconds"""
    def __init__(self, time):
        time = time_str.convert(time).total_seconds()
        return time

def Clean_String(string : discord.Message):
    """Clean a string"""
    return commands.clean_content(discord.utils.escape_markdown(string))
