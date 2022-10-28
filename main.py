import psycopg2
from pprint import pprint


# 1). Функция, создающая структуру БД (таблицы)
def create_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_base(
    id SERIAL PRIMARY KEY, 
    client_name VARCHAR(80) NOT NULL, 
    client_surname VARCHAR(80) NOT NULL, 
    client_email VARCHAR(80) NOT NULL
    );
    """)
    # Таблица с номерами телефонов клиентов
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_phone(
    id_phone SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES client_base(id),
    client_phone VARCHAR(30) UNIQUE)
    """)


# 2). Функция, позволяющая добавить нового клиента

def add_new_client(cur, client_name, client_surname, client_email):
    cur.execute("\n"
                "    INSERT INTO client_base(client_name, client_surname, client_email) VALUES(%s, %s, %s);\n"
                "    ", (client_name, client_surname, client_email))


# 3). Функция, позволяющая добавить телефон для существующего клиента

def add_new_phone(cur, client_id, client_phone):
    cur.execute("""
    INSERT INTO client_phone(client_id, client_phone) VALUES(%s, %s);
    """, (client_id, client_phone))


# 4). Функция, позволяющая изменить данные о клиенте

def change_client_data():
    print("Для изменения информации о клиенте, пожалуйста, введите нужную Вам команду.\n "
          "1 - изменить имя; 2 - изменить фамилию; 3 - изменить e-mail; 4 - изменить номер телефона")

    while True:
        order_number = int(input())
        if order_number == 1:
            input_id_change_name = input("Введите id клиента (Для дальнейшего изменения его имени): ")
            input_new_name = input("Введите новое 'имя' клиента: ")
            cur.execute("""
            UPDATE client_base SET client_name=%s WHERE id=%s;
            """, (input_new_name, input_id_change_name))
            break
        elif order_number == 2:
            input_id_change_surname = input("Введите id клиента (Для дальнейшего изменения его фамилии): ")
            input_new_surname = input("Введите новую 'фамилию' клиента: ")
            cur.execute("""
            UPDATE client_base SET client_surname=%s WHERE id=%s;
            """, (input_new_surname, input_id_change_surname))
            break
        elif order_number == 3:
            input_id_change_email = input("Введите id клиента (Для дальнейшего изменения его e-mail): ")
            input_new_email = input("Введите новый e-mail: ")
            cur.execute("""
            UPDATE client_base SET client_email=%s WHERE id=%s;
            """, (input_new_email, input_id_change_email))
            break
        elif order_number == 4:
            input_change_old_phone = input("Введите номер телефона, который необходимо изменить: ")
            input_new_phone = input("Введите новый номер телефона: ")
            cur.execute("""
            UPDATE client_phone SET client_phone=%s WHERE client_phone=%s;
            """, (input_new_phone, input_change_old_phone))
            break
        else:
            print("Вы ввели неверную команду. Пожалуйста, повторите попытку!")


# 5). Функция, позволяющая удалить телефон для существующего клиента

def delete_client_phone():
    input_id_client_delete_phone = input("Введите id клиента (Для дальнейшего удаления его номера телефона): ")
    input_delete_phone = input("Введите номер телефона, который необходимо удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM client_phone WHERE client_id=%s AND client_phone=%s
        """, (input_id_client_delete_phone, input_delete_phone))


# 6). Функция, позволяющая удалить существующего клиента

def delete_client():
    input_id_delete_client = input("Введите id клиента, которого необходимо удалить: ")
    input_client_surname_delete = input("Введите фамилию клиента, которого необходимо удалить: ")
    with conn.cursor() as cur:

        cur.execute("""
        DELETE FROM client_phone WHERE client_id=%s
        """, (input_id_delete_client,))

        cur.execute("""
        DELETE FROM client_base WHERE id=%s AND client_surname=%s
        """, (input_id_delete_client, input_client_surname_delete))


# 7). Функция, позволяющая найти клиента по его данным (имени, фамилии, email, телефону)

def find_client():
    print("Для поиска информации о клиенте, пожалуйста, введите команду, где:\n "
          "1 - Поиск по имени; 2 - Поиск по фамилии; 3 - Поиск по e-mail; 4 - Поиск по номеру телефона")
    while True:
        input_search_order = int(input("Введите команду, соответствующую нужному поиску информации: "))
        if input_search_order == 1:
            input_search_name = input("Введите имя для получения информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phone
            FROM client_base AS cb
            LEFT JOIN client_phone AS cp ON cp.id_phone = cb.id
            WHERE client_name=%s
            """, (input_search_name,))
            print(cur.fetchall())
        elif input_search_order == 2:
            input_surname_search = input("Введите фамилию для получения информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phone
            FROM client_base AS cb
            LEFT JOIN client_phone AS cp ON cp.id_phone = cb.id
            WHERE client_surname=%s
            """, (input_surname_search,))
            print(cur.fetchall())
        elif input_search_order == 3:
            input_email_search = input("Введите email для получения информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phone
            FROM client_base AS cb
            LEFT JOIN client_phone AS cp ON cp.id_phone = cb.id
            WHERE client_email=%s
            """, (input_email_search,))
            print(cur.fetchall())
        elif input_search_order == 4:
            input_phone_search = input("Введите номер телефона для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, client_name, client_surname, client_email, client_phone
            FROM client_base AS cb
            LEFT JOIN client_phone AS cp ON cp.id_phone = cb.id
            WHERE client_phone=%s
            """, (input_phone_search,))
            print(cur.fetchall())
        else:
            print("Вы ввели неверную команду. Пожалуйста, повторите попытку")


# Функция для проверки

def check_function(cur):
    cur.execute("""
    SELECT * FROM client_base;
    """)
    pprint(cur.fetchall())
    cur.execute("""
    SELECT * FROM client_phone;
    """)
    pprint(cur.fetchall())


with psycopg2.connect(database="DataBase_psycopg", user="postgres", password="11170309") as conn:
    with conn.cursor() as cur:
        create_tables(cur)
        check_function(cur)
        add_new_client(cur, "Emmy", "Rose", "emmy@gmail.com")
        add_new_client(cur, "Billy", "Black", "billy@gmail.com")
        add_new_client(cur, "Terry", "Diablo", "terry@gmail.com")
        add_new_client(cur, "Shawn", "Second", "shawn@gmail.com")
        add_new_client(cur, "Brian", "Good", "brian@gmail.com")
        add_new_phone(cur, 1, "+7123")
        add_new_phone(cur, 2, "+7456")
        add_new_phone(cur, 3, "+7789")
        add_new_phone(cur, 4, "+7453")
        add_new_phone(cur, 5, "+7976")
        change_client_data()
        delete_client_phone()
        delete_client()
        find_client()

conn.close()
