from socket import timeout
from discord import Embed
from discord.ext import commands
from discord.utils import get
import discord
import asyncio

import requests

class chatai(commands.Cog, name='chatai'):
    """
    Can be used by anyone, you'll find ai chatbots here.
    """
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def ai(chat):
        url = "https://waifu.p.rapidapi.com/path"
        querystring = {"user_id":"sample_user_id","message":"hello","from_name":"Boy","to_name":"Girl","situation":"Girl loves Boy.","translate_from":"auto","translate_to":"auto"}
        payload = {}
        headers = {
	        "content-type": "application/json",
	        "X-RapidAPI-Key": "", #put you rapid api key here (goto https://rapidapi.com/waifuai/api/waifu/)
	        "X-RapidAPI-Host": "waifu.p.rapidapi.com"
        }
        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
        return response.text

    @commands.command(brief='Du start [bot name]', description='Allow you to have upto 5 conversations with a bot')
    async def start(self, ctx, arg):
        if arg.lower() == 'waifu':
            await ctx.send('Say hii!! Your waifu is here')
            #chat = "hii"
            for i in range(5):
                
                try:
                    message = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=60)
                    #await ctx.send("check 1 complete")
                    chat = message.content.lower()
                    await ctx.send(chatai.ai(chat))
                except asyncio.TimeoutError:
                    await ctx.send("Sorry, you didn't reply in time!")
                    await ctx.send("Waifu is not happy with you!!")
                    break
            await ctx.send("Waifu has left the chat!! Run the command again to call her back :)")
            
        else:
            await ctx.send('❌ This bot is unavailable, Please check the spellings and try again.')

async def setup(bot):
    await bot.add_cog(chatai(bot))