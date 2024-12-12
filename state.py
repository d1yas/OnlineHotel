from aiogram.dispatcher.filters.state import State, StatesGroup

# Define states for the user
class UserStates(StatesGroup):
    get_people_count = State()  # State for collecting people count
    get_phone = State()         # State for collecting phone number
    get_fio = State()           # State for collecting full name
    get_email = State()         # State for collecting email (optional)
