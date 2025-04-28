import discord
from discord.ext import commands
from discord import app_commands
from utils.fetcher import get_realtime_data, get_kline_data
from utils.analysis import analyze_stock
from utils.kline_analysis import kline_pattern
from utils.database import save_history

class StockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stock", description="查詢台股即時資料")
    async def stock(self, interaction: discord.Interaction, stock_id: str):
        # 取得即時資料
        realtime = get_realtime_data(stock_id)
        if not realtime:
            await interaction.response.send_message("查詢失敗，請確認股票代碼。", ephemeral=True)
            return
        
        # 均線分析 + 巴菲特邏輯建議
        ma_analysis, buffett_suggestion = analyze_stock(stock_id)

        # K線型態分析
        kline_type, meaning = kline_pattern(stock_id)

        # 存查詢紀錄
        save_history(interaction.user.id, stock_id, realtime['latest_trade_price'])

        # 整理回覆訊息
        embed = discord.Embed(title=f"{realtime['name']} ({stock_id})", color=0x00ff00)
        embed.add_field(name="今日股價", value=f"開: {realtime['open']} 高: {realtime['high']} 低: {realtime['low']} 收: {realtime['latest_trade_price']}", inline=False)
        embed.add_field(name="均線分析", value=ma_analysis, inline=False)
        embed.add_field(name="操作建議", value=buffett_suggestion, inline=False)
        embed.add_field(name="K線型態", value=f"{kline_type}\n{meaning}", inline=False)

        # 加按鈕互動
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="查看新聞", style=discord.ButtonStyle.primary, custom_id=f"news_{stock_id}"))
        view.add_item(discord.ui.Button(label="設定提醒", style=discord.ButtonStyle.success, custom_id=f"alert_{stock_id}"))
        view.add_item(discord.ui.Button(label="查詢紀錄", style=discord.ButtonStyle.secondary, custom_id=f"history_{stock_id}"))

        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(StockCog(bot))
