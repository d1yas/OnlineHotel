from aiogram.dispatcher.filters.state import State, StatesGroup

# Define states for the user
class UserStates(StatesGroup):
    get_people_count = State()
    get_phone = State()
    get_fio = State()
    get_email = State()

