import discord
from discord.ext import commands
import datetime
import secrets # Contains CLIENT_SECRET and other secret variables, it's in a .gitignore so that no one can steal my OAuth2

client = commands.Bot(command_prefix="BellBot ", case_insensitive=True)

client.embed_color = discord.Color.orange()


@client.event
async def on_ready():
  print(f"Logged in as '{client.user}' in channel '{secrets.DISCORD_CHANNEL}'")
  
  game = discord.Game(name="with some bells")
  await client.change_presence(activity=game)
  
  embed = discord.Embed(
    title = f"{client.user.name} Online!",
    color = client.embed_color,
    timestamp = datetime.datetime.now(datetime.timezone.utc)
  )
  embed.set_footer  (
    text = f"{client.user.name} has successfully booted up"
  )
  
  client.channel = client.get_channel(secrets.DISCORD_CHANNEL)
  await client.channel.send(embed = embed)

@client.command(name = "restart", aliases = ["rs","you-stupid"], help = "Restarts the bot")
async def restart(ctx):
  print(f"Restart command requested by {ctx.author} in channel #{ctx.channel}")
  embed = discord.Embed(
    title = f"{client.user.name} is restarting...",
    color = client.embed_color,
    timestamp = datetime.datetime.now(datetime.timezone.utc)
  )
  embed.set_author(
    name = ctx.author.name,
    icon_url = ctx.author.avatar_url
  )
  embed.set_footer(
    text = f"Please wait a moment while we restart"
  )
  
  await client.channel.send(embed = embed)
  
  await ctx.message.add_reaction("✅")
  
  await client.close()

client.run(secrets.CLIENT_SECRET, bot=True, reconnect=True)