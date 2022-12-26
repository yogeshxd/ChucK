import discord
from discord.ext import commands
from os import environ
import time
import datetime
import random
import os
import config
import asyncio
from discord import File
from easy_pil import Editor, load_image_async, Font
from discord import Embed
import logging
from discord_logging.handler import DiscordHandler

#New Logging
webhook_url = config.wh
logger = logging.getLogger()

stream_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
discord_format = logging.Formatter("%(message)s")

discord_handler = DiscordHandler(
    "Doctor ChucK", 
    webhook_url,)

#discord_handler = DiscordHandler("Happy Bot", webhook_url, emojis={})
discord_handler.setFormatter(discord_format)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_format)

# Add the handlers to the Logger
logger.addHandler(discord_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

logger.info("This is an info message")
logger.debug("A debug message - usually not that interesting")
logger.error("Very nasty error messgae!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.ext, intents=intents)

bot.remove_command('help')

async def load_extensions():
    for filename in os.listdir("./Desktop/ChucK/cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f'\nLogged as: {bot.user.name} - {bot.user.id}\nConnected to:')
    for i in bot.guilds:
        print(
        f'{i}'
        )
    print(f'Bot is ready to go!')
    global start_time
    start_time = time.time()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Du help | Du invite'))

@bot.command(hidden=True)
async def reload(ctx, extension):
    await bot.reload_extension(extension)

@bot.command(pass_context=True)
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(color=random.randint(0, 0xffffff))
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text="ChucK")
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        await ctx.send("Current uptime: " + text)

#Old welcomer
@bot.event
async def on_member_join(member):
    #channel = bot.get_channel(1017488032259133613)
    gandu = "Welcome to "+"{}".format(member.guild.name)
    embed = (Embed(title=gandu, description=member.mention, color=random.randint(0, 0xffffff))
                  #.set_image(url = image)
                  #.set_footer(text = f"Please verify yourself from #Rules")
                  .set_thumbnail(url = member.avatar) 
                  )
    await member.guild.system_channel.send(embed=embed)
    role = discord.utils.get(member.guild.roles, name='Member')
    await member.add_roles(role)

#new welcomer
# @bot.event
# async def on_member_join(member):
#     channel = member.guild.system_channel
#     background = Editor("pic1.jpg")
#     profile_image = await load_image_async(str(member.avatar))
#     profile = Editor(profile_image).resize((150, 150)).circle_image()
#     poppins = Font.poppins(size=50, variant="bold")
#     poppins_small = Font.poppins(size=20, variant="light")
#     background.paste(profile, (325, 90))
#     background.ellipse((325, 90), 150, 150, outline="white", stroke_width=5)
#     background.text((400, 260), f"WELCOME TO {member.guild.name}", color="white", font=poppins, align="center")
#     background.text((400, 325), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")
#     file = File(fp=background.image_bytes, filename="pic1.jpg")
#     await channel.send(f"Hello {member.mention}! Welcome to {member.guild.name} For more info check out #rules", file=file)
#     role = discord.utils.get(member.guild.roles, name='Member')
#     await member.add_roles(role)

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

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.token, reconnect = True)

asyncio.run(main())
