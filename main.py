import discord
from discord.ext import commands
import os
import threading
import time

# 保持活躍 (避免Render自動斷線)
def keep_alive():
    def run():
        while True:
            time.sleep(600)
            print("✅ Keep alive pinging...")
    t = threading.Thread(target=run)
    t.start()

if os.environ.get('RENDER'):
    keep_alive()

# 設定 Intents
intents = discord.Intents.default()
intents.message_content = True

# 初始化Bot
bot = commands.Bot(command_prefix="/", intents=intents)

# 要載入的Cogs清單
extensions = [
    'cogs.stock',
    'cogs.news',
    'cogs.alert',
    'cogs.history',
    'cogs.portfolio',  # ✅ Correct
    'cogs.admin'
]

@bot.event
async def setup_hook():
    for ext in extensions:
        await bot.load_extension(ext)
    
    # 強制全域同步 Slash 指令（大概15分鐘生效）
    await bot.tree.sync()
    print("✅ Slash commands globally synced!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv('DISCORD_TOKEN'))
