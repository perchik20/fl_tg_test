from config import bot, translator
from questions import repeat_msg_0, repeat_msg_1
from telebot import types


def trans(text, language):
    text_trns = translator.translate(text, src='ru', dest=language).text
    return text_trns


def ad_from_landlord(category, ad, username, language):
    mass = ad
    photo4 = None
    if category == 0:
        photo4 = open(f'{mass[12]}', "rb")
        mass.pop(0)
        mass.pop(11)
        mass.append(username)
    elif category == 1 and len(ad) == 7:
        photo4 = open(f'{mass[6]}', "rb")
        mass.pop(0)
        mass.pop(5)
        mass.append(username)
    elif category == 1 and ad[1] == 'Мопед/Мотоцикл':
        photo4 = open(f'{mass[7]}', "rb")
        mass.pop(0)
        mass.pop(1)
        mass.pop(5)
        mass.append(username)
    elif category == 1:
        photo4 = open(f'{mass[7]}', "rb")
        mass.pop(0)
        mass.pop(6)
        mass.append(username)

    msg = '#сдам\n\n'

    link = types.InlineKeyboardMarkup()
    link .add(types.InlineKeyboardButton(text='Разместить/Найти объявление', url='https://t.me/HH_Buro_bot'))

    if category == 1 and len(ad) == 6:
        for sent in range(len(mass)):
            if sent == 5:
                msg += f'<b>{trans(repeat_msg_1[2][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
            else:
                msg += f'<b>{trans(repeat_msg_1[2][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
    else:
        for sent in range(len(mass)):
            if category == 0:
                if sent == 9 or sent == 11:
                    msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
                else:
                    msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
            elif category == 1:
                if sent == 1:
                    msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
                else:
                    msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + str(mass[sent]) + '\n'

    if category == 0:
        bot.send_photo(chat_id=-1001827743242, photo=photo4, caption=msg, parse_mode='HTML',
                       reply_markup=link,)
    elif category == 1:
        bot.send_photo(chat_id=-1001827743242, photo=photo4, caption=msg, parse_mode='HTML',
                       reply_markup=link, reply_to_message_id=362)


def ad_from_tenant(ad, category, username, language):
    link = types.InlineKeyboardMarkup()
    link.add(types.InlineKeyboardButton(text='Разместить/Найти объявление', url='https://t.me/HH_Buro_bot'))

    msg = '#Ищу\n\n'

    mass = ad
    mass.append(username)
    if category == 1 and len(ad) == 6:
        for sent in range(len(mass)):
            if sent == 5:
                msg += f'<b>{trans(repeat_msg_1[2][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
            else:
                msg += f'<b>{trans(repeat_msg_1[2][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
    elif category == 1 and ad[0] == 'Мопед/Мотоцикл':
        mass.pop(1)
        for sent in range(len(mass)):
            if sent == 5:
                msg += f'<b>{trans(repeat_msg_1[2][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
            else:
                msg += f'<b>{trans(repeat_msg_1[2][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
    else:
        for sent in range(len(mass)):
            if category == 0:
                if sent == 9:
                    msg += f'<b>{trans(repeat_msg_0[1][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
                else:
                    msg += f'<b>{trans(repeat_msg_0[1][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
            elif category == 1:
                if sent == 2 or sent == 6:
                    msg += f'<b>{trans(repeat_msg_1[1][sent][0], language)}</b> ' + str(mass[sent]) + '\n'
                else:
                    msg += f'<b>{trans(repeat_msg_1[1][sent][0], language)}</b> ' + str(mass[sent]) + '\n'

    if category == 0:
        bot.send_message(chat_id=-1001827743242, text=msg, parse_mode='HTML',
                         reply_markup=link,)
    elif category == 1:
        bot.send_message(chat_id=-1001827743242, text='.', parse_mode='HTML',
                         reply_markup=link, reply_to_message_id=362)