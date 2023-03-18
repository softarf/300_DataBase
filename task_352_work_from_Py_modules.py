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


def find_by_phone(cursor, find_phone, customers_list=None):
    """Выборка по телефону."""
    phones_id_list = []
    select_query = """
            SELECT customer_id FROM phones
                WHERE phone_number = %s;
        """
    query_items = (find_phone, )
    if customers_list is not None and customers_list:
        select_query = (select_query[: select_query.rindex(';')]
                        + """ AND customer_id = %s;""")
        for found_id in customers_list[:]:
            cursor.execute(select_query, query_items + (found_id, ))
            res = cursor.fetchone()
            if res is not None:
                phones_id_list.append(res[0])
    else:
        cursor.execute(select_query, query_items)
        res = cursor.fetchone()
        if res is not None:
            phones_id_list.append(res[0])

    found_id_list = phones_id_list[:]
    return found_id_list


def find_by_value(cursor, attribute_name, find_value, records_ids_list=None):
    """Выборка по одному атрибуту."""
    find_list = []
    select_query = """
            SELECT customer_id FROM customers
                WHERE {select_attribute} = %s;
            """
    query_item = (find_value, )
    if records_ids_list is not None and records_ids_list:
        select_query = (select_query[: select_query.rindex(';')]
                        + """ AND customer_id = %s;""")
        stmt = sql.SQL(select_query
                       ).format(select_attribute=sql.Identifier(attribute_name))
        for record_id in records_ids_list[:]:
            cursor.execute(stmt, query_item + (record_id, ))
            res = cursor.fetchone()
            if res is not None:
                find_list.append(res[0])
    else:
        stmt = sql.SQL(select_query
                       ).format(select_attribute=sql.Identifier(attribute_name))
        cursor.execute(stmt, query_item)
        res = cursor.fetchone()
        if res is not None:
            find_list.append(res[0])
    found_ids_list = find_list[:]
    return found_ids_list


def find_client(cursor, first_name=None, last_name=None, email=None, phone=None):
    """ 7. Находит клиента по его данным: имени, фамилии, email или телефону."""
    found_ids_list = []
    if first_name is not None:
        found_ids_list = find_by_value(cursor, 'first_name', first_name)
        if found_ids_list and last_name is not None:
                found_ids_list = find_by_value(cursor, 'last_name', last_name, found_ids_list)
                if found_ids_list and email is not None:
                    found_ids_list = find_by_value(cursor, 'email', email, found_ids_list)
    else:
        if last_name is not None:
            found_ids_list = find_by_value(cursor, 'last_name', last_name)
            if found_ids_list and email is not None:
                found_ids_list = find_by_value(cursor, 'email', email, found_ids_list)
        else:
            if email is not None:
                found_ids_list = find_by_value(cursor, 'email', email)

    if (first_name is None and last_name is None and email is None) or found_ids_list:
        if phone is not None:
            found_ids_list = find_by_phone(cursor, phone, found_ids_list)

    if len(found_ids_list) == 0:
        print("   Такого человека в Базе нет.")
    elif len(found_ids_list) > 1:
        print("   Слишком много совпадений. Уточните параметры поиска.")
    return found_ids_list, len(found_ids_list) if found_ids_list else ([0], 0)
