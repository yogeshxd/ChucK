from discord import Embed
from discord.ext import commands
from discord.utils import get

from datetime import datetime

import aiohttp
import asyncio
import random
from random import choice, randint
from requests import get as rget

class Random(commands.Cog, name='Random'):
    """
    Can be used by anyone, you'll find games and random related commands here.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='24h toss [heads/tails]', description='Make a coin toss against the bot')
    async def toss(self, ctx, arg):
        if arg.lower() == 'heads' or arg.lower() == 'tails':
            piece = choice(['heads', 'tails'])
            if arg.lower() in piece:
                await ctx.send(f':white_check_mark: {piece}! You won.')
            else:
                await ctx.send(f':negative_squared_cross_mark:  {piece}! You lost.')
        else:
            await ctx.send('❌ You must input either "heads" or "tails"!')         

    @commands.command(brief='24h poke', description="Mention someone randomly.")
    async def poke(self, ctx):
        members = [x for x in ctx.guild.members if not x.bot]
        await ctx.send(f'Hey {choice(members).mention} !')

    @commands.command(aliases=['r'], brief='Du roll [x]', description="Roll a [x] sided dice")
    async def roll(self, ctx, faces: int):
        number = randint(1, faces)
        await ctx.send(f'🎲 You rolled a {number} !')

    @commands.command(brief='24h meme', description='Watch a random meme from reddit')
    async def meme(self, ctx):
        data = rget('https://meme-api.com/gimme/SaimanSays').json()
        embed = (Embed(title=f":speech_balloon: r/{data['subreddit']} :", color=0x3498db)
                .set_image(url=data['url'])
                .set_footer(text=data['postLink']))
        await ctx.send(embed=embed)

    @commands.command(brief='24h rep [text]', description='Bot will repeat the text')
    async def rep(self, ctx, *, text):
        await ctx.send(text)

    @commands.command(brief='24h ping', description='Checks wheather bot is online or not.')
    async def ping(self, ctx):
        await ctx.send("Yes Yes I'm online my baby...")

    # @commands.command(brief='24h avt [member]', description='Gives avatar of the person.')
    # async def avt(self, ctx, avamember : discord.Member=None):
    #     temp=discord.Embed(title='Here\'s your requested Avatar', color=randint(0, 0xffffff))
    #     temp.set_image(url=avamember.avatar.url)
    #     await ctx.send(embed=temp)
    
    @commands.command(brief='24h valstat (name) (tag)', description='Give stats of valorant player')
    async def valstat(self, ctx, username,tag):
    
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.henrikdev.xyz/valorant/v1/mmr/ap/healme/115') as p:
                data2=await p.json()
                global pic2, rank
                pic2 = data2['data']['images']['small']
                rank = data2['data']['currenttierpatched']
        
    
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}') as r:
                data=await r.json()
                pic = data['data']['card']['wide']
                tag = data['data']['tag']
                name = data['data']['name']

                embed = (Embed(title='Player Stats', color=random.randint(0, 0xffffff)))
                embed.add_field(name = 'Name', value = (f"{name}#{tag}"), inline = True)
                embed.add_field(name = 'account level', value = data['data']['account_level'], inline = True)
                embed.add_field(name = 'rank', value = rank, inline = True)
                embed.set_image(url=pic)
                embed.set_thumbnail(url=pic2)
                await ctx.send(embed=embed)
    
    @commands.command(brief='24h valmatstat (name) (tag)', description='Give stats of last played match')
    async def valmatstat(self, ctx, username,tag):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.henrikdev.xyz/valorant/v3/matches/ap/{username}/{tag}') as a:
                data3=await a.json()
                mapname = data3['data'][0]['metadata']['map']
                date = data3['data'][0]['metadata']['game_start_patched']
                mode = data3['data'][0]['metadata']['mode']
                server = data3['data'][0]['metadata']['cluster']
                roundsplayed = data3['data'][0]['metadata']['rounds_played']
                pic="https://cdn.discordapp.com/attachments/1048454267842875424/1081546330834485429/best-gpu-for-valorant.png"
            
            
                embed = (Embed(title='Last Match Stats', color=random.randint(0, 0xffffff)))
                embed.add_field(name = 'mapname', value = mapname, inline = True)
                embed.add_field(name = 'date', value = date, inline = True)
                embed.add_field(name = 'mode', value = mode, inline = True)
                embed.add_field(name = 'server', value = server, inline = True)
                embed.add_field(name = 'roundsplayed', value = roundsplayed, inline = True)
                embed.set_image(url=pic)
                await ctx.send(embed=embed)
        


async def setup(bot):
    await bot.add_cog(Random(bot))
