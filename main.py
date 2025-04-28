import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True  # 讓Bot能讀取訊息內容

bot = commands.Bot(command_prefix="/", intents=intents)

extensions = ['cogs.stock', 'cogs.news', 'cogs.alert', 'cogs.history', 'cogs.portfolio']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def setup_hook():
    # 載入所有功能模組
    for ext in extensions:
        await bot.load_extension(ext)

    # 同步 Slash Commands
    synced = await bot.tree.sync()
    print(f'Successfully synced {len(synced)} slash commands.')

bot.run(os.getenv('DISCORD_TOKEN'))
