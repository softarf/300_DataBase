# -*- coding: utf-8 -*-
#                       Работа с PostgreSQL из Python.

#       Задача 1. Создайте программу для управления клиентами на Python.
#                 Требуется хранить персональную информацию: имя, фамилия, email и телефон.

#                 Модуль с функциями. ("Каркас кода прилагается")

import psycopg2
from psycopg2 import sql


def create_tables(conn,cursor):
    """1. Создаёт таблицы в БД."""

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id SERIAL PRIMARY KEY,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30),
            email VARCHAR(60));
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phones (
            phone_id SERIAL PRIMARY KEY,
            phone_number VARCHAR(30) UNIQUE,
            customer_id INTEGER REFERENCES customers);
    """)
    conn.commit()


def add_client(cursor, first_name, last_name=None, email=None):
    """2. Добавляет нового клиента."""
    cursor.execute("""
        INSERT INTO customers (first_name, last_name, email)
            VALUES(%s, %s, %s) RETURNING customer_id ;
    """, (first_name, last_name, email))
    customer_id = cursor.fetchone()[0]
    return customer_id


def add_phone(cursor, client_id, phone):
    """3. Добавляет телефон для существующего клиента."""
    cursor.execute("""
        INSERT INTO phones (phone_number, customer_id)
            VALUES(%s, %s) RETURNING phone_id;
    """, (phone, client_id))
    phone_id = cursor.fetchone()[0]
    return phone_id


def change_client(cursor, client_id, first_name=None, last_name=None, email=None):
    """4. Меняет данные о клиенте.."""
    if first_name is not None:
        stmt = sql.SQL("""
            UPDATE customers SET {attr} = %s
            WHERE customer_id = %s;
        """).format(attr=sql.Identifier('first_name'), )
        cursor.execute(stmt, (first_name, client_id))
    if last_name is not None:
        stmt = sql.SQL("""
            UPDATE customers SET {attr} = %s
            WHERE customer_id = %s;
        """).format(attr=sql.Identifier('last_name'), )
        cursor.execute(stmt, (last_name, client_id))
    if email is not None:
        stmt = sql.SQL("""
            UPDATE customers SET {attr} = %s
            WHERE customer_id = %s;
        """).format(attr=sql.Identifier('email'), )
        cursor.execute(stmt, (email, client_id))


def delete_phone(cursor, customer_id, phone):
    """5. Удаляет телефон у существующего клиента."""
    cursor.execute("""
        DELETE FROM phones
        WHERE phone_number = %s AND customer_id = %s RETURNING phone_id;
    """, (phone, customer_id))
    phone_id = cursor.fetchone()[0]
    return phone_id


def delete_client(cursor, customer_id):
    """6. Удаляет существующего клиента."""
    pass
    cursor.execute("""
        SELECT phone_id FROM phones
        WHERE customer_id = %s;
    """, (customer_id, ))
    find_list = [item[0] for item in cursor.fetchall()]
    for item in find_list:
        cursor.execute("""
            DELETE FROM phones
            WHERE phone_id = %s RETURNING phone_id;
        """, (item, ))
    cursor.execute("""
        DELETE FROM customers
        WHERE customer_id = %s RETURNING customer_id;
    """, (customer_id, ))
    customer_id = cursor.fetchone()[0]
    return customer_id


def find_first_select(cursor, attribute_name, find_value):
    """Предварительная выборка."""
    stmt = sql.SQL("""
        SELECT customer_id FROM customers
        WHERE {attr} = %s;
    """).format(attr=sql.Identifier(attribute_name), )
    cursor.execute(stmt, (find_value, ))
    find_list = [item[0] for item in cursor.fetchall()]
    return find_list


def find_next_select(cursor, find_values, customers_ids_list):
    """Последующая выборка."""
    find_list = []
    for item in find_values:
        find_list = []
        for cus_id in customers_ids_list[:]:
            stmt = sql.SQL("""
                SELECT customer_id FROM customers
                WHERE {attribute_name} = %s AND customer_id = %s;
            """).format(attribute_name=sql.Identifier(item[0]), )
            cursor.execute(stmt, (item[1], cus_id))
            res = cursor.fetchone()
            if res is not None:
                find_list.append(res[0])
        customers_ids_list = find_list[:]
    return find_list


def find_phone_select(cursor, find_phone):
    """Выборка по телефону."""
    customer_id = []
    cursor.execute("""
        SELECT customer_id FROM phones
            WHERE phone_number = %s;
    """, (find_phone, ))
    customer_id = [item[0] for item in cursor.fetchall()]
    return customer_id


def find_client(cursor, first_name=None, last_name=None, email=None, phone=None):
    """ 7. Находит клиента по его данным: имени, фамилии, email или телефону."""
    item_found_list = []
    first_parameter = ''
    next_parameter = []
    if first_name is not None:
        first_parameter = first_name
    if first_parameter != '':
        item_found_list = find_first_select(cursor, 'first_name', first_parameter)
        if item_found_list:
            if last_name is not None:
                next_parameter.append(('last_name', last_name))
            if email is not None:
                next_parameter.append(('email', email))
            if next_parameter:
                item_found_list = find_next_select(cursor, next_parameter, item_found_list)
    else:
        if last_name is not None:
            first_parameter = last_name
        if first_parameter != '':
            item_found_list = find_first_select(cursor, 'last_name', first_parameter)
            if item_found_list:
                if email is not None:
                    next_parameter.append(email)
                if next_parameter:
                    item_found_list = find_next_select(cursor, next_parameter, item_found_list)
        else:
            if email is not None:
                first_parameter = email
            if first_parameter != '':
                item_found_list = find_first_select(cursor, 'email', first_parameter)

    if (first_name is None and last_name is None and email is None) or item_found_list:
        if phone is not None:
            item_found_list = find_phone_select(cursor, phone)

    if len(item_found_list) == 0:
        print("   Такого человека в Базе нет.")
    elif len(item_found_list) > 1:
        print("   Слишком много совпадений. Уточните параметры поиска.")
    return item_found_list, len(item_found_list)
