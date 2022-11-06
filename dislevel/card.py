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
    
    min_xp = 0
    var_level = 0
    for i in range(0 , user_level):
        min_xp = min_xp + (5*(var_level**2)+(50*var_level)+100)
        var_level = var_level + 1

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
