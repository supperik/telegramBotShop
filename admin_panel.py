import database as db
from telebot import types
import client
import telebot
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
last_send_message = {}
goods_id_by_enter = 0
edit_goods_id = 0


def check_password(check_password_message):
    try:
        bot.delete_message(chat_id=check_password_message.chat.id, message_id=check_password_message.message_id)
        bot.delete_message(chat_id=check_password_message.chat.id, message_id=check_password_message.message_id - 1)
    except:
        pass
    to_admin_panel(check_password_message.chat.id, 'Пароль введен верно!')


def to_admin_panel(chat_id, admin_panel_output_data):
    global last_send_message
    markup = types.InlineKeyboardMarkup()
    markup.row(client.make_button('Добавить карточку товара', 'ADMIN_ADD_CARD'),
               client.make_button('Изменить информацию товара', 'ADMIN_EDIT_CARD'))
    markup.add(client.make_button('В главное меню', 'BACK_TO_MAIN_MENU'))
    last_send_message = bot.send_message(text=f"<b>Вы находитесь в панели администратора</b>\n"
                                              f"<em>{admin_panel_output_data}</em>",
                                         chat_id=chat_id,
                                         reply_markup=markup,
                                         parse_mode='html')


def add_card_panel(callback, chat_id):
    global last_send_message
    try:
        bot.delete_message(message_id=last_send_message.message_id, chat_id=last_send_message.chat.id)
    except:
        pass
    last_message = bot.send_message(chat_id=chat_id, text='Впишите информацию о товаре в порядке: '
                                                          'Название,цена,ссылка на фотографию,описание\n'
                                                          '<b>Для отмены действия напишите Отмена</b>',
                                    parse_mode='html')

    @bot.message_handler(func=lambda m: m.message_id == last_send_message.message_id + 1)
    def add_card_to_db(new_card_info):
        print(new_card_info.text.split(','))
        if len(new_card_info.text.split(',')) == 4:
            insert_data = new_card_info.text.split(',')
            db.insert_db_data(callback, name=insert_data[0], cost=(int(insert_data[1])), photourl=insert_data[2],
                              description=insert_data[3])
            try:
                bot.delete_message(chat_id=chat_id, message_id=last_message.message_id)
                bot.delete_message(chat_id=chat_id, message_id=new_card_info.message_id)
            except:
                pass
            to_admin_panel(chat_id, 'Карточка товара добавлена!')
        elif new_card_info.text.lower() == 'отмена' or len(new_card_info.text.split(',')) != 4:
            to_admin_panel(chat_id, 'Действие отменено!')
            try:
                bot.delete_message(chat_id=chat_id, message_id=last_send_message.message_id - 2)
                bot.delete_message(chat_id=chat_id, message_id=last_send_message.message_id - 1)
            except:
                pass


def edit_card_panel(chat_id, edit_output_data):
    global last_send_message
    try:
        bot.delete_message(chat_id=chat_id, message_id=last_send_message.message_id)
    except:
        pass

    markup = types.InlineKeyboardMarkup()
    markup.row(client.make_button('Изменить фотографию', 'EDIT_PHOTOURL'), client.make_button('Изменить название товара',
                                                                                              'EDIT_NAME'))
    markup.row(client.make_button('Изменить стоимость товара', 'EDIT_COST'), client.make_button('Изменить описание товара',
                                                                                                'EDIT_DESCRIPTION'))
    markup.add(client.make_button('Назад', 'BACK_TO_ADMIN_PANEL'))

    last_send_message = bot.send_message(chat_id=chat_id, text=f"<b>Панель изменения карточек товаров</b>\n "
                                                               f"<em>{edit_output_data}</em>",
                                         reply_markup=markup,
                                         parse_mode='html')


def edit_card_in_db(edit_callback):

    try:
        bot.delete_message(chat_id=edit_callback.message.chat.id, message_id=edit_callback.message.message_id)
    except:
        pass


def get_edit_name(input_data, edit_callback):
    if (input_data.text.split(',')[0].lower() == 'отмена') or (len(input_data.text.split(',')) != 2):
        try:
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id)
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id - 1)
        except:
            pass
        edit_card_panel(chat_id=input_data.chat.id, edit_output_data='Действие отменено')
    else:
        try:
            data = input_data.text.split(',')
            db.insert_db_data(callback=edit_callback.data, goods_id=(int(data[0])), name=data[1])

            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id)
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id - 1)
        except:
            pass
        edit_card_panel(chat_id=input_data.chat.id, edit_output_data='Название изменено!')


def get_edit_photourl(input_data, edit_callback):
    if (input_data.text.split(',')[0].lower() == 'отмена') or (len(input_data.text.split(',')) != 2) or ('.jp' not in input_data.text.split(',')[1]):
        try:
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id)
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id - 1)
        except:
            pass
        edit_card_panel(chat_id=input_data.chat.id, edit_output_data='Действие отменено')
    else:
        try:
            data = input_data.text.split(',')
            db.insert_db_data(callback=edit_callback.data, goods_id=(int(data[0])), photourl=data[1])

            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id)
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id - 1)
        except:
            pass
        edit_card_panel(chat_id=input_data.chat.id, edit_output_data='Ссылка на фотографию изменена!')


def get_edit_cost(input_data, edit_callback):
    if (input_data.text.split(',')[0].lower() == 'отмена') or (len(input_data.text.split(',')) != 2) or (input_data.text.split(',')[0].isdigit()):
        try:
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id)
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id - 1)
        except:
            pass
        edit_card_panel(chat_id=input_data.chat.id, edit_output_data='Действие отменено')
    else:
        try:
            data = input_data.text.split(',')
            db.insert_db_data(callback=edit_callback.data, goods_id=(int(data[0])), cost=(int(data[1])))

            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id)
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id - 1)
        except:
            pass
        edit_card_panel(chat_id=input_data.chat.id, edit_output_data='Стоимость изменена!')


def get_edit_description(input_data, edit_callback):
    if (input_data.text.split(',')[0].lower() == 'отмена') or (len(input_data.text.split(',')) != 2):
        try:
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id)
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id - 1)
        except:
            pass
        edit_card_panel(chat_id=input_data.chat.id, edit_output_data='Действие отменено')
    else:
        try:
            data = input_data.text.split(',')
            db.insert_db_data(callback=edit_callback.data, goods_id=(int(data[0])), description=data[1])

            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id)
            bot.delete_message(chat_id=input_data.chat.id, message_id=input_data.message_id - 1)
        except:
            pass
        edit_card_panel(chat_id=input_data.chat.id, edit_output_data='Описание товара изменено!')
