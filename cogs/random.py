from discord import Embed
from discord.ext import commands
from discord.utils import get
import discord

from random import choice, randint
from requests import get as rget

class Random(commands.Cog, name='Random'):
    """
    Can be used by anyone, you'll find games and random related commands here.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Du toss [heads/tails]', description='Make a coin toss against the bot')
    async def toss(self, ctx, arg):
        if arg.lower() == 'heads' or arg.lower() == 'tails':
            piece = choice(['heads', 'tails'])
            if arg.lower() in piece:
                await ctx.send(f':white_check_mark: {piece}! You won.')
            else:
                await ctx.send(f':negative_squared_cross_mark:  {piece}! You lost.')
        else:
            await ctx.send('❌ You must input either "heads" or "tails"!')         

    @commands.command(brief='Du poke', description="Mention someone randomly.")
    async def poke(self, ctx):
        members = [x for x in ctx.guild.members if not x.bot]
        await ctx.send(f'Hey {choice(members).mention} !')

    @commands.command(aliases=['r'], brief='Du roll [x]', description="Roll a [x] sided dice")
    async def roll(self, ctx, faces: int):
        number = randint(1, faces)
        await ctx.send(f'🎲 You rolled a {number} !')

    @commands.command(brief='Du meme', description='Watch a random meme from reddit')
    async def meme(self, ctx):
        data = rget('https://meme-api.herokuapp.com/gimme').json()
        embed = (Embed(title=f":speech_balloon: r/{data['subreddit']} :", color=0x3498db)
                .set_image(url=data['url'])
                .set_footer(text=data['postLink']))
        await ctx.send(embed=embed)

    @commands.command(brief='Du rep [text]', description='Bot will repeat the text')
    async def rep(self, ctx, *, text):
        await ctx.send(text)

    @commands.command(brief='Du ping', description='Checks wheather bot is online or not.')
    async def ping(self, ctx):
        await ctx.send("Yes Yes I'm online. Stop checking me out...")

    @commands.command(brief='Du avt [member]', description='Gives avatar of the person.')
    async def avt(self, ctx, avamember : discord.Member=None):
        temp=discord.Embed(title='Here\'s your requested Avatar', color=randint(0, 0xffffff))
        temp.set_image(url=avamember.avatar_url)
        await ctx.send(embed=temp)
        


async def setup(bot):
    bot.add_cog(Random(bot))