import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
import os
import json
import yfinance as yf
import ta
from utils.database import view_portfolio

class AlertScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("PUSH_CHANNEL_ID", 0))  # 指定推播頻道
        self.daily_push.start()

    def cog_unload(self):
        self.daily_push.cancel()

    @tasks.loop(hours=24)
    async def daily_push(self):
        today = datetime.now().date()
        if today.weekday() >= 5:  # 六日不推播
            return
        await self.push_stock_summary()

    @daily_push.before_loop
    async def before_daily_push(self):
        await self.bot.wait_until_ready()
        now = datetime.utcnow() + timedelta(hours=8)  # 台灣時間
        target = now.replace(hour=8, minute=45, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        print(f"⏳ 等待 {int(wait_seconds)} 秒後開始每日推播...")
        await asyncio.sleep(wait_seconds)

    async def push_stock_summary(self):
        if not self.channel_id:
            print("❗ 未設定推播頻道 ID。")
            return

        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print("❗ 找不到推播頻道。")
            return

        message = "**📢 每日自選股提醒！ (以昨日收盤分析)**\n"

        try:
            with open("data/portfolio.json", encoding="utf-8") as f:
                portfolios = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            portfolios = {}

        symbols = set()
        for user_id, stocks in portfolios.items():
            for s in stocks:
                symbols.add(s["stock_id"])

        for stock_id in symbols:
            try:
                yahoo_symbol = f"{stock_id}.TW"
                df = yf.download(yahoo_symbol, period="10d", interval="1d", progress=False)

                if df.empty or "Close" not in df:
                    message += f"\n❌ `{stock_id}` 無法取得資料"
                    continue

                close_price = df["Close"].iloc[-1]
                rsi = ta.momentum.RSIIndicator(df["Close"]).rsi().iloc[-1]
                ma5 = df["Close"].rolling(5).mean().iloc[-1]
                ma20 = df["Close"].rolling(20).mean().iloc[-1]

                analysis = []
                if close_price > ma5 > ma20:
                    analysis.append("🔼 多頭排列")
                elif close_price < ma5 < ma20:
                    analysis.append("🔽 空頭排列")
                else:
                    analysis.append("➡️ 盤整區間")

                if rsi >= 70:
                    analysis.append("⚠️ RSI 過熱")
                elif rsi <= 30:
                    analysis.append("💡 RSI 超跌")

                message += f"\n📈 `{stock_id}` 昨收：{close_price:.2f} 元 ｜{', '.join(analysis)}"

            except Exception as e:
                print(f"[ERROR] 分析 {stock_id} 時發生錯誤：{e}")
                message += f"\n❗ `{stock_id}` 分析失敗"

        await channel.send(message)

    @commands.command(name="simulatepush")
    async def simulate_push(self, ctx):
        await self.push_stock_summary()
        await ctx.send("✅ 推播模擬完成！")

async def setup(bot):
    await bot.add_cog(AlertScheduler(bot))
