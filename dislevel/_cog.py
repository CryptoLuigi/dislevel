import os
from typing import Union, Optional

from discord import Embed, File, Member, Interaction
from discord.ext import commands
from easy_pil.utils import run_in_executor

from .card import get_card
from .utils import *

botchannel = f'<#1029782845071294595>'

class Leveling(commands.Cog):
    """Leveling commands"""

    def __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx: commands.Context, *, member: Member = None):
        """Check rank of a user"""
        if member == None:
            member = ctx.author
        try:
            current_channel = f"{ctx.channel}"
            if current_channel == f'bots' or current_channel == f'bot-development'or current_channel ==f'🐍-bots':
                await get_rank(self.bot, ctx, member)
        except:
            await ctx.send(content=f"{ctx.author.mention} That user is unranked or a bot.")

    @commands.command(aliases=["lb"])
    async def leaderboard(self, interaction: Interaction, page:Optional[int]):
        """See the server leaderboard"""
        current_channel = f"{interaction.channel}"
        if current_channel == f'bots' or current_channel == f'bot-development'or current_channel ==f'🐍-bots':
            await get_page(self.bot, interaction, page)
            print(f"Leaderboard Requested by {interaction.author}")

    @commands.command()
    async def setbg(self, ctx: commands.Context, *, url: str):
        """Set image of your card bg"""
        await set_bg_image(self.bot, ctx.author.id, ctx.guild.id, url)
        await ctx.send(content=f"Background image has been updated")

    @commands.command()
    async def resetbg(self, ctx: commands.Context):
        """Reset image of your card bg"""
        await set_bg_image(self.bot, ctx.author.id, ctx.guild.id, "")
        await ctx.send("Background image has been set to default")

    @commands.command()
    async def setcolor(self, ctx: commands.Context, color: str, color2: str, color3: str):
        """Set color of the text of your rank card"""
        await set_text_color(self.bot, ctx.author.id, ctx.guild.id, color, color2, color3)
        await ctx.send(content=f"Text color has been updated")

    @commands.command()
    async def overlay(self, ctx: commands.Context, toggle:int):
        """Toggle the overlay in your rank card"""
        await toggle_overlay(self.bot, ctx.author.id, ctx.guild.id, state=toggle)
        await ctx.send(content=f"The overlay has been toggled")

    @commands.command()
    async def nick(self, ctx: commands.Context, toggle:int):
        """Toggle the overlay in your rank card"""
        await toggle_nick(self.bot, ctx.author.id, ctx.guild.id, state=toggle)
        await ctx.send(content=f"Your nickname has been toggled")

    @commands.command()
    async def resetcolor(self, ctx: commands.Context):
        """Reset color of your card bg"""
        await set_text_color(self.bot, ctx.author.id, ctx.guild.id, color=f"white", color2=f"grey", color3=f"white")
        await ctx.send(content=f"Text color has been set to default")

