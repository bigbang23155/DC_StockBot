import discord
from discord.ext import commands
from discord import app_commands
from utils.database import add_to_portfolio, remove_from_portfolio, view_portfolio

class PortfolioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addstock", description="新增自選股到清單")
    async def addstock(self, interaction: discord.Interaction, stock_id: str, shares: int):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            add_to_portfolio(interaction.user.id, stock_id, shares)
            await interaction.followup.send(f"✅ 已將 {shares} 股 {stock_id} 加入你的自選股清單！")
        except Exception as e:
            print(f"❌ addstock error: {e}")
            await interaction.followup.send("新增自選股失敗，請稍後再試～")

    @app_commands.command(name="removestock", description="從自選股清單移除")
    async def removestock(self, interaction: discord.Interaction, stock_id: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            remove_from_portfolio(interaction.user.id, stock_id)
            await interaction.followup.send(f"🗑️ 已將 {stock_id} 從你的自選股清單中移除！")
        except Exception as e:
            print(f"❌ removestock error: {e}")
            await interaction.followup.send("移除自選股失敗，請稍後再試～")

    @app_commands.command(name="overview", description="查看你的自選股總覽（含 ETF）")
    async def overview(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            portfolio = view_portfolio(interaction.user.id)
            if not portfolio:
                await interaction.followup.send("📋 你的自選股清單是空的。")
                return

            stocks = [s for s in portfolio if not s["stock_id"].startswith("0")]
            etfs = [s for s in portfolio if s["stock_id"].startswith("0")]

            text = "**📈 自選個股：**\n" if stocks else ""
            text += "\n".join([f"• {s['stock_id']} - {s['cost']} 股" for s in stocks]) + "\n\n" if stocks else ""

            text += "**🧺 自選 ETF：**\n" if etfs else ""
            text += "\n".join([f"• {s['stock_id']} - {s['cost']} 股" for s in etfs]) if etfs else ""

            await interaction.followup.send(text or "📋 清單為空！")
        except Exception as e:
            print(f"❌ overview error: {e}")
            await interaction.followup.send("查詢失敗，請稍後再試～")

async def setup(bot):
    await bot.add_cog(PortfolioCog(bot))
