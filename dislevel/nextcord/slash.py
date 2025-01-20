from typing import Optional, Union
from nextcord.ui import View, Button, Select, TextInput, Modal
from nextcord import Interaction, Member, slash_command, ButtonStyle, user_command, SlashOption, SelectOption, utils, File, TextInputStyle
from nextcord.ext import commands, application_checks
from ..mee6_export import get_mee6_data
from ..utils import *
from databases import Database
from dislevel import init_dislevel

level_roles = [
    (5, "Farmer (Level 5)"),
    (10, "Soldier (Level 10)"),
    (15, "Craftsman (Level 15)"),
    (20, "Merchant (Level 20)"),
    (25, "Mayor (Level 25)"),
    (30, "Shrine Maiden (Level 30)"),
    (35, "Noble (Level 35)"),
    (40, "Aub (Level 40)"),
    (50, "Zent (Level 50)"),
    (60, "Goddess (Level 60)"),
]


class LevelingSlash(commands.Cog):
    """Leveling commands"""

    def __init__(self, bot: Union[commands.Bot, commands.AutoShardedBot]):
        self.bot = bot

    @user_command(name="Rank User")
    async def rank_user(self, interaction: Interaction, member: Member):
        """Check rank of a user"""
        botchannel = await get_setting(self.bot, interaction.guild_id, name="botchannel")
        try:
            current_channel = interaction.channel.id
            if current_channel == int(botchannel[0]):
                await get_rank(self.bot, interaction, member)
            else:
                await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in <#{botchannel[0]}>")
        except Exception:
            await interaction.response.send_message(content=f"{interaction.user.mention} That user is unranked or a bot.")

    @slash_command(description="Check rank of a user")
    async def rank(self, interaction: Interaction, *, member: Optional[Member]):
        """Check rank of a user"""
        botchannel = await get_setting(self.bot, interaction.guild_id, name="botchannel")
        try:
            current_channel = interaction.channel.id
            if current_channel == int(botchannel[0]):
                await get_rank(self.bot, interaction, member)
            else:
                await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in <#{botchannel[0]}>")
        except:
            await interaction.response.send_message(content=f"{interaction.user.mention} That user is unranked or a bot.")

    @slash_command(description="See the server leaderboard")
    async def leaderboard(self, interaction: Interaction, page:Optional[int]):
        """See the server leaderboard"""
        botchannel = await get_setting(self.bot, interaction.guild_id, name="botchannel")
        current_channel = interaction.channel.id
        if current_channel == int(botchannel[0]):
            await get_page(self.bot, interaction, page)
            print(f"Leaderboard Requested by {interaction.user.name}")
        else:
            await interaction.response.send_message(ephemeral=True, content=f"{interaction.user.mention} This can only be used in <#{botchannel[0]}>")

    @slash_command(description="Set image of your card bg")
    async def setbg(self, interaction: Interaction, *, url: str):
        """Set image of your card bg"""
        await set_bg_image(self.bot, interaction.user.id, interaction.guild.id, url)
        await interaction.send(ephemeral=True, content=f"Background image has been updated")

    @slash_command(description="Reset image of your card bg")
    async def resetbg(self, interaction: Interaction):
        """Reset image of your card bg"""
        await set_bg_image(self.bot, interaction.user.id, interaction.guild.id, "")
        await interaction.send(ephemeral=True, content=f"Background image has been set to default")

    @slash_command(description="Set text color of your name in your rank card")
    async def setcolor(self, interaction: Interaction, *, color: str, color2: str, color3: str):
        """Set color of the text of your rank card"""
        await set_text_color(self.bot, interaction.user.id, interaction.guild.id, color, color2, color3)
        await interaction.send(ephemeral=True, content=f"Text color has been updated")

    @slash_command(description="Toggle the overlay in your rank card(Default:On)")
    async def overlay(self, interaction: Interaction, toggle:int=SlashOption(name="toggle", choices={"On":1,"Off":0})):
        """Toggle the overlay in your rank card"""
        await toggle_overlay(self.bot, interaction.user.id, interaction.guild.id, state=toggle)
        await interaction.send(ephemeral=True, content=f"The overlay has been toggled")

    @slash_command(description="Toggle your nickname in your rank card (Default:On)")
    async def nick(self, interaction: Interaction, toggle:int=SlashOption(name="toggle", choices={"On":1,"Off":0})):
        """Toggle the overlay in your rank card"""
        await toggle_nick(self.bot, interaction.user.id, interaction.guild.id, state=toggle)
        await interaction.send(ephemeral=True, content=f"Your nickname has been toggled")

    @slash_command(description="Reset the color text of your rank card")
    async def resetcolor(self, interaction: Interaction):
        """Reset color of your card bg"""
        await set_text_color(self.bot, interaction.user.id, interaction.guild.id, color=f"white", color2=f"grey", color3=f"white")
        await interaction.send(ephemeral=True, content=f"Text color has been set to default")

    @slash_command(description="Reset your rank card")
    async def resetrank(self, interaction: Interaction):
        button_yes1 = Button(label="Yes", style=ButtonStyle.red)
        guild = self.bot.get_guild(interaction.guild.id)
        member = guild.get_member(interaction.user.id)

        async def areyousure(ctx):
            button_yes2 = Button(label="Yes I am sure", style=ButtonStyle.red)

            async def resetxp(ctx):
                await reset_rank(self.bot, interaction.user.id, interaction.guild.id)
                await ctx.response.send_message(f"{ctx.user.mention} has reset their rank.")
                for _, role_name in level_roles:
                    role = utils.get(guild.roles, name=role_name)
                    await member.remove_roles(role)
        
            button_yes2.callback = resetxp
            warnview2 = View (timeout=180)
            warnview2.add_item(button_yes2)
            embed2=Embed(title="Reset Rank", description="Are you **really** sure you want to reset your rank?\nLost XP and level cannot recovered afterwards.\nPress \"Yes\" if you want to proceed.\n",color=0x99c1f1)

            await ctx.response.send_message(embed=embed2, view=warnview2, ephemeral=True)

        button_yes1.callback = areyousure

        warnview1 = View(timeout=180)
        warnview1.add_item(button_yes1)

        embed1=Embed(title="Reset Rank", description="Are you sure you want to reset your rank?\nPress \"Yes\" if you want to proceed.\n",color=0x99c1f1)

        await interaction.response.send_message(embed=embed1, view=warnview1, ephemeral=True)

    @slash_command(description="Reset image of a user's card bg")
    @application_checks.has_any_role("Aub", "Zent", "Giebe")
    async def sresetbg(self, interaction: Interaction, *, member: Member):
        """Reset image of a users card bg"""
        await set_bg_image(self.bot, member.id, interaction.guild.id, "")
        await interaction.send(ephemeral=True, content=f"Background image has been set to default")

    @slash_command(description="Reset a user's rank card")
    @application_checks.has_any_role("Aub", "Zent", "Giebe")
    async def sresetrank(self, interaction: Interaction, *, member: Member):
        button_yes1 = Button(label="Yes", style=ButtonStyle.red)
        guild = self.bot.get_guild(interaction.guild.id)
        member = guild.get_member(interaction.user.id)

        async def areyousure(ctx):
            button_yes2 = Button(label="Yes I am sure", style=ButtonStyle.red)

            async def resetxp(ctx):
                await reset_rank(self.bot, member.id, interaction.guild.id)
                await ctx.response.send_message(f"{ctx.user.mention} has reset {member.mention}'s rank.")
                for _, role_name in level_roles:
                    role = utils.get(guild.roles, name=role_name)
                    await member.remove_roles(role)
        
            button_yes2.callback = resetxp
            warnview2 = View (timeout=180)
            warnview2.add_item(button_yes2)
            embed2=Embed(title="Reset Rank", description=f"Are you **really** sure you want to reset {member.mention}'s rank?",color=0x99c1f1)

            await ctx.response.send_message(embed=embed2, view=warnview2, ephemeral=True)

        button_yes1.callback = areyousure

        warnview1 = View(timeout=180)
        warnview1.add_item(button_yes1)

        embed1=Embed(title="Reset Rank", description=f"Are you sure you want to reset {member.mention}'s rank?",color=0x99c1f1)

        await interaction.response.send_message(embed=embed1, view=warnview1, ephemeral=True)

    @slash_command(description="Get help from Leidenschaft")
    async def help_leidenschaft(self, interaction: Interaction):

        rcommands='''
        </leaderboard:0> `page` - Shows the leaderboard.
        `page` (Optional) = Sets the page on the leaderboard (Each page shows 10 users). Defaults to page 1.

        </rank:0> `member` - View your rank card.
        `member` (Optional) - Tell which user's rank card you want to see.

        </resetrank:0> - Resets your progress (Sets your level and xp to 0).
        
        '''

        ccommands='''        
        </setfont:0> - Set font via dropdown menu

        </overlay_off:0> - Turn off the overlay on the rank card.

        </overlay:0> - Turn on/off the overlay on the rank card.

        </nick:0> - Turn on/off the nicknames on your rank card.

        </setbg:0> `url` - Allow changing the background image of your rank card.
        `url` - The link of the background image.

        </setcolor:0> `color1` `color2` `color3` - Allow changing the colors of your rank card (Requires hex color value).
        `color1` - The color of your username.
        `color2` - The color of your discriminator(Discord tag).
        `color3` - The color of your progress bar.

        </resetbg:0> - Resets your custom rank card background image to default.

        </resetcolor:0> - Resets custom colors on your rank card to default.

        '''

        acommands='''
        </sresetbg:0> `member` - Resets anyone's rank card background image to default (for spoiler image prevention).
        `member` - User to reset their background image.

        </sresetrank:0> `member` - Resets anyone's rank to zero.
        `member` - User to reset their rank.
        '''

        embed=Embed(title="Help", description="This is the list of commands for <@1029559354673868801>.",color=0x006bb1)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1029266425862434846/1030948597547663420/80b67817a5b119041027ce242452026a.png?size=4096")
        embed.add_field(name="Rank Commands:", value=f"{rcommands}", inline=False)
        embed.add_field(name="Customization Commands:", value=f"{ccommands}", inline=False)
        embed.add_field(name="Admin/Mod Slash Commands:", value=f"{acommands}", inline=False)

        await interaction.response.send_message(ephemeral=True, embed=embed)

    @slash_command(description="Set font of your name in your rank card")
    async def setfont(self, interaction: Interaction):
        """Set font of the text of your rank card"""

        select = Select(options=[
            SelectOption(label="1: MS Gothic", value="1"),
            SelectOption(label="2: Arial", value="2"),
            SelectOption(label="3: Caveat", value="3"),
            SelectOption(label="4: Montserrat", value="4"),
            SelectOption(label="5: Noto Sans", value="5"),
            SelectOption(label="6: Old English", value="6"),
            SelectOption(label="7: Pristina", value="7"),
            SelectOption(label="8: Poppins", value="8"),
            SelectOption(label="9: Redressed", value="9"),
            SelectOption(label="10: NotoSans JP", value="10"),
            SelectOption(label="11: NotoSerif", value="11"),
            SelectOption(label="12: Roboto", value="12"),
            SelectOption(label="13: NotoSerif JP", value="13"),
            SelectOption(label="14: Juergen Manuscript", value="14"),
            SelectOption(label="15: Juergen Stylo", value="15")
        ])
        
        view = View(timeout=360)
        view.add_item(select)

        async def my_callback(interaction):
            if int(select.values[0]) == 1:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 2:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 3:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 4:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )  

            elif int(select.values[0]) == 5:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 6:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 7:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 8:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 9:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 10:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 11:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 12:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 13:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 14:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

            elif int(select.values[0]) == 15:
                await set_text_font(self.bot, interaction.user.id, interaction.guild.id, font=select.values[0])
                await interaction.send(ephemeral=True, content=f"Text font has been updated", )

        select.callback = my_callback

        await interaction.send(ephemeral=True, content=f"Choose font", view=view)

    @slash_command(description="Add a bg to the db")
    @application_checks.has_any_role("Aub", "Zent", "Giebe")
    async def add_server_bg(self, interaction: Interaction, *, url: str):
        """adds a background image to the server"""
        bgmax = await get_bg_data(self.bot, interaction.guild.id)
        await add_bg_image(self.bot, interaction.guild.id, bgmax, url)
        await interaction.send(ephemeral=True, content=f"Background image has been added")

    @slash_command(description="Add a bg to the db")
    @application_checks.has_any_role("Aub", "Zent", "Giebe")
    async def remove_server_bg(self, interaction: Interaction, *, name: str):
        """removes a background iamge from the server"""
        bgmax = await get_bg_data(self.bot, interaction.guild.id)
        await delete_bg_image(self.bot, interaction.guild.id, interaction, bgmax, name)
        await interaction.send(ephemeral=True, content=f"Background image has been deleted")

    @slash_command(description="Emport DB")
    @application_checks.has_any_role("Aub", "Zent", "Giebe")
    async def ex_mee6(self, interaction: Interaction, *, server_id: Optional[str]):
        """removes a background iamge from the server"""
        await interaction.response.defer()
        await get_mee6_data(interaction, server_id)
        await interaction.send(file=File(f"{interaction.guild.id}_leaderboard_full_out.txt"))
   
    @slash_command(description="Emport DB")
    @application_checks.has_any_role("Aub", "Zent", "Giebe")
    async def setup(self, interaction: Interaction):
        """removes a background iamge from the server"""
        db = Database(f"sqlite:///{interaction.guild.id}_leveling.db")
        await db.connect()
        await init_dislevel(self, db, f"{interaction.guild.id}_leveling")
        await interaction.send("db created")

def setup(bot: commands.Bot):
    bot.add_cog(LevelingSlash(bot))