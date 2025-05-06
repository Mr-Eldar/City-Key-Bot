from aiogram.filters.state import State, StatesGroup


class Register(StatesGroup):
    name = State()
    surname = State()
    phone = State()
    email = State()


class AddCategory(StatesGroup):
    name = State()


class ReportProblem(StatesGroup):
    category = State()
    photo_or_video = State()
    description = State()
    adress = State()


class DoNotifications(StatesGroup):
    image = State()
    description = State()
    send = State()


class EditName(StatesGroup):
    name = State()


class EditSurName(StatesGroup):
    surname = State()


class EditPhone(StatesGroup):
    phone = State()


class EditEmail(StatesGroup):
    email = State()


class EditCategory(StatesGroup):
    category = State()
    name = State()