#-----------------------========= Imports -----------------------=========#

import discord
from discord.ext import commands
import json
import random
from discord.utils import find
import asyncio
from discord.ui import Select, View
import os
import datetime

from webserver import keep_alive

from dotenv import load_dotenv
load_dotenv()




#-----------------------========= Prefix -----------------------=========#
#prefix beginning
def get_prefix(client, message): 
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f) 
    return prefixes[str(message.guild.id)]


client = commands.Bot (intents=discord.Intents.all(), command_prefix= (get_prefix))
client.remove_command("help")



players = {}

#-----------------------========= Bot Status -----------------------=========#
LISTENING = ['Memes', 'Spotify', 'Spam', 'Dms']
PLAYING = ['Proteting your server!',
           'Helping Servers', 'Music', 'None your buisness.',
           'Moderating', 'Amoung Us', 'Fortnite', 'COD', 'Discord']
WATCHING = ['Paint dry', 'Music videos', 'Moderation', 'Youtube', 'Reddit', 'The Sky', 'Your Server']
ACTIVITYTYPE = {'LISTENING': discord.ActivityType.listening,
                'PLAYING': discord.ActivityType.playing,
                'WATCHING': discord.ActivityType.watching}
PRESENCELISTS = ['LISTENING', 'PLAYING', 'WATCHING']
PRESENCE = random.choice(PRESENCELISTS)

@client.event
async def on_ready():
  print('Voltage 2.2')
  print('Logged in as: '+client.user.name)
  print('Client User ID: '+str(client.user.id))
  
  await client.change_presence(activity=discord.Activity(
    type=ACTIVITYTYPE[PRESENCE], name=(random.choice(globals()[PRESENCE])+' | v!setup')))
        
  
#-----------------------========= Prefix -----------------------=========#



@client.command(pass_context=True)
async def prefix(ctx, prefix): 
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)
      
      await ctx.send(f'My Prefix has been changed to: {prefix}') 

@prefix.error
async def prefix_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please list a prefix that you would like to change to. Voltages prefix will be set back to the defult')
#prefix end


#-----------------------========= On join server -----------------------=========#
@client.event
async def on_guild_join(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)


    prefixes[str(guild.id)] = 'v!' 
    
    with open('prefixes.json', 'w') as f:
      json.dump(prefixes,f,indent=4)

    
      
      
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        embed=discord.Embed(title="**======== *Thanks For Adding Me!* ========**", description=f"""
        Thanks for adding me to {guild.name}!
        You can use the `v!setup` command to get started!
        """, color=0xd89522)
        await general.send(embed=embed)

         
         


#-----------------------========= Setup -----------------------=========###

@client.command()
async def setup(ctx):
    # Create the embed object
    embed = discord.Embed(
        
        title="Select an option",
        description="Choose one of the following options",
        color=0x00ff00
    )
    # Add the options as fields to the embed
    embed.timestamp = datetime.datetime.now()
    embed.add_field(name="⚙️ Prefix Setup ⚙️", value="Setup your custom server prefix!", inline=False)
    embed.add_field(name="❗ Help Command ❗", value="Use this command anytime!", inline=False)
    embed.set_footer(text="React with 🗑️ to clear this message")
    # Send the embed as a message
    msg = await ctx.send(embed=embed)
    # Add reaction buttons for the options
    await msg.add_reaction("⚙️")  # Unicode for Regional Indicator Symbol Letter A
    await msg.add_reaction("❗")  # Unicode for Regional Indicator Symbol Letter A
    await msg.add_reaction("🗑️")
  
    # Wait for the user's reaction
    def check(reaction, user):
      return user == ctx.author and str(reaction.emoji) in ["⚙️", "❗", "🗑️"]
    reaction, user = await client.wait_for("reaction_add", check=check)
    # Respond based on the user's selection
    if str(reaction.emoji) == "⚙️":
      embed=discord.Embed(title="Setup - Prefix", description="Set your server prefix!" ,color = discord.Color.from_rgb(0,255,50))
      embed.add_field(name="Set Prefix", value="All you have to type is\n `v!prefix newprefix`\n Once set you should see a message that informs you of the change.  ", inline=False)
      
      
      await msg.edit(embed=embed)
    
    if str(reaction.emoji) == "❗":
      embed=discord.Embed(title="Setup - Help Cmd", description="Help Command!" ,color = discord.Color.from_rgb(0,255,50))
      embed.add_field(name="Help", value="You can use this command to assist all the time! If you need help use\n`v!help`", inline=False)
      
      
      await msg.edit(embed=embed)
   


        
    


    else:
      await msg.delete()
      await ctx.send("Setup Menu Deleted")
      
   

@setup.error
async def on_error(self, ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    await ctx.send("Time is up!")


#-----------------------========= Help Pannels -----------------------=========#


@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title="Help Pannel", description= f"v!<category> for extended infomation on that category.\n **All Help commands are displayed with the default prefix!**" ,color= 0xd10a07)

  em.add_field(name = "👮 Moderation 👮", value = "Use `v!modhelp`")
  em.add_field(name = "😀 Fun 😀 ", value= "Use `v!funhelp`")
  em.add_field(name = "📁 Stats 📁", value= "Use `v!statshelp`") 
  em.add_field(name = "⚙️ Settings ⚙️", value= "Use `v!settingshelp`")

  await ctx.send(embed = em)



@client.group(invoke_without_command=True, aliases=['modhelp', 'ModerationHelp', 'Moderationhelp'])
async def ModHelp(ctx):
  em = discord.Embed(title="Moderation Help", description= " Use v!modhelp <command> for extended infomation on a command." ,color = discord.Color.from_rgb(83, 84, 55))

  em.add_field(name = "👮 Moderation Commands 👮", value= "kick\nban\nunban\nslowmode\nclear\nmute\nunmute")
 

  await ctx.send(embed = em)

@client.group(invoke_without_command=True, aliases=['funhelp', 'funnyhelp'])
async def FunHelp(ctx):
  em = discord.Embed(title="Fun Commands Help", description= " Use v!funhelp <command> for extended infomation on a command." ,color = discord.Color.from_rgb(204, 131, 104))

  em.add_field(name = "😀 Fun 😀 ", value= "8ball\ngif\ncr\ngr\nspoilify\ngif\nyt\nemojify")
 

  await ctx.send(embed = em)


@client.group(invoke_without_command=True, aliases=['statshelp', 'statisticshelp'])
async def StatsHelp(ctx):
  em = discord.Embed(title="Stats Commands Help", description= " Use v!statshelp <command> for extended infomation on a command." ,color = discord.Color.from_rgb(104, 204, 154))

  em.add_field(name = "📁 Stats 📁", value= "ping\nuserinfo")
 

  await ctx.send(embed = em)

@client.group(invoke_without_command=True, aliases=['Setuphelp', 'settingshelp'])
async def SettingsHelp(ctx):
  em = discord.Embed(title="Stats Commands Help", description= " Use v!settingshelp <command> for extended infomation on a command." ,color = discord.Color.from_rgb(204, 104, 194))

  em.add_field(name = "⚙️ Settings ⚙️", value= "prefix")
 

  await ctx.send(embed = em)

  
#-----------------------========= Mod Help Pannel -----------------------=========#

@ModHelp.command()
async def ban(ctx):
  em = discord.Embed(title = "Ban", description= "Bans a specific user.", color = discord.Color.from_rgb(0, 81, 255))
   
  em.add_field(name= "**Syntax**", value = "v!ban [@user][reason]")

  
  await ctx.send(embed = em)  

@ModHelp.command()
async def unban(ctx):
  em = discord.Embed(title = "Unban", description= "Unbans a specific user.", color = discord.Color.from_rgb(117, 255, 0))
   
  em.add_field(name= "**Syntax**", value = "v!unban [@userid][reason]")

@ModHelp.command()
async def slowmode(ctx):
  em = discord.Embed(title = "Slowmode", description= "Slows down a specific Channel.", color = discord.Color.from_rgb(164, 162, 233))
   
  em.add_field(name= "**Syntax**", value = "v!slowmode [seconds]")
  
  await ctx.send(embed = em)  
  
#-----------------------========= Entertainment Help Pannel -----------------------=========#






#-----------------------========= Setup Commands -----------------------=========#





    

#-----------------------========= Entertainement Commands -----------------------=========#
@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms 🏓')


@client.command()
async def cr(ctx):
  embed = discord.Embed(title="CoolRate", description = f"You are {random.randrange(101)}% Cool {ctx.author.mention}", color = discord.Color.random ())
  await ctx.send (embed = embed)

@client.command()
async def echo(ctx, *, message):
  await ctx.send(message)

@client.command()
async def test1(ctx):
  await ctx.send("HE:LLO")

@client.command()
async def emojify(ctx,*,text):
  emojis = []
  for s in text.lower():
    if s.isdecimal():
      num2emo = {'0':'zero','1':'one','2':'two',
      '3':'three','4':'four','5':'five',
      '6':'six','7':'seven','8':'eight','9':'nine'}
     
      emojis.append(f':{num2emo.get(s)}:')
    elif s.isalpha():
      emojis.append(f':regional_indicator_{s}:')
    else:
      emojis.append(s)
  await ctx.send(''.join(emojis))

@client.command()
async def gr(ctx):
  embed = discord.Embed (title="Gayrate", description = f"You are {random.randrange(101) }% Gay {ctx.author.mention}", color = discord.Color.random ())
  await ctx.send (embed = embed)

@client.command(name="whois")
async def whois(ctx,user:discord.Member=None):

    if user==None:
        user=ctx.author

    rlist = []
    for role in user.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)


    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f'Requested by - {ctx.author}',
  icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value=user.display_name,inline=False)

    embed.add_field(name='Created at:',value=user.created_at,inline=False)
    embed.add_field(name='Joined at:',value=user.joined_at,inline=False)

  
 
    embed.add_field(name='Bot?',value=user.bot,inline=False)

    embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Role:',value=user.top_role.mention,inline=False)

    await ctx.send(embed=embed)





#-----------------------========= Moderation Commands -----------------------=========#
@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}",color = discord.Color.from_rgb(255, 0, 0))
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)


@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.ban(reason=reason)
        ban = discord.Embed(title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color = discord.Color.from_rgb(255, 0, 157))
       
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)

@client.command()
async def unban (ctx, user: discord.User):
    guild = ctx.guild
    mbed = discord. Embed(
        title = 'Success!',
        description= f"{user} has successfully been unbanned.", color = discord.Color.from_rgb(61, 255, 0))
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed=mbed)
        await guild.unban(user=user)
        await user.send(embed=mbed)

@client.command()
async def slowmode (ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  mbed = discord. Embed(
      title = 'Slowmode!',
      description= f"This channels slowmode has been set to {seconds} seconds ⏲️", color = discord.Color.from_rgb(188, 255, 0))
  await ctx.send(embed=mbed)
        
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear (ctx, amount : int):
  await ctx.channel.purge(limit=amount)
  mbed = discord.Embed(
      title = 'Messages Deleted!',
      description= f"{amount} Message(s) Cleared by {ctx.author.mention}", color = discord.Color.from_rgb(188, 255, 0))
  await ctx.send(embed=mbed)



#-----------------------========= Command Errors -----------------------=========#

@prefix.error
async def prefix_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please list a prefix that you would like to change to.')
#prefix end


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
      await ctx.send('Invalid Command Used :rolling_eyes:')
      await ctx.send('Try: `customprefix`help')

@clear.error 
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please specify an amount of messages to delete :confused:')

@slowmode.error 
async def slowmode_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please specify the slowmode wait time (in secs)')





token = os.environ['DISCORD_TOKEN']
client.run(token)
keep_alive()