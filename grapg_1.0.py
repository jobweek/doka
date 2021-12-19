import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import psycopg2

def match_reader(users_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call = "SELECT match_result, teammates_winrate_5_match, teammates_winrate_10_match, teammates_winrate_20_match, teammates_winrate_40_match, enemies_winrate_5_match, enemies_winrate_10_match, enemies_winrate_20_match, enemies_winrate_40_match FROM player_match_stat WHERE fk_player_match_stat_users =" + users_tid + ";"

            cursor.execute(
                call
            )

            match_list = cursor.fetchall()
             

    finally:

        if connection:

            cursor.close()
            connection.close()

    return match_list

def uper(list):

    res = []

    for i in list:

        res.append(int((i - 0.5) * 1000))

    return res

def main(users_tid):

    match_list = match_reader(users_tid)
    
    if match_list[0][0] == 'won':

        res = 25

    else:

        res = -25

    mmr_level = [float(res)]
    t_win_5 = [float(match_list[0][1])]
    t_win_10 = [float(match_list[0][2])]
    t_win_20 = [float(match_list[0][3])]
    t_win_40 = [float(match_list[0][4])]
    e_win_5 = [float(match_list[0][5])]
    e_win_10 = [float(match_list[0][6])]
    e_win_20 = [float(match_list[0][7])]
    e_win_40 = [float(match_list[0][8])]

    i = 1

    while i < len(match_list):

        match = match_list[i]

        if match[0] == 'won':

            res = 25

        else:

            res = -25

        var_mmr_level = mmr_level[-1] + float(res)

        mmr_level.append(float(var_mmr_level))
        t_win_5.append(float(match[1]))
        t_win_10.append(float(match[2]))
        t_win_20.append(float(match[3]))
        t_win_40.append(float(match[4]))
        e_win_5.append(float(match[5]))
        e_win_10.append(float(match[6]))
        e_win_20.append(float(match[7]))
        e_win_40.append(float(match[8]))

        i += 1

    x = [x + 1 for x in range(len(match_list))]

    plt.plot(x, mmr_level, label = "mmr_change")

    # y = uper(t_win_5)
    # print(y)
    # plt.plot(x, y, label = "teammates_winrate_5_matches")

    # y = uper(t_win_10)
    # plt.plot(x, y, label = "teammates_winrate_10_matches")    

    # y = uper(t_win_20)
    # plt.plot(x, y, label = "teammates_winrate_20_matches")    

    # y = uper(t_win_40)
    # plt.plot(x, y, label = "teammates_winrate_40_matches")    

    # y = uper(e_win_5)
    # plt.plot(x, y, label = "enemies_winrate_5_matches")   

    # y = uper(e_win_10)
    # plt.plot(x, y, label = "enemies_winrate_10_matches")   

    # y = uper(e_win_20)
    # plt.plot(x, y, label = "enemies_winrate_20_matches")   

    y = uper(e_win_40)
    plt.plot(x, y, label = "enemies_winrate_40_matches")  

    plt.xlabel('matches')
    plt.ylabel('y - axis')
    plt.title('Doka_2_fucker')
    plt.legend()
    plt.show()

if __name__ == '__main__':

    main('211')