from aiosocksy import connector
from bs4 import BeautifulSoup
import requests
import time
import psycopg2
import random
from tqdm import tqdm
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from tqdm.std import trange
import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector
import asyncio
from concurrent.futures import FIRST_COMPLETED
from multiprocessing import Process, Pipe, freeze_support

requests.packages.urllib3.disable_warnings()
main_player_id_1 = '/players/96527871'
main_player_id_2 = '/players/84409565'

def proxy_text():

    proxy_list = []
    user_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"        
    }
    url = 'https://spys.me/proxy.txt'

    for _ in range(10):

        try:

            r = requests.get(url, headers = user_agent, timeout = 1)

            break

        except:

            time.sleep(60)

    txt = r.text
    txt_line = txt.splitlines()

    for i in txt_line[9:-2]:

        ind = i.find(' ')

        proxy_list.append('http://'+i[:ind])

    return proxy_list

async def tasks(url):

    tasks = []

    proxy_list = ez_proxy.get_rand(10)

    for proxy in proxy_list:

        tasks.append(asyncio.create_task(async_request(url, proxy)))

    done, pending = await asyncio.wait(tasks, timeout = 4, return_when = FIRST_COMPLETED)

    for future in pending:
        future.cancel()

    return done.pop().result()

async def async_request(url, proxy):

    user_agent = rand_user_agent()
    conn = ProxyConnector.from_url(proxy)
    #session_timeout = aiohttp.ClientTimeout(total=6,sock_connect=None,sock_read=None)

    try:

        async with aiohttp.ClientSession(connector = conn, headers = user_agent) as session:

            async with session.get(url, ssl = False) as r:

                txt = await r.text()
                #print(r.status)
                if r.status == 200:

                    return txt

                else:

                    await asyncio.sleep(10)

    except asyncio.CancelledError:

        return

    except:

        await asyncio.sleep(10)

def proxy_dict_second_core(conn):

    while True:

        proxy_list = proxy_text()
        conn.send(proxy_list)
        time.sleep(60)

def rand_user_agent():

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value] 
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    rand_user_agent = {'User-Agent':user_agent_rotator.get_random_user_agent()}

    return rand_user_agent

class Ez_Proxy():
    
    def init(self):
        
        self.parent_conn, self.child_conn = Pipe()
        self.p = Process(target = proxy_dict_second_core, args = (self.child_conn,))
        self.p.daemon = True
        self.p.start()
        
        self.list = self.parent_conn.recv()

    def get(self):

        if self.parent_conn.poll() == False:
        
            return self.list
        
        else:
        
            self.list = self.parent_conn.recv()
        
            return self.list

    def get_rand(self, num):

        if self.parent_conn.poll() == False:
        
            rand_list = []

            for _ in range(num):

                rand_list.append(random.choice(self.list))

            return rand_list
        
        else:
        
            self.list = self.parent_conn.recv()
        
            rand_list = []

            for _ in range(num):

                rand_list.append(random.choice(self.list))

            return rand_list

ez_proxy = Ez_Proxy()

def game_info(main_player_id, game_count):

    i = 1
    result_list = []
    match_id_list = []
    loop_condition = True

    while loop_condition == True:

        url = 'https://ru.dotabuff.com' + main_player_id +'/matches?enhance=overview&page=' + str(i)

        while True:

            try:
                #print('Starting!')
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                r = asyncio.run(tasks(url))
                print('Good return!')
                break

            except KeyError:

                print('Empty return!')
                continue

        soup = BeautifulSoup(r, "lxml")

        match_list = soup.find_all("table")[1].tbody.find_all("tr")

        try:

            page_count = soup.find('span', class_='last').find('a')['href']
            page_count = int(page_count.split("page=")[1])

        except:

            page_count = i

        for match in match_list:
            
            match_type = match.find_all("td")[4]
            match_type = match_type.text[0]

            if match_type != "Р":

                continue

            td = match.find_all("td")[3]
            match = td.find("a")

            match_id = match['href']
            match_result = match['class'][0]

            result_list.append(match_result)
            match_id_list.append(match_id)

            if len(result_list) == game_count:

                loop_condition = False

                break

        i += 1

        if i > page_count:

            break

    print("game_info()")
    return result_list, match_id_list

def teammates_id(match_id, main_player_id):

    match_url = 'https://ru.dotabuff.com' + match_id

    while True:

        try:
            #print('Starting!')
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            r = asyncio.run(tasks(match_url))
            print('Good return!')
            break

        except KeyError:

            print('Empty return!')
            continue

    match_soup = BeautifulSoup(r, "lxml")

    player_list_dire = []
    player_list_radiant = []
    dire_players = match_soup.find_all('a', class_="player-dire link-type-player")
    radiant_players = match_soup.find_all('a', class_="player-radiant link-type-player")

    for dire_player in dire_players:

        player_id = dire_player['href']
        player_list_dire.append(player_id)

    for radiant_player in radiant_players:

        player_id = radiant_player['href']
        player_list_radiant.append(player_id)

    dire_side = False

    for pl in player_list_dire:

        if pl == main_player_id:

            dire_side = True

    if dire_side == True:

        player_list_dire.remove(main_player_id)
        teammates = player_list_dire
        enemies = player_list_radiant

    else:

        player_list_radiant.remove(main_player_id)
        teammates = player_list_radiant
        enemies = player_list_dire

    print("teammates_id()")
    return teammates, enemies

def winrate(searched_player_id, searched_match_id):

    player_match_list = []
    condition = False
    loop_condition = True
    i = 1

    while loop_condition == True:

        player_match_url = 'https://ru.dotabuff.com' + searched_player_id + '/matches?enhance=overview&page=' + str(i)

        while True:

            try:
                #print('Starting!')
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                r = asyncio.run(tasks(player_match_url))
                print('Good return!')
                break

            except KeyError:

                print('Empty return!')
                continue

        player_match_soup = BeautifulSoup(r, "lxml")

        player_matchs = player_match_soup.find_all("table")[1].tbody.find_all("tr")

        try:

            page_count = player_match_soup.find('span', class_='last').find('a')['href']
            page_count = int(page_count.split("page=")[1])

        except:

            page_count = i

        for player_match in player_matchs:

            player_match_type = player_match.find_all("td")[4]
            player_match_type = player_match_type.text[0]

            if player_match_type != "Р":

                continue

            player_match_td = player_match.find_all("td")[3]
            player_match = player_match_td.find("a")
            player_match_id = player_match['href']

            if player_match_id == searched_match_id:
                
                condition = True

            if condition == True:

                if len(player_match_list) == 5:

                    win_5 = player_match_list[1:].count('won')/5

                if len(player_match_list) == 10:

                    win_10 = player_match_list[1:].count('won')/10

                if len(player_match_list) == 20:

                    win_20 = player_match_list[1:].count('won')/20

                if len(player_match_list) == 40:

                    win_40 = player_match_list[1:].count('won')/len(player_match_list)

                    loop_condition = False

                    break

                else:
                    
                    player_match_result = player_match['class'][0]
                    player_match_list.append(player_match_result)

        i += 1

        if i > page_count:

            break  

    if 'win_5' not in vars():

        win_5 = 0.5

    if 'win_10' not in vars():

        win_10 = 0.5

    if 'win_20' not in vars():

        win_20 = 0.5

    if 'win_40' not in vars():

        win_40 = 0.5

    print("winrate()")
    return win_5, win_10, win_20, win_40

def game_info_writer(result_list, match_id_list, users_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True
        i = 0

        with  connection.cursor() as cursor:

            while i < len(result_list):

                call = "INSERT INTO player_match_stat (match_id, match_result, fk_player_match_stat_users) VALUES ('" + match_id_list[i] + "', '" + result_list[i] + "', '" + users_tid + "');"

                cursor.execute(
                    call
                )

                i += 1

    finally:

        if connection:

            cursor.close()
            connection.close()

    return

def users_writer(main_player_id):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call = "INSERT INTO users (user_id) VALUES ('" + main_player_id + "') RETURNING id;"

            cursor.execute(
                call
            )

            users_tid = str(cursor.fetchone()[0])

    except:

        connection = None
        print("DB connection lost")
        exit()

    finally:

        if connection:

            cursor.close()
            connection.close()

    return users_tid

def teammates_id_writer(teammates, player_match_stat_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            for i in teammates:

                call = "INSERT INTO teammates (teammate_id, fk_teammates_player_match_stat) VALUES ('" + i + "', '" + str(player_match_stat_tid) + "');"

                cursor.execute(
                    call
                )

    finally:

        if connection:

            cursor.close()
            connection.close()

    return

def enemies_id_writer(enemies, player_match_stat_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            for i in enemies:

                call = "INSERT INTO enemies (enemy_id, fk_enemies_player_match_stat) VALUES ('" + str(i) + "', '" + str(player_match_stat_tid) + "');"

                cursor.execute(
                    call
                )

    finally:

        if connection:

            cursor.close()
            connection.close()

    return

def game_info_reader(users_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call = "SELECT match_id, id FROM player_match_stat WHERE fk_player_match_stat_users =" + users_tid + ";"

            cursor.execute(
                call
            )

            match_list = cursor.fetchall()

    finally:

        if connection:

            cursor.close()
            connection.close()

    return match_list

def teammates_id_reader(player_match_stat_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call = "SELECT teammate_id, id FROM teammates WHERE fk_teammates_player_match_stat =" + str(player_match_stat_tid) + ";"

            cursor.execute(
                call
            )

            teammates_id_list = cursor.fetchall()

    finally:

        if connection:

            cursor.close()
            connection.close()

    return teammates_id_list

def enemies_id_reader(player_match_stat_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call = "SELECT enemy_id, id FROM enemies WHERE fk_enemies_player_match_stat =" + str(player_match_stat_tid) + ";"

            cursor.execute(
                call
            )

            enemies_id_list = cursor.fetchall()

    finally:

        if connection:

            cursor.close()
            connection.close()

    return enemies_id_list

def win_teammates_writer(win_5, win_10, win_20, win_40, teammates_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call_0 = "UPDATE teammates SET winrate_5_match =" + str(win_5) + "WHERE id = " + str(teammates_tid) + ";"
            call_1 = " UPDATE teammates SET winrate_10_match =" + str(win_10) + "WHERE id = " + str(teammates_tid) + ";"
            call_2 = " UPDATE teammates SET winrate_20_match =" + str(win_20) + "WHERE id = " + str(teammates_tid) + ";"
            call_3 = " UPDATE teammates SET winrate_40_match =" + str(win_40) + "WHERE id = " + str(teammates_tid) + ";"
            call = call_0 + call_1 + call_2 + call_3

            cursor.execute(
                call
            )

    finally:

        if connection:

            cursor.close()
            connection.close()

    return

def win_enemies_writer(win_5, win_10, win_20, win_40, enemies_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call_0 = "UPDATE enemies SET winrate_5_match =" + str(win_5) + "WHERE id = " + str(enemies_tid) + ";"
            call_1 = " UPDATE enemies SET winrate_10_match =" + str(win_10) + "WHERE id = " + str(enemies_tid) + ";"
            call_2 = " UPDATE enemies SET winrate_20_match =" + str(win_20) + "WHERE id = " + str(enemies_tid) + ";"
            call_3 = " UPDATE enemies SET winrate_40_match =" + str(win_40) + "WHERE id = " + str(enemies_tid) + ";"
            call = call_0 + call_1 + call_2 + call_3

            cursor.execute(
                call
            )

    finally:

        if connection:

            cursor.close()
            connection.close()

    return

def main(main_player_id, game_count):

    ez_proxy.init()

    users_tid = users_writer(main_player_id)

    result_list, match_id_list = game_info(main_player_id, game_count)

    game_info_writer(result_list, match_id_list, users_tid)

    match_list = game_info_reader(users_tid)
 
    for i in match_list:

        teammates, enemies = teammates_id(i[0], main_player_id)
        teammates_id_writer(teammates, i[1])
        enemies_id_writer(enemies, i[1])

    return

    for i in match_list:

        teammates_id_list = teammates_id_reader(i[1])
        enemies_id_list = enemies_id_reader(i[1])

        for m in teammates_id_list:

            win_5, win_10, win_20, win_40 = winrate(m[0], i[0])
            win_teammates_writer(win_5, win_10, win_20, win_40, m[1])

        for m in enemies_id_list:

            win_5, win_10, win_20, win_40 = winrate(m[0], i[0])
            win_enemies_writer(win_5, win_10, win_20, win_40, m[1])

    return

def main_restart_wirate(users_tid, start):

    ez_proxy.init()

    match_list = game_info_reader(users_tid)
 
    i = start

    while i < len(match_list):

        k = match_list[i]

        teammates_id_list = teammates_id_reader(k[1])
        enemies_id_list = enemies_id_reader(k[1])

        for m in teammates_id_list:

            win_5, win_10, win_20, win_40 = winrate(m[0], k[0])
            win_teammates_writer(win_5, win_10, win_20, win_40, m[1])

        for m in enemies_id_list:

            win_5, win_10, win_20, win_40 = winrate(m[0], k[0])
            win_enemies_writer(win_5, win_10, win_20, win_40, m[1])

        i += 1


if __name__ == '__main__':

    freeze_support()
    main(main_player_id_1, 300)
    main(main_player_id_2, 300)
    #main_restart_wirate('182', 161)

