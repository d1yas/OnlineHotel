# state.py
from aiogram.dispatcher.filters.state import State, StatesGroup

class BookingStates(StatesGroup):
    get_phone = State()
    get_fio = State()
    get_email = State()
    get_start_date = State()
    get_duration = State()
    get_people = State()
    confirm_booking = State()

