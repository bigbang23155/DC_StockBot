import discord
from discord.ext import commands
from utils.database import add_to_portfolio, remove_from_portfolio, view_portfolio

class PortfolioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addstock")
    async def addstock(self, ctx, stock_id: str, cost: float):
        add_to_portfolio(ctx.author.id, stock_id, cost)
        await ctx.send(f"已新增到自選股清單：{stock_id}，成本價：{cost}元。")

    @commands.command(name="removestock")
    async def removestock(self, ctx, stock_id: str):
        remove_from_portfolio(ctx.author.id, stock_id)
        await ctx.send(f"已從自選股清單移除：{stock_id}。")

    @commands.command(name="mystocks")
    async def mystocks(self, ctx):
        portfolio = view_portfolio(ctx.author.id)
        if not portfolio:
            await ctx.send("你的自選股清單是空的。")
            return

        text = "\n".join([f"{p['stock_id']} 成本價：{p['cost']}" for p in portfolio])
        await ctx.send(f"你的自選股清單：\n{text}")

async def setup(bot):
    bot.add_cog(PortfolioCog(bot))
