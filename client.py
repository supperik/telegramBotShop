import database as db
from telebot import types
import telebot
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
welcome_message = 'Телеграм бот для просмотра товаров <НАЗВАНИЕ>'
last_send_message = {}
goods_id = 0


def make_button(data, callback):
    return types.InlineKeyboardButton(data, callback_data=callback)


def main_menu(chat_id, output_data):
    global last_send_message
    try:
        bot.delete_message(chat_id=chat_id, message_id=last_send_message.message_id)
    except:
        pass
    markup = types.InlineKeyboardMarkup()
    markup.row(make_button('Смотреть товары', 'START_SEARCHING'), types.InlineKeyboardButton('Отзывы',
                                                                                             url='https://vk.com/topic-173930249_49415474'))
    markup.add(types.InlineKeyboardButton('Магазин ВКонтакте', url='https://vk.com/heartbreakeryo'))
    last_send_message = bot.send_message(text=output_data, chat_id=chat_id, reply_markup=markup)


def view_first_card(callback_data, message_id, chat_id):
    global goods_id, last_send_message
    goods_data_by_id = db.get_db_data(goods_id, callback_data)

    goods_id = goods_data_by_id[0]['id']
    markup = types.InlineKeyboardMarkup()
    markup.row(make_button('В главное меню', 'BACK_TO_MAIN_MENU'), make_button('Далее', 'NEXT_CARD'))
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    if goods_data_by_id[0]['id'] == goods_id:
        last_send_message = bot.send_photo(chat_id=chat_id,
                                           photo=goods_data_by_id[0]['PhotoURL'],
                                           caption=f"<b>{goods_data_by_id[0]['Name']}</b>\n"
                                                       f"<em>{str(goods_data_by_id[0]['Cost'])}</em>\n"
                                                       f"{goods_data_by_id[0]['Description']}",
                                           parse_mode='html',
                                           reply_markup=markup
                                           )
    else:
        main_menu(chat_id, 'Вы достигли конца списка товаров и были перенаправленны в главное меню')


def view_last_card(callback_data, message_id, chat_id):
    global goods_id, last_send_message
    goods_data_by_id = db.get_db_data(goods_id, callback_data)

    goods_id = goods_data_by_id[0]['id']
    markup = types.InlineKeyboardMarkup()
    markup.row(make_button('Назад', 'PREV_CARD'), make_button('В главное меню', 'BACK_TO_MAIN_MENU'))
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    try:
        if goods_data_by_id[0]['id'] == goods_id:
            last_send_message = bot.send_photo(chat_id=chat_id,
                                               photo=goods_data_by_id[0]['PhotoURL'],
                                               caption=f"<b>{goods_data_by_id[0]['Name']}</b>\n"
                                                       f"<em>{str(goods_data_by_id[0]['Cost'])}</em>\n"
                                                       f"{goods_data_by_id[0]['Description']}",
                                               parse_mode='html',
                                               reply_markup=markup
                                               )
        else:
            main_menu(chat_id, 'Вы достигли конца списка товаров и были перенаправленны в главное меню')
    except:
        pass


def view_card(callback_data, message_id, chat_id):
    global goods_id, last_send_message
    goods_data_by_id = db.get_db_data(goods_id, callback_data)

    goods_id = goods_data_by_id[0]['id']
    markup = types.InlineKeyboardMarkup()
    markup.row(make_button('Назад', 'PREV_CARD'), make_button('Далее', 'NEXT_CARD'))
    markup.add(make_button('В главное меню', 'BACK_TO_MAIN_MENU'))
    try:
        if (goods_data_by_id[0] != 'prev_ended') and (goods_data_by_id[0] != 'next_ended'):
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            last_send_message = bot.send_photo(chat_id=chat_id,
                                               photo=goods_data_by_id[0]['PhotoURL'],
                                               caption=f"<b>{goods_data_by_id[0]['Name']}</b>\n"
                                                       f"<em>{str(goods_data_by_id[0]['Cost'])}</em>\n"
                                                       f"{goods_data_by_id[0]['Description']}",
                                               parse_mode='html',
                                               reply_markup=markup
                                               )

        elif goods_data_by_id[0] == 'next_ended':
            main_menu(chat_id, 'Вы достигли конца списка товаров, поэтому были перенаправленны в главное меню')

        elif goods_data_by_id[0] == 'prev_ended':
            main_menu(chat_id, 'Вы достигли конца списка товаров, поэтому были перенаправленны в главное меню')
    except Exception as ex:
        pass


def start_bot(message):
    global last_send_message

    last_send_message = bot.send_message(chat_id=message.chat.id, text='Перенаправление в главное меню...')

    try:
        bot.delete_message(chat_id=last_send_message.chat.id, message_id=last_send_message.message_id)
        bot.delete_message(chat_id=last_send_message.chat.id, message_id=last_send_message.message_id - 1)
    except:
        pass

    markup = types.InlineKeyboardMarkup()
    markup.row(make_button('Ассортимент', 'START_SEARCHING'), types.InlineKeyboardButton('Отзывы',
                                                                                         url='https://vk.com/topic-173930249_49415474'))
    markup.add(types.InlineKeyboardButton('Магазин ВКонтакте', url='https://vk.com/heartbreakeryo'))
    last_send_message = bot.send_message(chat_id=last_send_message.chat.id, text=welcome_message, reply_markup=markup)
    try:
        bot.delete_message(chat_id=last_send_message.chat.id, message_id=message.message_id)
    except:
        pass


def next_start_callback(callback):
    global goods_id
    goods_id += 1
    if goods_id == 1:
        view_first_card(callback.data, callback.message.message_id, callback.message.chat.id)
    elif goods_id == db.get_max_id():
        view_last_card(callback.data, callback.message.message_id, callback.message.chat.id)
    else:
        view_card(callback.data, callback.message.message_id, callback.message.chat.id)


def prev_callback(callback):
    global goods_id
    goods_id -= 1
    if goods_id == 1:
        view_first_card(callback.data, callback.message.message_id, callback.message.chat.id)
    elif goods_id == db.get_max_id():
        view_last_card(callback.data, callback.message.message_id, callback.message.chat.id)
    else:
        view_card(callback.data, callback.message.message_id, callback.message.chat.id)


def main_menu_callback(callback):
    global goods_id
    goods_id = 0
    main_menu(callback.message.chat.id, 'Вы находитесь на главной странице магазина')