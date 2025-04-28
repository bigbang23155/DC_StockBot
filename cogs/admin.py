import discord
from discord.ext import commands
from discord import app_commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sync", description="🔄 重新同步Slash指令（伺服器快速同步）")
    @commands.has_permissions(administrator=True)
    async def sync_commands(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            guild = discord.Object(id=1366258423435362377)  # 🛠 改成你的伺服器ID
            synced = await interaction.client.tree.sync(guild=guild)
            await interaction.followup.send(f"✅ 成功同步 {len(synced)} 個指令到伺服器！")
        except Exception as e:
            await interaction.followup.send(f"❌ 同步失敗：{e}")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
