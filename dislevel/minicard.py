import re
from easy_pil import Canvas, Editor, Font, load_image
from numerize.numerize import numerize

URL_REGEX = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")

def get_leadercard(data, bg:str):

    position = 1
    profile_pos = 5
    data_pos = 35
    rec_pos = 0
    rank_pos = 10
    xp_pos = 25
    profile_align = 150
    height = 550
    width = 760

    if data[f"bg_{position}"][0] and URL_REGEX.match(data[f"bg_{position}"][0]):
        try:
            bg_image = load_image(data[f"bg_{position}"])
        except Exception as e:
            bg_image = load_image(bg)
    else:
        bg_image = load_image(bg)

    background = Editor(bg_image).resize((width, height), crop=True)
    overlay = Canvas((width, height), color=(0, 0, 0, 100))
    background.paste(overlay, (0, 0))

    while position != 11:

        try:
            profile_image = Editor(load_image(data[f"profile_image_{position}"])).resize((45, 45))
            background.rectangle((0, rec_pos), width-1, 55, outline="white", stroke_width=2)

            
            background.paste(profile_image, (profile_align-50, profile_pos))
            background.text((profile_align, profile_pos), f"{data[f'username_{position}']}", font=Font.msgothic(size=25, variant="bold"), color="white",)

            background.text((profile_align, data_pos), "LVL ", font=Font.Redressed(size=20, variant="bold"), color="white")
            background.text((profile_align+50, data_pos), str(data[f"level_{position}"]), font=Font.Redressed(size=20, variant="bold"), color="white")

            rank = data[f"position_{position}"]
            background.text((15, rank_pos), f"{rank}", font=Font.Redressed(size=35, variant="bold"), color="white")

            display_xp=(data[f"xp_{position}"])
            background.text((width-200, xp_pos), f"XP : {numerize(display_xp)}", font=Font.Redressed(size=35, variant="bold"), color="white")

            background.rectangle((profile_align-50, profile_pos), 45, 45, outline="white", stroke_width=1)

            position +=1
            profile_pos += 55
            data_pos += 55
            rec_pos += 55
            rank_pos += 55
            xp_pos += 55
        except:
            position +=1
            pass

    return background.image_bytes