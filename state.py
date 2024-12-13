from aiogram.dispatcher.filters.state import State, StatesGroup

# class UserStates(StatesGroup):
#     language = State()
#     send_phone = State()
#     get_fio = State()
#     get_email = State()
#     choose_menu = State()


class UserStates(StatesGroup):
    send_phone = State()
    get_fio = State()
    get_email = State()
    menu = State()

