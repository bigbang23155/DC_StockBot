import discord
from discord.ext import commands, tasks
import os
import json
import asyncio
from datetime import datetime, timedelta
import pytz

from utils.database import view_portfolio
from utils.fetcher import get_realtime_data

class AlertScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("PUSH_CHANNEL_ID", 0))  # 推播頻道 ID（環境變數設定）
        self.daily_push.start()

    def cog_unload(self):
        self.daily_push.cancel()

    @tasks.loop(hours=24)
    async def daily_push(self):
        await self.push_stock_summary()

    @daily_push.before_loop
    async def before_daily_push(self):
        tz = pytz.timezone("Asia/Taipei")
        now = datetime.now(tz)
        target = now.replace(hour=8, minute=45, second=0, microsecond=0)

        # 若現在已過時間或為週末，找下一個平日
        if now > target or now.weekday() >= 5:
            days_to_add = 1
            while True:
                next_day = now + timedelta(days=days_to_add)
                if next_day.weekday() < 5:
                    target = next_day.replace(hour=8, minute=45, second=0, microsecond=0)
                    break
                days_to_add += 1

        wait_seconds = (target - now).total_seconds()
        print(f"⏳ 等待 {wait_seconds:.2f} 秒（至 {target.strftime('%Y-%m-%d %H:%M:%S')}）後開始每日推播任務...")
        await asyncio.sleep(wait_seconds)

    async def push_stock_summary(self):
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

        sent = False
        for user_id, stocks in portfolios.items():
            for stock in stocks:
                stock_id = stock["stock_id"]
                realtime = get_realtime_data(stock_id)
                if realtime:
                    message += f"\n📈 `{stock_id}` {realtime['name']} 現價：{realtime['latest_trade_price']} 元"
                    sent = True

        if sent:
            await channel.send(message)
        else:
            await channel.send("📭 今天沒有任何自選股資料可供推播。")

    @commands.command(name="simulatepush")
    async def simulate_push(self, ctx):
        """手動測試推播（管理員用）"""
        await self.push_stock_summary()
        await ctx.send("✅ 推播模擬完成！訊息已送出。")

async def setup(bot):
    await bot.add_cog(AlertScheduler(bot))
