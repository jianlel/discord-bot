import discord
from discord.ext import commands

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Commands",
            description="Play WORDLE and BANLUCK (WIP) with this bot!",
            color=discord.Color.blurple()
        )
        embed.add_field(name="!wordle", value="Start a Wordle game", inline=False)
        embed.add_field(name="!daily", value="Start the daily Wordle challenge", inline=False)
        embed.add_field(name="!stats", value="See your Wordle stats", inline=False)
        embed.add_field(name="!streak", value="Check your current streak", inline=False)
        embed.add_field(name="!guess", value="Submit a guess for your current game", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Helper(bot))