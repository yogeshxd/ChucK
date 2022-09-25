import discord
from discord.ext import commands
from os import environ
import time
import random
import os
import config
import asyncio

from discord import Embed

import logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
discord.utils.setup_logging(level=logging.DEBUG, handler=handler, root=False)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.ext, intents=intents)

#bot = commands.Bot(command_prefix=['Du '])
bot.remove_command('help')
initial_extensions = ['cogs.admin', 'cogs.chat', 'cogs.music', 'cogs.random', 'cogs.chatai']

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")

##if __name__ == '__main__':
##    for extension in initial_extensions:
##        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\nLogged as: {bot.user.name} - {bot.user.id}\nConnected to:')
    for i in bot.guilds:
        print(
        f'{i}'
        )
    print(f'Bot is ready to go!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Du help | Du invite'))

@bot.command(hidden=True)
async def reload(ctx, extension):
    await bot.reload_extension(extension)

@bot.event
async def on_member_join(member):
    #channel = bot.get_channel(1017488032259133613)
    gandu = "Welcome to "+"{}".format(member.guild.name)
    embed = (Embed(title=gandu, description=member.mention, color=random.randint(0, 0xffffff))
                  #.set_image(url = image)                                                                     #use this if you want big image
                  #.set_footer(text = f"Please verify yourself from #Rules")
                  .set_thumbnail(url = member.avatar) 
                  )
    role = discord.utils.get(member.guild.roles, name='Member')
    await member.add_roles(role)                                                                                        # await channel.send(member.avatar)
    await member.guild.system_channel.send(embed=embed)

@bot.command(hidden=True)
async def status(ctx, arg, arg2, arg3=None):
    author = ctx.message.author
    if author.id == config.author:
        if arg == 'playing':
            await bot.change_presence(activity=discord.Game(name=arg2))
        elif arg == 'streaming':
            await bot.change_presence(activity=discord.Streaming(name=arg2, url=arg3))
        elif arg == 'listening':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=arg2))
        elif arg == 'watching':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg2))
        await ctx.send('Status Updated')
        await ctx.channel.purge(limit=2)
        print('Status Updated')
    else:
        await ctx.send('Fuck off. You are not authorized')

#bot.run(config.token, reconnect = True)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.token, reconnect = True)

asyncio.run(main())
