import discord
from discord.ext import commands, tasks
import os
import json
from utils.database import view_portfolio
from utils.fetcher import get_realtime_data
from datetime import datetime, timedelta
import asyncio

class AlertScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("PUSH_CHANNEL_ID", 0))  # 環境變數設定推播頻道 ID
        self.daily_push.start()  # ⏰ 啟動每天定時任務

    def cog_unload(self):
        self.daily_push.cancel()  # Cog卸載時取消任務

    @tasks.loop(hours=24)
    async def daily_push(self):
        """每天固定時間推播自選股資訊"""
        await self.push_stock_summary()

    @daily_push.before_loop
    async def before_daily_push(self):
        """等待到每天9:00再開始推播"""
        now = datetime.now()
        target = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        print(f"⏳ 等待 {wait_seconds} 秒後開始每日推播任務...")
        await asyncio.sleep(wait_seconds)

    async def push_stock_summary(self):
        """推送目前所有自選股現價"""
        if not self.channel_id:
            print("❗ PUSH_CHANNEL_ID 未設定，跳過推播。")
            return

        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print("❗ 找不到推播頻道，ID設定錯誤。")
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
