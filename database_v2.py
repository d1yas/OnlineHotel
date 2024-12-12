# import sqlite3
#
# connect = sqlite3.connect('hotel_db.db')
# cursor = connect.cursor()
#
# cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS empty_rooms (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         room_number INTEGER,
#         room_class TEXT,
#         price_per_day INTEGER
#     )
#     """
# )
# cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS booked_rooms (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         room_number INTEGER,
#         room_class TEXT,
#         people_count INTEGER,
#         days INTEGER,
#         total_price INTEGER
#     )
#     """
# )
# connect.commit()
#
# def add_room(table, room_number, room_class, price_per_day):
#     cursor.execute(
#         f"INSERT INTO {table} (room_number, room_class, price_per_day) VALUES (?, ?, ?)",
#         (room_number, room_class, price_per_day)
#     )
#     connect.commit()
#
# def get_rooms(table, room_class=None):
#     if room_class:
#         cursor.execute(f"SELECT * FROM {table} WHERE room_class = ?", (room_class,))
#     else:
#         cursor.execute(f"SELECT * FROM {table}")
#     return cursor.fetchall()
#
# def move_room_to_booked(room_number, people_count, days):
#     cursor.execute("SELECT * FROM empty_rooms WHERE room_number = ?", (room_number,))
#     room = cursor.fetchone()
#     if room:
#         total_price = room[3] * days
#         cursor.execute(
#             "INSERT INTO booked_rooms (room_number, room_class, people_count, days, total_price) VALUES (?, ?, ?, ?, ?)",
#             (room[1], room[2], people_count, days, total_price)
#         )
#         cursor.execute("DELETE FROM empty_rooms WHERE room_number = ?", (room_number,))
#         connect.commit()
#
# def get_booked_rooms():
#     cursor.execute("SELECT * FROM booked_rooms")
#     return cursor.fetchall()
#
# def initialize_rooms():
#     room_classes = {
#         "economy": (30, 50000),
#         "standard": (30, 100000),
#         "comfort": (15, 200000),
#         "business": (15, 500000),
#         "vip": (5, 800000),
#     }
#     room_number = 1
#     for room_class, (count, price) in room_classes.items():
#         for _ in range(count):
#             add_room("empty_rooms", room_number, room_class, price)
#             room_number += 1
#
# cursor.execute("SELECT COUNT(*) FROM empty_rooms")
# if cursor.fetchone()[0] == 0:
#     initialize_rooms()
