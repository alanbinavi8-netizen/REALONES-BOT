import discord
from discord.ext import commands
import os
import aiohttp
# ... پاشان کۆدێ تە یێ دی یێ هاتی)
import asyncio      # بۆ کومانداێن remind و کاتژمێران پێدڤییە
import random       # بۆ کومانداێن flip و joke و یارییان پێدڤییە
import datetime     # بۆ کومانداێن stats و ئەنجامێن کاتژمێری پێدڤییە
from  discord.ext import tasks
import random
from datetime import datetime

# ==================== پشکا کلاسێ کێبڕکێیێ ====================
class CustomGiveawayView(discord.ui.View):
    def __init__(self, timeout, log_id, prize):
        super().__init__(timeout=timeout)
        self.participants = []
        self.log_id = log_id
        self.prize = prize

    @discord.ui.button(label="تۆمارکرن 🎟️", style=discord.ButtonStyle.green, custom_id="custom_join_g")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # پشکنین کو تەنێ ئێک جار بەشدار ببیت
        if interaction.user in self.participants:
            return await interaction.response.send_message("تە بەری نوکە ناڤێ خۆ تۆمار کرییە! ❌", ephemeral=True)
        
        self.participants.append(interaction.user)
        
        # لۆگ د چاتا تایبەت دا
        log_channel = interaction.guild.get_channel(self.log_id)
        if log_channel:
            log_embed = discord.Embed(
                title="👤 پشکدارەکێ نوو",
                description=f"**ناڤ:** {interaction.user.mention}\n**بەریکانە:** {self.prize}",
                color=0x2ecc71,
                timestamp=datetime.datetime.now()
            )
            log_embed.set_thumbnail(url=interaction.user.display_avatar.url)
            log_embed.set_footer(text=f"کۆمێ پشکداران: {len(self.participants)} | REAL ONES")
            try:
                await log_channel.send(embed=log_embed)
            except: pass

        await interaction.response.send_message("ناڤێ تە ب سەرکەفتن هاتە تۆمارکرن! ✅", ephemeral=True)




        
# ئەڤە ژی بۆ ناساندنا بۆتی و Prefix (نیشانە) یە
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='^', intents=intents)

# ل ڤێرە دشێی دەست ب نڤیسینا کوماندا بکەی...

# --- ئامادەکرنا تۆکنێ ---
# ل سەر Hugging Face دێ ژ بەشێ Secrets وەرگریت
TOKEN = os.environ.get('TOKEN')

# ئەگەر ل سەر کۆمپیوتەری بی و TOKEN نەبوو، ڤێ تۆکنێ ب کار دئینیت
if not TOKEN:
    TOKEN = 'MTQ4NTc0Mzk2OTMxNTg0ODIzOQ.GICZPy.SSD4gEM-atHCZu7ACi85XcJK3s0J72dmjc9MWc'

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

bot = commands.Bot(command_prefix='^', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------ REALONES BOT IS ONLINE 24/7 ------')

    #11111
    
    
    # ١ # --- [ڕێکخستنا سەرەکی] ---
STAFF_ROLE_ID = 1462582644956205086 
STAFF_ROLE_ID = 1465553167868629126
LOG_CHANNEL_ID = 1486828183968940052
# لینکێ وێنەیێ تە ل ڤێرە دانی
LOGO_URL = "https://media.discordapp.net/attachments/1461000548764487802/1466427093247201382/Snapchat-570505887.jpg?ex=69c68827&is=69c536a7&hm=a7f9948354e3ea4fad88d65438b470e54d44d529c2a0995f2ed30834e52ee2e6&=&format=webp&width=1005&height=1005" 

# 1.# --- [ڕێکخستنا سەرەکی - ئەڤان بگۆهۆڕە] ---

STAFF_ROLE_ID = 1462582644956205086
LOG_CHANNEL_ID = 1364674414091698176
LOGO_URL = "https://media.discordapp.net/attachments/1461000548764487802/1466427093247201382/Snapchat-570505887.jpg?ex=69c68827&is=69c536a7&hm=a7f9948354e3ea4fad88d65438b470e54d44d529c2a0995f2ed30834e52ee2e6&=&format=webp&width=1005&height=1005" # لینکێ وێنەیێ REAL ONES لێرە دانی



# 1. Hello Command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello! I am REALONES bot. I am online 24/7 now!')

# 2. Kick ban unban Command
# --- ١. کوماندا Ban ب ڕێکا ID یان Mention ---

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason=None): # مە کرە None
    try:
        await ctx.message.delete()
        
        # ئەگەر تە چ نەنڤیسیبوو، دێ بێژیت "دیار نەکرییە"
        if reason is None:
            reason = "چ هوکار نەهاتینە دیارکرن"

        # پشکنینا باندی (وەک مە بەری نوکە چێکری)
        is_banned = False
        async for entry in ctx.guild.bans(limit=1000):
            if entry.user.id == user.id:
                is_banned = True
                break
        
        if is_banned:
            already_embed = discord.Embed(title="⚠️ ئاگاداری", description=f"{user.mention} بەری نوکە یێ باندکرییە!", color=0xf1c40f)
            return await ctx.send(embed=already_embed)

        await ctx.guild.ban(user, reason=reason)

        embed = discord.Embed(title="⛔ ئەندام هاتە باندکرن", color=0xff0000, timestamp=datetime.datetime.now())
        embed.add_field(name="👤 کەسێ باندبووی:", value=f"{user.mention} (`{user.id}`)", inline=False)
        embed.add_field(name="📝 هوکار:", value=f"`{reason}`", inline=False)
        embed.add_field(name="👮 ژ لایێ ئەدمین:", value=f"{ctx.author.mention}", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        await ctx.send(embed=embed)

    except Exception as e:
        error_embed = discord.Embed(title="❌ خەلەتی", description=f"نکارم باند بکەم.\n**هوکار:** `{str(e)}`", color=0xff0000)
        await ctx.send(embed=error_embed)

# --- ٢. کوماندا Kick ب ڕێکا ID یان Mention ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason="hiii"):
    try:
        await ctx.message.delete()
        await ctx.guild.kick(user, reason=reason)

        embed = discord.Embed(title="👢 ئەندام هاتە دەرخستن", color=0xf1c40f, timestamp=datetime.datetime.now())
        embed.add_field(name="👤 کەسێ دەرکەفتی:", value=f"{user.mention} (`{user.id}`)", inline=False)
        embed.add_field(name="📝 هوکار:", value=f"`{reason}`", inline=False)
        embed.add_field(name="👮 ژ لایێ ئەدمین:", value=f"{ctx.author.mention}", inline=False) # دێ چیتە بن هوکاری
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ کێشەیەک چێبوو: {e}", delete_after=5)

# --- ٣. کوماندا Unban ب ڕێکا ID ---
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: str): # مە کرە سترینگ دا ئەڕۆڕا ئایدی نەمینیت
    try:
        # ١. سڕینا نامەیا کوماندا تە
        await ctx.message.delete()

        # ٢. پەیداکرنا بەکارهێنەری
        user = await bot.fetch_user(int(user_id))
        
        # ٣. لادانا باندی
        await ctx.guild.unban(user)

        # ئیمبێدا سەرکەفتنێ
        embed = discord.Embed(
            title="✅ ئەندام هاتە ئازادکرن",
            color=0x2ecc71,
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="👤 کەسێ ئازادبووی:", value=f"{user.mention} (`{user.id}`)", inline=False)
        embed.add_field(name="👮 ژ لایێ ئەدمین:", value=f"{ctx.author.mention}", inline=False)
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await ctx.send(embed=embed)

    except Exception as e:
        # ئیمبێدا خەلەتیێ (دێ مینیت)
        error_embed = discord.Embed(
            title="❌ کێشەیەک چێبوو د Unban دا",
            description=f"ئەو ئایدییا تە دایە `{user_id}` نەهاتە دیتن یان یێ باندکری نینە.\n\n**ئەڕۆڕ:** `{str(e)}`",
            color=0xff0000
        )
        await ctx.send(embed=error_embed)

# 3. counting 

# 5. Clear Command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'🧹 Deleted {amount} messages.', delete_after=5)

# 6. Send Private Message (DM)
@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, user: discord.User, *, message):
    try:
        await user.send(f"**Message from {ctx.guild.name}:**\n{message}")
        await ctx.send(f"✅ Message sent to {user.mention} privately.")
    except:
        await ctx.send("❌ I couldn't send a DM to this user.")

# 7.Timeout Command 
@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, user_id: int, minutes: int):
    try:
        user = await ctx.guild.fetch_member(user_id)
        duration = datetime.timedelta(minutes=minutes)
        await user.timeout(duration)
        await ctx.send(f"✅ User {user.mention} has been timed out for {minutes} minutes.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# 8.Untimeout Command 
# @bot.command()
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, user_id: int):
    try:
        user = await ctx.guild.fetch_member(user_id)
        await user.timeout(None)
        await ctx.send(f"✅ Timeout removed for {user.mention}.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

 # 9.Server info 
 # @bot.command()
async def server(ctx):
    name = str(ctx.guild.name)
    member_count = str(ctx.guild.member_count)
    await ctx.send(f"✅ Server Name: {name}\n👥 Total Members: {member_count}")

# 10.Lock Channel
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    # ئەڤە دێ رۆلێ @everyone ل ناڤ سێرڤەری دۆزیتەڤە
    everyone = ctx.guild.default_role
    # ئەڤە دێ دەستهەلاتا نامە ناردنێ ل وی کەناڵی کەتە False
    await ctx.channel.set_permissions(everyone, send_messages=False)
    await ctx.send("🔒 This channel has been locked.")

# 11.Unlock Channel
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Channel has been unlocked.")

# 12.USER INFO 
@bot.command()
async def whois(ctx, user_id: int):
    try:
        user = await ctx.guild.fetch_member(user_id)
        roles = [role.mention for role in user.roles[1:]] # @everyone ناگریت
        await ctx.send(f"👤 **User:** {user.mention}\n🆔 **ID:** {user.id}\n📅 **Joined:** {user.joined_at.strftime('%Y-%m-%d')}\n🎭 **Roles:** {' '.join(roles) if roles else 'None'}")
    except:
        await ctx.send("❌ Error: User not found in this server.")

# 13.Clear User
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearuser(ctx, user_id: int, amount: int = 10):
    def is_user(m):
        return m.author.id == user_id
        
    deleted = await ctx.channel.purge(limit=amount, check=is_user)
    await ctx.send(f"✅ Deleted {len(deleted)} messages from {user_id}.", delete_after=5)

# 14.Old Name
@bot.command()
async def oldname(ctx, user_id: int):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.send(f"📌 The global name for this ID is: **{user.name}**")
    except Exception:
        await ctx.send("❌ Error: Could not find any user with this ID.")

# 15.Server Icon
@bot.command()
async def icon(ctx):
    if ctx.guild.icon:
        await ctx.send(f"🖼️ Server Icon:\n{ctx.guild.icon.url}")
    else:
        await ctx.send("❌ This server has no icon.")

# 16.Say 
@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message: str):
    await ctx.message.delete() # ناما تە ژێدبەت دا کو بتنێ یا بۆتی بمینیت
    await ctx.send(message)
# 17.Role list 
@bot.command()
async def roles(ctx):
    role_list = [role.name for role in ctx.guild.roles if role.name != "@everyone"]
    await ctx.send(f"🎭 **Server Roles ({len(role_list)}):**\n{', '.join(role_list)}")

# 18. Announce Command
@bot.command()
@commands.has_permissions(administrator=True)
async def announce(ctx, url: str, *, message: str):
    # ژێبرنا نامەیا تە دا کو تەنێ یا بۆتی بمینیت
    try:
        await ctx.message.delete()
    except:
        pass

    # دروستکرنا قالبه‌كێ پاقژ و فەرمی
    embed = discord.Embed(
        description=message, # ل ڤێرە نامەیا تە ب دلێ تە دەرکەڤیت
        color=0x2f3136 # ڕەنگێ تارێ فەرمی یێ دیسکۆردێ
    )
    
    # دانانا وێنەی (لینکێ وێنەی دێ ون بیت و تەنێ وێنە دێ مینیت)
    embed.set_image(url=url)
    
    # ناردنا نامەیێ دگەل @everyone
    await ctx.send(content="@everyone", embed=embed)

# 19.Onlinee Member
@bot.command()
async def online(ctx):
    online_count = len([m for m in ctx.guild.members if m.status != discord.Status.offline])
    await ctx.send(f"🟢 Members Online: **{online_count}**")

# 20.Poll
@bot.command()
async def poll(ctx, *, question: str):
    message = await ctx.send(f"📊 **POLL:** {question}")
    await message.add_reaction("✅")
    await message.add_reaction("❌")


# 21.Alert 
@bot.command()
@commands.has_permissions(manage_messages=True)
async def alert(ctx, user_id: int, *, message: str = "Please check the server!"):
    try:
        user = await bot.fetch_user(user_id)
        # دروستکرنا نامەکا جوان بۆ DM
        alert_msg = (
            f"⚠️ **URGENT ALERT FROM {ctx.guild.name}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **From Admin:** {user.mention}\n"
            f"📝 **Message:** {message}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👉 Please return to the server immediately!"
        )
        await user.send(alert_msg)
        await ctx.send(f"✅ Alert successfully sent to {user.mention}.")
    except Exception:
        await ctx.send(f"❌ Could not send alert to <@{user_id}>. (DMs are closed)")
# 22.Clear All
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearall(ctx, amount: int = 100):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"🧹 Cleared {amount} messages!", delete_after=5)


# 23. Warn Command
# --- [⚠️ REALONES WARNING SYSTEM - FINAL VERSION] ---

# ئایدییێن رۆلان ل ڤێرە دابنێ
WARN_ROLE_ID = 1488661667100233902  # ئایدییا رۆلێ Warned
STAFF_ROLE_ID = 1462582644956205086 # ئایدییا ئەو رۆلێ دشێت وارنینگێ بدەت

@bot.command(name="warn")
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    """کوماندایێ وارنینگێ ب ئایدی یان تاگ دگەل ئۆتۆ رۆل و نامەیا تایبەت"""
    
    # 1. پشکنینا دەستوورێ ستافی (ئەگەر ستاف بیت یان ئەدمین)
    staff_role = ctx.guild.get_role(STAFF_ROLE_ID)
    is_staff = staff_role in ctx.author.roles if staff_role else False
    is_admin = ctx.author.guild_permissions.administrator

    if not is_staff and not is_admin:
        return await ctx.send("❌ **تو دەستیر دای نینی ڤێ کوماندێ ب کار بینی!**")

    # 2. زێدەکرنا رۆلێ وارنینگێ ب ئۆتۆماتیکی
    warn_role = ctx.guild.get_role(WARN_ROLE_ID)
    if warn_role:
        try:
            await member.add_roles(warn_role)
        except Exception as e:
            print(f"Error adding role: {e}")
            await ctx.send("⚠️ **من نەشیا رۆلێ وارنینگێ بدەمە ئەندامی (رۆلێ بۆتی یێ نزمە)!**")
    else:
        return await ctx.send("❌ **ئایدییا رۆلێ وارنینگێ خەلەتە، ل ناو کۆدی چاک بکە!**")

    # 3. دروستکرنا Embed بۆ ناو سێرڤەرێ (وەک وێنەیێ تە دڤێت)
    server_embed = discord.Embed(title="⚠️ WARNING", color=0xe74c3c)
    server_embed.description = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    server_embed.add_field(name="👤 User:", value=f"{member.mention} (`{member.id}`)", inline=False)
    server_embed.add_field(name="📝 Reason:", value=f"```{reason}```", inline=False)
    server_embed.add_field(name="🛡️ Staff:", value=ctx.author.mention, inline=False)
    server_embed.set_thumbnail(url=member.display_avatar.url)
    server_embed.set_footer(text="REALONES FAMILY PROTECTION", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
    
    await ctx.send(embed=server_embed)

    # 4. دروستکرنا Embed بۆ ناو DM (نامەیا تایبەت بۆ ئەندامی)
    try:
        dm_embed = discord.Embed(
            title="⚠️ ئاگەهدارییا وارنینگێ | REALONES",
            description=(
                f"سڵاڤ {member.name}، تە وارنینگەک وەرگرت ل سێرڤەرێ **{ctx.guild.name}**\n\n"
                f"**📝 ئەگەر (Reason):**\n`{reason}`\n\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                "تکایە یاسایێن سێرڤەری بپارێزە دا کو تووشی سزادانا گرانتر نەبی."
            ),
            color=0xe74c3c
        )
        # وێنەیێ مافیا بۆ ناو DM
        dm_embed.set_image(url="https://i.postimg.cc/mD8D1Vj6/godfather.jpg")
        dm_embed.set_footer(text="REALONES FAMILY SYSTEM")
        
        await member.send(embed=dm_embed)
    except discord.Forbidden:
        await ctx.send(f"⚠️ **ئاگەهداری:** {member.mention} نامەیێن تایبەت (DM) گرتینە، نامە بۆ نەچوو بەس وارنینگ وەرگرت.")

# --- [پشتراست بە ئەڤ دێڕە ل دوماهیکا on_message هەبیت] ---
# await bot.process_commands(message)



# 27.Server Mute (speakstop)
@bot.command()
@commands.has_permissions(mute_members=True)
async def speakstop(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        if not member.guild_permissions.administrator:
            await member.edit(mute=True)
    await ctx.send(f"🔇 Everyone in **{vc.name}** has been muted.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def speakstart(ctx):
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=False)
    await ctx.send(f"🔊 Everyone in **{vc.name}** is unmuted.")

# 28.spam 
from collections import defaultdict
user_messages = defaultdict(list)

@bot.event
async def on_message(message):
    if message.author.bot: return
    
    now = discord.utils.utcnow().timestamp()
    user_messages[message.author.id].append(now)
    
    # ئەگەر پتر ژ ٥ نامان د ٥ کێلەکا دا بنێرێت
    user_messages[message.author.id] = [t for t in user_messages[message.author.id] if now - t < 5]
    
    if len(user_messages[message.author.id]) > 2:
        await message.delete()
        await message.channel.send(f"🚫 {message.author.mention}, slow down! No spamming.", delete_after=3)
    
    await bot.process_commands(message)

# 29.Jail
@bot.command()
@commands.has_permissions(manage_roles=True)
async def jail(ctx, member: discord.Member):
    if member.guild_permissions.administrator:
        return await ctx.send("❌ تو نەشی ئەدمینەکی زیندان بکەی!")

    # گوهۆڕینا دەستهەلاتان د هەمی کەناڵان دا
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(member, 
                send_messages=False, 
                connect=False, 
                add_reactions=False, 
                view_channel=False # ئەگەر تە ڤیا چ کەناڵان نەبینیت
            )
        except:
            continue
            
    await ctx.send(f"⛓️ **{member.display_name}** ب سەرکەفتی هاتە زیندانکرن ل هەمی کەناڵان!")

 # 30.unjail
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unjail(ctx, member: discord.Member):
    for channel in ctx.guild.channels:
        try:
            await channel.set_permissions(member, overwrite=None)
        except:
            continue
            
    await ctx.send(f"🔓 **{member.display_name}** هاتە ئازادکرن و دەستهەلاتێن وی زڤڕینەڤە.")

# 31.Slowmode
@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"🐢 Slowmode هاتە چالاککرن بۆ {seconds} چرکە.")

# 32.steal emoji
@bot.command()
@commands.has_permissions(manage_emojis=True)
async def steal(ctx, emoji: discord.PartialEmoji, *, name=None):
    # ئەگەر ناڤەکێ تایبەت نەدەیتێ، دێ هەمان ناڤێ ئەسلی یێ ئیمۆجی وەرگریت
    if not name:
        name = emoji.name
    
    try:
        # وەرگرتنا وێنەیێ ئیمۆجی ژ سێرڤەرێ دی
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji.url) as resp:
                if resp.status != 200:
                    return await ctx.send("❌ نەشێم وێنەیێ ئیمۆجی وەرگرم.")
                img = await resp.read()
        
        # دروستکرنا ئیمۆجیێ نوو ل سێرڤەرێ تە
        new_emoji = await ctx.guild.create_custom_emoji(name=name, image=img)
        
        embed = discord.Embed(
            title="✅ ئیمۆجی ب سەرکەفتی هاتە زێدە کرن!",
            description=f"ئیمۆجیێ نوو: {new_emoji}\nناڤێ وی: **{name}**",
            color=0x00ffcc
        )
        await ctx.send(embed=embed)
        
    except discord.Forbidden:
        await ctx.send("❌ دەستھەلاتا من نینە ئیمۆجییان زێدە بکەم.")
    except Exception as e:
        await ctx.send(f"❌ کێشەیەک چێبوو: {e}")

# 32.help
@bot.command()
async def helpme(ctx):
    embed = discord.Embed(
        title="📜 REALONES BOT COMMANDS",
        description="لیستا هەمی کومانداێن بۆتی ب شێوەیەکێ رێکخستی:",
        color=0x0055ff
    )
    
    embed.add_field(name="🛡️ Moderation", value="`^kick`, `^ban`, `^warn`, `^mute`, `^clear`, `^nuke`, `^lock`", inline=False)
    embed.add_field(name="⚙️ Admin Tools", value="`^announce`, `^slowmode`, `^say`, `^steal`, `^giveaway`", inline=False)
    embed.add_field(name="👤 General", value="`^avatar`, `^user`, `^server`, `^poll`, `^online`, `^roles`", inline=False)
    embed.add_field(name="⛓️ Jail System", value="`^jail`, `^unjail`", inline=False)
    
    embed.set_footer(text="Developed for REALONES Family")
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    
    await ctx.send(embed=embed)
# 33.clearweb
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearweb(ctx, amount: int = 20):
    def is_link(m):
        return "http" in m.content.lower() or "discord.gg" in m.content.lower()
    
    deleted = await ctx.channel.purge(limit=amount, check=is_link)
    await ctx.send(f"🧹 {len(deleted)} نامێن لینک تێدا هاتنە سڕینەڤە.", delete_after=5)
# 34.EmbedImage
#  @bot.command()
@commands.has_permissions(manage_messages=True)
async def imgembed(ctx, url, *, title="REALONES ANNOUNCEMENT"):
    await ctx.message.delete()
    
    embed = discord.Embed(title=title, color=0x0055ff)
    embed.set_image(url=url)
    embed.set_footer(text=f"By: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

# 35 auto spowner
@bot.event
async def on_message(message):
    # ناهێلیت بۆت بەرسڤا خۆ بدەت
    if message.author.bot:
        return

    # --- تنظیمات ---
    TRIGGER_WORD = "reklam" # ئەو پەیڤا تە دڤێت
    ROLE_ID_1 = 1462582644956205086  # ئایدییا ڕۆڵێ ئێکێ (Staff / Admin)
    ROLE_ID_2 =1111111111111111111  # 👈 ل ڤێرە ئایدییا ڕۆڵێ دووێ دابنێ
    CHANNEL_ID = 1364674414091698176 # ئایدییا وی کەناڵێ تە دڤێت کوماندا تێدا کار بکەت

    # پشکنین: ئەرێ نامە ل وی کەناڵی هاتینە و پەیڤ تێدا هەبوو؟
    if message.channel.id == CHANNEL_ID:
        if TRIGGER_WORD in message.content.lower():
            embed = discord.Embed(
                description=f" {message.author.mention} ل نێزیکترین دەم بەرسڤا تە دێ هێتە دان ژ لایێ ستافی ڤە. ✅",
                color=0xff0000
            )
            
            # 🔥 ناردنا نامەیێ دگەل تاگکرنا هەردوو ڕۆڵان ب لێکدابڕانی خشتەکی
            await message.channel.send(content=f"<@&{ROLE_ID_1}> ", embed=embed)
            
            # ئەگەر تە ڤیا نامەیا وی کەسی ژێببەی:
            # await message.delete()

    # ئەڤ دێڕە گەلەک گرنگە دا کومانداێن دی نەوەستن
    await bot.process_commands(message)
# 36 welcome 
import discord
from discord.ext import commands
import datetime

# --- 🎯 لۆجیکێ پێشوازیێ (Welcome System) ---
@bot.event
async def on_member_join(member):
    # ⚠️ ل ڤێرە ئایدییا چاتا پێشوازیێ (Welcome Channel ID) دابنێ:
    WELCOME_CHANNEL_ID = 1361724782458175629 
    
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    # 📊 وەرگرتنی ژمارا ئەندامان
    member_count = member.guild.member_count

    # 📅 وەرگرتنی کات و مێژووا هاتنە ژوورێ ب فۆرماتێ دروست
    now = datetime.datetime.now(datetime.timezone.utc)
    joined_at_str = now.strftime("%a %b %d %Y %H:%M:%S GMT+0000 (Coordinated Universal Time)")

    # ✨ دروستکرنا ئیمبێدێ ڕێک وەک دیزاینێ تە
    embed = discord.Embed(
        title="New Member Invited",
        description=f"Welcome {member.mention} 👋,\n\n"
                    f"You were invited by **Unknown**, who now has NaN invites!\n\n"
                    f"\"🔥 A new legend has arrived!\",\n"
                    f"\"🎮 Get ready to dominate!\",\n"
                    f"\"💀 Another warrior joins the squad!\",\n"
                    f"\"🚀 Welcome to the chaos!\"",
        color=0xff4500 # ڕەنگێ پرتەقاڵی/سۆر یێ ڕیال وەنز
    )

    # 🕒 زێدەکرنا پشکا Joined At
    embed.add_field(
        name="Joined At",
        value=joined_at_str,
        inline=False
    )

    # 👥 زێدەکرنا پشکا Member Count
    embed.add_field(
        name="Member Count",
        value=f"You are member #{member_count}",
        inline=False
    )

    # 🖼️ دانانا وێنەیێ خوارێ (Banner)
    BANNER_URL = "https://cdn.discordapp.com/attachments/1459722705904599074/1496259942699765860/r1_mix.png?ex=6a253869&is=6a23e6e9&hm=8a2f0579acd399a9457f73388d30bb976bbd54f7d790803a679ba12e9b300ee9&"
    embed.set_image(url=BANNER_URL)

    # 👤 دانانا وێنەیێ بچووک یێ لایێ ڕاستێ (Avatar)
    embed.set_thumbnail(url=member.display_avatar.url)

    # 📝 نڤیسینا بنێ ئیمبێدێ
    embed.set_footer(text="Welcome to the server, enjoy your stay!")

    # 🚀 فرێکرنا نامەیێ بۆ چاتێ
    await channel.send(embed=embed)

  # 38.giveway
# ==============================================================================
# 🎉 REALONES FULL GIVEAWAY SYSTEM (WITH WORKING BUTTON & HOST TRACKING)
# ==============================================================================

import discord
from discord.ext import commands, tasks
import random
import datetime

active_giveaways = {}

# --- 🎟️ دروستکرنا دوگمەیی و کاردانەوەیا وێ ---
class GiveawayView(discord.ui.View):
    def __init__(self, timeout=None, message_id=None):
        super().__init__(timeout=timeout)
        self.message_id = message_id

    @discord.ui.button(label="تۆمارکرن 🎟️", style=discord.ButtonStyle.success, custom_id="join_giveaway")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # ئەگەر بۆت هاتبووە سەرلەنوو پێکرن یان مێسج ئایدی نەبوو، ل ڤێرە ڕێک دکەین
        msg_id = self.message_id or interaction.message.id
        
        if msg_id not in active_giveaways:
            return await interaction.response.send_message("❌ ئەڤ گیڤئەوەیە ب دوماهی هاتییە یان یێ چالاك نینە!", ephemeral=True)
        
        g_data = active_giveaways[msg_id]
        if interaction.user.id in g_data["participants"]:
            return await interaction.response.send_message("❌ تۆ بەری نوکە پشکدار بووی د ڤی گیڤئەوەی دا!", ephemeral=True)
        
        # زێدەکرنا پشکداربووی
        g_data["participants"].add(interaction.user.id)
        
        # نووکرنا ژمارا سەر دوگمەیی
        button.label = f"تۆمارکرن 🎟️ ({len(g_data['participants'])})"
        await interaction.message.edit(view=self)
        
        await interaction.response.send_message("✅ تۆ ب سەرکەفتنی ڤە هاتییە تۆمارکرن د گیڤئەوەی دا!", ephemeral=True)

        # 🚨 لۆگ چانڵ کاتێ ئێک پشکدار دبیت
        LOG_CHANNEL_ID = 1488244673729269780
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            now_static = datetime.datetime.now().strftime('%Y/%m/%d | %I:%M:%S %p')
            log_embed = discord.Embed(
                title="📥 پشکداربووەکێ نوو تۆماربوو",
                description=f"**👤 بەکارهێنەر:** {interaction.user.mention} (`{interaction.user.name}`)\n"
                            f"**🆔 ناسنامە (ID):** `{interaction.user.id}`\n"
                            f"**🎁 خەڵات:** `{g_data['prize']}`\n"
                            f"**📊 کۆی پشکداران نوکە:** `{len(g_data['participants'])}`",
                color=0x3498db
            )
            log_embed.add_field(name="📅 دەم و مێژوو", value=f"`{now_static}`", inline=False)
            log_embed.set_footer(text="REALONES GIVEAWAY SYSTEM")
            await log_channel.send(embed=log_embed)


# --- 🚀 کوماندا سەرەکی یا گیڤئەوەی ---
@bot.command(name="giveaway")  # ⚠️ ئەگەر ل دەف تە client بیت، بکە @client.command
@commands.has_permissions(administrator=True)
async def giveaway(ctx, *, args: str):
    parts = [p.strip() for p in args.split("|")]
    if len(parts) < 3:
        return await ctx.send("❌ شێواز خەلەتە!\n`^giveaway مێژوو کات | مەرج | خەڵات`")
    
    datetime_str, rules, prize = parts[0], parts[1], parts[2]
    
    try:
        target_datetime = datetime.datetime.strptime(datetime_str, "%Y/%m/%d %H:%M")
    except ValueError:
        return await ctx.send("❌ فۆرماتێ کاتی خەلەتە! نموونە: `2026/06/03 14:30`")

    # 🖼️ لینكا وێنەیێ جێگیر
    DEFAULT_IMAGE_URL = "https://cdn.discordapp.com/attachments/1472835696896249898/1488242647364665544/010fcba7-5abe-4f45-afc2-a9c11a155030.png?ex=6a211a39&is=6a1fc8b9&hm=00a713d620597e840bfc0548334e217b5d0fa82e10043e803c9ea24e5573f1d0&"  # 👈 ل ڤێرە لینکا ڕاستەقینە دابنێ

    # دیزاینێ ئیمبێدێ ڕێک وەک جارا پێشتر
    embed = discord.Embed(
        title="🎉 REALONES GIVEAWAY 🎉",
        description=f"**🎁خەلات:** `{prize}`\n\n"
                    f"**📜مەرج:** `{rules}`\n\n"
                    f"**👑ڕێکخەر:** {ctx.author.mention}\n\n"
                    f"**⏳دەمێ ب دووماهی هاتنێ:** `ڕۆژا {datetime_str}`",
        color=0xff4500
    )
    embed.set_footer(text="REALONES FAMILY – کلیکێ ل دوگمێ خوارێ بکه بۆ پشکدارینێ")
    
    if DEFAULT_IMAGE_URL.startswith("http"):
        embed.set_image(url=DEFAULT_IMAGE_URL)

    # 🔥 ل ڤێرە دوگمە (View) ڕاستەوخۆ دهێتە ناردن دگەل مێسجێ!
    view = GiveawayView()
    giveaway_msg = await ctx.send(content="@everyone", embed=embed, view=view)
    
    # گرێدانا مێسج ئایدی ب دوگمەی ڤە
    view.message_id = giveaway_msg.id

    active_giveaways[giveaway_msg.id] = {
        "target_time": target_datetime,
        "channel_id": ctx.channel.id,
        "prize": prize,
        "host_id": ctx.author.id,
        "participants": set()
    }


# --- ⏱️ لۆپ و پشکنینا چرکەیی بۆ کۆتایی هاتنێ ---
@tasks.loop(seconds=10)
async def check_giveaways():
    now = datetime.datetime.now()
    ended_ids = []
    LOG_CHANNEL_ID = 1488244673729269780

    for msg_id, data in list(active_giveaways.items()):
        if now >= data["target_time"]:
            ended_ids.append(msg_id)
            channel = bot.get_channel(data["channel_id"])
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if not channel:
                continue

            try:
                msg = await channel.fetch_message(msg_id)
            except:
                continue

            participants = list(data["participants"])
            now_static = datetime.datetime.now().strftime('%Y/%m/%d | %I:%M:%S %p')
            host_mention = f"<@{data['host_id']}>"
            
            # ١. ئەگەر کەس پشکدار نەبوو
            if not participants:
                error_embed = discord.Embed(
                    title="🎉 GIVEAWAY ENDED 🎉",
                    description=f"**🎁 خەڵات:** `{data['prize']}`\n"
                                f"**👑 ڕێکخەر:** {host_mention}\n\n"
                                f"❌ چ کەسەک پشکدار نەبوو، براوە نینە!",
                    color=0xe74c3c
                )
                if msg.embeds and msg.embeds[0].image:
                    error_embed.set_image(url=msg.embeds[0].image.url)
                
                # لادانا دوگمەی (view=None) چونکی ب دووماهی هات
                await msg.edit(content=None, embed=error_embed, view=None)

                if log_channel:
                    log_ended_embed = discord.Embed(
                        title="🛑 گیڤئەوەی ب دوماهی هات (بێ براوە)",
                        description=f"**🎁 خەڵات:** `{data['prize']}`\n"
                                    f"**👑 ڕێکخەر:** {host_mention}\n"
                                    f"**📊 ژمارا پشکداران:** `0`",
                        color=0xe74c3c
                    )
                    log_ended_embed.add_field(name="📅 دەمێ کۆتاییێ", value=f"`{now_static}`", inline=False)
                    log_ended_embed.set_footer(text="REALONES LOG SYSTEM")
                    await log_channel.send(embed=log_ended_embed)
                continue

            # ٢. هەڵبژارتنا براوەی
            winner_id = random.choice(participants)
            winner_mention = f"<@{winner_id}>"

            # نووکرنا ئیمبێدا سەرەکی
            success_embed = discord.Embed(
                title="🎉 GIVEAWAY ENDED | گیڤئەوەی ب دوماهی هات 🎉",
                description=f"**🎁 خەڵات:** `{data['prize']}`\n"
                            f"**👑 ڕێکخەر:** {host_mention}\n\n"
                            f"**🏆 براوە:** {winner_mention}\n\nپیرۆزە!",
                color=0x2ecc71
            )
            if msg.embeds and msg.embeds[0].image:
                success_embed.set_image(url=msg.embeds[0].image.url)
            
            # لادانا دوگمەی ل کۆتاییێ
            await msg.edit(content=None, embed=success_embed, view=None)

            # ئیمبێدا نوو یا پیرۆزباییێ
            winner_embed = discord.Embed(
                title="🎊 Gg | پیرۆزە دۆستێ هێژا 🎊",
                description=f"👤 پيرۆزە ل تە {winner_mention}!\n"
                            f"🎁 تە خەڵاتێ **{data['prize']}** بردەڤە د تیروپشکێ دا.\n\n"
                            f"📩 ژ بۆ وەرگرتنا خەڵاتی، نامەیەکێ بۆ ڕێکخەرێ گیڤئەوەی {host_mention} فرێکە.",
                color=0x2ecc71
            )
            winner_embed.set_footer(text="REALONES FAMILY CONGRATULATIONS")
            await channel.send(content=winner_mention, embed=winner_embed, reference=msg)

            # 🚨 ٣. لۆگکرنا ئیمبێدا لۆگی بۆ چاتا لۆگی
            if log_channel:
                log_winner_embed = discord.Embed(
                    title="🏆 گیڤئەوەی ب دوماهی هات و براوە دیار بوو",
                    description=f"**🎁 خەڵات:** `{data['prize']}`\n"
                                f"**👑 ڕێکخەر:** {host_mention}\n"
                                f"**🥇 براوە:** {winner_mention}\n"
                                f"**📊 کۆی گشتی پشکداران:** `{len(participants)}`",
                    color=0x2ecc71
                )
                log_winner_embed.add_field(name="📅 دەمێ کۆتاییێ", value=f"`{now_static}`", inline=False)
                log_winner_embed.set_footer(text="REALONES LOG SYSTEM")
                await log_channel.send(embed=log_winner_embed)

    for msg_id in ended_ids:
        active_giveaways.pop(msg_id, None)

@bot.event
async def on_ready():
    if not check_giveaways.is_running():
        check_giveaways.start()
    print(f"Logged in as {bot.user.name} and Fix Button System Started!")
         
# 39.giveamay2
# # --- 1. پەنجەرەیا پێشبینیێ (Modal) ---
class PredictionModal(discord.ui.Modal, title=' :gift: بەریکانە'):
    score = discord.ui.TextInput(
        label='پێشبینیا تە چیە؟',
        placeholder='پێشبینیا خو بنڤێسە',
        required=True,
        min_length=2,
        max_length=50
    )

    def __init__(self, participants, log_id, target_time):
        super().__init__()
        self.participants = participants
        self.log_id = log_id
        self.target_time = target_time

    async def on_submit(self, interaction: discord.Interaction):
        # پشکنینا کاتی: ئەگەر کاتێ نوکە یێ چوو بیتە پێش دەمێ دیارکری
        if datetime.datetime.now() > self.target_time:
            return await interaction.response.send_message("ببورە، دەمێ پێشبینیێ ب دووماهی هاتییە و بەریکانە ڕاوەستایە! ❌", ephemeral=True)

        if interaction.user in self.participants:
            return await interaction.response.send_message("تە بەری نوکە پێشبینیا خۆ نڤیسییە! ❌", ephemeral=True)
        
        self.participants.append(interaction.user)
        
        log_channel = interaction.guild.get_channel(self.log_id)
        if log_channel:
            log_embed = discord.Embed(title="🎯 پێشبینییەکا نوو هات", color=0x00ffcc, timestamp=datetime.datetime.now())
            log_embed.add_field(name="👤 پشکدار:", value=f"{interaction.user.mention}", inline=True)
            log_embed.add_field(name="⚽ ئەنجام:", value=f"**{self.score.value}**", inline=False)
            log_embed.set_thumbnail(url=interaction.user.display_avatar.url)
            try: await log_channel.send(embed=log_embed)
            except: pass

        await interaction.response.send_message(f"✅ پێشبینیا تە هاتە تۆمارکرن: **{self.score.value}**", ephemeral=True)

# --- 2. کلاسێ دوگمەی ---
class MyGiveawayView(discord.ui.View):
    def __init__(self, timeout, log_id, target_time):
        super().__init__(timeout=timeout)
        self.participants = []
        self.log_id = log_id
        self.target_time = target_time

    @discord.ui.button(label="پێشبینی بکە", emoji="📝", style=discord.ButtonStyle.green)
    async def join_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        # پشکنینا بەری ڤەکرنا شاشا ڕەش
        if datetime.datetime.now() > self.target_time:
            return await interaction.response.send_message("ببورە، کاتێ بەریکانێ ب دووماهی هاتییە! ❌", ephemeral=True)
            
        await interaction.response.send_modal(PredictionModal(self.participants, self.log_id, self.target_time))

# --- 3. کوماندا Giveaway2 ---
@bot.command()
async def giveaway2(ctx, end_time_str: str, *, content: str):
    LOG_CHANNEL_ID = 1338197816660725916
    SPECIAL_ROLE_ID = 1488244673729269780 
    MY_IMAGE_URL = "https://cdn.discordapp.com/attachments/1472835696896249898/1488242647364665544/010fcba7-5abe-4f45-afc2-a9c11a155030.png?ex=69cc1179&is=69cabff9&hm=59348862e0f8b77b06e10e4263ed6c7200eea5a5340e5cb8555bf157af5cea22&" 

    has_role = discord.utils.get(ctx.author.roles, id=SPECIAL_ROLE_ID)
    if not (has_role or ctx.author.guild_permissions.administrator):
        return await ctx.send("❌ تو مۆڵەتا بکارئینانا ڤێ کوماندا نینی!")

    try:
        now = datetime.datetime.now()
        target_time = datetime.datetime.strptime(end_time_str, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if target_time < now: target_time += datetime.timedelta(days=1)
        
        seconds_left = int((target_time - now).total_seconds())
        discord_timestamp = int(target_time.timestamp())
    except ValueError:
        return await ctx.send("❌ دەمی ب دروستی بنڤیسە (نموونە: `22:00`).")

    if "|" in content:
        requirement, prize = content.split("|", 1)
    else:
        requirement, prize = content, "خەڵاتەکێ نادیار"

    # لێرە target_time دهێتە ناردن بۆ ڤیو و مۆدال دا کۆنترۆڵا کاتی بکەن
    view = MyGiveawayView(timeout=seconds_left, log_id=LOG_CHANNEL_ID, target_time=target_time)
    
    embed = discord.Embed(
        title="🏆 پێشبینیا یاریێ و بەخشین 🏆",
        description=(
            f"🎁 **خەڵات:** **{prize.strip()}**\n"
            f"📜 **مەرج:** {requirement.strip()}\n\n"
            f"⏳ **دێ ب دووماهی هێت:** <t:{discord_timestamp}:R>\n"
            f"⏰ **دەمێ بڕانەوەی:** `{end_time_str}`"
        ),
        color=0x00aaff
    )
    if MY_IMAGE_URL.startswith("http"): embed.set_image(url=MY_IMAGE_URL)
    embed.set_footer(text="REALONES BOT – Real Ones Family")
    
    msg = await ctx.send(content="@everyone", embed=embed, view=view)

    await asyncio.sleep(seconds_left)

    end_embed = discord.Embed(
        title="🎊 GIVEAWAY ENDED - ب دووماهی هات 🎊",
        description=f"🎁 **خەڵات:** **{prize.strip()}**\n\nبەریکانە ب دووماهی هات و دوگمە ڕاوەستیا! 🏁",
        color=0xff0000
    )
    if MY_IMAGE_URL.startswith("http"): end_embed.set_image(url=MY_IMAGE_URL)
    
    await msg.edit(content=None, embed=end_embed, view=None)     

    #40 ticket 
# ==============================================================================
# 🎫 سیستەمێ تیکێتا پێشکەشکرنێ یێ پێشکەفتی (TICKET SYSTEM - REALONES)
# ==============================================================================

import discord
from discord.ext import commands
import asyncio
import datetime
import io

# --- 🔒 دوگمێن ناڤ تیکێتێ (Claim & Close Buttons) ---
class TicketActionView(discord.ui.View):
    def __init__(self, log_channel_id, staff_role_id, fields_dict=None):
        super().__init__(timeout=None)
        self.log_channel_id = log_channel_id
        self.staff_role_id = staff_role_id
        self.fields_dict = fields_dict or {}
        self.claimed_by = None

    @discord.ui.button(label="Claim 🙋‍♂️", style=discord.ButtonStyle.blurple, custom_id="claim_ticket")
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role = interaction.guild.get_role(self.staff_role_id)
        has_staff_role = staff_role in interaction.user.roles if staff_role else False
        
        if not (has_staff_role or interaction.user.guild_permissions.manage_channels):
            return await interaction.response.send_message("❌ ئەڤ دوگمە تەنێ بۆ ستاف و ئادمینانە!", ephemeral=True)
        
        if self.claimed_by:
            return await interaction.response.send_message(f"❌ ئەڤ تیکێتە بەری نوکە هاتییە وەرگرتن ژ لایێ: {self.claimed_by.mention}", ephemeral=True)
        
        self.claimed_by = interaction.user
        button.disabled = True
        button.label = f"Claimed by {interaction.user.name} ✅"
        button.style = discord.ButtonStyle.success
        
        await interaction.message.edit(view=self)
        await interaction.response.send_message(f"🔔 ئەڤ تیکێتە هاتە وەرگرتن (Claim) ژ لایێ: {interaction.user.mention}")

    @discord.ui.button(label="گرتنا تیکێتێ 🔒", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ئەڤ تیکێتە دێ پاش ٥ چرکێن دی هێتە ڕەشکرن و لۆگ هێتە پاراستن...", ephemeral=False)
        
        log_channel = interaction.guild.get_channel(self.log_channel_id)
        if log_channel:
            # 📜 کۆمکرنا تەماما نامەیێن ناو چاتێ بۆ فایلێ ترانسکریپت
            transcript_text = f"--- TRANSCRIPT FOR TICKET: {interaction.channel.name} ---\n"
            transcript_text += f"Closed By: {interaction.user.name} ({interaction.user.id})\n"
            if self.claimed_by:
                transcript_text += f"Claimed By: {self.claimed_by.name} ({self.claimed_by.id})\n"
            transcript_text += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            transcript_text += "--------------------------------------------------\n\n"

            async for message in interaction.channel.history(limit=None, oldest_first=True):
                time_str = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
                transcript_text += f"[{time_str}] {message.author.name}: {message.content}\n"

            file_buffer = io.BytesIO(transcript_text.encode('utf-8'))
            discord_file = discord.File(fp=file_buffer, filename=f"transcript-{interaction.channel.name}.txt")

            embed = discord.Embed(
                title="🔒 Ticket Closed & Saved",
                description=f"**🔹 ناڤێ چاتێ:** `{interaction.channel.name}`\n**🔹 یێ تیکێت گرتی:** {interaction.user.mention}",
                color=0xe74c3c,
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text="REAL ONE FAMILY SYSTEM")
            if self.claimed_by:
                embed.add_field(name="👤 ئادمینێ بەرسڤدای (Claimed)", value=self.claimed_by.mention, inline=True)
            
            await log_channel.send(embed=embed, file=discord_file)

        await asyncio.sleep(5)
        await interaction.channel.delete()


# --- 📋 ١. فۆرمێ پێشکەشکرنێ (Apply Modal) ---
class ApplyModal(discord.ui.Modal, title="Apply to Team - Real One"):
    name = discord.ui.TextInput(label="ناڤێ تە چییە؟", placeholder="ناڤێ خۆ یێ سێین بنڤیسە...", min_length=3, max_length=50)
    age = discord.ui.TextInput(label="تەمەنێ تە چەندە؟", placeholder="بۆ نموونە: 20", min_length=2, max_length=2)
    device = discord.ui.TextInput(label="ئامێرێ تە چییە؟ (Device)", placeholder="بۆ نموونە: PC / Mobile / PS5", max_length=30)
    reason = discord.ui.TextInput(label="ئەگەرێ هاتنا تە بۆ گانگی چییە؟", style=discord.TextStyle.long, placeholder="بنڤیسە بۆچی دڤێت ببیە ئەندام ل دەف مە...", max_length=300)
    experience = discord.ui.TextInput(label="بەری نوکە د کیژ گانگی دا بووی؟", style=discord.TextStyle.long, placeholder="ناڤێ وان گانگێن تە بەری نوکە تێدا کارکری بنڤیسە...", max_length=200)

    def __init__(self, category_id, log_channel_id, staff_role_id):
        super().__init__()
        self.category_id = category_id
        self.log_channel_id = log_channel_id
        self.staff_role_id = staff_role_id

    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket_channel(interaction, "apply", self.category_id, self.log_channel_id, self.staff_role_id, {
            "👤 ناڤ": self.name.value,
            "⏳ تەمەن": self.age.value,
            "🎮 ئامێر (Device)": self.device.value,
            "❓ ئەگەرێ هاتنێ": self.reason.value,
            "🎖️ ئەزموونا کەڤن": self.experience.value
        })

# --- 📋 ٢. فۆرمێ ئاریشەیان (Problem Modal) ---
class ProblemModal(discord.ui.Modal, title="Have a Problem - Real One"):
    subject = discord.ui.TextInput(label="بابەتێ ئاریشەیێ چییە؟", placeholder="ب کورتى بنڤیسە...", max_length=100)
    details = discord.ui.TextInput(label="شرووڤەکرنا ئاریشەیێ", style=discord.TextStyle.long, placeholder="هەمی ئاریشەیا خۆ ل ڤێرە ڕوون بکەڤە...", max_length=500)

    def __init__(self, category_id, log_channel_id, staff_role_id):
        super().__init__()
        self.category_id = category_id
        self.log_channel_id = log_channel_id
        self.staff_role_id = staff_role_id

    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket_channel(interaction, "problem", self.category_id, self.log_channel_id, self.staff_role_id, {
            "🛠️ بابەتێ ئاریشەیێ": self.subject.value,
            "📝 شرووڤەکرن": self.details.value
        })

# --- 📋 ٣. فۆرمێ ڕیپۆرتکرنێ (Report Modal) ---
class ReportModal(discord.ui.Modal, title="Report a User - Real One"):
    user_reported = discord.ui.TextInput(label="ناڤ یان ئایدییا کەسێ سەرپێچیکار", placeholder="بۆ نموونە: Name#0000 یان ID", max_length=100)
    reason = discord.ui.TextInput(label="ئەگەرێ ڕیپۆرتێ چییە؟", style=discord.TextStyle.long, placeholder="چ جۆرە سەرپێچییەک کرییە؟", max_length=400)
    proof = discord.ui.TextInput(label="بەڵگە (Proof Link)", placeholder="لینکا وێنەی یان ڤیدیۆی دابنێ ئەگەر هەبیت...", required=False, max_length=200)

    def __init__(self, category_id, log_channel_id, staff_role_id):
        super().__init__()
        self.category_id = category_id
        self.log_channel_id = log_channel_id
        self.staff_role_id = staff_role_id

    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket_channel(interaction, "report", self.category_id, self.log_channel_id, self.staff_role_id, {
            "🚨 کەسێ سەرپێچیکار": self.user_reported.value,
            "❓ ئەگەرێ ڕیپۆرتێ": self.reason.value,
            "📸 بەڵگە (Proof)": self.proof.value if self.proof.value else "نەهاتییە دانان"
        })


# --- 🏢 فەنکشنا دروستکرنا چاتێ و لۆگی ---
async def create_ticket_channel(interaction, ticket_type, category_id, log_channel_id, staff_role_id, fields_dict):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    category = discord.utils.get(guild.categories, id=category_id)
    staff_role = guild.get_role(staff_role_id)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    if staff_role:
        overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)

    ticket_channel = await guild.create_text_channel(
        name=f"{ticket_type}-{interaction.user.name}",
        category=category,
        overwrites=overwrites
    )

    embed = discord.Embed(
        title=f"📥 تیکێتەکا نوو ڤەبوو - {ticket_type.upper()}",
        description=f"**خودانێ تیکێتێ:** {interaction.user.mention}\n**ناسنامە (ID):** `{interaction.user.id}`",
        color=0xe74c3c if ticket_type == "apply" else (0x3498db if ticket_type == "problem" else 0xf1c40f)
    )
    
    # ✅ ل ڤێرە کێشەیا فۆرماتێ و f-string ب دروستی هاتە چارەسەرکرن!
    for title, val in fields_dict.items():
        embed.add_field(name=title, value=f"```\n{val}\n```", inline=False)
        
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text="REAL ONE FAMILY SYSTEM")

    # ناردنا لۆگێ ڤەکرنێ (Ticket Opened)
    log_channel = guild.get_channel(log_channel_id)
    if log_channel:
        log_embed = discord.Embed(
            title="🎫 Ticket Opened",
            color=0x2ecc71,
            timestamp=datetime.datetime.now()
        )
        log_embed.add_field(name="Ticket Name", value=f"`{ticket_channel.name}`", inline=True)
        log_embed.add_field(name="Created By", value=interaction.user.mention, inline=True)
        log_embed.add_field(name="Opened Date", value=f"`{datetime.datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')}`", inline=True)
        log_embed.add_field(name="Ticket Type", value=f"**{ticket_type.capitalize()}**", inline=False)
        
        form_data = ""
        for t, v in fields_dict.items():
            form_data += f"**{t}:** {v}\n"
        if form_data:
            log_embed.add_field(name="📋 پێزانینێن فۆرمی", value=form_data, inline=False)
            
        log_embed.set_footer(text="REALONE • TICKET SYSTEM")
        await log_channel.send(embed=log_embed)

    view = TicketActionView(log_channel_id=log_channel_id, staff_role_id=staff_role_id, fields_dict=fields_dict)
    mention_msg = f"{interaction.user.mention}" + (f" | {staff_role.mention}" if staff_role else " | @here")
    await ticket_channel.send(content=mention_msg, embed=embed, view=view)
    
    # ✅ ل ڤێرە خەلەتیا .followup.send_message هاتە چاککرن بۆ .send
    await interaction.followup.send(content=f"تیکێتا تە ب سەرکەفتن ڤەبوو! 🔗 {ticket_channel.mention}", ephemeral=True)


# --- 🗂️ کلاسێ بژاردەیان (Ticket Dropdown Menu) ---
class TicketSelect(discord.ui.Select):
    def __init__(self):
        # ⚠️ ل ڤێرە ناسنامەیا کاتیگۆرییا تیکێتان دابنێ:
        self.CATEGORY_ID = 1487914823181271202      # ئایدییا پشکا تیکێتان ل ڤێرە دابنێ
        self.LOG_CHANNEL_ID = 1487915087346929845   # لۆگ چانڵ یێ تە بخۆیە
        self.STAFF_ROLE_ID = 1462582644956205086   # رۆڵێ ستاف یێ تە بخۆیە
        self.STAFF_ROLE_ID_2 = 1511640295786156125
        options = [
            discord.SelectOption(label="Apply to Team", description="Join Krn Bo Real One!", emoji="🎯", value="apply"),
            discord.SelectOption(label="Have a Problem", description="Ta Arishak Haya.", emoji="🛠️", value="problem"),
            discord.SelectOption(label="Report a User", description="Reporta Ta L Sar Kasake Ya.", emoji="🚨", value="report")
        ]
        super().__init__(placeholder="Select a category...", min_values=1, max_values=1, options=options, custom_id="ticket_select")

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "apply":
            await interaction.response.send_modal(ApplyModal(self.CATEGORY_ID, self.LOG_CHANNEL_ID, self.STAFF_ROLE_ID))
        elif self.values[0] == "problem":
            await interaction.response.send_modal(ProblemModal(self.CATEGORY_ID, self.LOG_CHANNEL_ID, self.STAFF_ROLE_ID))
        elif self.values[0] == "report":
            await interaction.response.send_modal(ReportModal(self.CATEGORY_ID, self.LOG_CHANNEL_ID, self.STAFF_ROLE_ID))


class TicketSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


# --- 🚀 فەرمانا دروستکرنا پنلا تیکێتێ ---
@bot.command(name="createticket")  # ⚠️ ئەگەر ل سەرێ ناڤێ بۆتێ تە client بیت، ڤێرێ بکە @client.command
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(
        title="📥 Support Tickets",
        description="BU HAR TSHTAKE TICKET VAKA.\n\nژ بۆ ڤەکرنا تیکێتێ، ل خوارێ بابەتێ پێویست هەڵبژێڕە.",
        color=0x2f3136
    )
    # 🖼️ لینکا دروستا وێنەیێ مافیای د لێرەدا دابنێ
    embed.set_image(url="https://cdn.discordapp.com/attachments/1468617671540084767/1487943716189638786/1774082287767-d029482d-5516-44e5-8d38-26fe1cbf4edd_1.jpg?ex=6a215552&is=6a2003d2&hm=336f802bc78cebe8fe183a64c15bdb88bbc57cb8a0c4be3f3615ad8eac4e96c8&") 
    embed.set_footer(text="REALONES SYSTEM")
    
    await ctx.send(embed=embed, view=TicketSelectView())
    
  #41 ZIKR
@bot.event
async def on_ready():
    print(f'{bot.user} چالاک بوو!')
    
    # 🌟 ئەڤان هەردوو هێلان ل ڤێرە زێدە بکە دا کو سیستەمێ ئۆتۆماتیک دەستپێبکات:
    if not send_zikr_auto.is_running():
        send_zikr_auto.start()
    if not check_thursday_salawat.is_running():
        check_thursday_salawat.start()
# لیستی هەموو زیکران ب عەرەبی
zikr_list = [
    "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ",
    "سُبْحَانَ اللَّهِ الْعَظِيمِ",
    "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ، وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
    "أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ",
    "أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ الَّذِي لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ وَأَتُوبُ إِلَيْهِ",
    "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّه",
    "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّه الْعَلِيِّ الْعَظِيمِ",
    "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ",
    "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ",
    "صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ",
    "اللَّهُمَّ صَلِّ وَسَلِّمْ وَبَارِكْ عَلَى حَبِيبِنَا مُحَمَّدٍ",
    "لَا إِلَهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ",
    "يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ وَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ",
    "اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي",
    "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ",
    "حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ ۖ عَلَيْهِ تَوَكَّلْتُ ۖ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ",
    "رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ",
    "سُبْحَانَ اللهِ عَدَدَ خَلْقِهِ، وَرِضَا نَفْسِهِ، وَزِنَةَ عَرْشِهِ، وَمِدَادَ كَلِمَاتِهِ",
    "الْحَمْدُ لِلَّهِ حَمْدًا كَثِيرًا طَيِّبًا مُبَارَكًا فِيهِ",
    "اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ",
    "رَبِّ اغْفِرْ لِي وَتُبْ عَلَيَّ إِنَّكَ أَنْتَ التَّوَّابُ الرَّحِيمُ",
    "Yَا مُقَلِّبَ الْقُلُوبِ ثَبِّتْ قَلْبِي عَلَى دِينِكَ",
    "اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ",
    "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ",
    "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ",
    "رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ نَبِيًّا",
    "يَا ذَا الْجَلَالِ وَالْإِكْرَامِ",
    "رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي",
    "اللَّهُمَّ أَجِرْنِي مِنَ النَّارِ",
    "لَا إِلَهَ إِلَّا اللَّهُ الْعَظِيمُ الْحَلِيمُ، لَا إِلَهَ إِلَّا اللَّهُ رَبُّ الْعَرْشِ الْعَظِيمِ",
    "اللَّهُمَّ اغْفِرْ لِلْمُؤْمِنِينَ وَالْمُؤْمِنَاتِ وَالْمُسْلِمِينَ وَالْمُسْلِمَاتِ الْأَحْيَاءِ مِنْهُمْ وَالْأَمْوَاتِ",
    "رَبَّنَا تَقَبَّلْ مِنَّا ۖ إِنَّكَ أَنْتَ السَّمِيعُ الْعَلِيمُ",
    "تَوَفَّنِي مُسْلِمًا وَأَلْحِقْنِي بِالصَّالِحِينَ",
    "رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِنْ لَدُنْكَ رَحْمَةً",
    "لَا إِلَهَ إِلَّا اللهُ المَلِكُ الحَقُّ المُبِينُ",
    "رَبِّ اغْفِرْ وَارْحَمْ وَأَنْتَ خَيْرُ الرَّاحِمِينَ"
]

# زێدەکرنا لۆپێ بۆ زێدەبوونا زیکران
for i in range(1, 201):
    zikr_list.append("اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ")
    zikr_list.append("أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ")

# 🔴 ئایدییا چەناڵێ خۆ یێ زیکران ل ڤێرە دابنێ
ZIKR_CHANNEL_ID = 1524843087363313845
# --- فەرمانێن دەستی (Manual Commands) ---

@bot.command(name="zikr")
async def get_zikr(ctx):
    selected_zikr = random.choice(zikr_list)
    embed = discord.Embed(
        title="✨ زیکرێ تە ✨",
        description=f"**{selected_zikr}**",
        color=discord.Color.from_rgb(52, 152, 219)
    )
    embed.set_footer(text="خودێ خێرا تە بنڤیسیت 🤍")
    await ctx.send(embed=embed)

@bot.command(name="salawat")
async def get_salawat(ctx):
    embed = discord.Embed(
        title="🕌 سلاڤدان ل سەر پێغەمبەری 🕌",
        description="**اللَّهُمَّ صَلِّ وَسَلِّم *عَلَى نَبِيِّنَا مُحَمَّدٍ ﷺ**",
        color=discord.Color.gold()
    )
    embed.set_footer(text="اللَّهُمَّ صَلِّ وَسَلِّم *وَبَارِكْ عَلَيْهِ")
    await ctx.send(embed=embed)

# --- تاسیێن ئۆتۆماتیک (Automated Tasks) ---

@tasks.loop(minutes=30)
async def send_zikr_auto():
    channel = bot.get_channel(ZIKR_CHANNEL_ID)
    if channel:
        selected_zikr = random.choice(zikr_list)
        embed = discord.Embed(
            title="✨ زیکرێ ئۆتۆماتیک ✨",
            description=f"**{selected_zikr}**",
            color=discord.Color.from_rgb(46, 204, 113)
        )
        embed.set_footer(text="أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ 🤍")
        await channel.send(embed=embed)

@tasks.loop(minutes=1)
async def check_thursday_salawat():
    now = datetime.datetime.now()
    if now.weekday() == 3 and now.hour == 22 and now.minute == 0:
        channel = bot.get_channel(ZIKR_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="🕌 شەڤا ئەینیێ (سلاڤدان ل سەر پێغەمبەری) 🕌",
                description="**اللَّهُمَّ صَلِّ وَسَلِّم *وَبَارِكْ عَلَى نَبِيِّنَا وَحَبِيبِنَا مُحَمَّدٍ ﷺ**\n\nشەڤا ئەینیێ یە، دلێن خۆ ڕووناک بکەن ب سلاڤدانێ ل سەر ڕوحا پاقژا پێغەمبەرێ مە.",
                color=discord.Color.gold()
            )
            embed.set_footer(text="إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ ۚ يَا أَيُّهَا الَّذِينَ آمَنُوا صَلُّوا عَلَيْهِ وَسَلِّمُوا تَسْلِيمًا")
            await channel.send(content="@everyone", embed=embed)

# --- Error Handling ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ This command does not exist!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to do this!")

# --- کارپێکرنا بۆتی ---
if TOKEN:
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("❌ Error: Login failed. Check your Token!")
else:
    print("❌ Error: TOKEN not found!")