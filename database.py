import sqlite3

connect = sqlite3.connect('hotel_db.db', check_same_thread=False)
cursor = connect.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        phone TEXT,
        fio TEXT,
        email TEXT
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS empty_rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number INTEGER,
        room_class TEXT
    )
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS booked_rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        room_number INTEGER,
        room_class TEXT,
        people_count INTEGER,
        phone TEXT,
        fio TEXT,
        email TEXT
    )
    """
)
connect.commit()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS ratings (
        user_id INTEGER PRIMARY KEY,
        rating INTEGER
    )
    """
)
connect.commit()


connect.commit()

def add_user(user_id, phone, fio, email):
    cursor.execute(
        "INSERT INTO users (user_id, phone, fio, email) VALUES (?, ?, ?, ?)",
        (user_id, phone, fio, email)
    )
    connect.commit()

def get_user_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        return {"user_id": row[0], "phone": row[1], "fio": row[2], "email": row[3]}
    return None

# Добавление комнаты
def add_room(table, room_number, room_class):
    cursor.execute(
        f"INSERT INTO {table} (room_number, room_class) VALUES (?, ?)", (room_number, room_class)
    )
    connect.commit()

# Получение комнат
def get_rooms(table, room_class=None):
    if room_class:
        cursor.execute(f"SELECT * FROM {table} WHERE room_class = ?", (room_class,))
    else:
        cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

# Перемещение комнаты из свободных в забронированные
# def move_room_to_booked(room_number, people_count, phone=None, fio=None, email=None):
#     cursor.execute("SELECT * FROM empty_rooms WHERE room_number = ?", (room_number,))
#     room = cursor.fetchone()
#     if room:
#         cursor.execute(
#             "INSERT INTO booked_rooms (room_number, room_class, people_count, phone, fio, email) VALUES (?, ?, ?, ?, ?, ?)",
#             (room[1], room[2], people_count, phone, fio, email),
#         )
#         cursor.execute("DELETE FROM empty_rooms WHERE room_number = ?", (room_number,))
#         connect.commit()

# def move_room_to_booked(user_id, room_number, people_count):
#     try:
#         # Foydalanuvchi ma'lumotlarini olish
#         cursor.execute("SELECT phone, fio, email FROM users WHERE user_id = ?", (user_id,))
#         user = cursor.fetchone()
#         if not user:
#             return False  # Foydalanuvchi topilmadi, xatolik
#
#         phone, fio, email = user
#
#         # Bo'sh xona borligini tekshirish
#         cursor.execute("SELECT * FROM empty_rooms WHERE room_number = ?", (room_number,))
#         room = cursor.fetchone()
#         if not room:
#             return False  # Xona topilmadi, xatolik
#
#         # Xonani booked_rooms jadvaliga o'tkazish
#         cursor.execute(
#             """
#             INSERT INTO booked_rooms (user_id, room_number, room_class, people_count, phone, fio, email)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#             """,
#             (user_id, room[1], room[2], people_count, phone, fio, email)
#         )
#
#         # Bo'sh xonani o'chirish
#         cursor.execute("DELETE FROM empty_rooms WHERE room_number = ?", (room_number,))
#         connect.commit()
#         return True  # Xona muvaffaqiyatli bron qilindi
#     except Exception as e:
#         print(f"Xatolik yuz berdi: {e}")
#         return False  # Xatolik yuz berdi

def move_room_to_booked(user_id, room_number, people_count):
    try:
        # Получаем данные пользователя
        cursor.execute("SELECT phone, fio, email FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            print("Пользователь не найден в базе данных!")
            return False  # Пользователь не найден

        phone, fio, email = user

        # Проверяем, что у пользователя есть все необходимые данные
        if not phone or not fio or not email:
            print("У пользователя отсутствуют обязательные данные для бронирования!")
            return False

        # Проверяем наличие свободной комнаты
        cursor.execute("SELECT * FROM empty_rooms WHERE room_number = ?", (room_number,))
        room = cursor.fetchone()
        if not room:
            print("Комната не найдена среди свободных!")
            return False

        # Переносим комнату в booked_rooms
        cursor.execute(
            """
            INSERT INTO booked_rooms (user_id, room_number, room_class, people_count, phone, fio, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, room[1], room[2], people_count, phone, fio, email)
        )

        # Удаляем комнату из empty_rooms
        cursor.execute("DELETE FROM empty_rooms WHERE room_number = ?", (room_number,))
        connect.commit()
        print("Комната успешно забронирована!")
        return True
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


# Инициализация комнат
def initialize_rooms():
    room_classes = {
        "economy": 30,
        "standard": 30,
        "comfort": 15,
        "business": 15,
        "vip": 5,
    }
    room_number = 1
    for room_class, count in room_classes.items():
        for _ in range(count):
            add_room("empty_rooms", room_number, room_class)
            room_number += 1

cursor.execute("SELECT COUNT(*) FROM empty_rooms")
if cursor.fetchone()[0] == 0:
    initialize_rooms()
