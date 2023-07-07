from config import bot, translator
from questions import repeat_msg_0, repeat_msg_1
from telebot import types


def trans(text, language):
    text_trns = translator.translate(text, src='ru', dest=language).text
    return text_trns


def ad_from_landlord(category, ad, username, language):
    mass = ad
    photo4 = None
    print(f'mass->{mass}')
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
    print(mass)
    msg = '#сдам\n\n'

    if category == 1:
        link = types.InlineKeyboardMarkup()
        link .add(types.InlineKeyboardButton(text='Разместить/Найти объявление', url='https://facebook.com'))
    elif category == 0:
        link = types.InlineKeyboardMarkup()
        link.add(types.InlineKeyboardButton(text='Разместить/Найти объявление', url='https://facebook.com'))

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


    bot.send_photo(chat_id=-1001901862304, photo=photo4, caption=msg, parse_mode='HTML')


def ad_from_tenant(ad, category, username, language):
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
    
    bot.send_message(chat_id=-1001901862304, text=msg, parse_mode='HTML')