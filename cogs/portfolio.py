import discord
from discord.ext import commands
from discord import app_commands
from utils.database import add_to_portfolio, view_portfolio

class PortfolioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addstock", description="新增自選股到清單")
    async def addstock(self, interaction: discord.Interaction, stock_id: str, shares: int):
        # ⚡ 立刻 defer，防止超時
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        try:
            add_to_portfolio(interaction.user.id, stock_id, shares)
            await interaction.followup.send(f"✅ 已將 {shares} 股 {stock_id} 加入你的自選股清單！")
        except Exception as e:
            print(f"❌ addstock error: {e}")
            await interaction.followup.send("新增自選股失敗，請稍後再試～")

    @app_commands.command(name="mystocks", description="查看我的自選股清單")
    async def mystocks(self, interaction: discord.Interaction):
        # ⚡ 立刻 defer，防止超時
        await interaction.response.defer(thinking=True, ephemeral=True)
        
        try:
            portfolio = view_portfolio(interaction.user.id)
            if not portfolio:
                await interaction.followup.send("📋 你的自選股清單是空的。")
                return

            stocks_text = "\n".join([f"📈 {s['stock_id']} - {s['cost']} 股" for s in portfolio])
            await interaction.followup.send(f"你的自選股列表：\n{stocks_text}")
        except Exception as e:
            print(f"❌ mystocks error: {e}")
            await interaction.followup.send("查詢自選股失敗，請稍後再試～")

async def setup(bot):
    await bot.add_cog(PortfolioCog(bot))
