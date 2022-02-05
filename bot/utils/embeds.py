import discord
import random
import datetime

class Embeds:
    """Embed for handling errors"""
    def __init__(self):
        self.cooldown_choices = [
            "Woah, slow down man",
            "A little too quick there",
            "Too fast man",
            "Spamming is not cool"
        ]
        self.time = datetime.datetime.utcnow().strftime('%Y:%m:%d %H:%M:%S')
        
    def OnCooldown(self, error: str):
        """Returns an embed for when a command is on cooldown"""
        cooldown_name = random.choice(self.cooldown_choices)
        return discord.Embed(
            title=cooldown_name,
            description=f"You need to slow down and don't spam the "
            f"bot\n Retry after {round(error.retry_after, 2)}s",
            color=discord.Color.blue(),
        )

    def OnError(self, command_name: str, time: str, reason: str):
        """Returns an embed for when a command raises an error"""
        Embed = discord.Embed(title="Oh no an error occurred", color=discord.Color.red())
        Embed.add_field(name="Command Name: ", value=command_name)
        Embed.add_field(name="At: ", value=time)
        Embed.add_field(name="Reason", value=reason)
        return Embed
