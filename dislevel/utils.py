from code import interact
import re
from typing import List, Union
from ._models import Field
import os, nextcord
from math import ceil
from nextcord.ui import View, Button
from nextcord import Embed

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
        Field(name="last_message", type="NUMERIC", null=False, default=0),
        Field(name="font", type="INT", null=False, default=1),              
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

def get_percentage(data):
    user_xp = data["xp"]
    user_level = data["level"]
    if user_level == 0:
        min_xp = 0
    elif user_level == 1:
        min_xp = 100
    elif user_level == 2:
        min_xp = 255
    elif user_level == 3:
        min_xp = 475
    elif user_level == 4:
        min_xp = 770
    elif user_level == 5:
        min_xp = 1150
    elif user_level == 6:
        min_xp = 1625
    elif user_level == 7:
        min_xp = 2205
    elif user_level == 8:
        min_xp = 2900
    elif user_level == 9:
        min_xp = 3720
    elif user_level == 10:
        min_xp = 4675
    elif user_level == 11:
        min_xp = 5775
    elif user_level == 12:
        min_xp = 7030
    elif user_level == 13:
        min_xp = 8450
    elif user_level == 14:
        min_xp = 10045
    elif user_level == 15:
        min_xp = 11825
    elif user_level == 16:
        min_xp = 13800
    elif user_level == 17:
        min_xp = 15980
    elif user_level == 18:
        min_xp = 18375
    elif user_level == 19:
        min_xp = 20995
    elif user_level == 20:
        min_xp = 23850
    elif user_level == 21:
        min_xp = 26950
    elif user_level == 22:
        min_xp = 30305
    elif user_level == 23:
        min_xp = 33925
    elif user_level == 24:
        min_xp = 37820
    elif user_level == 25:
        min_xp = 42000
    elif user_level == 26:
        min_xp = 46475
    elif user_level == 27:
        min_xp = 51255
    elif user_level == 28:
        min_xp = 56350
    elif user_level == 29:
        min_xp = 61770
    elif user_level == 30:
        min_xp = 67525
    elif user_level == 31:
        min_xp = 73625
    elif user_level == 32:
        min_xp = 80080
    elif user_level == 33:
        min_xp = 86900
    elif user_level == 34:
        min_xp = 94095
    elif user_level == 35:
        min_xp = 101675
    elif user_level == 36:
        min_xp = 109650
    elif user_level == 37:
        min_xp = 118030
    elif user_level == 38:
        min_xp = 126825
    elif user_level == 39:
        min_xp = 136045
    elif user_level == 40:
        min_xp = 145700
    elif user_level == 41:
        min_xp = 155800
    elif user_level == 42:
        min_xp = 166355
    elif user_level == 43:
        min_xp = 177375
    elif user_level == 44:
        min_xp = 188870
    elif user_level == 45:
        min_xp = 200850
    elif user_level == 46:
        min_xp = 213325
    elif user_level == 47:
        min_xp = 226305
    elif user_level == 48:
        min_xp = 239800
    elif user_level == 49:
        min_xp = 253820
    elif user_level == 50:
        min_xp = 268375
    elif user_level == 51:
        min_xp = 283475
    elif user_level == 52:
        min_xp = 299130
    elif user_level == 53:
        min_xp = 315350
    elif user_level == 54:
        min_xp = 332145
    elif user_level == 55:
        min_xp = 349525
    elif user_level == 56:
        min_xp = 367500
    elif user_level == 57:
        min_xp = 386080
    elif user_level == 58:
        min_xp = 405275
    elif user_level == 59:
        min_xp = 425095
    elif user_level == 60:
        min_xp = 445550   
    elif user_level == 61:
        min_xp = 466650
    elif user_level == 62:
        min_xp = 488405
    elif user_level == 63:
        min_xp = 510825
    elif user_level == 64:
        min_xp = 533920
    elif user_level == 65:
        min_xp = 557700
    elif user_level == 66:
        min_xp = 582175
    elif user_level == 67:
        min_xp = 607355
    elif user_level == 68:
        min_xp = 633250
    elif user_level == 69:
        min_xp = 659870
    elif user_level == 70:
        min_xp = 687225
    elif user_level == 71:
        min_xp = 715325
    elif user_level == 72:
        min_xp = 744180
    elif user_level == 73:
        min_xp = 773800
    elif user_level == 74:
        min_xp = 804194
    elif user_level == 75:
        min_xp = 835375
    elif user_level == 76:
        min_xp = 867350
    elif user_level == 77:
        min_xp = 900130
    elif user_level == 78:
        min_xp = 933725
    elif user_level == 79:
        min_xp = 968145
    elif user_level == 80:
        min_xp = 1003400
    elif user_level == 81:
        min_xp = 1039500
    elif user_level == 82:
        min_xp = 1076455
    elif user_level == 83:
        min_xp = 1114275
    elif user_level == 84:
        min_xp = 1152970
    elif user_level == 85:
        min_xp = 1192550
    elif user_level == 86:
        min_xp = 1233025
    elif user_level == 87:
        min_xp = 1274405
    elif user_level == 88:
        min_xp = 1316700
    elif user_level == 89:
        min_xp = 1359920
    elif user_level == 90:
        min_xp = 1404075
    elif user_level == 91:
        min_xp = 1449175
    elif user_level == 92:
        min_xp = 1495175
    elif user_level == 93:
        min_xp = 1542250
    elif user_level == 94:
        min_xp = 1590245
    elif user_level == 95:
        min_xp = 1639225
    elif user_level == 96:
        min_xp = 1689200
    elif user_level == 97:
        min_xp = 1740180
    elif user_level == 98:
        min_xp = 1792175
    elif user_level == 99:
        min_xp = 1845195
    elif user_level == 100:
        min_xp = 1899250

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

    #member_id = user_data['member_id']
    guild = bot.get_guild(guild_id)
    member = await guild.fetch_member(member_id)

    COOLDOWN_AMOUNT = 60
    new_time=last_message+COOLDOWN_AMOUNT
    print(f"{member} gained {amount} exp")
    if user_data:
        level = user_data["level"]
        new_xp = user_data["xp"] + amount
        if new_xp <= 100:
            new_level = 0
        elif new_xp <= 255:
            new_level=1
        elif new_xp <= 475:
            new_level=2
        elif new_xp <= 770:
            new_level=3
        elif new_xp <= 1150:
            new_level=4
        elif new_xp <= 1625:
            new_level=5
        elif new_xp <= 2205:
            new_level=6
        elif new_xp <= 2900:
            new_level=7
        elif new_xp <= 3720:
            new_level=8
        elif new_xp <= 4675:
            new_level=9
        elif new_xp <= 5775:
            new_level=10
        elif new_xp <= 7035:
            new_level=11
        elif new_xp <= 8450:
            new_level=12
        elif new_xp <= 10045:
            new_level=13
        elif new_xp <= 11825:
            new_level=14
        elif new_xp <= 13800:
            new_level=15
        elif new_xp <= 15980:
            new_level=16
        elif new_xp <= 18375:
            new_level=17
        elif new_xp <= 20995:
            new_level=18
        elif new_xp <= 23850:
            new_level=19
        elif new_xp <= 26950:
            new_level=20
        elif new_xp <= 30305:
            new_level=21
        elif new_xp <= 33925:
            new_level=22
        elif new_xp <= 37820:
            new_level=23
        elif new_xp <= 42000:
            new_level=24
        elif new_xp <= 46475:
            new_level=25
        elif new_xp <= 51255:
            new_level=26
        elif new_xp <= 56350:
            new_level=27
        elif new_xp <= 61770:
            new_level=28
        elif new_xp <= 67525:
            new_level=29
        elif new_xp <= 73625:
            new_level=30
        elif new_xp <= 80080:
            new_level=31
        elif new_xp <= 86900:
            new_level=32
        elif new_xp <= 94095:
            new_level=33
        elif new_xp <= 101675:
            new_level=34
        elif new_xp <= 109650:
            new_level=35
        elif new_xp <= 118030:
            new_level=36
        elif new_xp <= 126285:
            new_level=37
        elif new_xp <= 136045:
            new_level=38
        elif new_xp <= 145700:
            new_level=39
        elif new_xp <= 155800:
            new_level=40
        elif new_xp <= 166355:
            new_level=41
        elif new_xp <= 177375:
            new_level=42  
        elif new_xp <= 188870:
            new_level=43
        elif new_xp <= 200850:
            new_level=44
        elif new_xp <= 213325:
            new_level=45
        elif new_xp <= 226305:
            new_level=46
        elif new_xp <= 239800:
            new_level=47
        elif new_xp <= 253820:
            new_level=48
        elif new_xp <= 268375:
            new_level=49
        elif new_xp <= 283475:
            new_level=50
        elif new_xp <= 299130:
            new_level=51
        elif new_xp <= 315350:
            new_level=52
        elif new_xp <= 332145:
            new_level=53
        elif new_xp <= 349525:
            new_level=54
        elif new_xp <= 367500:
            new_level=55
        elif new_xp <= 386080:
            new_level=56
        elif new_xp <= 405275:
            new_level=57
        elif new_xp <= 425095:
            new_level=58
        elif new_xp <= 445550:
            new_level=59
        elif new_xp <= 466650:
            new_level=60
        elif new_xp <= 488405:
            new_level=61
        elif new_xp <= 510825:
            new_level=62
        elif new_xp <= 533920:
            new_level=63
        elif new_xp <= 557700:
            new_level=64
        elif new_xp <= 582175:
            new_level=65
        elif new_xp <= 607355:
            new_level=66
        elif new_xp <= 633250:
            new_level=67
        elif new_xp <= 659870:
            new_level=68
        elif new_xp <= 687225:
            new_level=69
        elif new_xp <= 715325:
            new_level=70
        elif new_xp <= 744180:
            new_level=71
        elif new_xp <= 773800:
            new_level=72
        elif new_xp <= 804195:
            new_level=73
        elif new_xp <= 835375:
            new_level=74
        elif new_xp <= 867350:
            new_level=75
        elif new_xp <= 900130:
            new_level=76
        elif new_xp <= 933725:
            new_level=77
        elif new_xp <= 968145:
            new_level=78
        elif new_xp <= 1003400:
            new_level=79
        elif new_xp <= 1039500:
            new_level=80
        elif new_xp <= 1076455:
            new_level=81
        elif new_xp <= 1114275:
            new_level=82
        elif new_xp <= 1152970:            
            new_level=83
        elif new_xp <= 1192550:
            new_level=84
        elif new_xp <= 1233025:
            new_level=85
        elif new_xp <= 1274405:
            new_level=86
        elif new_xp <= 1316700:
            new_level=87
        elif new_xp <= 1359920:
            new_level=88
        elif new_xp <= 1404075:
            new_level=89
        elif new_xp <= 1449175:
            new_level=90
        elif new_xp <= 1495230:
            new_level=91
        elif new_xp <= 1542250:
            new_level=92
        elif new_xp <= 1590245:
            new_level=93
        elif new_xp <= 1639225:
            new_level=94
        elif new_xp <= 1689200:
            new_level=95
        elif new_xp <= 1740180:
            new_level=96
        elif new_xp <= 1792175:
            new_level=97
        elif new_xp <= 1845195:
            new_level=98
        elif new_xp <= 1899250:
            new_level=99
        elif new_xp <= 1954350:
            new_level=100

        #new_level = int(new_xp ** (1 / 5))

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
        #level = int(amount ** (1 / 5))
        if amount <= 100:
            level = 0
        elif amount <= 255:
            level = 1
        elif amount <= 475:
            level=2
        elif amount <= 770:
            level=3
        elif amount <= 1150:
            level=4
        elif amount <= 1625:
            level=5
        elif amount <= 2205:
            level=6
        elif amount <= 2900:
            level=7
        elif amount <= 3720:
            level=8
        elif amount <= 4675:
            level=9
        elif amount <= 5775:
            level=10
        elif amount <= 7035:
            level=11
        elif amount <= 8450:
            level=12
        elif amount <= 10045:
            level=13
        elif amount <= 11825:
            level=14
        elif amount <= 13800:
            level=15
        elif amount <= 15980:
            level=16
        elif amount <= 18375:
            level=17
        elif amount <= 20995:
            level=18
        elif amount <= 23850:
            level=19
        elif amount <= 26950:
            level=20
        elif amount <= 30305:
            level=21
        elif amount <= 33925:
            level=22
        elif amount <= 37820:
            level=23
        elif amount <= 42000:
            level=24
        elif amount <= 46475:
            level=25
        elif amount <= 51255:
            level=26
        elif amount <= 56350:
            level=27
        elif amount <= 61770:
            level=28
        elif amount <= 67525:
            level=29
        elif amount <= 73625:
            level=30
        elif amount <= 80080:
            level=31
        elif amount <= 86900:
            level=32
        elif amount <= 94095:
            level=33
        elif new_xp <= 101675:
            level=34
        elif amount <= 109650:
            level=35
        elif amount <= 118030:
            level=36
        elif amount <= 126285:
            level=37
        elif amount <= 136045:
            level=38
        elif amount <= 145700:
            level=39
        elif amount <= 155800:
            level=40
        elif amount <= 166355:
            level=41
        elif amount <= 177375:
            level=42
        elif amount <= 188870:
            level=43
        elif amount <= 200850:
            level=44
        elif amount <= 213325:
            level=45
        elif amount <= 226305:
            level=46
        elif amount <= 239800:
            level=47
        elif amount <= 253820:
            level=48
        elif amount <= 268375:
            level=49
        elif amount <= 283475:
            level=50
        elif amount <= 299130:
            level=51
        elif amount <= 315350:
            level=52
        elif amount <= 332145:
            level=53
        elif amount <= 349525:
            level=54
        elif amount <= 367500:
            level=55
        elif amount <= 386080:
            level=56
        elif amount <= 405275:
            level=57
        elif amount <= 425095:
            level=58
        elif amount <= 445550:
            level=59
        elif amount <= 466650:
            level=60
        elif amount <= 488405:
            level=61
        elif amount <= 510825:
            level=62
        elif amount <= 533920:
            level=63
        elif amount <= 557700:
            level=64
        elif amount <= 582175:
            level=65
        elif amount <= 607355:
            level=66
        elif amount <= 633250:
            level=67
        elif amount <= 659870:
            level=68
        elif amount <= 687225:
            level=69
        elif amount <= 715325:
            level=70
        elif amount <= 744180:
            level=71
        elif amount <= 773800:
            level=72
        elif amount <= 804195:
            level=73
        elif amount <= 835375:
            level=74
        elif amount <= 867350:
            level=75
        elif amount <= 900130:
            level=76
        elif amount <= 933725:
            level=77
        elif amount <= 968145:
            level=78
        elif amount <= 1003400:
            level=79
        elif amount <= 1039500:
            level=80
        elif amount <= 1076455:
            level=81
        elif amount <= 1114275:
            level=82
        elif amount <= 1152970:            
            level=83
        elif amount <= 1192550:
            level=84
        elif amount <= 1233025:
            level=85
        elif amount <= 1274405:
            level=86
        elif amount <= 1316700:
            level=87
        elif amount <= 1359920:
            level=88
        elif amount <= 1404075:
            level=89
        elif amount <= 1449175:
            level=90
        elif amount <= 1495230:
            level=91
        elif amount <= 1542250:
            level=92
        elif amount <= 1590245:
            level=93
        elif amount <= 1639225:
            level=94
        elif amount <= 1689200:
            level=95
        elif amount <= 1740180:
            level=96
        elif amount <= 1792175:
            level=97
        elif amount <= 1845195:
            level=98
        elif amount <= 1899250:
            level=99
        elif amount <= 1954350:
            level=100

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
    NextButton = Button(label="Next", style=nextcord.ButtonStyle.blurple, emoji="⏭")
    PrevButton = Button(label="Previous", style=nextcord.ButtonStyle.blurple, emoji="⏮")
    MyRank = Button(label="My Rank", style=nextcord.ButtonStyle.blurple, emoji="<:praisekami:946117405111898192>")
    view = View(timeout=600)
    view.add_item(PrevButton)
    view.add_item(MyRank)
    view.add_item(NextButton)

    print(f"Leaderboard Requested by {interaction.user.name}")
    leaderboard_data = await get_leaderboard_data(bot, interaction.guild.id)

    selfrank = 0
    position = 1
    for data in leaderboard_data:
        member = None
        if bot.intents.members:
            member = interaction.guild.get_member(data["member_id"])
        else:
            member = await interaction.guild.fetch_member(data["member_id"])
        if member == interaction.user:
            selfrank = position
        position += 1

    leaderboard_content = f"This is the {interaction.guild} server's leaderboard.\n\nYou are ranked `{selfrank}`.\n\n"

    last_page = ceil(len(leaderboard_data)/10)

    if page == None or page <= 0:
        page = int(1)
    elif page > last_page:
        page = last_page

    caller = interaction.user

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

    position = 0
    for data in leaderboard_data[(((page*10)-10)):(10+((page*10)-10))]:
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
                    leaderboard_content += f"{(position+((page*10)-10))}.  **{user}**  - {data['xp']} xp   -  **lvl  {data['level']}**\n"
                else:
                    leaderboard_content += f"{(position+((page*10)-10))}.  **{member.nick}**  - {data['xp']} xp   -  **lvl  {data['level']}**\n"
            except:
                    leaderboard_content += f"{(position+((page*10)-10))}.  **{memberid}**  - {data['xp']} xp   -  **lvl  {data['level']}**\n"

    embed = Embed(title=f"Leaderboard", description=f"{leaderboard_content}",color=0x006bb1)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1029266425862434846/1030948597547663420/80b67817a5b119041027ce242452026a.png?size=4096")
    embed.set_footer(text=f"Page ({page}/{last_page})", icon_url="https://cdn.discordapp.com/attachments/1029782845071294595/1037140824875614278/unknown.png")
    try:
        await interaction.response.edit_message(embed=embed, view=view)
    except:
        await interaction.response.send_message(embed=embed, view=view)


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