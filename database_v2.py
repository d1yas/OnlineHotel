import sqlite3

# Initialize database connections
connect = sqlite3.connect('hotel_db.db', check_same_thread=False)
cursor = connect.cursor()

# Tables creation
def create_tables():
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
            people_count INTEGER DEFAULT 1,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """
    )
    connect.commit()

# Initialize rooms
def initialize_rooms():
    room_classes = {
        "economy": 30,
        "standard": 30,
        "comfort": 15,
        "business": 15,
        "vip": 5,
    }
    cursor.execute("SELECT COUNT(*) FROM empty_rooms")
    if cursor.fetchone()[0] == 0:
        room_number = 1
        for room_class, count in room_classes.items():
            for _ in range(count):
                cursor.execute(
                    "INSERT INTO empty_rooms (room_number, room_class) VALUES (?, ?)",
                    (room_number, room_class)
                )
                room_number += 1
        connect.commit()

# User functions
def add_user(user_id, phone, fio, email):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, phone, fio, email) VALUES (?, ?, ?, ?)",
        (user_id, phone, fio, email)
    )
    connect.commit()

def get_user_by_id(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return {"user_id": row[0], "phone": row[1], "fio": row[2], "email": row[3]} if row else None

# Room functions
def get_rooms(table, room_class=None):
    if room_class:
        cursor.execute(f"SELECT * FROM {table} WHERE room_class = ?", (room_class,))
    else:
        cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

def move_room_to_booked(user_id, room_number, people_count):
    cursor.execute("SELECT * FROM empty_rooms WHERE room_number = ?", (room_number,))
    room = cursor.fetchone()
    if room:
        cursor.execute(
            """
            INSERT INTO booked_rooms (user_id, room_number, room_class, people_count)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, room[1], room[2], people_count)
        )
        cursor.execute("DELETE FROM empty_rooms WHERE room_number = ?", (room_number,))
        connect.commit()

# Initialize the database
create_tables()
initialize_rooms()
