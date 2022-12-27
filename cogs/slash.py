from discord import Embed
from discord.ext import commands
from discord import app_commands
from discord.utils import get
import discord
from random import choice, randint
import random
from requests import get as rget

class Slash(commands.Cog):
    """
    Can be used by anyone, you'll find slash commands here.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="hello", description="says hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"hello {interaction.user.mention}!", ephemeral=True)

    
    @app_commands.command(name="avatar", description="Mention the user to get his avatar")
    async def avatar(self, interaction: discord.Interaction, avamember : discord.Member=None):
        temp=discord.Embed(title='Here\'s your requested Avatar', color=randint(0, 0xffffff))
        temp.set_image(url=avamember.avatar.url)
        await interaction.response.send_message(embed=temp,ephemeral=True)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Slash(bot))