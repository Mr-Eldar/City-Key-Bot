from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.database.requset import *

register = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Зарегистрироваться ⚙️', callback_data='register')]
])

stop = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена ❌', callback_data='stop')]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад ⬅️', callback_data='edit_profile')]
])

edit_profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить имя 🖊️', callback_data=f'editname')],
    [InlineKeyboardButton(text='Изменить фамилию 🖊️', callback_data=f'editsurname')],
    [InlineKeyboardButton(text='Изменить номер телефона 📞', callback_data=f'editphone')],
    [InlineKeyboardButton(text='Изменить почтовый адресс ✉️', callback_data=f'editemail')],
    [InlineKeyboardButton(text='В профиль ⬅️', callback_data=f'profile')],
])

on_notifications = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получать уведомления ✅', callback_data='on_notifications')]
])

off_notifications = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отключить уведомления ❌', callback_data='off_notifications')]
])

admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕ Добавить категорию', callback_data='add_category')],
    [InlineKeyboardButton(text='✏️ Изменить категорию', callback_data='edit_category')],
    [InlineKeyboardButton(text='📢 Сделать рассылку', callback_data='do_notifications')]
])

back_in_apanel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена ❌', callback_data='apanel')]
])

back_in_category = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад ⬅️', callback_data='categories')]
])


async def btns_report_problems(category_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад ⬅️', callback_data='history_bid')],
        [InlineKeyboardButton(text='Удалить 🗑', callback_data=f'delete_problem_{category_id}')]
    ])


async def profile(user):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить профиль ✏️', callback_data=f'editprofile_{user.id}')],
        [InlineKeyboardButton(text='Мои заявки 📝', callback_data='history_bid')],
        [InlineKeyboardButton(text='Уведомления 🔔', callback_data='push_notifications')]
    ])


async def category():
    keyboard = InlineKeyboardBuilder()
    categories = await get_categories()

    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.category_name, callback_data=f'category_{category.id}'))

    return keyboard.adjust(2).as_markup()


async def get_history_at_bid_user():
    keyboard = InlineKeyboardBuilder()
    problems = await get_report_problem()

    for problem in problems:
        keyboard.add(InlineKeyboardButton(text=problem.description,
                                          callback_data=f'history_at_bid_{problem.problem_category_id}'))
    keyboard.row(InlineKeyboardButton(text='Назад ⬅️', callback_data='profile'))
    return keyboard.adjust(1).as_markup()