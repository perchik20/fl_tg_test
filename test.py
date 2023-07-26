#
# import sqlite3
#
# def read_sqlite_table(records):
#     try:
#         sqlite_connection = sqlite3.connect('db.db')
#         cursor = sqlite_connection.cursor()
#         print("Подключен к SQLite")
#
#         sqlite_select_query = f"INSERT INTO ad_realty" \
#         f"(user_id, person, contact, type, rooms, bathrooms, size, pool, child, " \
#         f"pets, minimal_months, price, link_maps, comment, path_photo, last_date)" \
#         f"VALUES "
#         f"(1, 215005591, 'landlord', 'Кондо', 3, 3, 100, 'Частный и Общественный', 'Есть', 'Можно', '1 день', 111111, 'https://goo.gl/maps/WytUmSgCrpQf4tSHA', 'Кккккккк', {'<a href="https://t.me/Fedya_Pipiskin">V</a>'}, 'static/photos/AgACAgIAAxkBAAJmf2S7UqO5htki91FKIuNIQ8wTybeDAAIZzzEbo2_YSXZYqZfFYYBLAQADAgADbQADLwQ.jpg', {date('2023-08-21')});"
#         cursor.execute(sqlite_select_query)
#         records = cursor.fetchall()
#         print("Всего строк:  ", len(records))
#         print("Вывод каждой строки")
#         for row in records:
#             print(row)
#
#         cursor.close()
#
#     except sqlite3.Error as error:
#         print("Ошибка при работе с SQLite", error)
#     finally:
#         if sqlite_connection:
#             sqlite_connection.close()
#             print("Соединение с SQLite закрыто")
#
# read_sqlite_table()

# (1, 215005591, 'landlord', 'Кондо', 3, 3, 100, 'Частный и Общественный', 'Есть', 'Можно', '1 день', 111111, 'https://goo.gl/maps/WytUmSgCrpQf4tSHA', 'Кккккккк', '<a href="https://t.me/Fedya_Pipiskin">V</a>', 'static/photos/AgACAgIAAxkBAAJmf2S7UqO5htki91FKIuNIQ8wTybeDAAIZzzEbo2_YSXZYqZfFYYBLAQADAgADbQADLwQ.jpg', '2023-08-21')
# (2, 215005591, 'landlord', 'Вилла', 3, 3, 11111, 'Частный и Общественный', 'Есть', 'Нельзя', 111111, 1111111, 'https://goo.gl/maps/WytUmSgCrpQf4tSHA', 'Ппппп', '<a href="https://t.me/Fedya_Pipiskin">V</a>', 'static/photos/AgACAgIAAxkBAAJmlmS7UxlcWvkdxJ4Rf-hIySVnvy9ZAAIZzzEbo2_YSXZYqZfFYYBLAQADAgADbQADLwQ.jpg', '2023-08-21')
# (3, 215005591, 'landlord', 'Коммерческая недвижимость', 'Склад', None, 1111, None, None, None, None, None, 'https://goo.gl/maps/WytUmSgCrpQf4tSHA', 'Рррр', '<a href="https://t.me/Fedya_Pipiskin">V</a>', 'static/photos/AgACAgIAAxkBAAJm1GS7VNx_cKDgpr9lRc2wUrjzP7ihAAIZzzEbo2_YSXZYqZfFYYBLAQADAgADbQADLwQ.jpg', '2023-08-21')
# (4, None, 'tenant', 'Кондо', '2 и более', '2 и более', 100, 'Частный и Общественный', 'Не имеет значения', 'Нет', '2 мес', 1111111, None, 'Оаовлвлввьвь', '<a href="https://t.me/Fedya_Pipiskin">V</a>', None, '2023-08-21')