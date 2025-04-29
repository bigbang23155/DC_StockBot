import discord
from discord.ext import commands
from discord import app_commands

class SimulatePushCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="simulatepush", description="模擬一次每日自選股推播")
    async def simulatepush(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # 模擬資料（未來會用真實自選股資料）
        stocks = [
            {"name": "台積電", "stock_id": "2330", "cost": 650, "current": 720},
            {"name": "聯電", "stock_id": "2303", "cost": 40, "current": 39}
        ]
        etfs = [
            {"name": "元大台灣50", "stock_id": "0050", "cost": 135, "current": 140},
            {"name": "富邦台50", "stock_id": "006208", "cost": 72, "current": 75}
        ]

        stock_text = ""
        for stock in stocks:
            rate = (stock["current"] - stock["cost"]) / stock["cost"] * 100
            emoji = "🟢" if rate >= 0 else "🔴"
            stock_text += f"- {stock['stock_id']} {stock['name']}｜成本 {stock['cost']}｜現價 {stock['current']}｜{emoji} 報酬率 {rate:+.2f}%\n"

        etf_text = ""
        for etf in etfs:
            rate = (etf["current"] - etf["cost"]) / etf["cost"] * 100
            emoji = "🟢" if rate >= 0 else "🔴"
            etf_text += f"- {etf['stock_id']} {etf['name']}｜成本 {etf['cost']}｜現價 {etf['current']}｜{emoji} 報酬率 {rate:+.2f}%\n"

        embed = discord.Embed(title="🗓️【每日自選總覽】", color=0x00ff00)
        embed.add_field(name="📈【個股列表】", value=stock_text or "無", inline=False)
        embed.add_field(name="🏦【ETF列表】", value=etf_text or "無", inline=False)
        embed.set_footer(text="✨ 堅持紀律，掌握市場脈動！")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SimulatePushCog(bot))
