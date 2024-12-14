# state.py
from aiogram.dispatcher.filters.state import State, StatesGroup

class UserStates(StatesGroup):
    send_phone = State()
    get_fio = State()
    get_email = State()

class BookingStates(StatesGroup):
    get_start_date = State()
    get_duration = State()
    get_people = State()
    confirm_booking = State()
