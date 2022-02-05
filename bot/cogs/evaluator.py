import discord
import re
from discord.ext import commands
from jishaku.codeblocks import codeblock_converter

class EvaluatorCog(commands.Cog):
    """The cog that is for evaluation commands"""
    def __init__(self, bot):
        self.bot = bot
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")
        
    @property
    def session(self):
        """Session for making requests"""
        return self.bot.http._HTTPClient__session

    async def _run_code(self, *, lang: str, code: str):
        """Run code by sending a request to piston executor"""
        res = await self.session.post(
            "https://emkc.org/api/v1/piston/execute",
            json={"language": lang, "source": code},
        )
        return await res.json()
    
    def _format_embed(self, result: dict):
        """Embed for code execution"""
        output = result["output"]
        output = output[:500].strip()
        shortened = len(output) > 500
        lines = output.splitlines()
        shortened = shortened or (len(lines) > 15)
        output = "\n".join(lines[:15])
        output += shortened * "\n\n**Output shortened**"
        
        return discord.Embed(title="Code Evaluation", description=f"```{result['language']}\n{output}```")
    

    @commands.command(name='run', aliases=['exec', 'execute'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _run(self, ctx: commands.Context, *, codeblock: str):
        """Run code and get results instantly using codeblocks."""
        matches = self.regex.findall(codeblock)
        
        code = matches[0][2]
        lang = matches[0][0] or matches[0][1]
        
        result = await self._run_code(lang=lang, code=code)
        
        await ctx.send(embed = self._format_embed(result))

    @commands.command(name='eval')
    @commands.has_permissions(administrator=True)
    async def _eval(self, ctx, *, code: codeblock_converter):
        """Eval some code"""
        cog = self.bot.get_cog("Jishaku")
        await cog.jsk_python(ctx, argument=code)
    
def setup(bot):
    bot.add_cog(EvaluatorCog(bot))
