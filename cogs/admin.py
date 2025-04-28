import discord
from discord.ext import commands
from discord import app_commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sync", description="🔄 重新同步Slash指令（管理員專用）")
    @commands.has_permissions(administrator=True)  # 必須是管理員才能用
    async def sync_commands(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)  # 先 defer
        
        try:
            synced = await interaction.client.tree.sync()
            await interaction.followup.send(f"✅ 成功同步 {len(synced)} 個指令到全域！")
        except Exception as e:
            await interaction.followup.send(f"❌ 同步失敗：{e}")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
