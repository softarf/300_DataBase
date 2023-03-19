# -*- coding: utf-8 -*-
#                       Работа с PostgreSQL из Python.

#       Задача 1. Создайте программу для управления клиентами на Python.
#                 Требуется хранить персональную информацию: имя, фамилия, email и телефон.

#                 Управляющий модуль.                (Каркас кода прилагается.)

from task_352_work_from_Py_modules import *


def working_from_Python() -> str:
    """Работает с PostgreSQL из Python."""
    print('\n    В этой программе...')
    with psycopg2.connect(database="clients_db", user="postgres", password="postgres", ) as conn:
        with conn.cursor() as cur:

            # На этапе проектирования - Удаляем старые таблицы.
            # cur.execute("""
            # DROP TABLE homework;
            # DROP TABLE course;
            # """)

            table_name = 'customers'
            print("\n1. Создаём таблицы '", table_name, "' и '", 'phones', "'.", sep='')
            create_tables(conn, cur)

            print("\n2. Заполняем их данными.")
            clients_data = [['Алиса', 'Семёнова', 'alisa@mail.ru'],
                            ['Василий', 'Адушкин', 'vas@mail.ru'],
                            ['Оксана', 'Шукшина', 'oksana@mail.ru'],
                            ['Пётр', 'Харламов', 'peter@mail.ru']]
            phones_data = [['002', '005', '007'],
                           ['003'],
                           [],
                           ['004', '006']]
            for items,phones  in zip(clients_data, phones_data):
                customer_id = add_client(cur, *items)
                for phone in phones:
                    add_phone(cur, customer_id, phone)

            print("\n3. Находим id Василия, в данном случае - по имени.")
            found_result = find_client(cur, first_name='Василий')
            if found_result[1] == 1:
                vas_id = found_result[0][0]
                print("Id Василия:", vas_id)

            print("\n4. Добавляем телефон для Василия.")
            add_phone(cur, vas_id, '008')

            print("\n5. Меняем данные (фамилию) у клиента Оксана. Находим id Оксаны по фамилии Шукшина.")
            found_result = find_client(cur, last_name='Шукшина')
            if found_result[1] == 1:
                oksana_id = found_result[0][0]
                change_client(cur, oksana_id, last_name='Сидорова')

            print("\n6. Удаляем телефон у Петра. Находим id Петра по email-у.")
            found_result = find_client(cur, email='peter@mail.ru')
            if found_result[1] == 1:
                peter_id = found_result[0][0]
                delete_phone(cur, peter_id, '004')

            print("\n7. Удаляем клиента Алиса. Находим id Алисы по телефону.")
            found_result = find_client(cur, phone='005')
            if found_result[1] == 1:
                alisa_id = found_result[0][0]
                delete_client(cur, alisa_id)

    conn.close()  # Не понятно зачем? Контекстный менеджер разве этого не делает?
    return "\nПрограмма 'working_from_Python' отработала."


def main():
    """ Осуществляет вызов рабочей функции и вывод результатов выполнения. """
    res: str = working_from_Python()
    print(res)


if __name__ == '__main__':
    main()

    print('\n  -- Конец --  ')  # - Для блокнота
    # input('\n  -- Конец --  ')  # - Для среды

# Включает в общий коммит для отправки на проверку