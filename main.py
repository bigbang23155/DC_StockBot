import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

extensions = [
    'cogs.stock',
    'cogs.news',
    'cogs.alert',
    'cogs.history',
    'cogs.portfolio'
]

@bot.event
async def setup_hook():
    for ext in extensions:
        await bot.load_extension(ext)
    
    # 強制重新同步指令樹
    try:
        guild = discord.Object(id=你的伺服器ID)  # <<< 這邊要放你的伺服器ID
        await bot.tree.sync(guild=guild)
        print(f"✅ Slash commands synced to guild {guild.id}")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv('DISCORD_TOKEN'))
