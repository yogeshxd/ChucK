import discord
from discord.ext import commands
from os import environ
import time
import random

bot = commands.Bot(command_prefix=['Du '])
bot.remove_command('help')
initial_extensions = ['cogs.admin', 'cogs.chat', 'cogs.music', 'cogs.random', 'cogs.logs', 'cogs.live']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

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
    bot.reload_extension(extension)

@bot.command(hidden=True)
async def status(ctx, arg, arg2, arg3=None):
    author = ctx.message.author
    if author.id == discord_id:
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

bot.run('Discord_bot_token', bot=True, reconnect = True)