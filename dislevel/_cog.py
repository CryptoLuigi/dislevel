import os
from typing import Union, Optional

from discord import Embed, File, Member, Interaction
from discord.ext import commands
import nextcord
from easy_pil.utils import run_in_executor

from .card import get_card
from .utils import *

botchannel = f'<#638020706935767100>'
bot_channel_id = 638020706935767100

def is_bot_channel(channel: nextcord.TextChannel):
    return  channel.id == bot_channel_id or str(channel) in ["bots", "🐍-bots"]


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
            if is_bot_channel(ctx.channel):
                await get_rank(self.bot, ctx, member)
        except Exception as ex:
            print("Exception getting user rank:", ex)
            await ctx.send(content=f"{ctx.author.mention} That user is unranked or a bot.")

    @commands.command(aliases=["lb"])
    async def leaderboard(self, interaction: Interaction, page:Optional[int]):
        """See the server leaderboard"""
        if is_bot_channel(interaction.channel):
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

