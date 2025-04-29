import discord
from discord.ext import commands, tasks
import os
from utils.database import view_portfolio
from utils.fetcher import get_realtime_data

class AlertScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("PUSH_CHANNEL_ID", 0))  # 記得環境變數設定
        self.daily_push.start()  # ⏰ 啟動定時任務！

    def cog_unload(self):
        self.daily_push.cancel()

    @tasks.loop(hours=24)
    async def daily_push(self):
        if not self.channel_id:
            print("❗ PUSH_CHANNEL_ID 沒設定，跳過推播。")
            return
        
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print("❗ 找不到指定推播頻道，請確認ID正確。")
            return

        # 建立訊息
        message = "**📢 每日自選股提醒！**\n"
        user_ids = [f for f in os.listdir("data") if f.endswith(".json")]

        # 因為資料是共用一個檔案，所以用 view_portfolio 取每個用戶
        for user_id in set(json.loads(open('data/portfolio.json', encoding="utf-8").read() or "{}").keys()):
            portfolio = view_portfolio(user_id)
            for stock in portfolio:
                stock_id = stock["stock_id"]
                realtime = get_realtime_data(stock_id)
                if realtime:
                    message += f"\n📈 `{stock_id}` {realtime['name']} 現價：{realtime['latest_trade_price']} 元"

        await channel.send(message)

    @daily_push.before_loop
    async def before_daily_push(self):
        from datetime import datetime, timedelta
        import asyncio

        now = datetime.now()
        target = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        print(f"⏳ 等待 {wait_seconds} 秒後開始每日推播任務...")
        await asyncio.sleep(wait_seconds)

async def setup(bot):
    await bot.add_cog(AlertScheduler(bot))import discord
from discord.ext import commands, tasks
import os
import json
from utils.database import view_portfolio
from utils.fetcher import get_realtime_data

class AlertScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("PUSH_CHANNEL_ID", 0))
        self.daily_push.start()

    def cog_unload(self):
        self.daily_push.cancel()

    @tasks.loop(hours=24)
    async def daily_push(self):
        await self.push_stock_summary()

    @daily_push.before_loop
    async def before_daily_push(self):
        from datetime import datetime, timedelta
        import asyncio
        now = datetime.now()
        target = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        print(f"⏳ 等待 {wait_seconds} 秒後開始每日推播任務...")
        await asyncio.sleep(wait_seconds)

    async def push_stock_summary(self):
        if not self.channel_id:
            print("❗ PUSH_CHANNEL_ID 未設定，跳過推播。")
            return
        
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print("❗ 找不到推播頻道，ID可能設定錯誤。")
            return

        message = "**📢 每日自選股提醒！**\n"
        try:
            with open('data/portfolio.json', encoding="utf-8") as f:
                portfolios = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            portfolios = {}

        for user_id, stocks in portfolios.items():
            for stock in stocks:
                stock_id = stock["stock_id"]
                realtime = get_realtime_data(stock_id)
                if realtime:
                    message += f"\n📈 `{stock_id}` {realtime['name']} 現價：{realtime['latest_trade_price']} 元"

        await channel.send(message)

    @commands.command(name="simulatepush")
    async def simulate_push(self, ctx):
        """手動測試推播 (管理員用)"""
        await self.push_stock_summary()
        await ctx.send("✅ 推播模擬完成！訊息已送出。")

async def setup(bot):
    await bot.add_cog(AlertScheduler(bot))

