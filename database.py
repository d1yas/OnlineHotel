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
        email TEXT,
        start_date TEXT,
        duration INTEGER,
        total_cost INTEGER
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS ratings (
        user_id INTEGER PRIMARY KEY,
        rating INTEGER
    )
    """
)

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

def add_room(table, room_number, room_class):
    cursor.execute(
        f"INSERT INTO {table} (room_number, room_class) VALUES (?, ?)", (room_number, room_class)
    )
    connect.commit()

def get_rooms(table, room_class=None):
    if room_class:
        cursor.execute(f"SELECT * FROM {table} WHERE room_class = ?", (room_class,))
    else:
        cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

def move_room_to_booked_with_date(user_id, room_number, room_class, start_date, duration, total_cost, people_count):
    try:
        cursor.execute("SELECT phone, fio, email FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            print("Foydalanuvchi topilmadi.")
            return False

        phone, fio, email = user

        cursor.execute(
            """
            INSERT INTO booked_rooms (user_id, room_number, room_class, people_count, phone, fio, email, start_date, duration, total_cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, room_number, room_class, people_count, phone, fio, email, start_date, duration, total_cost)
        )

        cursor.execute("DELETE FROM empty_rooms WHERE room_number = ?", (room_number,))
        connect.commit()
        print("Xona muvaffaqiyatli bron qilindi!")
        return True
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return False


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

def add_rating(user_id, rating):
    cursor.execute(
        "INSERT INTO ratings (user_id, rating) VALUES (?, ?)",
        (user_id, rating)
    )
    connect.commit()

def get_average_rating():
    cursor.execute("SELECT AVG(rating) FROM ratings")
    avg = cursor.fetchone()[0]
    return avg if avg else 0

def has_rated(user_id):
    cursor.execute("SELECT rating FROM ratings WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

def get_booked_rooms(user_id):
    cursor.execute(
        "SELECT room_number, room_class, people_count, start_date, duration, total_cost FROM booked_rooms WHERE user_id = ?",
        (user_id,)
    )
    return cursor.fetchall()
