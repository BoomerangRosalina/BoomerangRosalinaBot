import discord
from discord.ext import commands
import datetime
import asyncio
import random
import sys
import aiohttp

client = commands.Bot(command_prefix= commands.when_mentioned_or('br;'))
client.remove_command("help")
client.session = aiohttp.ClientSession()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("Boomerang Rosalina is Online")

def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2


  return val * time_dict[unit]

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Boomerang Rosalina", description="MY PREFIX IS: br; or my mention", color=(64255))
    embed.add_field(name = "CORE COMMANDS", value = "br;help - This Message\nbr;ping - Gets the Latency of the Bot\nbr;invite - Get the link to invite the bot AND get a link to its support server\nbr;botinfo - Get Information about the bot", inline=False)
    embed.add_field(name = "MODERATION COMMANDS", value = "br;slowmode - Adjusts the slowmode of a channel\nbr;lock - Locks a text channel for @ everyone.\nbr;unlock - Unlocks a text channel for @ everyone\nbr;clear - Clears a certain amount of messages\nbr;kick - Kicks a member from the server\nbr;ban - Bans a member from the server.\nbr;timeout - Time out a member from talking in the server\nbr;mute - Mutes a member\nbr;unmute - Unmutes a Member", inline=False)
    embed.add_field(name = "UTILITY COMMANDS", value = "br;serverinfo - Get information about your server\nbr;userinfo - Get information about yourself or another person\nbr;say - Make the bot say things\nbr;esay - Make the bot say things in a embed\nbr;pollyn - Make a Yes/No Poll\nbr;gsetup - Set up a giveaway for your server", inline=False)
    embed.add_field(name = "MISC", value = "br;createmuterole - Create a Mute role for the mute command\nbr;eightball - Ask the Magic 8Ball things\nbr;dice - Roll a 1-6 dice", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! My Latency is {round(client.latency * 1000)}ms')

@client.command()
async def invite(ctx):
    embed = discord.Embed(title="Invite", description="Invite me here: https://discord.com/api/oauth2/authorize?client_id=877686202906583060&permissions=0&scope=bot\n\nOur Support Server: https://discord.gg/cbqDfn8jvd", color=(64255))
    await ctx.send(embed=embed)

@client.command()
async def botinfo(ctx):
    embed = discord.Embed(title="Boomerang Rosalina | Bot Info", description="My Developers: Boomerang Mario#5018 and AMarioLover#3304", color=(64255))
    embed.add_field(name = "STATS", value = f"Servers I am in: {len(client.guilds)}", inline=False)
    embed.add_field(name = "PRIVACY POLICY", value = "The Bots Privacy Policy can be found here: https://boomerangrosalina.glitch.me/brprivacy.html", inline=False)
    embed.add_field(name = "CREDITS", value = "Orignal Source Code: https://github.com/BoomerangRosalina/BoomerangRosalina", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def say(ctx, *, question: commands.clean_content):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error

@client.command()
async def esay(ctx, *, question):
    embed = discord.Embed(description=f'{question}', color=(64255))
    await ctx.send(embed=embed)
    await ctx.message.delete()

@esay.error
async def esay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error





@client.command()
@commands.has_permissions(manage_channels=True)
@commands.bot_has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"I set the channels slowmode to {seconds} seconds!")

@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please add how many seconds of slowmode you want me to add. To disable slowmode, use br;slowmode 0")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``MANAGE_CHANNELS`` Permission to execute this command.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``MANAGE_CHANNELS`` Permission to use this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages Successfully Deleted. You can now delete this message.")
    if (amount < 0):
        await ctx.send("The number cant be a negative number")
        return

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("How many messages do you want to me clear?")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``MANAGE_MESSAGES`` Permission to execute this command.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``MANAGE_MESSAGES`` Permission to use this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(manage_channels=True)
@commands.bot_has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel has been locked for @ everyone.')

@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``MANAGE_CHANNELS`` Permission to use this command.")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``MANAGE_CHANNELS`` Permission to execute this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(manage_channels=True)
@commands.bot_has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel has been unlocked for @ everyone.')

@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You need to have the ``MANAGE_CHANNELS`` Permission to use this command.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``MANAGE_CHANNELS`` Permission to execute this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cant kick yourself")
        return
    if reason == None:
        reason = "For being dumb"
    await member.kick(reason=reason)
    await ctx.send("Member successfully Kicked")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user you want me to kick")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``KICK_MEMBERS`` Permission to execute this command.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You need to have the ``KICK_MEMBERS`` Permission to use this command.')
    else:
        raise error
    
@client.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("Why would you ban yourself?")
        return
    if reason == None:
        reason = "UNSPECIFIED REASON [USED BOOMERANG ROSALINA]"
    await member.ban(reason=reason)
    await ctx.send("Member successfully Banned.")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user you want me to ban")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``BAN_MEMBERS`` Permission to execute this command.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``BAN_MEMBERS`` Permission to use this command.")
    else:
        raise error

async def timeout_user(*, user_id: int, guild_id: int, until):
    headers = {"Authorization": f"Bot {client.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}
    async with client.session.patch(url, json=json, headers=headers) as session:
        if session.status in range(200, 299):
           return True
        return False

@client.command()
@commands.has_permissions(kick_members=True)
async def timeout(ctx: commands.Context, member: discord.Member, until: int, *, reason=None):
    if member == ctx.message.author:
        await ctx.channel.send("Why would you timeout yourself? That sounds stupid")
        return
    if member == client.user:
        await ctx.send("What have I done to deserve this?")
        return
    if reason == None:
        reason = "No Reason provided by Mod"
    
    handshake = await timeout_user(user_id=member.id, guild_id=ctx.guild.id, until=until)

    try:
        embed = discord.Embed(title="TIMEOUT", description=f"You have been Timed out from: {ctx.guild.name}\nTimeout time: {until} minutes\nReason: {reason}\nResponsible Moderator: {ctx.author.display_name}", color=(16755968))
        await member.send(embed=embed)
    except:
        await ctx.send("The user had DMs off or has blocked me. Therefor, I cant DM them the case details")
    
    if handshake:
        return await ctx.send(f"Successfully timed out {member.mention} for {until} minutes for {reason}")
    await ctx.send("Something went wrong. I may not have the TIMEOUT_MEMBERS permission or the person you are trying to timeout has a higher role than me.")

@timeout.error
async def timeout_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to mention who you want to timeout and specify the minutes. (example: br;timeout @Usermention 5)")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``KICK_MEMBERS`` Permission (timeout members permission) to use this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if member == ctx.message.author:
        await ctx.channel.send("Why would you mute yourself? That sounds stupid")
        return
    if member == client.user:
        await ctx.send("What have I done to deserve this?")
        return
    if reason == None:
        reason = "No Reason provided by Mod"
    
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        await ctx.send("I cannot find the role called **Muted**. Try br;createmuterole to create a mute role.")

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} has been muted successfully for: {reason}")
    try:
        embed = discord.Embed(title="MUTE", description=f"You have been muted from: {guild.name}\nReason: {reason}\nResponsible Moderator: {ctx.author.display_name}", color=(16755968))
        await member.send(embed=embed)
    except:
        await ctx.send("The user had DMs off or has blocked me. Therefor, I cant DM them the case details")

@client.command()
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await ctx.send(f"{member.mention} Has been unmuted successfully")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing required arguments or arguments are invalid\n\nbr;mute @MemberMention reason")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You need to have the ``MANAGE_ROLES`` Permission (timeout members permission) to use this command.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``MANAGE_ROLES`` Permission to execute this command.")
    else:
        raise error

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing required arguments or arguments are invalid\n\nbr;unmute @MemberMention")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You need to have the ``MANAGE_ROLES`` Permission (timeout members permission) to use this command.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``MANAGE_ROLES`` Permission to execute this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(manage_roles=True)
async def createmuterole(ctx):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if mutedRole:
        await ctx.send("The mute role for br;mute already exists. There is no need to rerun this command.")
        return

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
    await ctx.send("The role **Muted** has successfully been created.")

@createmuterole.error
async def createmuterole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You need to have the ``MANAGE_ROLES`` Permission to use this command.')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I do not have the ``MANAGE_ROLES`` Permission to execute this command.")
    else:
        raise error





format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

@client.command(aliases=["_serverinfo", "si", "serverstats"])
async def serverinfo(ctx):
    embed = discord.Embed(title="SERVER INFORMATION", description=f"Guild Name: {ctx.guild.name}\nMember Count: {ctx.guild.member_count}\nCurrent Guild ID: {ctx.guild.id}\nServer Region: {ctx.guild.region}\nServer Owner: {ctx.guild.owner}\nVerification Level: {ctx.guild.verification_level}\nServer Creation Date: {ctx.guild.created_at.strftime(format)}", color=(4771839))
    embed.add_field(name = "SPECIAL", value = f"Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \nSplash: {ctx.guild.splash}")

    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.add_field(name = "Channel Count", value = f"Channels: **{channels}**\nText Channels; **{text_channels}**\nVoice Channels; **{voice_channels}**\nCategories; **{categories}**", inline=False)
    embed.add_field(name = "Boosters", value = f"BOOST COUNT: Server Boost Count: {ctx.guild.premium_subscription_count}\nBOOSTER SUBSCRIBERS: {ctx.guild.premium_subscribers}", inline=False)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text="Boomerang Rosalina")
    await ctx.send(embed=embed)

@client.command(aliases=["_userinfo", "ui"])
async def userinfo(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(title="USER INFORMATION/STATS", description=f"USERNAME: {user.name}\nUSER ID: {user.id}\nDISCRIMINATOR TAG: {user.discriminator}\nRegistered At: {user.created_at.strftime(date_format)}\n\nJoined Server AT: {user.joined_at.strftime(date_format)}", color=(64255))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text="Boomerang Rosalina")
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def pollyn(ctx, *, question):
    message = await ctx.send(f"**New poll:** {question}\n\n✅ = Yes\n❎ = No")
    await message.add_reaction('✅')
    await message.add_reaction('❎')

@pollyn.error
async def pollyn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing permissions. You need the ``MANAGE_MESSAGES`` Permission to use this command')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing required arguments or arguments are invalid\n\nbr;poll <question>")
    else:
        raise error





@client.command()
async def eightball(ctx, *, question):
    responses = ["Yes",
                 "Heck Yeah",
                 "Of Course",
                 "My signs point to yes",
                 "Possibly",
                 "Very Likely",
                 "Maybe",
                 "My Sources points to no",
                 "If you use your imagination",
                 "I dont know that",
                 "I dont understand what you mean by the question, can you specify what you mean?",
                 "If you think I am answering that, then you have mistaken me for another bot"]
    await ctx.send(f'8ball\n\nQuestion: {question}\nAnswer: {random.choice(responses)}', allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False))

@eightball.error
async def eightball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Uhm, What are you trying to ask me? rerun this command but this time add a question to ask me.")
    else:
        raise error

@client.command()
async def dice(ctx):
    responses = ["1",
                 "2",
                 "3",
                 "4",
                 "5",
                 "6"]
    await ctx.send(f'You Rolled a: {random.choice(responses)}')








botdev = [872608213076426763, 839289231305605120]

@client.command()
async def owners(ctx):
    embed = discord.Embed(title="Boomerang Rosalina Owner Commands", description="These commands can only be executed by the Bot Developers and owner", color=(64255))
    embed.add_field(name="UTILITIES", value="br;restart - Restarts the Bot", inline=False)
    await ctx.send(embed=embed)

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@client.command()
async def restart(ctx):
    if ctx.author.id in botdev:
        await ctx.send("Restarting... This may take some time")
        restart_program()
    else:
        await ctx.send("This command can only be used by Boomerang Rosalina Developers")
        return



client.run("BOTTOKENHERE")
