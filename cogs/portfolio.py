import discord
from discord.ext import commands
from discord import app_commands
from utils.database import load_portfolio, save_portfolio

class PortfolioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addstock", description="新增自選股到清單")
    async def addstock(self, interaction: discord.Interaction, stock_id: str, shares: int):
        await interaction.response.defer(ephemeral=True)
        save_portfolio(interaction.user.id, stock_id, shares)
        await interaction.followup.send(f"✅ 已將 {shares} 股 {stock_id} 加入你的自選股清單。")

    @app_commands.command(name="mystocks", description="查看我的自選股清單")
    async def mystocks(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        portfolio = load_portfolio(interaction.user.id)
        if not portfolio:
            await interaction.followup.send("📋 你的自選股清單是空的。")
            return

        stocks_text = "\n".join([f"📈 {s['stock_id']} - {s['shares']} 股" for s in portfolio])
        await interaction.followup.send(f"你的自選股列表：\n{stocks_text}")

async def setup(bot):
    await bot.add_cog(PortfolioCog(bot))
