import psycopg2
from decimal import Decimal, ROUND_HALF_UP

def game_info_reader(users_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call = "SELECT match_id, id, match_result FROM player_match_stat WHERE fk_player_match_stat_users =" + users_tid + ";"

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

def win_teammates_reader(fk_teammates_player_match_stat):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call = "SELECT winrate_5_match, winrate_10_match, winrate_20_match, winrate_40_match FROM teammates WHERE fk_teammates_player_match_stat =" + str(fk_teammates_player_match_stat) + ";"

            cursor.execute(
                call
            )

            teammate_win_list = cursor.fetchall()

    finally:

        if connection:

            cursor.close()
            connection.close()

    return teammate_win_list

def win_enemies_reader(fk_enemies_player_match_stat):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call = "SELECT winrate_5_match, winrate_10_match, winrate_20_match, winrate_40_match FROM enemies WHERE fk_enemies_player_match_stat =" + str(fk_enemies_player_match_stat) + ";"

            cursor.execute(
                call
            )

            enemy_win_list = cursor.fetchall()

    finally:

        if connection:

            cursor.close()
            connection.close()

    return enemy_win_list

def win_stat(list):

    if len(list) == 0:

        win_5 = Decimal(0.5)
        win_10 = Decimal(0.5)
        win_20 = Decimal(0.5)
        win_40 = Decimal(0.5)

        return win_5, win_10, win_20, win_40

    else:   

        win_5 = Decimal(0)
        win_10 = Decimal(0)
        win_20 = Decimal(0)
        win_40 = Decimal(0)

    for i in list:

        win_5 += Decimal(i[0])
        win_10 += Decimal(i[1])
        win_20 += Decimal(i[2])
        win_40 += Decimal(i[3])

    win_5 = win_5/len(list)
    win_10 = win_10/len(list)
    win_20 = win_20/len(list)
    win_40 = win_40/len(list)

    num = Decimal('1.11')

    win_5 = win_5.quantize(num, ROUND_HALF_UP)
    win_10 = win_10.quantize(num, ROUND_HALF_UP)
    win_20 = win_20.quantize(num, ROUND_HALF_UP)
    win_40 = win_40.quantize(num, ROUND_HALF_UP)

    return win_5, win_10, win_20, win_40

def win_match_writer(t_win_5, t_win_10, t_win_20, t_win_40, e_win_5, e_win_10, e_win_20, e_win_40, id):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call_0 = "UPDATE player_match_stat SET teammates_winrate_5_match =" + str(t_win_5) + "WHERE id = " + str(id) + ";"
            call_1 = " UPDATE player_match_stat SET teammates_winrate_10_match =" + str(t_win_10) + "WHERE id = " + str(id) + ";"
            call_2 = " UPDATE player_match_stat SET teammates_winrate_20_match =" + str(t_win_20) + "WHERE id = " + str(id) + ";"
            call_3 = " UPDATE player_match_stat SET teammates_winrate_40_match =" + str(t_win_40) + "WHERE id = " + str(id) + ";"
            call_4 = " UPDATE player_match_stat SET enemies_winrate_5_match =" + str(e_win_5) + "WHERE id = " + str(id) + ";"
            call_5 = " UPDATE player_match_stat SET enemies_winrate_10_match =" + str(e_win_10) + "WHERE id = " + str(id) + ";"
            call_6 = " UPDATE player_match_stat SET enemies_winrate_20_match =" + str(e_win_20) + "WHERE id = " + str(id) + ";"
            call_7 = " UPDATE player_match_stat SET enemies_winrate_40_match =" + str(e_win_40) + "WHERE id = " + str(id) + ";"
            call = call_0 + call_1 + call_2 + call_3 + call_4 + call_5 + call_6 + call_7

            cursor.execute(
                call
            )

    finally:

        if connection:

            cursor.close()
            connection.close()

    return

def win_user_writer(u_t_win_5, u_t_win_10, u_t_win_20, u_t_win_40, u_e_win_5, u_e_win_10, u_e_win_20, u_e_win_40, user_win, users_tid):

    try:

        connection = psycopg2.connect(database = "dota2_base", user = "admin", password = "108", port = 5432)
        connection.autocommit = True

        with  connection.cursor() as cursor:

            call_0 = "UPDATE users SET teammates_winrate_5_matches =" + str(u_t_win_5) + "WHERE id = " + str(users_tid) + ";"
            call_1 = " UPDATE users SET teammates_winrate_10_matches =" + str(u_t_win_10) + "WHERE id = " + str(users_tid) + ";"
            call_2 = " UPDATE users SET teammates_winrate_20_matches =" + str(u_t_win_20) + "WHERE id = " + str(users_tid) + ";"
            call_3 = " UPDATE users SET teammates_winrate_40_matches =" + str(u_t_win_40) + "WHERE id = " + str(users_tid) + ";"
            call_4 = " UPDATE users SET enemies_winrate_5_matches =" + str(u_e_win_5) + "WHERE id = " + str(users_tid) + ";"
            call_5 = " UPDATE users SET enemies_winrate_10_matches =" + str(u_e_win_10) + "WHERE id = " + str(users_tid) + ";"
            call_6 = " UPDATE users SET enemies_winrate_20_matches =" + str(u_e_win_20) + "WHERE id = " + str(users_tid) + ";"
            call_7 = " UPDATE users SET enemies_winrate_40_matches =" + str(u_e_win_40) + "WHERE id = " + str(users_tid) + ";"
            call_8 = " UPDATE users SET user_winrate =" + str(user_win) + "WHERE id = " + str(users_tid) + ";"
            call = call_0 + call_1 + call_2 + call_3 + call_4 + call_5 + call_6 + call_7 + call_8

            cursor.execute(
                call
            )

    finally:

        if connection:

            cursor.close()
            connection.close()

    return

def main(users_tid):

    match_list = game_info_reader(users_tid)

    u_t_win_5 = Decimal(0)
    u_t_win_10 = Decimal(0)
    u_t_win_20 = Decimal(0)
    u_t_win_40 = Decimal(0)
    u_e_win_5 = Decimal(0)
    u_e_win_10 = Decimal(0)
    u_e_win_20 = Decimal(0)
    u_e_win_40 = Decimal(0)
    user_win = Decimal(0)

    for match in match_list:

        if match[2] == 'won':

            user_win += Decimal(1)

        teammate_win_list = win_teammates_reader(match[1])
        enemy_win_list = win_enemies_reader(match[1])

        t_win_5, t_win_10, t_win_20, t_win_40 = win_stat(teammate_win_list)

        e_win_5, e_win_10, e_win_20, e_win_40 = win_stat(enemy_win_list)

        win_match_writer(t_win_5, t_win_10, t_win_20, t_win_40, e_win_5, e_win_10, e_win_20, e_win_40, match[1])

        u_t_win_5 += Decimal(t_win_5)
        u_t_win_10 += Decimal(t_win_10)
        u_t_win_20 += Decimal(t_win_20)
        u_t_win_40 += Decimal(t_win_40)
        u_e_win_5 += Decimal(e_win_5)
        u_e_win_10 += Decimal(e_win_10)
        u_e_win_20 += Decimal(e_win_20)
        u_e_win_40 += Decimal(e_win_40)

    u_t_win_5 = u_t_win_5/len(match_list)
    u_t_win_10 = u_t_win_10/len(match_list)
    u_t_win_20 = u_t_win_20/len(match_list)
    u_t_win_40 = u_t_win_40/len(match_list)
    u_e_win_5 = u_e_win_5/len(match_list)
    u_e_win_10 = u_e_win_10/len(match_list)
    u_e_win_20 = u_e_win_20/len(match_list)
    u_e_win_40 = u_e_win_40/len(match_list)
    user_win = user_win/len(match_list)

    num = Decimal('1.11')

    u_t_win_5 = u_t_win_5.quantize(num, ROUND_HALF_UP)
    u_t_win_10 = u_t_win_10.quantize(num, ROUND_HALF_UP)
    u_t_win_20 = u_t_win_20.quantize(num, ROUND_HALF_UP)
    u_t_win_40 = u_t_win_40.quantize(num, ROUND_HALF_UP)
    u_e_win_5 = u_e_win_5.quantize(num, ROUND_HALF_UP)
    u_e_win_10 = u_e_win_10.quantize(num, ROUND_HALF_UP)
    u_e_win_20 = u_e_win_20.quantize(num, ROUND_HALF_UP)
    u_e_win_40 = u_e_win_40.quantize(num, ROUND_HALF_UP)
    user_win = user_win.quantize(num, ROUND_HALF_UP)

    win_user_writer(u_t_win_5, u_t_win_10, u_t_win_20, u_t_win_40, u_e_win_5, u_e_win_10, u_e_win_20, u_e_win_40, user_win, users_tid)

if __name__ == '__main__':

    main('221')