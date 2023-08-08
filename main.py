import telebot
from config import TOKEN, ADMIN_PASSWORD
import client
import admin_panel

edit_input_data = []
last_send_message = {}
goods_id_by_enter = 0
edit_goods_id = 0
edit_callback_data = {}

bot = telebot.TeleBot(TOKEN)

# ---------------------------------------CLIENT-------------------------------------------------------------------------


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda m: m.text.lower() in ['запуск', 'запустить', 'начать', 'старт', 'пуск'])
def start_bot(message):
    client.start_bot(message)


@bot.callback_query_handler(func=lambda callback: callback.data in ['START_SEARCHING', 'NEXT_CARD', 'PREV_CARD',
                                                                    'BACK_TO_MAIN_MENU'])
def get_callback(callback):
    if callback.data == 'NEXT_CARD' or callback.data == 'START_SEARCHING':
        client.next_start_callback(callback)

    elif callback.data == 'PREV_CARD':
        client.prev_callback(callback)

    elif callback.data == 'BACK_TO_MAIN_MENU':
        try:
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        except:
            pass
        client.main_menu_callback(callback)


# ---------------------------------------/CLIENT------------------------------------------------------------------------


# ---------------------------------------ADMIN--------------------------------------------------------------------------


@bot.message_handler(func=lambda m: m.text == ADMIN_PASSWORD)
def check_password(message):
    admin_panel.check_password(message)


@bot.callback_query_handler(func=lambda admin_callback: admin_callback.data in ['ADMIN_ADD_CARD', 'ADMIN_EDIT_CARD',
                                                                                'BACK_TO_ADMIN_PANEL'])
def get_admin_callback(admin_callback):
    if admin_callback.data == 'ADMIN_ADD_CARD':
        admin_panel.add_card_panel(admin_callback.data, admin_callback.message.chat.id)

    if admin_callback.data == 'ADMIN_EDIT_CARD':
        admin_panel.edit_card_panel(chat_id=admin_callback.message.chat.id, edit_output_data='')

    if admin_callback.data == 'BACK_TO_ADMIN_PANEL':
        try:
            bot.delete_message(chat_id=admin_callback.message.chat.id, message_id=admin_callback.message.message_id)
        except:
            pass
        admin_panel.to_admin_panel(chat_id=admin_callback.message.chat.id,
                                   admin_panel_output_data='Вы были возвращены в панель администратора')


@bot.callback_query_handler(func=lambda edit_callback: edit_callback.data in ['EDIT_PHOTOURL', 'EDIT_NAME',
                                                                              'EDIT_COST', 'EDIT_DESCRIPTION'])
def edit_card_in_db(edit_callback):
    goods_id = admin_panel.edit_card_in_db(edit_callback)

    if edit_callback.data == 'EDIT_NAME':
        last_send_message = bot.send_message(chat_id=edit_callback.message.chat.id,
                                             text='Введите номер товара и новое название через запятую без пробелов:')

        @bot.message_handler(func=lambda m: m.message_id == last_send_message.message_id + 1)
        def get_edit_name(input_data):
            admin_panel.get_edit_name(input_data, edit_callback)

    if edit_callback.data == 'EDIT_PHOTOURL':
        last_send_message = bot.send_message(chat_id=edit_callback.message.chat.id,
                                             text='Введите номер товара и новую ссылку к фотографии через запятую без пробелов:')

        @bot.message_handler(func=lambda m: m.message_id == last_send_message.message_id + 1)
        def get_edit_photourl(input_data):
            admin_panel.get_edit_photourl(input_data, edit_callback)

    if edit_callback.data == 'EDIT_COST':
        last_send_message = bot.send_message(chat_id=edit_callback.message.chat.id,
                                             text='Введите номер товара и новую стоимость товара через запятую без пробелов:')

        @bot.message_handler(func=lambda m: m.message_id == last_send_message.message_id + 1)
        def get_edit_cost(input_data):
            admin_panel.get_edit_cost(input_data, edit_callback)

    if edit_callback.data == 'EDIT_DESCRIPTION':
        last_send_message = bot.send_message(chat_id=edit_callback.message.chat.id,
                                             text='Введите номер товара и новое описание товара через запятую без пробелов:')

        @bot.message_handler(func=lambda m: m.message_id == last_send_message.message_id + 1)
        def get_edit_description(input_data):
            admin_panel.get_edit_description(input_data, edit_callback)


# ---------------------------------------/ADMIN-------------------------------------------------------------------------

bot.polling(none_stop=True)
