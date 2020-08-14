import discord
import secrets # Contains CLIENT_SECRET, in a .gitignore so that no one can steal my OAuth2
from discord.ext import commands

client = commands.Bot(command_prefix="BellBot ", case_insensitive=True)

@client.event
async def on_ready():
  print("Bot is ready")
  channel = client.get_channel(secrets.DISCORD_CHANNEL)
  await channel.send(content="I am online")

client.run(secrets.CLIENT_SECRET, bot=True, reconnect=True)