import pymysql
import pymysql.cursors
from config import db_host, db_user, db_name, db_password
global connection


def initialize_db():
    try:
        global connection
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            '''create_table_query = "CREATE TABLE `Goods`(id int AUTO_INCREMENT, " \
                                     "Cost DECIMAL(8, 2), " \
                                     "Name varchar(32), " \
                                     "PhotoURL TEXT, " \
                                     "Description TEXT, " \
                                     "PRIMARY KEY (id));"
                                     
                                     "ALTER TABLE `Goods` CONVERT TO CHARACTER SET utf8;"
                                     
                                     "CREATE TABLE `Users`(id int AUTO_INCREMENT, "
                                     "Access varchar(32), "
                                     "Name TEXT, "
                                     "Cart TEXT, "
                                     "PRIMARY KEY (id));"
                                     
                                     "ALTER TABLE `Users` CONVERT TO CHARACTER SET utf8;"
                                     
            cursor.execute(create_table_query)
            print('Table created successfully!')'''
    except:
        pass


def get_min_id():
    with connection.cursor() as cursor:
        select_query = "SELECT * FROM `Goods` WHERE id = 1"
        cursor.execute(select_query)
        min_elem = cursor.fetchall()[0]['id']
        return min_elem


def get_max_id():
    with connection.cursor() as cursor:
        select_query = "SELECT * FROM `Goods` ORDER BY id DESC LIMIT 1"
        cursor.execute(select_query)
        return cursor.fetchall()[0]['id']


def insert_db_data(callback, goods_id=None, name=None, cost=None, photourl=None, description=None):
    print(callback)
    if callback == 'ADMIN_ADD_CARD':
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `Goods` (Name, Cost, PhotoURL, Description) " \
                           "VALUES('%s', '%s', '%s', '%s')" % (name, cost, photourl, description)
            cursor.execute(insert_query)
            connection.commit()
            print('ADD_SUCCESS!')

    if callback == 'EDIT_COST':
        with connection.cursor() as cursor:
            update_query = "UPDATE `Goods` SET cost = '%s' WHERE id = '%s'" % (cost, goods_id)
            cursor.execute(update_query)
            connection.commit()
            print('EDIT_COST_SUCCESS!')

    if callback == 'EDIT_NAME':
        with connection.cursor() as cursor:
            print(name, goods_id)
            update_query = "UPDATE `Goods` SET name = '%s' WHERE id = '%s'" % (name, goods_id)
            cursor.execute(update_query)
            connection.commit()
            print('EDIT_NAME_SUCCESS!')

    if callback == 'EDIT_PHOTOURL':
        with connection.cursor() as cursor:
            update_query = "UPDATE `Goods` SET PhotoURL = '%s' WHERE id = '%s'" % (photourl, goods_id)
            cursor.execute(update_query)
            connection.commit()
            print('EDIT_PHOTOURL_SUCCESS!')

    if callback == 'EDIT_DESCRIPTION':
        with connection.cursor() as cursor:
            update_query = "UPDATE `Goods` SET Description = '%s' WHERE id = '%s'" % (description, goods_id)
            cursor.execute(update_query)
            connection.commit()
            print('EDIT_DESCRIPTION_SUCCESS!')


def get_db_data(goods_id, callback_data):
    with connection.cursor() as cursor:

        if callback_data == 'START_SEARCHING':
            select_query = "SELECT * FROM `Goods` WHERE id = %s" % 1
            cursor.execute(select_query)
            rows = []
            for row in cursor.fetchall():
                rows.append(row)
            if rows is not None:
                return rows

        if (callback_data == 'NEXT_CARD') and (1 <= goods_id <= get_max_id()):
            while (cursor.execute("SELECT * FROM `Goods` WHERE id = %s" % goods_id)) == 0:
                goods_id += 1
            select_query = "SELECT * FROM `Goods` WHERE id = %s" % goods_id
            cursor.execute(select_query)
            rows = cursor.fetchall()
            if rows is not None:
                return rows

        if callback_data == 'NEXT_CARD' and goods_id > get_max_id():
            rows = ['next_ended']
            return rows

        if (callback_data == 'PREV_CARD') and (1 <= goods_id <= get_max_id()):
            while cursor.execute("SELECT * FROM `Goods` WHERE id = %s" % goods_id) == 0:
                goods_id -= 1
            select_query = "SELECT * FROM `Goods` WHERE id = %s" % goods_id
            cursor.execute(select_query)
            rows = cursor.fetchall()
            if rows is not None:
                return rows

        if callback_data == 'PREV_CARD' and goods_id < 1:
            rows = ['prev_ended']
            return rows


initialize_db()
