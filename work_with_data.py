import sqlite3
from googletrans import Translator

translator = Translator()


def trans(text):
    lang = translator.detect(text).lang
    if type(lang) == list:
        text_trns = translator.translate(text, src=lang[1], dest='ru').text
    else:
        text_trns = translator.translate(text, src=lang, dest='ru').text
    return text_trns


def get_ads_by_filter(person, category, filt):
    try:
        ads = {}
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        if person == 0:
            forma = f"SELECT * from ad_realty WHERE person='{category}' AND type='{filt}'"
        if person == 1:
            if type(filt) == list:
                forma = f"SELECT * from ad_transport WHERE category='{category}' AND type='{filt[0]}' AND type_of_avto='{filt[1]}'"
            else:
                forma = f"SELECT * from ad_transport WHERE category='{category}' AND type='{filt}'"
        if person == 2:
            forma = f"SELECT * from buy_sale WHERE buy_or_sale='{category}'"

        cursor.execute(forma)
        records = cursor.fetchall()
        keys = 1
        for el in records:
            element = list(el)
            ads.update({keys: element[3:]})
            keys += 1
        cursor.close()
        return ads

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_ads(person, category):
    try:
        ads = {}
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()
        if person == 0:
            forma = f"SELECT * from ad_realty WHERE person='{category}'"
        if person == 1:
            forma = f"SELECT * from ad_transport WHERE category='{category}'"
        if person == 2:
            forma = f"SELECT * from buy_sale WHERE buy_or_sale='{category}'"

        cursor.execute(forma)
        records = cursor.fetchall()
        keys = 1
        for el in records:
            element = list(el)
            ads.update({keys: element[3:]})
            keys += 1
        cursor.close()
        return ads

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add_ad(contact, category, type, ad):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        mass = ad

        if category == 0:
            # for i in range(0, len(mass)):
            #     if i != 7 or i != 8 or i != 9 or i != 11:
            #         mass[i] = trans(mass[i])

            try:
                forma = f"INSERT INTO ad_realty" \
                                    f"(user_id, person, contact, type, rooms, bathrooms, size, pool, child, " \
                                    f"pets, minimal_months, price, link_maps, comment, path_photo)" \
                                    f"VALUES " \
                                    f"({mass[0]}, '{type}', '{contact}', '{mass[1]}', '{mass[2]}', '{mass[3]}', '{mass[4]}', '{mass[5]}', '{mass[6]}', " \
                                    f"'{mass[7]}', '{mass[8]}', '{mass[9]}', '{mass[10]}', '{mass[11]}', '{mass[12]}');"
            except:
                forma = f"INSERT INTO ad_realty" \
                                      f"(person, contact, type, rooms, bathrooms, size, pool, child, " \
                                      f"pets, minimal_months, price)" \
                                      f"VALUES" \
                                      f"('{type}', '{contact}', '{mass[0]}', '{mass[1]}', '{mass[2]}', '{mass[3]}', '{mass[4]}', '{mass[5]}', " \
                                      f"'{mass[6]}', '{mass[7]}', '{mass[8]}');"

        elif category == 1:
            # for i in range(len(mass)):
            #     if i == 1 or i == 6:
            #         continue
            #     else:
            #         mass[i] = trans(mass[i])
            try:
                if len(mass) == 7:
                    mass.insert(1, 'Другой Транспорт')
                print(mass)

                forma = f"INSERT INTO ad_transport" \
                                      f"(user_id, category, contact, type, type_of_avto, model, period, money, comment, path_photo)" \
                                      f"VALUES " \
                                      f"({mass[0]}, '{type}', '{contact}', '{mass[1]}', '{mass[2]}' ,'{mass[3]}' ,'{mass[4]}' , '{mass[5]}', '{mass[6]}', '{mass[7]}');"
            except:
                forma = f"INSERT INTO ad_transport" \
                                      f"(category, contact, type, type_of_avto, model, period, money)" \
                                      f"VALUES" \
                                      f"('{type}', '{contact}', '{mass[0]}', '{mass[1]}' ,'{mass[2]}' ,'{mass[3]}' , '{mass[4]}');"
            finally:
                if mass[1] == 'Другой Транспорт':
                    mass.pop(1)
        elif category == 2:
            # for i in range(len(mass)):
            #     if i != 2:
            #         mass[i] = trans(mass[i])
            try:
                forma = f"INSERT INTO buy_sale" \
                                      f"(buy_or_sale, contact, category, discription, photo_path)" \
                                      f"VALUES" \
                                      f"('{type}', '{contact}', '{mass[0]}', '{mass[1]}', '{mass[2]}');"
            except:
                forma = f"INSERT INTO buy_sale" \
                                      f"(buy_or_sale, contact, category, discription)" \
                                      f"VALUES" \
                                      f"('{type}', '{contact}', '{mass[0]}', '{mass[1]}');"

        count = cursor.execute(forma)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_usernames():
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        forma = "SELECT * from admins "

        cursor.execute(forma)
        records = cursor.fetchall()

        mass = []
        for el in records:
            mass.append(el[1])
        cursor.close()
        return mass

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_table(table, pole, znach, id):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        forma = f"UPDATE {table} SET {pole} = '{znach}' WHERE username = '{id}';"

        cursor.execute(forma)
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def ad_time_data(table, pole, znach):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        forma = f"INSERT INTO {table} ({pole}) VALUES ('{znach}');"

        cursor.execute(forma)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get(znach, username):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        forma = f"SELECT {znach} from user_category where username='{username}'"

        cursor.execute(forma)
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return records[0][0]
        else:
            return 0

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_lng(username):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        forma = f"SELECT language from languages where username='{username}'"

        cursor.execute(forma)
        records = cursor.fetchall()
        cursor.close()
        if len(records) == 0:
            return 0
        else:
            return records[0][0]

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add_lng(username, lng):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        forma = f"INSERT INTO languages (language, username) VALUES ('{lng}', '{username}');"

        cursor.execute(forma)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite1111", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_elem(table, username):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        forma = f"DELETE FROM {table} WHERE username = '{username}'; "

        cursor.execute(forma)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite2", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add_counter(username):
    try:
        sqlite_connection = sqlite3.connect('db.db')
        cursor = sqlite_connection.cursor()

        forma = f"INSERT INTO counters (username, glb_counter, glb_counters_ads, menu_counter) VALUES ('{username}', {0}, {0}, {0});"

        cursor.execute(forma)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite2", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()







