import discord
from discord.ext import commands
import datetime
from ruamel.yaml import YAML

yaml = YAML()

with open("./config.yml", "r", encoding="utf-8") as file:
  config = yaml.load(file)

client = commands.Bot(command_prefix=config['Prefix'], case_insensitive=True)

log_channel_id = config['Log Channel ID']

client.embed_color = discord.Color.from_rgb(
  config['Embed Settings']['Color']['r'],
  config['Embed Settings']['Color']['g'],
  config['Embed Settings']['Color']['b']
)

client.prefix = config['Prefix']
client.playing_status = config['Playing Status']


@client.event
async def on_ready():
  print(f"Logged in as '{client.user}', putting logs in channel '{log_channel_id}'")
  
  game = discord.Game(name=client.playing_status)
  await client.change_presence(activity=game)
  
  embed = discord.Embed(
    title = f"{client.user.name} Online!",
    color = client.embed_color,
    timestamp = datetime.datetime.now(datetime.timezone.utc)
  )
  embed.set_footer  (
    text = f"{client.user.name} has successfully booted up"
  )
  
  client.channel = client.get_channel(log_channel_id)
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

from importlib import import_module
token_module = import_module(config['Bot Token File'][:-3])
token = getattr(token_module, config['Bot Token Variable Name'])

client.run(token, bot=True, reconnect=True)