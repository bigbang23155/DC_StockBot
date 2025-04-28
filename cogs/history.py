import discord
from discord.ext import commands
from utils.database import load_history

class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data.get("custom_id", "").startswith("history_"):
            stock_id = interaction.data["custom_id"].split("_")[1]
            history = load_history(interaction.user.id, stock_id)

            if not history:
                await interaction.response.send_message("沒有查詢紀錄。", ephemeral=True)
                return

            history_text = "\n".join([f"{h['date']} - {h['price']}元" for h in history[-10:]])
            await interaction.response.send_message(f"最近10次查詢紀錄：\n{history_text}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HistoryCog(bot))
