import os
import random
import re
from easy_pil import Canvas, Editor, Font, load_image
from numerize.numerize import numerize


URL_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
)

def get_card(data, nick:str):
    profile_image = load_image(data["profile_image"])
    profile = Editor(profile_image).resize((200, 200))
    overlay_state=(data["overlay"])
    tcolor=(data["text_color"])
    tcolor2=(data["text_color2"])
    tcolor3=(data["text_color3"])
    font=(data["font"])

    if tcolor == None:
        tcolor = "white"
    if tcolor2 == None:
        tcolor2 = "grey"
    if tcolor3 == None:
        tcolor3 = "white"


    if data["bg_image"] and URL_REGEX.match(data["bg_image"]):
        try:
            bg_image = load_image(data["bg_image"])
        except Exception as e:
            print("Hit this exception")
            bgnum = random.randint(1,55)
            bg_image = os.path.join(os.path.dirname(__file__), "assets", f"bg{bgnum}.png")
    else:
        bgnum = random.randint(1,55)
        bg_image = os.path.join(os.path.dirname(__file__), "assets", f"bg{bgnum}.png")

    background = Editor(bg_image).resize((800, 240), crop=True)

    if overlay_state == 1:
        overlay = Canvas((800, 240), color=(0, 0, 0, 100))
        background.paste(overlay, (0, 0))

    if overlay_state == None:
        overlay = Canvas((800, 240), color=(0, 0, 0, 100))
        background.paste(overlay, (0, 0)) 

    font_25 = Font.poppins(size=25)
    font_40_bold = Font.poppins(size=40, variant="bold")

    background.paste(profile, (20, 20))

    nicktoggle = data["nick"]

    if nicktoggle == None:
        display_name = f"{nick}"
        if nick == None:
            display_name = f"{data['name']}"
    elif nicktoggle == 1:
        display_name = f"{nick}"
        if nick == None:
            display_name = f"{data['name']}"
    else:
        display_name = f"{data['name']}"

    print(f'This is display name in card:{display_name}')

    display_name_len = len(display_name)

    print(display_name_len)

    if display_name_len >= 20:
        fontsl = 1
    else:
        fontsl = 0

    print(fontsl)

    if font == None:
        if fontsl == 1:
            font_40 = Font.msgothic(size=30, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.msgothic(size=35, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 1:
        if fontsl == 1:
            font_40 = Font.msgothic(size=30, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.msgothic(size=35, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 2:
        if fontsl == 1:
            font_40 = Font.arial(size=35, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.arial(size=40, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 3:
        if fontsl == 1:
            font_40 = Font.caveat(size=35, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.caveat(size=40, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 4:
        if fontsl == 1:
            font_40 = Font.montserrat(size=35, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.montserrat(size=40, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 5:
        if fontsl == 1:
            font_40 = Font.notosans(size=35, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.notosans(size=40, variant="bold")
            font_30 = Font.poppins(size=23) 

    elif font == 6:
        if fontsl == 1:
            font_40 = Font.OLDENGL(size=45, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.OLDENGL(size=50, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 7:
        if fontsl == 1:
            font_40 = Font.PRISTINA(size=40, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.PRISTINA(size=48, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 8:
        if fontsl == 1:        
            font_40 = Font.poppins(size=35, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.poppins(size=40, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 9:
        if fontsl == 1:  
            font_40 = Font.Redressed(size=40, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.Redressed(size=45, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 10:
        if fontsl == 1:  
            font_40 = Font.NotoSansJP(size=40, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.NotoSansJP(size=45, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 11:
        if fontsl == 1:  
            font_40 = Font.NotoSerif(size=40, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.NotoSerif(size=45, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 12:
        if fontsl == 1: 
            font_40 = Font.Roboto(size=40, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.Roboto(size=45, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 13:
        if fontsl == 1:
            font_40 = Font.NotoSerifJP(size=40, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.NotoSerifJP(size=45, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 14:
        if fontsl == 1:
            font_40 = Font.JuergenManuscript(size=40, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.JuergenManuscript(size=45, variant="bold")
            font_30 = Font.poppins(size=23)

    elif font == 15:
        if fontsl == 1:
            font_40 = Font.JuergenStylo(size=40, variant="bold")
            font_30 = Font.poppins(size=23)
        else:
            font_40 = Font.JuergenStylo(size=45, variant="bold")
            font_30 = Font.poppins(size=23)

    if font == 14:
        display_name = display_name.lower() 
    elif font == 15:
        display_name = display_name.lower() 

    background.text(
        (240, 20),
        display_name,
        font=font_40,
        color=f"{tcolor}",
    )

    background.text(
        (240, 65),
        f"#{data['descriminator']}",
        font=font_30,
        color=f"{tcolor2}"
    )

    background.text((250, 170), "LVL", font=font_25, color=f"{tcolor3}")
    background.text((310, 160), str(data["level"]), font=font_40_bold, color=f"{tcolor3}")

    background.rectangle((390, 170), 360, 25, outline=f"{tcolor3}", stroke_width=2)
    background.bar(
        (394, 174),
        352,
        17,
        percentage=data["percentage"],
        fill=f"{tcolor3}",
        stroke_width=2,
    )
    #background.text(
    #    (875, 42),
    #    f'#{data["position"]}',
    #    font=Font.montserrat(size=45),
    #    color="#ffffff",  #changing this did nothing?
    #    align="right",
    #)

    background.text(
        (390, 135), f"Rank : {data['position']}", font=font_25, color=tcolor3
    )
    user_level=(data["level"])
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

    xp=(data['xp'])
    display_xp = xp - min_xp
    background.text(
        (750, 135),
        f"XP : {display_xp}/{numerize(data['next_level_xp'])}",
        font=font_25,
        color=f"{tcolor3}",
        align="right",
    )

    return background.image_bytes
