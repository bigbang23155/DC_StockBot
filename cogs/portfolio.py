import discord
from discord.ext import commands
from discord import app_commands
from utils.database import add_to_portfolio, view_portfolio

class PortfolioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addstock", description="新增自選股到清單")
    async def addstock(self, interaction: discord.Interaction, stock_id: str, cost: int):
        await interaction.response.defer(ephemeral=True)
        add_to_portfolio(interaction.user.id, stock_id, cost)
        await interaction.followup.send(f"✅ 已將 {stock_id} (成本 {cost} 元) 加入你的自選股清單。")

    @app_commands.command(name="mystocks", description="查看我的自選股清單")
    async def mystocks(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        portfolio = view_portfolio(interaction.user.id)
        if not portfolio:
            await interaction.followup.send("📋 你的自選股清單是空的。")
            return

        stocks_text = "\n".join([
            f"📈 {item['stock_id']} - 成本 {item['cost']} 元"
            for item in portfolio
        ])
        await interaction.followup.send(f"你的自選股列表：\n{stocks_text}")

async def setup(bot):
    await bot.add_cog(PortfolioCog(bot))
