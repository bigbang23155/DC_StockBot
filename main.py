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
    'cogs.admin'
]

@bot.event
async def setup_hook():
    for ext in extensions:
        await bot.load_extension(ext)
    
    # 強制全域同步（不要只同步特定伺服器）
    await bot.tree.sync()
    print("✅ Slash commands globally synced!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv('DISCORD_TOKEN'))
