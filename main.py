import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True  # 讓Bot能讀取訊息內容

bot = commands.Bot(command_prefix="/", intents=intents)

# 載入功能模組
extensions = ['cogs.stock', 'cogs.news', 'cogs.alert', 'cogs.history', 'cogs.portfolio']
for ext in extensions:
    bot.load_extension(ext)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

bot.run(os.getenv('DISCORD_TOKEN'))