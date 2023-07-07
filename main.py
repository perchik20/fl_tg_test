from telebot import types
import datetime as DT

from config import bot, translator
from logic_function import send_questions, check_ad, photo_check, send_ad, send_ad_first_landlord, send_ad_first_tenant

from questions import realty, tenant, buy_sale, repeat_msg_1, repeat_msg_0
from work_with_data import add_ad, get_ads, get_usernames, update_table, ad_time_data, get, get_lng, add_lng, \
    delete_elem, get_ads_by_filter
from send_to_chanell import ad_from_landlord, ad_from_tenant
from parser import main, main1

# //////////////////////////////perem///////////////////////////////////////

categorys = ['Недвижимости', 'ТС']
ad = {}
questions = {}
ads = {}
counters = {}
filters = {}

# /////////////////////////////////////functions//////////////////////////////


def trans(text, language):
    text_trns = translator.translate(text, src='ru', dest=language).text
    return text_trns


def category1(language):
    ikb = types.InlineKeyboardMarkup()
    # ikb.add(types.InlineKeyboardButton(trans('Недвижимость', language), callback_data='realty'))
    ikb.add(types.InlineKeyboardButton(trans('Транспорт', language), callback_data='transport'))
    # ikb.add(types.InlineKeyboardButton(trans('Куплю/Продам', language), callback_data='buy_sale'))
    # ikb.add(types.InlineKeyboardButton(trans('Медицина', language), callback_data='medicines'))
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
                ikb2.add(types.InlineKeyboardButton(trans(f'Предложения аренды {categorys[category]}', language), callback_data='landlord'))
                ikb2.add(types.InlineKeyboardButton(trans(f'Спрос на аренду {categorys[category]}', language), callback_data='tenant'))
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
                ikb2.add(types.InlineKeyboardButton(trans(f'Предложения аренды {categorys[category]}', language), callback_data='landlord'))
                ikb2.add(types.InlineKeyboardButton(trans(f'Спрос на аренду {categorys[category]}', language), callback_data='tenant'))
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
                l_or_r = get('l_or_r',
                             f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
                all_realty_ads = get_ads(category, 'tenant')
                ads.update({username: all_realty_ads})

                if category == 0:
                    for i in ads[username]:
                        i.pop(9)
                        i.pop(9)
                        i.pop(10)

                elif category == 1:
                    for i in ads[username]:
                        i.pop(7)
                        i.pop(7)

                send_ad_first_landlord(call, l_or_r, category, ads[username], language)

        elif msg == 'tenant':
            update_table('user_category', 'l_or_r', 'tenant',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            if point == 'send':
                buttons = make_buttons(category, call.message.chat.username, call.message.chat.first_name, tenant[category][0], language)
                bot.send_message(call.message.chat.id, buttons[0], reply_markup=buttons[1])

            elif point == 'check':
                if category == 1:
                    check_ad = types.InlineKeyboardMarkup()
                    check_ad.add(types.InlineKeyboardButton(trans('Авто', language),
                                                            callback_data='Авто'))
                    check_ad.add(types.InlineKeyboardButton(trans('Мопед/Мотоцикл', language),
                                                            callback_data='Мопед/Мотоцикл'))
                    check_ad.add(types.InlineKeyboardButton(trans('Другой транспорт', language),
                                                            callback_data='Другой транспорт'))
                    check_ad.add(types.InlineKeyboardButton(trans('Посмотреть все объявления', language),
                                                            callback_data='check_all'))

                    bot.send_message(call.message.chat.id, trans('Выберите пункт ниже:', language),
                                     reply_markup=check_ad)
                elif category == 0:
                    check_ad = types.InlineKeyboardMarkup()
                    check_ad.add(types.InlineKeyboardButton(trans('Кондо', language),
                                                            callback_data='Кондо'))
                    check_ad.add(types.InlineKeyboardButton(trans('Вилла', language),
                                                            callback_data='Вилла'))
                    check_ad.add(types.InlineKeyboardButton(trans('Посмотреть все объявления', language),
                                                            callback_data='check_all'))

                    bot.send_message(call.message.chat.id, trans('Выберите пункт ниже:', language),
                                     reply_markup=check_ad)

        elif msg == 'Авто' or msg == 'Мопед/Мотоцикл' or msg == 'Другой транспорт':
            filters.update({username: []})
            filters[username].append(msg)
            if filters[username][0] == 'Авто':
                check_ad = types.InlineKeyboardMarkup()
                check_ad.add(types.InlineKeyboardButton(trans('Легковой', language),
                                                        callback_data='Легковой'))
                check_ad.add(types.InlineKeyboardButton(trans('Внедорожник', language),
                                                        callback_data='Внедорожник'))
                check_ad.add(types.InlineKeyboardButton(trans('Минивэн (5 и более пассажирских мест)', language),
                                                        callback_data='Минивэн'))
                check_ad.add(types.InlineKeyboardButton(trans('Посмотреть все объявления', language),
                                                        callback_data='check_all'))

                bot.send_message(call.message.chat.id, trans('Выберите пункт ниже:', language), reply_markup=check_ad)

            elif filters[username][0] == 'Мопед/Мотоцикл' or filters[username][0] == 'Другой транспорт':
                l_or_r = get('l_or_r',
                             f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')

                all_realty_ads = get_ads_by_filter(category, 'landlord', filters[username][0])
                ads.update({username: all_realty_ads})

                send_ad_first_tenant(call, l_or_r, category, ads[username], language)
        elif msg == 'Вилла' or msg == 'Кондо':
            l_or_r = get('l_or_r',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            all_realty_ads = get_ads_by_filter(category, 'landlord', msg)
            ads.update({username: all_realty_ads})

            send_ad_first_tenant(call, l_or_r, category, ads[username], language)

        elif msg == 'Легковой' or msg == 'Внедорожник' or msg == 'Минивэн':
            filters[username].append(msg)
            l_or_r = get('l_or_r',
                         f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
            all_realty_ads = get_ads_by_filter(category, 'landlord', filters[username])
            ads.update({username: all_realty_ads})

            send_ad_first_tenant(call, l_or_r, category, ads[username], language)

        elif msg == 'check_all':
            if l_or_r == 'tenant':
                l_or_r = get('l_or_r', f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
                all_realty_ads = get_ads(category, 'landlord')
                ads.update({username: all_realty_ads})

                send_ad_first_tenant(call, l_or_r, category, ads[username], language)
            elif l_or_r == 'landlord':
                l_or_r = get('l_or_r',
                             f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>')
                all_realty_ads = get_ads(category, 'tenant')
                ads.update({username: all_realty_ads})

                send_ad_first_landlord(call, l_or_r, category, ads[username], language)

        # //////////////////////////////// Choosing a button under check /////////////////////////////////////////////

        elif msg == 'access':
            back = types.InlineKeyboardMarkup()
            back.add(types.InlineKeyboardButton(trans('Главное меню', language) + '🔙', callback_data='back_menu1'))
            current_date = DT.datetime.now().date() + DT.timedelta(days=30)
            add_ad(username, category, l_or_r, ad[username], current_date)
            bot.send_message(call.message.chat.id, trans('Ваше объявление добавлено!', language), reply_markup=back)
            if l_or_r == 'landlord':
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
            # filters.pop(username)
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

        elif msg == 'Yes':
            if category == 1:
                check_ad = types.InlineKeyboardMarkup()
                check_ad.add(types.InlineKeyboardButton(trans('Авто', language),
                                                        callback_data='Авто'))
                check_ad.add(types.InlineKeyboardButton(trans('Мопед/Мотоцикл', language),
                                                        callback_data='Мопед/Мотоцикл'))
                check_ad.add(types.InlineKeyboardButton(trans('Другой транспорт', language),
                                                        callback_data='Другой транспорт'))
                check_ad.add(types.InlineKeyboardButton(trans('Посмотреть все объявления', language),
                                                        callback_data='check_all'))

                bot.send_message(call.message.chat.id, trans('Выберите пункт ниже:', language),
                                 reply_markup=check_ad)
            elif category == 0:
                check_ad = types.InlineKeyboardMarkup()
                check_ad.add(types.InlineKeyboardButton(trans('Кондо', language),
                                                        callback_data='Кондо'))
                check_ad.add(types.InlineKeyboardButton(trans('Вилла', language),
                                                        callback_data='Вилла'))
                check_ad.add(types.InlineKeyboardButton(trans('Посмотреть все объявления', language),
                                                        callback_data='check_all'))

                bot.send_message(call.message.chat.id, trans('Выберите пункт ниже:', language),
                                 reply_markup=check_ad)

        elif msg == 'No':
            ads[username].clear()
            counters.update({username: {'glb_counter': 0, 'glb_counter_ads': 1, 'menu_counter': 0}})
            language = get_lng(username)
            delete_elem('user_category', username)
            if username in ad:
                ad.pop(username)
            if username in questions:
                questions.pop(username)

            buttons = category1(language)
            bot.send_message(call.message.chat.id, buttons[0], reply_markup=buttons[1])

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
                        ad[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'].append('Не соотвествует')
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
                        ad[f'<a href="https://t.me/{call.message.chat.username}">{call.message.chat.first_name}</a>'].append('Не соотвествует')
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


@bot.message_handler(commands=['id'])
def admin(message):
    print(message)


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

        counters[username]['glb_counter'] += 1
        ad[f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'].append(msg)
        send_questions(message, realty[category][counters[username]['glb_counter']],
                       language, questions, l_or_r)

    else:

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
                    elif len(ad[username]) == 3:
                        bot.send_message(message.chat.id, '_', reply_markup=types.ReplyKeyboardRemove())
                        send_questions(message,  trans(tenant[category][counters[username]['glb_counter']], language),
                                       language, questions, l_or_r)
                    else:
                        send_questions(message,  trans(tenant[category][counters[username]['glb_counter']], language),
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