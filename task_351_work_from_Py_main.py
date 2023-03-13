# -*- coding: utf-8 -*-
#                       Работа с PostgreSQL из Python.

#       Задача 1. Создайте программу для управления клиентами на Python.
#                 Требуется хранить персональную информацию: имя, фамилия, email и телефон.

#                 Управляющий модуль.                (Каркас кода прилагается.)

from task_352_work_from_Py_modules import *


def working_from_Python() -> str:
    """Работает с PostgreSQL из Python."""
    print('\n    В этой программе...')
    with psycopg2.connect(database="clients_db", user="postgres", password="psdb") as conn:
        table_name = 'customers'
        print("\n1. Создаём таблицу '", table_name, "'.", sep='')
        create_table(conn, table_name, 'firstname', 'lastname', 'email', 'phone')

        print("\n2. Заполняем её данными.")
        clients_data = [['Алиса', 'Семёнова', 'alisa@mail.ru', '002', '005', '007'],
                        ['Василий', 'Адушкин', 'vas@mail.ru', '003'],
                        ['Оксана', 'Шукшина', 'oksana@mail.ru'],
                        ['Пётр', 'Харламов', 'peter@mail.ru', '004']]
        for item in clients_data:
            add_client(conn, table_name, item[0], item[1], item[2], *item[3:])

        print("\n3. Находим id Василия, в данном случае - по имени.")
        vas_id = find_client(conn, table_name, 'Василий')

        print("\n4. Добавляем телефон для Василия.")
        add_phone(conn, table_name, vas_id, '008')

        print("\n5. Меняем данные о клиенте Оксана. Находим id Оксаны по фамилии.")
        oksana_id = find_client(conn, table_name, last_name='Шукшина')
        change_client(conn, table_name, oksana_id, last_name='Сидорова')

        print("\n6. Удаляем телефон у Петра. Находим id Петра по email-у.")
        peter_id = find_client(conn, table_name, email='peter@mail.ru')
        delete_phone(conn, table_name, peter_id, '004')

        print("\n7. Удаляем клиента Алиса. Находим id Алисы по телефону.")
        alisa_id = find_client(conn, table_name, phones=['005'])
        delete_client(conn, table_name, alisa_id)

    conn.close()  # Не понятно, зачем?
    return "\nПрограмма 'working_from_Python' отработала."


def main():
    """Осуществляет вызов рабочей функции и вывод результатов выполнения."""
    res: str = working_from_Python()
    print(res)


if __name__ == '__main__':
    main()

    print('\n  -- Конец --  ')  # - Для блокнота
    # input('\n  -- Конец --  ')  # - Для среды
