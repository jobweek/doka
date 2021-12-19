from bs4 import BeautifulSoup
import requests
import time
import psycopg2
from random import randrange
from tqdm import tqdm
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from fp.fp import FreeProxy
from tqdm.std import trange
from shodan import Shodan
import aiohttp
import asyncio
from concurrent.futures import FIRST_COMPLETED

requests.packages.urllib3.disable_warnings()
main_player_id = '/players/402544056'

def proxy_dict(proxy_list):

    proxy_dict_list = []

    for i in proxy_list:

        if i[2] == 'HTTP':

            pr = {
                'http': 'http://' + str(i[0]) + ':' + str(i[1]),
                'https': 'http://' + str(i[0]) + ':' + str(i[1])
            }

        elif i[2] == 'SOCKS4':

            pr = {
                'http': 'socks4://' + str(i[0]) + ':' + str(i[1]),
                'https': 'socks4://' + str(i[0]) + ':' + str(i[1])
            }

        elif i[2] == 'SOCKS5':

            pr = {
                'http': 'socks5://' + str(i[0]) + ':' + str(i[1]),
                'https': 'socks5://' + str(i[0]) + ':' + str(i[1])
            }

        proxy_dict_list.append(pr)

    return proxy_dict_list

def proxy_search():

    proxy_list = []

    api = Shodan('CT87JkrMT1FyOzeCzp8ynakn0PdXYtuO')

    results = api.search('proxy port:8080')
    
    for result in results['matches']:

        ip_port = {'https':"http://" + str(result['ip_str']) + ":" + "8080"}

        proxy_list.append(ip_port)
    print("Total Found:", results['total'])
    return proxy_list

def proxy_pars(proxy_count):

    proxy_list = []
    user_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"        
    }

    i = 0
    
    while i <= proxy_count:

        time.sleep(5)

        url = "https://hidemy.name/ru/proxy-list/?start=" + str(i) + "#list"

        for _ in range(10):

            try:

                r = requests.get(url, headers = user_agent, timeout = 1)

                break

            except:

                time.sleep(1200)

        if r == None:

            print('proxy_pars(), connection lost')

            break

        if r.status_code != 200:

            print('proxy_pars()', r.status_code)

            break

        soup = BeautifulSoup(r.text, "lxml")

        tbody = soup.find("table").find("tbody")

        tr = tbody.find_all("tr")

        for t in tr:

            td = t.find_all("td")

            ip = td[0].text
            port = td[1].text
            prot = td[4].text

            if prot == "HTTPS":

                continue

            ckeck = prot.find(",")
                
            if ckeck == -1:
                
                pass

            else:
                
                prot = prot[:ckeck]

            proxy_list.append([ip, port, prot])

        print("parsed:",i)

        i += 64
    print("Total Parsed:", len(proxy_list))
    return proxy_list

def proxy_check(proxy_list):

    good_proxy_list = []
    c = 0

    for i in proxy_list:
        c += 1
        user_agent = rand_user_agent()
        timeout = 3
        try:

            if i[2] == 'HTTP':

                pr = {
                    'http': 'http://' + str(i[0]) + ':' + str(i[1]),
                    'https': 'http://' + str(i[0]) + ':' + str(i[1])
                }

                r = requests.get("https://ru.dotabuff.com/", headers = user_agent, proxies = pr, verify = False, cert = False, timeout = timeout)

            elif i[2] == 'HTTPS':

                pr = {
                    'http': 'https://' + str(i[0]) + ':' + str(i[1]),
                    'https': 'https://' + str(i[0]) + ':' + str(i[1])
                }

                r = requests.get("https://ru.dotabuff.com/", headers = user_agent, proxies = pr, verify = False, cert = False, timeout = timeout)

            elif i[2] == 'SOCKS4':

                pr = {
                    'https': 'socks4://' + str(i[0]) + ':' + str(i[1]),
                    'https': 'socks4://' + str(i[0]) + ':' + str(i[1])
                }

                r = requests.get("https://ru.dotabuff.com/", headers = user_agent, proxies = pr, verify = False, cert = False, timeout = timeout)

            elif i[2] == 'SOCKS5':

                pr = {
                    'https': 'socks5://' + str(i[0]) + ':' + str(i[1]),
                    'https': 'socks5://' + str(i[0]) + ':' + str(i[1])
                }

                r = requests.get("https://ru.dotabuff.com/", headers = user_agent, proxies = pr, verify = False, cert = False, timeout = timeout)

            if r.status_code == 200:

                good_proxy_list.append([pr,r.cookies])

        except:

            pass

        print("Proxy", c, "checked")

    print("Proxies Found:", len(good_proxy_list))
    return good_proxy_list

def rand_user_agent():

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value] 
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    rand_user_agent = {'User-Agent':user_agent_rotator.get_random_user_agent()}

    return rand_user_agent

class Ez_Proxy:

    def __init__(self):

        self.proxy_list = proxy_dict(proxy_pars(2048))
        self.proxy_id = 0

        if len(self.proxy_list) == 0:

            print("NO PROXIES")
            exit()

    def get(self):

        if self.proxy_id == len(self.proxy_list):

            time.sleep(1200)
            
            self.__init__()

        new_proxy = self.proxy_list[self.proxy_id]#[0]
        cookie = None#self.proxy_list[self.proxy_id][1]
        self.proxy_id += 1

        return new_proxy, cookie

ez_proxy = Ez_Proxy()

class Website_Fucker:

    def __init__(self):

        self.update()

    def update(self):

        self.user_agent = rand_user_agent()
        self.proxy, self.cookies = ez_proxy.get()

        print("new proxy:", self.proxy)

    def get(self):

        return self.user_agent, self.proxy, self.cookies

website_fucker = Website_Fucker()

def get_connection(url):

    time.sleep(randrange(4,10))

    user_agent, proxy, cookies = website_fucker.get()

    while True:

        try:

            r = requests.get(url, headers = user_agent, proxies = proxy, verify = False, cert = False, timeout = 4)

            break

        except:
            print("no_connection")
            website_fucker.update()
            user_agent, proxy, cookies = website_fucker.get()

    return r

def get_request(url):

    r = get_connection(url)

    while r.status_code != 200:
        print("bad_status_code")
        website_fucker.update()
        r = get_connection(url)

    soup = BeautifulSoup(r.text, "lxml")

    return soup

def game_info(main_player_id, game_count):

    i = 1
    result_list = []
    match_id_list = []
    loop_condition = True

    while loop_condition == True:

        url = 'https://ru.dotabuff.com' + main_player_id +'/matches?enhance=overview&page=' + str(i)

        soup = get_request(url)

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

    match_soup = get_request(match_url)

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

        player_match_soup = get_request(player_match_url)
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

                    loop_condition = False

                    break

                else:
                    
                    player_match_result = player_match['class'][0]
                    player_match_list.append(player_match_result)

        i += 1

        if i > page_count:

            break

    win_40 = player_match_list[1:].count('won')/len(player_match_list)

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

    users_tid = users_writer(main_player_id)

    result_list, match_id_list = game_info(main_player_id, game_count)

    game_info_writer(result_list, match_id_list, users_tid)

    match_list = game_info_reader(users_tid)
 
    for i in match_list:

        teammates, enemies = teammates_id(i[0], main_player_id)
        teammates_id_writer(teammates, i[1])
        enemies_id_writer(enemies, i[1])

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

main(main_player_id, 10)

def test():

    user_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"        
    }

    pr = {
        'http': 'http://173.245.49.7:80',
        'https': 'http://173.245.49.7:80' 
    }

    r = requests.get('https://ru.dotabuff.com/', headers = user_agent, proxies = pr, verify = False, cert = False, timeout = 4)

    return r
