from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

import os
import random
import discord
import time

from discord.utils import get
from discord.ext import commands


class Moderation(commands.Cog, name='Moderation'):
    """
    Can only be used by moderators and admins.
    """
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Moderation(bot))