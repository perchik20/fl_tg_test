from telebot import types

from config import bot, translator
from logic_function import send_questions, check_ad, photo_check

from questions import realty, tenant, buy_sale, repeat_msg_1, repeat_msg_0
from work_with_data import add_ad, get_ads, get_usernames, update_table, ad_time_data, get, get_lng, add_lng, \
    delete_elem
from send_to_chanell import ad_from_landlord, ad_from_tenant
from parser import main, main1

# bot = telebot.TeleBot(token)
# translator = Translator()

# //////////////////////////////perem///////////////////////////////////////

categorys = ['Недвижимость', 'Транспорт']
ad = {}
questions = {}
ads = {}
counters = {}

# /////////////////////////////////////functions//////////////////////////////


def trans(text, language):
    text_trns = translator.translate(text, src='ru', dest=language).text
    return text_trns


def category1(language):
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton(trans('Недвижимость', language), callback_data='realty'))
    ikb.add(types.InlineKeyboardButton(trans('Транспорт', language), callback_data='transport'))
    ikb.add(types.InlineKeyboardButton(trans('Куплю/Продам', language), callback_data='buy_sale'))
    ikb.add(types.InlineKeyboardButton(trans('Медицина', language), callback_data='medicines'))
    # ikb.add(types.InlineKeyboardButton(trans('Выполняю/Покупаю услуги', language), callback_data='do_buy'))

    text_trns = trans('Выберите категорию: ', language)

    return [text_trns, ikb]


def make_buttons(category, name, name1, mass, languge):
    counter = 0
    questions.update({f'<a href="https://t.me/{name}">{name1}</a>': {}})
    if category == 'medicines':
        ikb_medicines = types.InlineKeyboardMarkup()

        for med in mass:
            questions[f'<a href="https://t.me/{name}">{name1}</a>'].update({f'key{counter}': med[0]})
            ikb_medicines.add(types.InlineKeyboardButton(med[1], callback_data=f'key{counter}'))
            counter += 1

        return ikb_medicines

    else:
        text_trns = trans(mass[0], language)
        ikb_questions = types.InlineKeyboardMarkup()
        for i in mass[1]:
            questions[f'<a href="https://t.me/{name}">{name1}</a>'].update({f'key{counter}': trans(i, language)})
            ikb_questions.add(types.InlineKeyboardButton(trans(i, language), callback_data=f'key{counter}'))
            counter += 1

        return [text_trns, ikb_questions]


# ///////////////////////////////////buttons//////////////////////////////
markup_lng = types.ReplyKeyboardMarkup(True, True)
markup_lng.row("Русский 🇷🇺", "English 🇺🇸")


# ////////////////////////////////////////////////////////////////////////////////////
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global language
    global glb_counter
    global ad
    global glb_counter_ads
    global menu_counter

    if call.message:
        msg = call.data

        language = get_lng(f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
        point = get('point', f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
        category = get('category', f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
        l_or_r = get('l_or_r', f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
        username = f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'

    # //////////////////////////////// Choosing a category /////////////////////////////////////////////

        if msg == 'medicines':
            update_table('user_category', 'category', 'medicines',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            text = 'Напишите название препарата аналог которого вы ищите: '
            bot.send_message(call.message.chat.id, trans(text, language))

        elif msg == 'sale':
            update_table('user_category', 'l_or_r', 'landlord',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            if point == 'send':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                qstns = make_buttons(category, call.message.chat.username, call.message.chat.first_name, buy_sale[0], language)
                bot.send_message(call.message.chat.id, qstns[0], reply_markup=qstns[1])
            elif point == 'check':
                all_realty_ads = get_ads(category, 'tenant')
                ads.update({username: all_realty_ads})
                for i in ads[username]:
                    ads[username][i].pop(2)

                mass_buttons = [
                    [
                        types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                        types.InlineKeyboardButton(trans('Далее', language), callback_data='next1')
                    ],
                ]

                msg = f'Категория: {ads[username][counters[username]["glb_counter_ads"]][0]}\nОписание: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][1]}\nКонтакт: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][2]}'

                ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')

        elif msg == 'buy':
            update_table('user_category', 'l_or_r', 'tenant',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            if point == 'send':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                qstns = make_buttons(category, call.message.chat.username, call.message.chat.first_name, buy_sale[0], language)
                bot.send_message(call.message.chat.id, qstns[0], reply_markup=qstns[1])
            elif point == 'check':
                all_realty_ads = get_ads(category, 'landlord')
                ads.update({username: all_realty_ads})

                mass_buttons = [
                    [
                        types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                        types.InlineKeyboardButton(trans('Далее', language), callback_data='next1')
                    ],

                    [types.InlineKeyboardButton(trans('Бронь', language), callback_data='order')]
                ]

                msg = f'Категория: {ads[username][counters[username]["glb_counter_ads"]][0]}\nОписание: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][1]}\nКонтакт: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][3]}'

                photo1 = open(f'{ads[username][counters[username]["glb_counter_ads"]][2]}', "rb")

                ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_photo(call.message.chat.id, photo1, caption=msg, reply_markup=ikb3, parse_mode='HTML')

        elif msg == 'next1':

            counters[username]['glb_counter_ads'] += 1

            mass_buttons = [
                [
                    types.InlineKeyboardButton(trans('Назад', language), callback_data='back1'),
                    types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                    types.InlineKeyboardButton(trans('Далее', language), callback_data='next1')
                ]
            ]

            mass_buttons1 = [
                [
                    types.InlineKeyboardButton(trans('Назад', language), callback_data='back1'),
                    types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                ],
            ]

            msg = f'Категория: {ads[username][counters[username]["glb_counter_ads"]][0]}\nОписание: ' \
                  f'{ads[username][counters[username]["glb_counter_ads"]][1]}'

            if l_or_r == 'landlord':
                msg = f'Категория: {ads[username][counters[username]["glb_counter_ads"]][0]}\nОписание: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][1]}\nКонтакт: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][2]}'
                if len(ads[username]) == counters[username]["glb_counter_ads"]:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons1)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')
                else:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')

            elif l_or_r == 'tenant':
                photo2 = open(f'{ads[username][counters[username]["glb_counter_ads"]][2]}', "rb")
                msg = f'Категория: {ads[username][counters[username]["glb_counter_ads"]][0]}\nОписание: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][1]}\nКонтакт: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][3]}'
                if len(ads[username]) == counters[username]["glb_counter_ads"]:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons1)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, photo2, caption=msg, reply_markup=ikb3, parse_mode='HTML')
                else:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, photo2, caption=msg, reply_markup=ikb3, parse_mode='HTML')

        elif msg == 'back1':
            counters[username]["glb_counter_ads"] += 1

            mass_buttons = [
                [
                    types.InlineKeyboardButton(trans('Назад', language), callback_data='back1'),
                    types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                    types.InlineKeyboardButton(trans('Далее', language), callback_data='next1')
                ],
            ]

            mass_buttons1 = [
                [
                    types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads)}', callback_data='--'),
                    types.InlineKeyboardButton(trans('Далее', language), callback_data='next1'),
                ],
            ]

            msg = f'Категория: {ads[username][counters[username]["glb_counter_ads"]][0]}\nОписание: {ads[username][counters[username]["glb_counter_ads"]][1]}'

            if l_or_r == 'landlord':
                msg = f'Категория: {ads[username][counters[username]["glb_counter_ads"]][0]}\nОписание:' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][1]}\nКонтакт: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][2]}'

                if counters[username]["glb_counter_ads"] == 1:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons1)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')
                else:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')
            elif l_or_r == 'tenant':
                photo3 = open(f'{ads[username][counters[username]["glb_counter_ads"]][2]}', "rb")
                msg = f'Категория: {ads[username][counters[username]["glb_counter_ads"]][0]}\nОписание: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][1]}\nКонтакт: ' \
                      f'{ads[username][counters[username]["glb_counter_ads"]][3]}'

                if counters[username]["glb_counter_ads"] == 1:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons1)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, photo3, caption=msg, reply_markup=ikb3, parse_mode='HTML')
                else:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, photo3, caption=msg, reply_markup=ikb3, parse_mode='HTML')

        elif msg == 'realty':
            counters.update({f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>':
                                 {'glb_counter': 0, 'glb_counter_ads': 1, 'menu_counter': 0}})
            counters[username]['menu_counter'] += 1
            ad_time_data('user_category', 'username',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            update_table('user_category', 'category', '0',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            ikb1 = types.InlineKeyboardMarkup()
            ikb1.add(types.InlineKeyboardButton(trans('Разместить объявление', language), callback_data='send_ad'))
            ikb1.add(types.InlineKeyboardButton(trans('Посмотреть объявления', language), callback_data='check_ad'))
            ikb1.add(types.InlineKeyboardButton(trans('Назад 🔙', language), callback_data='back_menu'))
            bot.send_message(call.message.chat.id, trans('Выберите пункт:', language), reply_markup=ikb1)
        elif msg == 'transport':
            counters.update({f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>':
                                 {'glb_counter': 0, 'glb_counter_ads': 1, 'menu_counter': 0}})
            counters[username]['menu_counter'] += 1
            ad_time_data('user_category', 'username',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            update_table('user_category', 'category', '1',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            ikb1 = types.InlineKeyboardMarkup()
            ikb1.add(types.InlineKeyboardButton(trans('Разместить объявление', language), callback_data='send_ad'))
            ikb1.add(types.InlineKeyboardButton(trans('Посмотреть объявления', language), callback_data='check_ad'))
            ikb1.add(types.InlineKeyboardButton(trans('Назад 🔙', language), callback_data='back_menu'))
            bot.send_message(call.message.chat.id, trans('Выберите пункт:', language), reply_markup=ikb1)
        elif msg == 'buy_sale':
            counters.update({f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>':
                                 {'glb_counter': 0, 'glb_counter_ads': 1, 'menu_counter': 0}})
            counters[username]['menu_counter'] += 1
            ad_time_data('user_category', 'username',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            update_table('user_category', 'category', '2',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            ikb1 = types.InlineKeyboardMarkup()
            ikb1.add(types.InlineKeyboardButton(trans('Разместить объявление', language), callback_data='send_ad'))
            ikb1.add(types.InlineKeyboardButton(trans('Посмотреть объявления', language), callback_data='check_ad'))
            ikb1.add(types.InlineKeyboardButton(trans('Назад 🔙', language), callback_data='back_menu'))
            bot.send_message(call.message.chat.id, trans('Выберите пункт:', language), reply_markup=ikb1)
    # //////////////////////////////// Choosing a point /////////////////////////////////////////////

        elif msg == 'send_ad':
            ad.update({f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>': []})
            update_table('user_category', 'point', 'send',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            if category != 2:

                counters[username]['menu_counter'] += 1
                bot.delete_message(call.message.chat.id, call.message.message_id)
                ikb2 = types.InlineKeyboardMarkup()
                ikb2.add(types.InlineKeyboardButton(trans(f'Я сдаю {categorys[category]}', language), callback_data='landlord'))
                ikb2.add(types.InlineKeyboardButton(trans(f'Я ищу {categorys[category]}', language), callback_data='tenant'))
                ikb2.add(types.InlineKeyboardButton(trans('Назад 🔙', language), callback_data='back_menu'))
                bot.send_message(call.message.chat.id, trans('Выберите пункт:', language), reply_markup=ikb2)
            elif category == 2:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                ikb2 = types.InlineKeyboardMarkup()
                ikb2.add(types.InlineKeyboardButton(trans('Куплю', language), callback_data='buy'))
                ikb2.add(types.InlineKeyboardButton(trans('Продам', language), callback_data='sale'))
                ikb2.add(types.InlineKeyboardButton(trans('Назад 🔙', language), callback_data='back_menu'))
                bot.send_message(call.message.chat.id, trans('Выберите пункт:', language), reply_markup=ikb2)
        elif msg == 'check_ad':

            counters[username]['menu_counter'] += 1
            update_table('user_category', 'point', 'check',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            if category != 2:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                ikb2 = types.InlineKeyboardMarkup()
                ikb2.add(types.InlineKeyboardButton(trans(f'Я сдаю {categorys[category]}', language), callback_data='landlord'))
                ikb2.add(types.InlineKeyboardButton(trans(f'Я ищу {categorys[category]}', language), callback_data='tenant'))
                ikb2.add(types.InlineKeyboardButton(trans('Назад 🔙', language), callback_data='back_menu'))
                bot.send_message(call.message.chat.id, trans('Выберите пункт:', language), reply_markup=ikb2)
            elif category == 2:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                ikb2 = types.InlineKeyboardMarkup()
                ikb2.add(types.InlineKeyboardButton(trans('Куплю', language), callback_data='buy'))
                ikb2.add(types.InlineKeyboardButton(trans('Продам', language), callback_data='sale'))
                ikb2.add(types.InlineKeyboardButton(trans('Назад 🔙', language), callback_data='back_menu'))
                bot.send_message(call.message.chat.id, trans('Выберите пункт:', language), reply_markup=ikb2)

            # //////////////////////////////// Choosing a point /////////////////////////////////////////////

        elif msg == 'landlord':
            update_table('user_category', 'l_or_r', 'landlord',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            if point == 'send':
                buttons = make_buttons(category, call.message.chat.username, call.message.chat.first_name, realty[category][0], language)
                bot.send_message(call.message.chat.id, buttons[0], reply_markup=buttons[1])
            elif point == 'check':
                all_realty_ads = get_ads(category, 'tenant')
                ads.update({username: all_realty_ads})
                print(ads)
                if category == 0:
                    for i in ads[username]:
                        ads[username][i].pop(9)
                        ads[username][i].pop(9)
                        ads[username][i].pop(10)

                elif category == 1:
                    for i in ads[username]:
                        ads[username][i].pop(5)
                        ads[username][i].pop(6)


                mass_buttons = [
                    [
                        types.InlineKeyboardButton(trans('Назад', language), callback_data='back'),
                        types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                        types.InlineKeyboardButton(trans('Далее', language), callback_data='next')
                    ]
                ]

                msg = ''

                for sent in range(len(ads[username][counters[username]["glb_counter_ads"]])):
                    if category == 0:
                        if sent == 9:
                            msg += f'<b>{trans(repeat_msg_0[1][sent][0], language)}</b> ' + str(ads[username][counters[username]["glb_counter_ads"]][sent]) + '\n'
                        else:
                            msg += f'<b>{trans(repeat_msg_0[1][sent][0], language)}</b> ' + trans(ads[username][counters[username]["glb_counter_ads"]][sent],
                                                                                            language) + '\n'
                    elif category == 1:
                        if sent == 2 or sent == 6:
                            msg += f'<b>{trans(repeat_msg_1[1][sent][0], language)}</b> ' + ads[username][counters[username]["glb_counter_ads"]][sent] + '\n'
                        else:
                            msg += f'<b>{trans(repeat_msg_1[1][sent][0], language)}</b> ' + trans(ads[username][counters[username]["glb_counter_ads"]][sent],
                                                                                            language) + '\n'

                ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')

        elif msg == 'tenant':
            update_table('user_category', 'l_or_r', 'tenant',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            if point == 'send':
                buttons = make_buttons(category, call.message.chat.username, call.message.chat.first_name, tenant[category][0], language)
                bot.send_message(call.message.chat.id, buttons[0], reply_markup=buttons[1])

            elif point == 'check':
                all_realty_ads = get_ads(category, 'landlord')
                ads.update({username: all_realty_ads})
                # print(ads)

                mass_buttons = [
                    [
                        types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                        types.InlineKeyboardButton(trans('Далее', language), callback_data='next')
                    ]
                ]

                photo4 = None
                if l_or_r == 'tenant':
                    if category == 0:
                        photo4 = open(f'{ads[username][counters[username]["glb_counter_ads"]][12]}', "rb")
                        mass = ads[username][counters[username]["glb_counter_ads"]][0:12]
                    elif category == 1:
                        photo4 = open(f'{ads[username][counters[username]["glb_counter_ads"]][7]}', "rb")
                        mass = ads[username][counters[username]["glb_counter_ads"]][0:5]
                else:
                    mass = ads[username][counters[username]["glb_counter_ads"]]
                msg = ''


                for sent in range(len(ads[username][counters[username]["glb_counter_ads"]]) - 1):
                    if category == 0:
                        if sent == 9 or sent == 11:
                            msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + str(ads[username][counters[username]["glb_counter_ads"]][sent]) + '\n'
                        else:
                            msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + trans(ads[username][counters[username]["glb_counter_ads"]][sent],
                                                                                            language) + '\n'
                    elif category == 1:
                        if sent == 1:
                            msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + ads[username][counters[username]["glb_counter_ads"]][sent] + '\n'
                        else:
                            msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + trans(ads[username][counters[username]["glb_counter_ads"]][sent],
                                                                                            language) + '\n'

                ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_photo(call.message.chat.id, photo4, caption=msg, reply_markup=ikb3, parse_mode='HTML')


        # //////////////////////////////// Choosing a button under check /////////////////////////////////////////////

        elif msg == 'access':
            back = types.InlineKeyboardMarkup()
            back.add(types.InlineKeyboardButton(trans('Главное меню', language) + '🔙', callback_data='back_menu1'))
            print(username, '\n', category, '\n', l_or_r, '\n', ad[username])
            add_ad(username, category, l_or_r, ad[username])
            bot.send_message(call.message.chat.id, trans('Ваше объявление добавлено!', language), reply_markup=back)
            if l_or_r == 'landlord':
                print(category, ad[username], username, language)
                ad_from_landlord(category, ad[username], username, language)
            elif l_or_r == 'tenant':
                ad_from_tenant(ad[username], category, username, language)
            counters[username]["glb_counter"] = 0
            ad.pop(f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')\

        elif msg == 'remake':
            ad[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'].clear()
            counters[username]["glb_counter"] = 0
            buttons = make_buttons(category, call.message.chat.username, call.message.chat.first_name, realty[category][0], language)
            bot.send_message(call.message.chat.id, buttons[0], reply_markup=buttons[1])

        # //////////////////////////////// next, order or back /////////////////////////////////////////////

        elif msg == 'next':

            counters[username]['glb_counter_ads'] += 1
            mass_buttons = [
                [
                    types.InlineKeyboardButton(trans('Назад', language), callback_data='back'),
                    types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                    types.InlineKeyboardButton(trans('Далее', language), callback_data='next')
                ]
            ]

            mass_buttons1 = [
                [
                    types.InlineKeyboardButton(trans('Назад', language), callback_data='back'),
                    types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),

                ]
            ]
            photo5 = None
            if l_or_r == 'tenant':
                if category == 0:
                    photo5 = open(f'{ads[username][counters[username]["glb_counter_ads"]][12]}', "rb")
                    mass = ads[username][counters[username]["glb_counter_ads"]][0:12]
                elif category == 1:
                    photo5 = open(f'{ads[username][counters[username]["glb_counter_ads"]][7]}', "rb")
                    mass = ads[username][counters[username]["glb_counter_ads"]][0:7]
            else:
                mass = ads[username][counters[username]["glb_counter_ads"]]

            msg = ''

            for sent in range(len(mass)):
                if category == 0:

                    if sent == 9 or sent == 11:
                        msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + ads[username][counters[username]["glb_counter_ads"]][sent] + '\n'
                    else:
                        msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + trans(ads[username][counters[username]["glb_counter_ads"]][sent],
                                                                                        language) + '\n'
                elif category == 1:
                    if sent == 1:
                        msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + ads[username][counters[username]["glb_counter_ads"]][sent] + '\n'
                    else:
                        msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + trans(ads[username][counters[username]["glb_counter_ads"]][sent],
                                                                                        language) + '\n'
            if l_or_r == 'tenant':
                if len(ads[username]) == counters[username]["glb_counter_ads"]:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons1)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, photo5, caption=msg, reply_markup=ikb3, parse_mode='HTML')
                else:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, photo5, caption=msg, reply_markup=ikb3, parse_mode='HTML')
            else:
                if len(ads[username]) == counters[username]["glb_counter_ads"]:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons1)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')
                else:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')

        elif msg == 'back':
            counters[username]["glb_counter_ads"] -= 1

            mass_buttons = [
                [
                    types.InlineKeyboardButton(trans('Назад', language), callback_data='back'),
                    types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--'),
                    types.InlineKeyboardButton(trans('Далее', language), callback_data='next')
                ]
            ]

            mass_buttons1 = [
                [
                    types.InlineKeyboardButton(trans('Далее', language), callback_data='next'),
                    types.InlineKeyboardButton(f'{counters[username]["glb_counter_ads"]}/{len(ads[username])}', callback_data='--')
                ],
            ]
            photo6 = None
            if l_or_r == 'tenant':
                if category == 0:
                    photo6 = open(f'{ads[username][counters[username]["glb_counter_ads"]][12]}', "rb")
                    mass = ads[username][counters[username]["glb_counter_ads"]][0:12]
                elif category == 1:
                    photo6 = open(f'{ads[username][counters[username]["glb_counter_ads"]][7]}', "rb")
                    mass = ads[username][counters[username]["glb_counter_ads"]][0:7]
            else:
                mass = ads[username][counters[username]["glb_counter_ads"]]

            msg = ''

            for sent in range(len(mass)):
                if category == 0:
                    if sent == 9 or sent == 11:
                        msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + ads[username][counters[username]["glb_counter_ads"]][sent] + '\n'
                    else:
                        msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + trans(ads[username][counters[username]["glb_counter_ads"]][sent],
                                                                                        language) + '\n'
                if category == 1:
                    if sent == 1:
                        msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + ads[username][counters[username]["glb_counter_ads"]][sent] + '\n'
                    else:
                        msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + trans(ads[username][counters[username]["glb_counter_ads"]][sent],
                                                                                        language) + '\n'
            if l_or_r == 'tenant':
                if counters[username]["glb_counter_ads"] == 1:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons1)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, photo6, caption=msg, reply_markup=ikb3, parse_mode='HTML')
                else:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_photo(call.message.chat.id, photo6, caption=msg, reply_markup=ikb3, parse_mode='HTML')
            else:
                if counters[username]["glb_counter_ads"] == 1:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons1)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')
                else:
                    ikb3 = types.InlineKeyboardMarkup(mass_buttons)
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                    bot.send_message(call.message.chat.id, msg, reply_markup=ikb3, parse_mode='HTML')

        elif msg == 'back_menu':

            if counters[username]['menu_counter'] == 1:

                counters[username]['menu_counter'] -= 1
                bot.delete_message(call.message.chat.id, call.message.message_id)
                buttons = category1(language)
                bot.send_message(call.message.chat.id, buttons[0], reply_markup=buttons[1])
            elif counters[username]['menu_counter'] == 2:

                counters[username]['menu_counter'] -= 1
                bot.delete_message(call.message.chat.id, call.message.message_id)
                ikb1 = types.InlineKeyboardMarkup()
                ikb1.add(types.InlineKeyboardButton(trans('Разместить объявление', language), callback_data='send_ad'))
                ikb1.add(types.InlineKeyboardButton(trans('Посмотреть объявления', language), callback_data='check_ad'))
                ikb1.add(types.InlineKeyboardButton(trans('Назад 🔙', language), callback_data='back_menu'))
                bot.send_message(call.message.chat.id, trans('Выберите пункт:', language), reply_markup=ikb1)

        elif msg == 'back_menu1':
            delete_elem('user_category',
                        f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            counters.pop(f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')

            buttons = category1(language)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, buttons[0], reply_markup=buttons[1])

        elif category == 'medicines':
            bot.send_message(call.message.chat.id, trans('Загружаем аналоги лекарст, подождите...', language))
            ikb_medicines = types.InlineKeyboardMarkup()
            for i in questions[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>']:
                if i == msg:
                    medicines_btn = main1(questions[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'][msg])
                    for med in medicines_btn:

                        ikb_medicines.add(types.InlineKeyboardButton(text=med[1], url=f'https://pillintrip.com{med[0]}'))
            ikb_medicines.add(types.InlineKeyboardButton(trans('Главное меню', language) + '🔙',
                                                         callback_data='back_menu1'))
            bot.send_message(call.message.chat.id, trans('Все доступные аналоги: ', language),
                             reply_markup=ikb_medicines)

        else:

            for i in questions[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>']:
                if i == msg:
                    ad[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'].append(questions[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'][i])
            questions[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'].clear()

            counters[username]['glb_counter'] += 1

            if category < 2:
                if l_or_r == 'landlord':
                    if len(ad[username]) == 1 and ad[username][0] == 'Мопед/Мотоцикл' or ad[username][0] == 'Moped/Motorcycle':
                        counters[username]['glb_counter'] += 1
                        ad[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'].append('Не соотвесвует')
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        bot.send_message(call.message.chat.id,
                                         trans(realty[category][counters[username]["glb_counter"]], language))
                    elif len(ad[username]) == 1 and ad[username][0] == 'Другой транспорт' or ad[username][0] == 'Other transport':
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        bot.send_message(call.message.chat.id, trans('Укажите тип ТС (велосипед, яхта, самолет и т.д.)', language))

                    elif type(realty[category][counters[username]["glb_counter"]]) == list:
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        buttons = make_buttons(category, call.message.chat.username, call.message.chat.first_name, realty[category][counters[username]['glb_counter']], language)
                        bot.send_message(call.message.chat.id, trans(buttons[0], language), reply_markup=buttons[1])

                    else:
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        bot.send_message(call.message.chat.id,
                                         trans(realty[category][counters[username]["glb_counter"]], language))
                elif l_or_r == 'tenant':
                    if len(ad[username]) == 1 and ad[username][0] == 'Мопед/Мотоцикл' or ad[username][0] == 'Moped/Motorcycle':
                        counters[username]['glb_counter'] += 1
                        ad[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'].append('Не соотвесвует')
                        pass_button = types.ReplyKeyboardMarkup(True, True)
                        pass_button.row("Не имеет значения")
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        bot.send_message(call.message.chat.id,
                                         trans(tenant[category][counters[username]["glb_counter"]], language),
                                         reply_markup=pass_button)
                    elif len(ad[username]) == 1 and ad[username][0] == 'Другой транспорт' or ad[username][0] == 'Other transport':
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        bot.send_message(call.message.chat.id, trans('Укажите тип ТС (велосипед, яхта, самолет и т.д.)', language))

                    elif len(ad[username]) == 2 and category == 1:
                        pass_button = types.ReplyKeyboardMarkup(True, True)
                        pass_button.row("Не имеет значения")
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        bot.send_message(call.message.chat.id,
                                         trans(tenant[category][counters[username]["glb_counter"]], language),
                                         reply_markup=pass_button)
                    elif type(tenant[category][counters[username]["glb_counter"]]) == list:
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        buttons = make_buttons(category, call.message.chat.username, call.message.chat.first_name, tenant[category][counters[username]['glb_counter']], language)
                        bot.send_message(call.message.chat.id, trans(buttons[0], language),
                                         reply_markup=buttons[1])
                    else:
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        bot.send_message(call.message.chat.id,
                                         trans(tenant[category][counters[username]["glb_counter"]], language))

            elif category == 2:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, trans(buy_sale[counters[username]["glb_counter"]], language))

            elif category == 2 and l_or_r == 'tenant':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, trans('Описание: ', language))


@bot.message_handler(commands=['start', 'help'])
def send_stat_msg(message):

    text = "Select a language"
    bot.send_message(message.chat.id, text, reply_markup=markup_lng, parse_mode='HTML')


@bot.message_handler(commands=['category'])
def send_stat_msg(message):

    ads[f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'].clear()
    counters.update({f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>':
                         {'glb_counter': 0, 'glb_counter_ads': 1, 'menu_counter': 0}})
    language = get_lng(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    delete_elem('user_category', f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    if f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>' in ad:
        ad.pop(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    if f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>' in questions:
        questions.pop(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')

    buttons = category1(language)
    bot.send_message(message.chat.id, buttons[0], reply_markup=buttons[1])


@bot.message_handler(commands=['admin'])
def admin(message):
    update_table('user_category', 'category', 'admin',
                 f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    usernames = get_usernames()
    if message.from_user.username in usernames:
        bot.send_message(message.chat.id, trans('Введите срок времени жизни поста: ', language))
    else:
        bot.send_message(message.chat.id, trans('У вас нет доступа', language))


@bot.message_handler(content_types=['text'])
def text_messages(message):
    global language
    global translator
    global glb_counter
    global ad

    msg = message.text

    language = get_lng(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    point = get('point', f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    category = get('category', f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    l_or_r = get('l_or_r', f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    username = get('username', f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    # //////////////////////////////// Choosing a language /////////////////////////////////////////////

    if msg == 'Русский 🇷🇺':

        add_lng(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>', 'ru')
        language = get_lng(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
        buttons = category1(language)
        bot.send_message(message.chat.id, 'Язык был успешно изменен')
        bot.send_message(message.chat.id, buttons[0], reply_markup=buttons[1])
    elif msg == 'English 🇺🇸':
        add_lng(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>', 'en')
        buttons = category1(language=get_lng(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'))
        bot.send_message(message.chat.id, 'The language has been successfully changed')
        bot.send_message(message.chat.id, buttons[0], reply_markup=buttons[1])

    elif message.from_user.username in get_usernames() and category == 'admin':
        pass

    elif category == 2 and l_or_r == 'tenant':
        ad[f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'].append(msg)
        message1 = f'{trans("Давайте проверим ваше объявление перед тем, как я его опубликую👇", language)}\n\n' \
                    f'{trans("Описание", language)}: {ad[username][1]}\n'

        ikb4 = types.InlineKeyboardMarkup()
        ikb4.add(types.InlineKeyboardButton(trans('Подтвердить', language), callback_data='access'))
        ikb4.add(types.InlineKeyboardButton(trans('Исправить', language), callback_data='remake'))
        bot.send_message(message.chat.id, message1, reply_markup=ikb4)

    elif category == 'medicines':
        bot.send_message(message.chat.id, trans('Необходимо немного подождать, препараты загружаются', language))
        mass_med = main(msg)

        buttons = make_buttons(category, message.from_user.username, message.from_user.first_name, mass_med, language)
        bot.send_message(message.chat.id, trans('Какой тип препарата вас интересует: ', language), reply_markup=buttons)

    elif category == 1 and l_or_r == 'landlord' and len(ad[username]) >= 5:
        # print(ad[username])
        counters[username]['glb_counter'] += 1
        ad[f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'].append(msg)
        send_questions(message, realty[category][counters[username]['glb_counter']],
                       language, questions, l_or_r)

    else:
        # print(ad[username])
        ad[f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'].append(msg)

        counters[username]['glb_counter'] += 1

        if category == 1:
            if l_or_r == 'landlord':
                send_questions(message, realty[category][counters[username]['glb_counter']],
                               language, questions, l_or_r)
            elif l_or_r == 'tenant':
                if len(ad[username]) == 6:
                    check_ad(message, ad[username], category, language)
                else:
                    if ad[username][0] == 'Другой транспорт' and len(ad[username]) == 2:
                        pass_button = types.ReplyKeyboardMarkup(True, True)
                        pass_button.row("Не имеет значения")
                        bot.send_message(message.from_user.id,
                                         trans(tenant[category][counters[username]["glb_counter"]], language),
                                         reply_markup=pass_button)
                    else:
                        send_questions(message, tenant[category][counters[username]['glb_counter']],
                                    language, questions, l_or_r)

        elif category == 0:
            if l_or_r == 'landlord':
                send_questions(message, realty[category][counters[username]['glb_counter']],
                               language, questions, l_or_r)
            elif l_or_r == 'tenant':
                if len(ad[username]) == 9 or len(ad[username]) == 7:
                    check_ad(message, ad[username], category, language)
                else:
                    send_questions(message, tenant[category][counters[username]['glb_counter']],
                                   language, questions, l_or_r)

        elif category == 2 and l_or_r == 'landlord':
            bot.send_message(message.chat.id, trans(buy_sale[counters[username]['glb_counter']], language))


@bot.message_handler(content_types=['photo'])
def get_broadcast_picture(message):
    global ad

    language = get_lng(f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    category = get('category',
                   f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')
    username = get('username',
                   f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>')

    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'static/photos/' + f'{message.photo[1].file_id}.jpg'
    ad[username].append(src)

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


    msg = trans('Давайте проверим ваше объявление перед тем, как я его опубликую👇', language)
    msg += '\n\n'

    if category < 2:
        if category == 1 and ad[username][0] == 'Другой транспорт':
            # print(repeat_msg_1, '\n', ad[username])
            msg = photo_check(ad[username], language)
        else:
            for sent in range(len(ad[username])-1):
                if category == 0:
                    msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + ad[username][sent] + '\n'
                elif category == 1:
                    msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + ad[username][sent] + '\n'
        ad[username].insert(0, message.from_user.id)
    elif category == 2:
        msg += f'{trans("Категория", language)}: {ad[username][0]}\n{trans("Описание", language)}: {ad[username][1]}\n'

    ikb4 = types.InlineKeyboardMarkup()
    ikb4.add(types.InlineKeyboardButton(trans('Подтвердить', language), callback_data='access'))
    ikb4.add(types.InlineKeyboardButton(trans('Исправить', language), callback_data='remake'))
    bot.reply_to(message, msg, parse_mode="HTML", reply_markup=ikb4)


while True:
    try:
        bot.infinity_polling(1000)
    except:
        pass