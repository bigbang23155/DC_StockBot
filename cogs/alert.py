import discord
from discord.ext import commands
from utils.database import save_alert

class AlertCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data.get("custom_id", "").startswith("alert_"):
            stock_id = interaction.data["custom_id"].split("_")[1]

            modal = AlertModal(stock_id)
            await interaction.response.send_modal(modal)

class AlertModal(discord.ui.Modal):
    def __init__(self, stock_id):
        super().__init__(title="設定提醒")
        self.stock_id = stock_id
        self.add_item(discord.ui.InputText(label="提醒價格", placeholder="輸入目標價格", style=discord.InputTextStyle.short))

    async def callback(self, interaction: discord.Interaction):
        target_price = self.children[0].value
        if not target_price.replace('.', '', 1).isdigit():
            await interaction.response.send_message("請輸入正確的數字價格！", ephemeral=True)
            return

        save_alert(interaction.user.id, self.stock_id, float(target_price))
        await interaction.response.send_message(f"已設定提醒：{self.stock_id} 達到 {target_price} 元！", ephemeral=True)

def setup(bot):
    bot.add_cog(AlertCog(bot))
