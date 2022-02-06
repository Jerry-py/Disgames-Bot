import asyncio
import discord
import math
import os
import urllib.request
from discord.ext import commands
from ..utils import resolve_expr

class CalcView(discord.ui.View):
    def __init__(self, ctx : commands.Context, embed : discord.Embed):
        self.ctx = ctx
        self.embed = embed
        self._all_ans = [0]
        self.equation = ""
        super().__init__(timeout=120)
        
    def parse_equation(self):
        new_equation = self.equation.replace("%", " / 100")
        new_equation = new_equation.replace("x", "*")
        new_equation = new_equation.replace("÷", "/")
        new_equation = new_equation.replace("^", "**")
        new_equation = new_equation.replace("Ans", f"{self._all_ans[0]}")
        new_equation = new_equation.replace("π", "3.141592653589793")
        return new_equation    
    
    async def calculate(self):
        """Calculate the equation"""
        try:
            ans = resolve_expr(self.parse_equation())
            self._all_ans[0] = ans
        except Exception as e:
            self._all_ans[0] = 0
            ans = "Error! Make sure you closed your parenthesis and brackets!\n\n Do not do `number(...)` Instead use `number x (...)`\n Do not combine numbers into each other - Ex: `π6^2` Instead do `π*6^2` \n**They Will Result In Different Answers!**"
        self.equation = ""
        
        return ans
    
    def _remove_placeholder(self):
        self.embed.description = ""
        
    def _placeholder(self):
        self.embed.description = "`Enter your equation below`"
        
    def new_equation(self, value : str):
        self.equation += value
        
    def new_embed(self, value : str):
        self.new_equation(value)
        self.embed.description = f"```{self.equation}```"
        return self.embed
    
    @discord.ui.button(row=0, label="^", style=discord.ButtonStyle.secondary)
    async def power(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the exponent operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=0, label="(", style=discord.ButtonStyle.success)
    async def left_parathesis(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the left parenthesis to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=0, label=")", style=discord.ButtonStyle.success)
    async def right_parenthesis(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the right parenthesis to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=0, label="AC", style=discord.ButtonStyle.danger)
    async def ac(self, button : discord.ui.Button, inter : discord.Interaction):
        """Delete the last character of the equation"""
        await inter.response.defer()
        if len(self.equation) <= 1:
            self._placeholder()
        else:
            self.equation = self.equation.rstrip(self.equation[-1])
            self.embed.description = self.equation
        await inter.edit_original_message(embed=self.embed)
    
    @discord.ui.button(row=0, label="CE", style=discord.ButtonStyle.danger)
    async def ce(self, button : discord.ui.Button, inter : discord.Interaction):
        """Clear the equation"""
        await inter.response.defer()
        self._placeholder()
        self.equation = ""
        await inter.edit_original_message(embed=self.embed)
    
    @discord.ui.button(row=1, label="%", style=discord.ButtonStyle.secondary)
    async def percentage(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the percentage operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=1, label="7", style=discord.ButtonStyle.success)
    async def seven(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 7 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=1, label="8", style=discord.ButtonStyle.success)
    async def eight(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 8 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=1, label="9", style=discord.ButtonStyle.success)
    async def nine(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 9 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=1, label="÷", style=discord.ButtonStyle.secondary)
    async def divide(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the division operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="Ans", style=discord.ButtonStyle.secondary)
    async def ans(self, button : discord.ui.Button, inter : discord.Interaction):
        """Get previous answer"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="6", style=discord.ButtonStyle.success)
    async def six(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 6 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="5", style=discord.ButtonStyle.success)
    async def five(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 5 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="4", style=discord.ButtonStyle.success)
    async def four(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 4 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="x", style=discord.ButtonStyle.secondary)
    async def multiply(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the mutiplication operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="log(", style=discord.ButtonStyle.secondary)
    async def log(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the sin math function to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="3", style=discord.ButtonStyle.success)
    async def three(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 3 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="2", style=discord.ButtonStyle.success)
    async def two(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 2 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="1", style=discord.ButtonStyle.success)
    async def one(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the number 1 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="-", style=discord.ButtonStyle.secondary)
    async def subtract(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add the subtract operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=4, label="π", style=discord.ButtonStyle.secondary)
    async def pi(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add Cos math function"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=4, label="0", style=discord.ButtonStyle.success)
    async def zero(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add zero to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=4, label="(.)", style=discord.ButtonStyle.secondary)
    async def decimal(self, button : discord.ui.Button, inter : discord.Interaction):
        """Add a decimal to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed('.'))
    
    @discord.ui.button(row=4, label="=", style=discord.ButtonStyle.primary)
    async def solve(self, button : discord.ui.Button, inter : discord.Interaction):
        """Solve the equation"""
        await inter.response.defer()
        ans = await self.calculate()
        self.embed.description = str(ans)
        await inter.edit_original_message(embed=self.embed)
    
    @discord.ui.button(row=4, label="+", style=discord.ButtonStyle.secondary)
    async def add(self, button : discord.ui.Button, inter : discord.Interaction):
        """Math Add operation Button"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    async def interaction_check(self, inter : discord.Interaction):
        """Check if the user who used the the interaction is the author of the message"""
        if inter.user == self.ctx.author:
            return True
        await inter.response.send_message("Hey! You can't do that!", ephemeral=True)
        return False


class FunCog(commands.Cog):
    """The cog that is for fun commands"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='calc', aliases=['calculate', 'calculator'])
    async def calc(self, ctx : commands.Context):
        embed = discord.Embed(title='Calculator', description='`Enter your equation below`')
        await ctx.send(embed=embed, view=CalcView(ctx, embed))
        
    @property
    def session(self):
        """Session for making requests"""
        return self.bot.http._HTTPClient__session
        
    @commands.command(name='ttsobama')
    async def _ttsobama(self, ctx, *, text: str = None):
        if text is None:
            return await ctx.send("You need to enter text!")

        if len(text) > 280:
            return await ctx.send("Text is too long!")
        await ctx.send('Your video is loading... Might take up to 5-12 seconds', delete_after=12)

        response = self.session.post(url='http://talkobamato.me/synthesize.py', data={
            "input_text": text
        })
        await asyncio.sleep(12)
        url = response.url.replace('http://talkobamato.me/synthesize.py?speech_key=', '')
        url = 'http://talkobamato.me/synth/output/' + url + '/obama.mp4'
        await asyncio.sleep(1)
        urllib.request.urlretrieve(url, 'obama.mp4')
        file = discord.File('obama.mp4')
        await ctx.send(file=file)
        os.remove('obama.mp4')
        
    @commands.command(name='shorten', aliases=['urlshorten'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _shorten(self, ctx, *, url):
        o = urllib.parse.quote(url, safe='/ :')

        e = await self.session.get(f'https://is.gd/create.php?format=json&url={o}').json()

        return await ctx.send(f"<{e['result_url']}>")
    
    @commands.group(name='qr', invoke_without_command=True, description="Make a QR code!")
    async def qr(self, ctx, value=None):
        if value is None:
            o = ctx.message.attachments[0].url
        o = urllib.parse.quote(value)

        await ctx.send(f'https://api.qrserver.com/v1/create-qr-code/?data={o}')

    @qr.command(name="read")
    async def _read(self, ctx, image=None):
        if image is not None:
            url = urllib.parse.quote(image)

        else:
            if len(ctx.message.attachments) > 1:
                return await ctx.send("We can only decode one QR code at a time.")

            elif len(ctx.message.attachments) < 1:
                return await ctx.send("You have to add some type of QR code for us to decode.")

            url = urllib.parse.quote(ctx.message.attachments[0].url)

        try:
            res = await self.get_data('json', f'https://api.qrserver.com/v1/read-qr-code/?fileurl={url}')
        except Exception as e:
            return await ctx.send(f"I couldn't find any QR codes in that image.\nError: {e}")

        await ctx.send(res[0]['symbol'][0]['data'])
    
def setup(bot):
    bot.add_cog(FunCog(bot))
