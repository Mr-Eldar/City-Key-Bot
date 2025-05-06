from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery, TelegramObject
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction

import app.keyboards as kb
from app.states import *
from app.filters import ProtectAdmin
from app.database.requset import *

admin = Router()


async def send_chat_action(event: TelegramObject):
    user_id = getattr(event.from_user, 'user_id', None)
    bot = getattr(event, 'bot', None)

    if bot and user_id:
        await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)


@admin.message(ProtectAdmin(), Command('apanel'))
@admin.callback_query(F.data == 'apanel')
async def cmd_apanel(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, Message):
        await send_chat_action(event)
        await event.answer('🛠️ <b>Админ-панель</b>\n\n'
                             '<i>Только для администраторов города</i>\n\n'
                             '🔧 <b>Основные инструменты:</b>\n'
                             '• <b>➕ Добавить категорию</b> (новые типы проблем)\n'
                             '• <b>📢 Сделать рассылку</b> (всем пользователям)\n'
                             '• <b>📊 Статистика</b> (количетсво поданных заявок)\n\n'
                             '🔐 <b>Ваши права:</b>\n'
                             '🟢 <b>Полный доступ</b> (все функции доступны)\n\n',
                             reply_markup=kb.admin_panel)
    else:
        await send_chat_action(event)
        await event.answer()
        await event.message.edit_text('🛠️ <b>Админ-панель</b>\n\n'
                           '<i>Только для администраторов города</i>\n\n'
                           '🔧 <b>Основные инструменты:</b>\n'
                           '• <b>➕ Добавить категорию</b> (новые типы проблем)\n'
                           '• <b>📢 Сделать рассылку</b> (всем пользователям)\n'
                           '• <b>📊 Статистика</b> (количетсво поданных заявок)\n\n'
                           '🔐 <b>Ваши права:</b>\n'
                           '🟢 <b>Полный доступ</b> (все функции доступны)\n\n',
                           reply_markup=kb.admin_panel)
        await state.clear()


# Callbacck Обработчики


@admin.callback_query(ProtectAdmin(), F.data == 'add_category')
async def clb_add_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('📝 <b>Создание новой категории</b>\n\n'
                         '<b>Шаг 1:</b> Введите название категории\n'
                         '<i>Пример:</i> <code>"Разбитые дороги"</code>\n\n'
                         '◽ До 64 символов\n'
                         '◽ Без специальных символов (@#&*)\n'
                         '◽ Будет отображаться в списке для выбора', reply_markup=kb.back_in_apanel)
    await state.set_state(AddCategory.name)


@admin.callback_query(ProtectAdmin(), F.data == 'edit_category')
async def clb_edit_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('🔄 <b>Выберите категорию для того чтобы изменить имя:</b>\n', reply_markup=await kb.category())
    await state.set_state(EditCategory.category)


@admin.callback_query(ProtectAdmin(), F.data == 'do_notifications')
async def clb_do_notifications(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(DoNotifications.image)
    await callback.message.edit_text('📢 <b>Создание рассылки</b>\n\n'
                                     '<b>Шаг 1/2: Добавьте контент для рассылки</b>\n\n'
                                     'Вы можете отправить:\n'
                                     '🖼️ <b>Изображение</b>\n'
                                     '✏️ <b>Текст сообщения</b> (до 512 символов)\n\n'
                                     'Требования:\n'
                                     '✔ Изображение в формате JPG/PNG\n'
                                     '✔ Текст должен содержать полезную информацию\n'
                                     '✔ Можно использовать разметку (жирный, курсив)\n\n'
                                     '<b>Отправьте фото на это сообщение чтобы продолжить</b>')


# State Обработчики


@admin.message(ProtectAdmin(), AddCategory.name)
async def st_add_category_name(message: Message, state: FSMContext):
    await state.update_data(category_name=message.text)
    await message.answer('Категория была успешно добавлена 🎉')
    data = await state.get_data()
    await add_category(data['category_name'])
    await state.clear()


@admin.callback_query(ProtectAdmin(), EditCategory.category, F.data.startswith('category_'))
async def st_edit_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[1])
    await callback.answer()
    await callback.message.edit_text('Категория выбрана ✅\n\n'
    '🔄 <b>Введите новое название для:</b>\n'
    '<i>Требования: 3-64 символов, без спецзнаков</i>')
    await state.set_state(EditCategory.name)


@admin.message(ProtectAdmin(), EditCategory.name)
async def st_edit_category_name(message: Message, state: FSMContext):
    await state.update_data(category_name=message.text)
    await message.answer('Категория была успешно обновлена 🎉')
    data = await state.get_data()
    await edit_problem_category_name(data['category'], data['category_name'])
    await state.clear()


@admin.message(ProtectAdmin(), DoNotifications.image)
async def st_do_notifications(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(notifications_image=message.photo[-1].file_id)
        await message.answer('✏️ <b>Введите текст рассылки</b>\n\n'
        '<b>Что можно указать:</b>\n'
        '• Важные новости\n'
        '• Информацию о мероприятиях\n'
        '• Изменения в работе\n\n'
        '<b>Пример:</b>\n'
        '<i>"Уважаемые жители!\n'
        'Завтра с 9:00 до 12:00 будет проводиться плановый ремонт..."</i>')
        await state.set_state(DoNotifications.description)
    else:
        await message.answer('❌ Извините, отправьте мне изображение')


@admin.message(ProtectAdmin(), DoNotifications.description)
async def st_do_notifications_description(message: Message, state: FSMContext):
    if len(message.text) < 512:
        await state.update_data(notifications_description=message.text)
        data = await state.get_data()
        users_in_nf_list = await get_users_in_notifications_list()
        await message.answer('Расслыка сообщения пользователям началась.')
        for user in users_in_nf_list:
            try:
                await message.bot.send_photo(chat_id=user.tg_id, photo=data['notifications_image'], caption=data['notifications_description'])
            except:
                pass
                await state.clear()
        await message.answer('Расслыка сообщения пользователям была окончена.')
    else:
        await message.answer('❌ Извните но размер описания не может превышать более 512 символов')