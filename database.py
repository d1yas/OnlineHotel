import sqlite3



connect = sqlite3.connect('hotel_db.db')
cursor = connect.cursor()

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
        room_number INTEGER,
        room_class TEXT,
        people_count INTEGER
    )
    """
)
connect.commit()

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

def move_room_to_booked(room_number, people_count):
    cursor.execute("SELECT * FROM empty_rooms WHERE room_number = ?", (room_number,))
    room = cursor.fetchone()
    if room:
        cursor.execute(
            "INSERT INTO booked_rooms (room_number, room_class, people_count) VALUES (?, ?, ?)",
            (room[1], room[2], people_count),
        )
        cursor.execute("DELETE FROM empty_rooms WHERE room_number = ?", (room_number,))
        connect.commit()

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