import discord
from discord.ext import commands
import datetime
import pytz
from ruamel.yaml import YAML
import threading
import json
import asyncio
import time

yaml = YAML()

class ThreadJob(threading.Thread):
  def __init__(self,callback,event,interval):
    self.callback = callback
    self.event = event
    self.interval = interval
    super(ThreadJob,self).__init__()
  
  def run(self):
    while not self.event.wait(self.interval):
      client.loop.create_task(self.callback())

with open("./config.yml", "r", encoding="utf-8") as file:
  config = yaml.load(file)

with open(f"./{config['Block Calendar File']}", "r", encoding="utf-8") as file:
  block_schedule = yaml.load(file)

with open(f"./{config['Bell Schedule File']}", "r", encoding="utf-8") as file:
  bell_schedule = json.load(file)

client = commands.Bot(command_prefix=config['Prefix'], case_insensitive=True)



log_channel_id = config['Log Channel ID']

client.embed_color = discord.Color.from_rgb(
  config['Embed Settings']['Color']['r'],
  config['Embed Settings']['Color']['g'],
  config['Embed Settings']['Color']['b']
)

client.prefix = config['Prefix']
client.playing_status = config['Playing Status']

utc = pytz.utc
client.timezone = pytz.timezone(config["User Timezone"])

client.previous_bell = None
client.ping_channel = config['Announcements Channel ID']
client.pinged_role = f"<@&{config['Pinged Role ID']}>"
client.message_starter = config['Message Starter'].format(pinged_role = client.pinged_role)

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
  
  client.log_channel = client.get_channel(log_channel_id)
  await client.log_channel.send(embed = embed)

@client.command(name = "restart", aliases = ["rs","you-stupid"], help = "Restarts the bot")
@commands.has_permissions(administrator=True)
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
  
  await client.log_channel.send(embed = embed)
  
  await ctx.message.add_reaction("✅")
  
  game = discord.Game(name="shutting down...")
  await client.change_presence(activity=game)
  
  event.set()
  
  await client.close()

@client.command(name = "block", aliases = ['ab', 'todays-block', 'a/b', 'aorbday', '🆎'], help = "Adds a reaction based on what day it is")
async def a_or_b_day(ctx, *args):
  args = list(args)
  args_len = len(args)
  time = get_local_datetime()
  if args_len:
    if args_len >= 2:
      try:
        args[0] = int(args[0])
        args[1] = int(args[1])
      except:
        ""
    if args_len != 2 or type(args[0]) != int or type(args[1]) != int:
      await ctx.channel.send(f"""{ctx.author.mention}, this command takes either two or zero arguments. Zero arguments returns the current day's a/b day, two arguments [month] [day] (only numerical entries) and returns the a/b day of the specified date.

For Example:
`{config['Prefix']}🆎 8 14` would react with 🅱️ because that is a b-day""")
      return None
    else:
      time = datetime.datetime(time.year, args[0], args[1], time.hour, time.minute, time.second, time.microsecond)
  block_day = get_block_day(time)
  print(f"User '{ctx.author}' requested A or B day, the date is {time.month}/{time.day} and the result is {block_day}")
  
  if block_day == 'A':
    await ctx.message.add_reaction("🅰️")
  elif block_day == 'B':
    await ctx.message.add_reaction("🅱️")
  else:
    await ctx.message.add_reaction("❌")

def get_local_datetime(time = None, timezone = utc):
  if type(time) is not datetime.datetime:
    time = datetime.datetime.utcnow()
  time = timezone.localize(time)
  local_time = time.astimezone(client.timezone)
  return local_time

def get_block_day(time = None):
  if type(time) is not datetime.datetime:
    time = get_local_datetime()
  try:
    return block_schedule[time.month][time.day]
  except:
    return None

def get_current_bell(time = None, block_day = None):
  if type(time) != datetime.datetime:
    time = get_local_datetime()
  if block_day != "A" and block_day != "B":
    block_day = get_block_day(time)
  
  current_bell = client.previous_bell
  
  if block_day:
    for bell in bell_schedule:
      if time.hour == bell['hour'] and time.minute == bell['minute']:
        current_bell = bell
        return current_bell
  return client.previous_bell

async def bell_ringer():
  time = get_local_datetime()
  block_day = get_block_day(time)
  current_bell = get_current_bell(time, block_day)
  
  if current_bell == None:
    # print("Current bell is none")
    return
    
  period = current_bell['period']
  if block_day == "B":
    if type(current_bell['period']) == int:
      period += 4
  
  if client.previous_bell == current_bell:
    # print("Previous bell and Current bell are the same")
    return
  # elif client.previous_bell == None:
    # print("Previous bell is none")
  client.previous_bell = current_bell
  if current_bell['message'] == "default":
    if current_bell['type'] == "passing":
      await send_ping(f"period {period}{'🅰️' if block_day == 'A' else '🅱️'} starts in 5 minutes! Be sure to join your next zoom call!")
    elif current_bell['type'] == "tardy":
      await send_ping(f"period {period}{'🅰️' if block_day == 'A' else '🅱️'} has now officially started! Make sure you're in your zoom call!")
    elif current_bell['type'] == "starting":
      await send_ping(f"""Good morning everyone! Schools starts in 5 minutes, so be sure to join your first zoom.

Additional Info:
Today is {time.month}/{time.day}/{time.year}
It's a{'n' if block_day == 'A' else ''} {'🅰️' if block_day == 'A' else '🅱️'} day""")
  else:
    await send_ping(f"{current_bell['message']}")

async def send_ping(message):
  ping_channel = client.get_channel(client.ping_channel)
  print(f"{client.message_starter} : {message}")
  await ping_channel.send(f"{client.message_starter} : {message}")

@client.command(name = "bob")
async def bob(ctx):
  # await client.log_channel.send(f"<@&{config['Pinged Role ID']}>")
  await client.log_channel.send(':a: :b: :ab: :bell:')
  time.sleep(5)
  await client.log_channel.send(f"<@&{config['Pinged Role ID']}> :one:")

event = threading.Event()

bell_ringer_thread = ThreadJob(bell_ringer,event,5)
bell_ringer_thread.start()

from importlib import import_module
token_module = import_module(config['Bot Token File'][:-3])
token = getattr(token_module, config['Bot Token Variable Name'])

client.run(token, bot=True, reconnect=True)

# for i in range(5): 
#   i += 8
#   for j in range(31):
#     j += 1
#     if not (i == 9 and j > 30) and not (i == 11 and j > 30):
#       dt = get_local_datetime()
#       dt = datetime.datetime(dt.year, i, j, dt.hour, dt.minute, dt.second, dt.microsecond)
#       print(f"Month {i} \tDay {j}\t\tBlock {get_block_day(dt)}")