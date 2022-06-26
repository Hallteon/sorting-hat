import discord
from discord.ext import commands
from data.config import PREFIX

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
