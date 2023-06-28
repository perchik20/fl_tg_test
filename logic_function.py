from telebot import types

from config import translator, bot
from questions import repeat_msg_0, repeat_msg_1


def trans(text, language):
    text_trns = translator.translate(text, src='ru', dest=language).text
    return text_trns


def make_buttons(name, name1, mass, questions, language):
    counter = 0
    questions.update({f'<a href="https://t.me/{name}">{name1}</a>': {}})

    text_trns = trans(mass[0], language)
    ikb_questions = types.InlineKeyboardMarkup()
    for i in mass[1]:
        questions[f'<a href="https://t.me/{name}">{name1}</a>'].update({f'key{counter}': trans(i, language)})
        ikb_questions.add(types.InlineKeyboardButton(trans(i, language), callback_data=f'key{counter}'))
        counter += 1

    return [text_trns, ikb_questions]


def send_questions(message, question, language, questions, l_or_r):
    if l_or_r == 'tenant':
        try:
            if type(question) == list:
                buttons = make_buttons(message.from_user.username,
                                       message.from_user.first_name, question, questions, language)
                bot.send_message(message.chat.id, trans(buttons[0], language), reply_markup=buttons[1])
            else:
                bot.send_message(message.chat.id, trans(question, language))
        except Exception as ex:
            print(ex)
    elif l_or_r == 'landlord':
        try:
            if type(question) == list:
                buttons = make_buttons(message.from_user.username, message.from_user.first_name,
                                       question, questions, language)
                bot.send_message(message.chat.id, trans(buttons[0], language), reply_markup=buttons[1])
            else:
                bot.send_message(message.chat.id,
                                 trans(question, language))
        except Exception as ex:
            print(ex)


def check_ad(message, ad, category, language):
    if ad[0] == 'Другой транспорт':
        repeat_msg = repeat_msg_1[2]
        ad_clone = ad
        msg = trans('Давайте проверим ваше объявление перед тем, как я его опубликую👇', language)
        msg += '\n\n'
        ad_clone.pop(0)
        for sent in range(len(ad)):
            msg += f'<b>{trans(repeat_msg[sent][0], language)}</b> ' + ad_clone[sent] + '\n'

        ikb4 = types.InlineKeyboardMarkup()
        ikb4.add(types.InlineKeyboardButton(trans('Подтвердить', language), callback_data='access'))
        ikb4.add(types.InlineKeyboardButton(trans('Исправить', language), callback_data='remake'))
        bot.send_message(message.chat.id, msg, parse_mode="HTML", reply_markup=ikb4)
    else:
        msg = trans('Давайте проверим ваше объявление перед тем, как я его опубликую👇', language)
        msg += '\n\n'

        for sent in range(len(ad)):
            if category == 0:
                msg += f'<b>{trans(repeat_msg_0[0][sent][0], language)}</b> ' + ad[sent] + '\n'
            elif category == 1:
                msg += f'<b>{trans(repeat_msg_1[0][sent][0], language)}</b> ' + ad[sent] + '\n'

        ikb4 = types.InlineKeyboardMarkup()
        ikb4.add(types.InlineKeyboardButton(trans('Подтвердить', language), callback_data='access'))
        ikb4.add(types.InlineKeyboardButton(trans('Исправить', language), callback_data='remake'))
        bot.send_message(message.chat.id, msg, parse_mode="HTML", reply_markup=ikb4)


def photo_check(ad, language):
    repeat_msg = repeat_msg_1[2]
    ad_clone = ad
    ad_clone.pop(0)

    print(repeat_msg, '\n', ad_clone)

    msg = trans('Давайте проверим ваше объявление перед тем, как я его опубликую👇', language)
    msg += '\n\n'

    for sent in range(len(ad_clone) - 1):
        msg += f'<b>{trans(repeat_msg[sent][0], language)}</b> ' + ad_clone[sent] + '\n'

    return msg

