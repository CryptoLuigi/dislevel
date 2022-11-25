import re, random, os
from typing import List, Union
from ._models import Field
from easy_pil.utils import run_in_executor
from .card import get_card
from .minicard import get_leadercard
from math import ceil
from nextcord.ui import View, Button
from nextcord import Embed, File, ButtonStyle

leveling_table: str = None

async def prepare_db(database, additional_fields: List[Field] = list()) -> None:
    """Prepares the database for leveling"""
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    default_fields = [
        Field(name="id", type="BIGSERIAL", primary=True),
        Field(name="member_id", type="BIGINT", null=False),
        Field(name="guild_id", type="BIGINT", null=False),
        Field(name="xp", type="BIGINT", null=False, default=0),
        Field(name="level", type="BIGINT", null=False, default=0),
        Field(name="bg_image", type="TEXT"),
        Field(name="text_color", type="TEXT"),
        Field(name="text_color2", type="TEXT"),
        Field(name="text_color3", type="TEXT"),
        Field(name="overlay", type="INT", null=False, default=1),
        Field(name="last_message", type="NUMERIC"),
        Field(name="font", type="INT", null=False, default=1),     
        Field(name="first_run", type="INT"),
        Field(name="nick", type="INT"),         
    ]

    all_fields = default_fields + additional_fields
    field_schema = ""

    for index, field in enumerate(all_fields):
        statement = f"{field.name} {field.type}"

        if field.primary:
            statement += " PRIMARY KEY"

        if not field.null:
            statement += " NOT NULL"

        if field.default != None:
            statement = f"{statement} DEFAULT %r" % field.default

        field_schema += statement + (", " if index < len(all_fields) - 1 else "")

    schema = f"CREATE TABLE IF NOT EXISTS {leveling_table}({field_schema})"

    try:
        await database.execute(schema)
    except Exception as e:
        print(e)


    server_settings_table = "server_settings" 

    default_fields = [
        Field(name="id", type="BIGSERIAL", primary=True),
        Field(name="guild_id", type="BIGINT", null=False),
        Field(name="name", type="TEXT"),
        Field(name="value", type="TEXT"),        
    ]

    all_fields = default_fields + additional_fields
    field_schema = ""

    for index, field in enumerate(all_fields):
        statement = f"{field.name} {field.type}"

        if field.primary:
            statement += " PRIMARY KEY"

        if not field.null:
            statement += " NOT NULL"

        if field.default != None:
            statement = f"{statement} DEFAULT %r" % field.default

        field_schema += statement + (", " if index < len(all_fields) - 1 else "")

    schema = f"CREATE TABLE IF NOT EXISTS {server_settings_table}({field_schema})"

    try:
        await database.execute(schema)
    except Exception as e:
        print(e)

def get_percentage(data):
    user_xp = data["xp"]
    user_level = data["level"]
    
    min_xp = 0
    var_level = 0
    for i in range(0 , user_level):
    
        min_xp = min_xp + (5*(var_level**2)+(50*var_level)+100)
        var_level = var_level + 1

    next_level_xp = 5*(user_level**2)+(50*user_level)+100
    xp_required = next_level_xp
    xp_have = user_xp - min_xp

    data["percentage"] = (100 * xp_have) / xp_required
    data["next_level_xp"] = next_level_xp

    return data

async def get_member_data(bot, member_id: int, guild_id: int) -> Union[dict, None]:
    """Returns data of an member"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    data = await database.fetch_one(
        f"""
        SELECT  * 
        FROM    {leveling_table} 
        WHERE   guild_id = :guild_id 
        AND     member_id = :member_id
        """,
        {"guild_id": guild_id, "member_id": member_id},
    )

    if not data:
        return None

    return get_percentage(dict(data))

async def get_leaderboard_data(bot, guild_id: int):
    """Get a guild's leaderboard data"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    data = await database.fetch_all(
        f"""
        SELECT   member_id, xp, level
        FROM     {leveling_table}
        WHERE    guild_id = :guild_id
        ORDER BY xp
        DESC
        """,
        {"guild_id": guild_id},
    )

    guild_data = [dict(row) for row in data]
    return guild_data

async def get_member_position(bot, member_id: int, guild_id: int):
    """Get position of a member"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    data = await database.fetch_all(
        f"""SELECT  *
             FROM   {leveling_table} 
            WHERE   guild_id = :guild_id 
         ORDER BY   xp 
             DESC
        """,
        {"guild_id": guild_id},
    )

    position = 0
    for row in data:
        position += 1
        if member_id == row["member_id"]:
            break

    return position

async def update_xp(bot, member_id: int, guild_id: int, last_message: float, amount: int = 0) -> None:
    """Increate xp of a member"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")
    user_data = await get_member_data(bot, member_id, guild_id)

    guild = bot.get_guild(guild_id)
    member = await guild.fetch_member(member_id)

    COOLDOWN_AMOUNT = 60
    new_time=last_message+COOLDOWN_AMOUNT
    print(f"{member} gained {amount} exp")
    if user_data:
        level = user_data["level"]
        new_xp = user_data["xp"] + amount
        
        var_level = 0
        levelm = level + 1
        m_xp = new_xp
        for i in range(0, levelm): 
            m_xp = m_xp - (5*(var_level**2)+(50*var_level)+100)
            if m_xp <= 0:
                break
            var_level = var_level + 1
        new_level = var_level  

        await database.execute(
            f"""
            UPDATE  {leveling_table} 
                SET  xp = :xp, 
                    level = :level
                WHERE  member_id = :member_id 
                AND  guild_id = :guild_id
            """,
            {
                "xp": new_xp,
                "level": new_level,
                "guild_id": guild_id,
                "member_id": member_id,
            },
        )
        await database.execute(
            f"""
            UPDATE  {leveling_table} 
                SET  last_message = :last_message 
                WHERE  member_id = :member_id 
                AND  guild_id = :guild_id
            """,
            {
                "last_message": new_time,
                "guild_id": guild_id,
                "member_id": member_id,
            },
        )

        if new_level > level:
            bot.dispatch(
                "dislevel_levelup",
                guild_id=guild_id,
                member_id=member_id,
                level=new_level,
            )

    else:
        var_level = 0
        levelm = 1
        amountm = amount
        for i in range(0, levelm): 
            amountm = amountm - (5*(var_level**2)+(50*var_level)+100)
            if amountm <= 0:
                break
            var_level = var_level + 1

        level = var_level

        await database.execute(
            f"""
            INSERT  INTO {leveling_table}
                    (member_id, guild_id, xp, level) 
            VALUES  (:member_id, :guild_id, :xp, :level)
            """,
            {
                "xp": amount,
                "level": level,
                "guild_id": guild_id,
                "member_id": member_id,
            },
        )

async def delete_member_data(bot, member_id: int, guild_id: int) -> None:
    """Deletes a member's data. Usefull when you want to delete member's data if they leave server"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    await database.executec(
        f"""
        DELETE  FROM {leveling_table}
         WHERE  member_id = :member_id
           AND  guild_id = :guild_id
        """,
        {
            "guild_id": guild_id,
            "member_id": member_id,
        },
    )

async def set_bg_image(bot, member_id: int, guild_id: int, url) -> None:
    """Set bg image"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    await database.execute(
        f"""
        UPDATE  {leveling_table}
        SET     bg_image = :bg_image
        WHERE   guild_id = :guild_id
        AND     member_id = :member_id 
        """,
        {"bg_image": url, "guild_id": guild_id, "member_id": member_id},
    )

async def set_text_color(bot, member_id: int, guild_id: str, color, color2, color3) -> None:
    """Set text color"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    await database.execute(
        f"""
        UPDATE  {leveling_table}
        SET     text_color = :text_color
        WHERE   guild_id = :guild_id
        AND     member_id = :member_id 
        """,
        {"text_color": color, "guild_id": guild_id, "member_id": member_id},
    )
    await database.execute(
        f"""
        UPDATE  {leveling_table}
        SET     text_color2 = :text_color2
        WHERE   guild_id = :guild_id
        AND     member_id = :member_id 
        """,
        {"text_color2": color2, "guild_id": guild_id, "member_id": member_id},
    )
    await database.execute(
        f"""
        UPDATE  {leveling_table}
        SET     text_color3 = :text_color3
        WHERE   guild_id = :guild_id
        AND     member_id = :member_id 
        """,
        {"text_color3": color3, "guild_id": guild_id, "member_id": member_id},
    )

async def toggle_overlay(bot, member_id: int, guild_id: int, state:int) -> None:
    """toggle overlay"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    await database.execute(
        f"""
        UPDATE  {leveling_table}
        SET     overlay = :overlay
        WHERE   guild_id = :guild_id
        AND     member_id = :member_id 
        """,
        {"overlay": state, "guild_id": guild_id, "member_id": member_id},
    )

async def toggle_nick(bot, member_id: int, guild_id: int, state:int) -> None:
    """toggle nickname"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    await database.execute(
        f"""
        UPDATE  {leveling_table}
        SET     nick = :nick
        WHERE   guild_id = :guild_id
        AND     member_id = :member_id 
        """,
        {"nick": state, "guild_id": guild_id, "member_id": member_id},
    )

async def reset_rank(bot, member_id: int, guild_id: int) -> None:
    """Reset Rank of a user"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")       
    xp = 0
    level = 0

    await database.execute(
            f"""
            UPDATE  {leveling_table} 
                SET  xp = :xp 
                WHERE  member_id = :member_id 
                AND  guild_id = :guild_id
            """,
            {
                "xp": xp,
                "guild_id": guild_id,
                "member_id": member_id,
            },
    )

    await database.execute(
            f"""
            UPDATE  {leveling_table} 
                SET  level = :level 
                WHERE  member_id = :member_id 
                AND  guild_id = :guild_id
            """,
            {
                "level": level,
                "guild_id": guild_id,
                "member_id": member_id,
            },
    )

async def set_text_font(bot, member_id: int, guild_id: str, font) -> None:
    """Set text color"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    await database.execute(
        f"""
        UPDATE  {leveling_table}
        SET     font = :font
        WHERE   guild_id = :guild_id
        AND     member_id = :member_id 
        """,
        {"font": font, "guild_id": guild_id, "member_id": member_id},
    )

async def get_page(bot, interaction, page:int) -> None:
    """See the server leaderboard"""
    NextButton = Button(label="Next", style=ButtonStyle.blurple, emoji="⏭")
    PrevButton = Button(label="Previous", style=ButtonStyle.blurple, emoji="⏮")
    MyRank = Button(label="My Rank", style=ButtonStyle.blurple, emoji="<:praisekami:946117405111898192>")
    view = View(timeout=600)
    view.add_item(PrevButton)
    view.add_item(MyRank)
    view.add_item(NextButton)

    leaderboard_data = await get_leaderboard_data(bot, interaction.guild.id)

    selfrank = 0
    position = 1
    for data in leaderboard_data:
        member = None
        if bot.intents.members:
            member = interaction.guild.get_member(data["member_id"])
        else:
            member = await interaction.guild.fetch_member(data["member_id"])
        try:
            if member == interaction.user:
                selfrank = position
        except:
            if member == interaction.author:
                selfrank = position
        position += 1

    leaderboard_content = f"This is the {interaction.guild} server's leaderboard.\n\nYou are ranked `{selfrank}`.\n\n"

    last_page = ceil(len(leaderboard_data)/10)

    if page == None or page <= 0:
        page = int(1)
    elif page > last_page:
        page = last_page

    try:
        caller = interaction.user
    except:
        caller = interaction.author

    async def button_callback(interaction):
        if interaction.user == caller:
            await get_page(bot, interaction, page=page+1)
        else:
            await interaction.response.send_message("Only the caller can do that.", ephemeral=True)

    async def button_callback2(interaction):
        if interaction.user == caller:
            await get_page(bot, interaction, page=page-1)
        else:
            await interaction.response.send_message("Only the caller can do that.", ephemeral=True)

    async def button_callback3(interaction):
        if interaction.user == caller:
            await get_page(bot, interaction, page = ceil(selfrank/10))
        else:
            await interaction.response.send_message("Only the caller can do that.", ephemeral=True)

    NextButton.callback = button_callback
    PrevButton.callback = button_callback2
    MyRank.callback = button_callback3

    bgmax = await get_bg_data(bot, interaction.guild.id)
    bgmax = int(bgmax[0])

    leaderboard_image_data = dict()

    await interaction.response.defer()

    position = 0
    for data in leaderboard_data[(((page*10)-10)):(10+((page*10)-10))]:
            bgnum = random.randint(1, bgmax)
            memberid = data['member_id']
            guild = bot.get_guild(interaction.guild.id)

            try:
                member = await guild.fetch_member(memberid)
            except:
                member = "Left server"
            position += 1
            try:                
                if member.nick == f'None' or member.nick == None:
                    user = bot.get_user(data["member_id"])
                    user = re.sub(r'#(.?)(.?)(.?)(.?)', '', f'{user}')
                    leaderboard_image_data[f"username_{position}"] = user
                else:
                    leaderboard_image_data[f"username_{position}"] = member.nick     
            except:
                    leaderboard_image_data[f"username_{position}"] = memberid

            bg = await get_bg_value(bot=bot, guild_id=interaction.guild.id, bgnum=bgnum)
            leaderboard_image_data[f"position_{position}"] = position+((page*10)-10)
            leaderboard_image_data[f"bg_{position}"] = await get_bg_value(bot=bot, guild_id=interaction.guild.id, bgnum=bgnum)         
            leaderboard_image_data[f"profile_image_{position}"] = str(member.display_avatar.url)
            leaderboard_image_data[f"xp_{position}"] = data['xp']
            leaderboard_image_data[f"level_{position}"] = data['level']
            leaderboard_image_data[f"position_{position}"] = await get_member_position(bot, memberid, interaction.guild.id)

    image = await run_in_executor(get_leadercard, data=leaderboard_image_data, bg=bg[0])
    file = File(fp=image, filename="card.png")
    embed = Embed(title=f"Leaderboard", description=f"{leaderboard_content}", color=0x006bb1)
    embed.set_image(url="attachment://card.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1029266425862434846/1030948597547663420/80b67817a5b119041027ce242452026a.png")
    embed.set_footer(text=f"{interaction.guild} Page ({page}/{last_page})", icon_url = interaction.guild.icon)
    try:
        await interaction.message.edit(file=file,embed=embed, view=view)
    except:
        await interaction.send(file=file, embed=embed, view=view)

async def set_first_run(bot, member_id: int, guild_id: int) -> None:
    """Set first run"""
    database = bot.dislevel_database
    leveling_table = os.environ.get("DISLEVEL_TABLE")

    firstrun = 1

    await database.execute(
        f"""
        UPDATE  {leveling_table}
        SET     first_run = :first_run
        WHERE   guild_id = :guild_id
        AND     member_id = :member_id 
        """,
        {"first_run": firstrun, "guild_id": guild_id, "member_id": member_id},
    )

async def get_bg_data(bot, guild_id: int) -> Union[dict, None]:
    """Returns data number of custom bgs"""
    database = bot.dislevel_database
    name="custom_bg"

    data = await database.fetch_one(
        f"""
        SELECT  value 
        FROM    server_settings 
        WHERE   guild_id = :guild_id 
        AND     name = :name
        """,
        {"guild_id": guild_id, "name": name},
    )

    if not data:
        return None

    return data

async def get_bg_value(bot, guild_id: int, bgnum:int) -> Union[dict, None]:
    """Returns data number of custom bgs"""
    database = bot.dislevel_database
    bgname = f"bg{bgnum}"

    data = await database.fetch_one(
        f"""
        SELECT  value 
        FROM    server_settings 
        WHERE   guild_id = :guild_id 
        AND     name = :name
        """,
        {"guild_id": guild_id, "name": bgname},
    )

    if not data:
        return None

    return data

async def add_bg_image(bot, guild_id: int, bgmax:int, value:str) -> None:
    """Set bg image"""
    database = bot.dislevel_database
    custom_bg="custom_bg"
    bgnum = int(bgmax[0])
    bgnum = bgnum + 1
    name = f"bg{bgnum}"
    await database.execute(
        f"""
        INSERT  INTO server_settings
                (guild_id, name, value) 
        VALUES  (:guild_id, :name, :value)
        """,
        {"guild_id": guild_id, "name": name, "value": value,},
    )

    await database.execute(
        f"""
        UPDATE  server_settings
        SET     value = :value
        WHERE   guild_id = :guild_id
        AND     name = :name
        """,
        {"value": bgnum, "guild_id": guild_id, "name": custom_bg},
    )

async def delete_bg_image(bot, guild_id: int, interaction, bgmax:int, name:str) -> None:
    """Deletes a background image from the db"""
    database = bot.dislevel_database
    custom_bg="custom_bg"
    bgnum = int(bgmax[0])
    bgnum = bgnum - 1

    value = await database.fetch_one(
        f"""
        SELECT  value
        FROM    server_settings
        WHERE   name = :name
        AND     guild_id = :guild_id
        """,
        {"guild_id": guild_id, "name": name},
    )

    if value == None:
        await interaction.send(ephemeral=True, content=f"Background image does not exist")
    else:

        bgcheck = await database.fetch_one(
            f"""
            SELECT  name
            FROM    server_settings
            WHERE   value = :value
            AND     guild_id = :guild_id
            """,
            {"guild_id": guild_id, "value": value[0]},
        )

        bgmaxname = f"bg{bgmax[0]}"
        
        maxvalue = await database.fetch_one(
            f"""
            SELECT  value
            FROM    server_settings
            WHERE   name = :name
            AND     guild_id = :guild_id
            """,
            {"guild_id": guild_id, "name": bgmaxname},
        )

        bgcheck = str(bgcheck[0])
        bgcheck = re.sub(r'bg',  '', f'{bgcheck}')

        if bgcheck == bgmax[0]:
            await database.execute(
                f"""
                UPDATE  server_settings
                SET     value = :value
                WHERE   guild_id = :guild_id
                AND     name = :name
                """,
                {"value": bgnum, "guild_id": guild_id, "name": custom_bg},
            )
            await database.execute(
                f"""
                DELETE  FROM server_settings
                WHERE   name = :name
                AND     guild_id = :guild_id
                """,
                {"guild_id": guild_id, "name": name},
            )
        else:
            bgname = f"bg{bgcheck}"

            await database.execute(
                f"""
                UPDATE  server_settings
                SET     value = :value
                WHERE   guild_id = :guild_id
                AND     name = :name
                """,
                {"value": bgnum, "guild_id": guild_id, "name": custom_bg},
            )
            await database.execute(
                f"""
                DELETE  FROM server_settings
                WHERE   name = :name
                AND     guild_id = :guild_id
                """,
                {"guild_id": guild_id, "name": name},
            )

            await database.execute(
                f"""
                UPDATE  server_settings
                SET     name = :name
                WHERE   guild_id = :guild_id
                AND     value = :value
                """,
                {"value": maxvalue[0], "guild_id": guild_id, "name": bgname},
            )    

        await interaction.send(ephemeral=True, content=f"Background image has been removed")

async def get_rank(bot, interaction, member) -> None:
    """Gets the rank card for a user"""

    if not member:
        member = interaction.user
        user_data = await get_member_data(bot, member.id, interaction.guild.id)
        first_run = user_data["first_run"]                 
    else:
        user_data = await get_member_data(bot, member.id, interaction.guild.id)
        first_run = 1

    mestiid=int(1027592830719377439)
    if member.id == mestiid:
        await interaction.response.send_message(content=f"https://cdn.discordapp.com/attachments/1028883555713032234/1037415184072982528/card.png")            

    elif first_run == 1:

        user_data["position"] = await get_member_position(bot, member.id, interaction.guild.id)
        user_data["profile_image"] = str(member.display_avatar.url)
        user_data["name"] = str(member).split("#")[0]
        user_data["descriminator"] = str(member).split("#")[1]
        
        bgmax = await get_bg_data(bot, interaction.guild.id)
        bgmax = int(bgmax[0])
        bgnum = random.randint(1, bgmax)
        bg = await get_bg_value(bot=bot, guild_id=interaction.guild.id, bgnum=bgnum)
        image = await run_in_executor(get_card, data=user_data, nick=member.nick, bg=bg[0])
        file = File(fp=image, filename="card.png")
        Leaderboard = Button(label="Show the Leaderboard", style=ButtonStyle.green, emoji="<:MyneSparkle:1018941182430154902>")
        view2 = View(timeout=600)
        view2.add_item(Leaderboard)


        async def leader_callback(interaction):
            selfrank = await get_member_position(bot, interaction.user.id, interaction.guild.id)
            await get_page(bot, interaction, page=ceil(selfrank/10))
            print(f"Leaderboard Requested by {interaction.user.name}")

        Leaderboard.callback = leader_callback

        await interaction.send(file=file,view=view2)


    else:
        user_data["position"] = await get_member_position(bot, member.id, interaction.guild.id)
        user_data["profile_image"] = str(member.display_avatar.url)
        user_data["name"] = str(member).split("#")[0]
        user_data["descriminator"] = str(member).split("#")[1]

        bgmax = await get_bg_data(bot, interaction.guild.id)
        bgmax = int(bgmax[0])
        bgnum = random.randint(1, bgmax)
        bg = await get_bg_value(bot=bot, guild_id=interaction.guild.id, bgnum=bgnum)
        image = await run_in_executor(get_card, data=user_data, nick=member.nick, bg=bg[0])
        file = File(fp=image, filename="card.png")

        ShowButton = Button(label="Show me", style=ButtonStyle.green, emoji="<:praisekami:946117405111898192>")
        Leaderboard = Button(label="Show the Leaderboard", style=ButtonStyle.green, emoji="<:MyneSparkle:1018941182430154902>")
        view = View(timeout=600)
        view2 = View(timeout=600)
        view.add_item(ShowButton)
        view2.add_item(Leaderboard)

        async def button_callback(interaction):
            ccommands='''        
            </setfont:0> Set the font via dropdown menu.

            </overlay:0> - Turn off/on the overlay on the rank card.

            </overlay_on:0> - Turn on the overlay on the rank card.

            </setbg:0> `url` - Allow changing the background image of your rank card.
            `url` - The link of the background image.

            </setcolor:0> `color1` `color2` `color3` - Allow changing the colors of your rank card (Requires hex color value).
            `color1` - The color of your username.
            `color2` - The color of your discriminator(Discord tag).
            `color3` - The color of your progress bar.

            </resetbg:0> - Resets your custom rank card background image to default.

            </resetcolor:0> - Resets custom colors on your rank card to default.

            '''
            embed=Embed(title="Help", description="This is the list of commands for <@1029559354673868801>.",color=0x006bb1)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1029266425862434846/1030948597547663420/80b67817a5b119041027ce242452026a.png?size=4096")
            embed.add_field(name="Customization Commands:", value=f"{ccommands}", inline=False)

            await interaction.send(ephemeral=True, embed=embed)                    
        
        async def leader_callback(interaction):
            selfrank = await get_member_position(bot, interaction.user.id, interaction.guild.id)
            page = ceil(selfrank/10)
            await get_page(bot, interaction, page)
            print(f"Leaderboard Requested by {interaction.user.name}")

        Leaderboard.callback = leader_callback
        ShowButton.callback = button_callback
        await set_first_run(bot, member.id, interaction.guild.id)
        await interaction.send(file=file, view=view2)
        await interaction.send(ephemeral=True, content="This is your first time seeing your rank card.\nWould you like to see how to customize your card?\n" , view=view)

async def get_setting(bot, guild_id: int, name) -> None:
    """Returns data number of custom bgs"""
    database = bot.dislevel_database

    data = await database.fetch_one(
        f"""
        SELECT  value 
        FROM    server_settings 
        WHERE   guild_id = :guild_id 
        AND     name = :name
        """,
        {"guild_id": guild_id, "name": name},
    )

    if not data:
        return None

    return data