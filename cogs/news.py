import discord
from discord.ext import commands
from utils.fetcher import fetch_news

class NewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data.get("custom_id", "").startswith("news_"):
            stock_id = interaction.data["custom_id"].split("_")[1]
            news_list = fetch_news(stock_id)
            if not news_list:
                await interaction.response.send_message("找不到相關新聞。", ephemeral=True)
                return

            news_text = "\n\n".join([f"📌 {n['title']}\n{n['link']}" for n in news_list])
            await interaction.response.send_message(news_text, ephemeral=True)

def setup(bot):
    bot.add_cog(NewsCog(bot))
