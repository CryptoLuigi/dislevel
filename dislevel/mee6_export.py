import re
from mee6_py_api import API

async def get_mee6_data(interaction, serverid):
    mee6API = API(serverid)

    #f = open("leaderboard_full.txt",encoding='utf-8', mode='r')
    #leaderboard_page = f.read()

    leaderboard_page = str(await mee6API.levels.get_all_leaderboard_pages(page_count_limit=50))

    #leaderboard_page = str(await mee6API.levels.get_leaderboard_page(2))
    #f.write(str(leaderboard_page))
    #f.close()

    leaderboard_page = leaderboard_page.replace('\'', '')
    leaderboard_page = leaderboard_page.replace(':', '')
    leaderboard_page = leaderboard_page.replace('[', '')  
    leaderboard_page = leaderboard_page.replace(']', '')
    leaderboard_page = leaderboard_page.replace(f'id {serverid},', '')

    res = re.sub(r'.?guild_id ([^ ]*), ',  '', f'{leaderboard_page}') 
    res = re.sub(r'.?{admin ([^ ]*), ([^ ]*) ([^ ]*), ([^ ]*) ([^ ]*), ([^ ]*) ([^ ]*) ([^ ]*), ([^ ]*) ([^ ]*), ([^ ]*) ([^ ]*), ([^ ]*) ([^ ]*), ',  '', f'{res}')
    res = re.sub(r'.?invite_leaderboard ([^ ]*), ',  '', f'{res}') 
    res = re.sub(r'.?avatar ([^ ]*), ',  '', f'{res}')
    res = re.sub(r'.?detailed_xp ([^ ]*), ([^ ]*), ([^ ]*), ',  '', f'{res}')
    res = re.sub(r'.?discriminator ([^ ]*),',  '', f'{res}')
    res = re.sub(r'.?message_count ([^ ]*), ',  '', f'{res}')
    res = re.sub(r'.?leaderboard_url ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*)guild_ ',  '', f'{res}') 
    res = re.sub(r'.?rank ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*), ([^,]*), unicode_emoji }}, ',  '', f'{res}')
    res = re.sub(r'} guild_',  ',', f'{res}')                
    res = re.sub(r' level ',  '', f'{res}')
    res = re.sub(r'username ',  '', f'{res}')
    res = re.sub(r' xp ',  '', f'{res}')
    res = re.sub(r'},.?role_rewards ([^,]*), ([^,]*), ([^,]*), ([^,]*)}',  ', ', f'{res}')
    res = re.sub(r' id ',  '\n', f'{res}')   
    res = re.sub(r'^id ',  '', f'{res}')  

    g = open(f"{interaction.guild.id}_leaderboard_full_out.txt",encoding='utf-8', mode='w')
    g.write(str(res))
    g.close() 
    return g