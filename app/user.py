import asyncio

from aiogram import F, Router
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message, CallbackQuery, TelegramObject
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.requset import *
from app.states import *

user = Router()


# Обработчики Команд


async def send_typing_action(event: TelegramObject):
    user_id = getattr(event.from_user, 'id', None)
    bot = getattr(event, 'bot', None)

    if bot and user_id:
        await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        await asyncio.sleep(0.5)


@user.message(CommandStart())
async def cmd_start(message: Message):
    await send_typing_action(message)
    await message.answer_sticker(sticker='CAACAgUAAxkBAAEOVI9oA6UuI8VCNj7KCBC6nYf_XzxhpQACXREAAq97UVWRKrlFhzZOKDYE')
    await message.answer(f'Здравствуйте, <b>{message.from_user.first_name}</b>\n\n'
                         f'🏙️ Добро пожаловать в бот <b>«Городской ключ»</b>!\n\n'
                         f'<b>Этот бот создан для улучшения Грозного вместе с вами. Здесь можно сообщить о проблемах городской инфраструктуры:</b>\n'
                         f'<b>• Разбитые дороги 🚧\n'
                         f'• Неисправное освещение 💡\n'
                         f'• Переполненные мусорные баки 🗑️\n'
                         f'• Проблемы с водоснабжением 💧\n'
                         f'• Другие нарушения</b>\n\n'
                         f'<b>Как это работает?</b>\n'
                         f'1️⃣ Отправьте фото и описание проблемы.\n'
                         f'2️⃣ Укажите адрес или место на карте.\n'
                         f'3️⃣ Мы проверим заявку и передадим в ответственную службу.\n\n'
                         f'Ваше обращение поможет сделать город лучше!\n\n'
                         f'📌 Отправьте команду <b>«/report_problem»</b>, чтобы начать.')


@user.message(Command('help'))
async def cmd_help(message: Message):
    await send_typing_action(message)
    await message.answer('<b>ℹ️ Справка по боту "Городской ключ"</b>\n\n'
                         'Этот бот создан для оперативного реагирования на проблемы городской инфраструктуры Грозного. Вот что он умеет:\n\n'
                         '<b>Основные функции:</b>\n'
                         '📝 Отправка заявок о проблемах (дороги, освещение, мусор и др.)\n'
                         '🖼️ Прикрепление фотографий с геолокацией или адресом\n'
                         '📊 Просмотр статуса ваших обращений\n'
                         '📋 Ознакомление с правилами подачи заявок <b>(/rules)</b>\n\n'
                         '<B>Как пользоваться:</b>\n'
                         'Нажмите <b>/start</b> для создания новой заявки\n'
                         'Выберите категорию проблемы\n'
                         'Прикрепите фото и укажите место\n'
                         'Добавьте описание\n\n'
                         '<b>Дополнительно:</b>\n'
                         '🔄 История ваших обращений\n'
                         '⏱️ Уведомления об изменении статуса\n'
                         'ℹ️ Контакты поддержки (@support)\n\n'
                         'Ваши заявки помогают сделать город лучше!')


@user.message(Command('profile'))
@user.callback_query(F.data == 'profile')
async def cmd_profile(event: Message | CallbackQuery):
    user = await find_user(event.from_user.id)
    if isinstance(event, Message):
        await send_typing_action(event)
        if not user:
            await event.answer('Вам нужно зарегистрироваться!\n\n'
                                 'Для того чтобы зарегистрироваться вам нужно нажать на кнопку ниже и следовать всем инструкциям.',
                                 reply_markup=kb.register)
        else:
            await event.answer('👤 <b>Личный кабинет</b>\n\n'
                                    '<i>Здесь хранятся ваши данные и история обращений</i>\n\n'
                                    '📌 <b>Основная информация:</b>\n\n'
                                    f'Имя: <b>{user.name}</b>\n'
                                    f'Фамилия: <b>{user.surname}</b>\n'
                                    f'📧 E-mail: <b>{user.email}</b>\n'
                                    f'📞 Телефон: <b>+{user.phone}</b>\n\n'
                                    'ℹ️ <b>Как пользоваться:</b>\n'
                                    '• Нажмите <b>«Мои заявки»</b> для просмотра всех обращений\n'
                                    '• Выберите <b>«Изменить профиль»</b> для корректировки профиля\n'
                                    '• Все изменения сохраняются автоматически\n\n'
                                    '🔒 <b>Ваши данные защищены</b>\n'
                                    '<i>Мы используем их только для связи с вами и обработки заявок</i>',
                reply_markup=await kb.profile(user))
    elif isinstance(event, CallbackQuery):
        if not user:
            await event.answer()
            await event.message.answer('Вам нужно зарегистрироваться!\n\n'
                                 'Для того чтобы зарегистрироваться вам нужно нажать на кнопку ниже и следовать всем инструкциям.',
                                 reply_markup=kb.register)
        else:
            await event.answer()
            await event.message.edit_text('👤 <b>Личный кабинет</b>\n\n'
                                    '<i>Здесь хранятся ваши данные и история обращений</i>\n\n'
                                    '📌 <b>Основная информация:</b>\n\n'
                                    f'Имя: <b>{user.name}</b>\n'
                                    f'Фамилия: <b>{user.surname}</b>\n'
                                    f'📧 E-mail: <b>{user.email}</b>\n'
                                    f'📞 Телефон: <b>+{user.phone}</b>\n\n'
                                    'ℹ️ <b>Как пользоваться:</b>\n'
                                    '• Нажмите <b>«Мои заявки»</b> для просмотра всех обращений\n'
                                    '• Выберите <b>«Изменить профиль»</b> для корректировки профиля\n'
                                    '• Все изменения сохраняются автоматически\n\n'
                                    '🔒 <b>Ваши данные защищены</b>\n'
                                    '<i>Мы используем их только для связи с вами и обработки заявок</i>', reply_markup=await kb.profile(user))


@user.message(Command('rules'))
async def cmd_rules(message: Message):
    await send_typing_action(message)
    await message.answer('📜 <b>Правила подачи заявок</b>\n\n'
                         '<i>Чтобы ваше обращение рассмотрели максимально быстро:</i>\n\n'
                         '1. <b>📸 Фото/Видео проблемы</b>\n'
                         '• Четкий снимок (видно всю проблему)\n'
                         '• Видео — до 30 секунд\n'
                         '• Без редактирования\n\n'
                         '2. <b>📝 Описание</b>\n'
                         '• Тип проблемы (яма, мусор и т.д.)\n'
                         '• Детали (размеры, опасность)\n'
                         '• Без нецензурной лексики\n\n'
                         '3. <b>📍 Адрес</b>\n'
                         '• Точный адрес или отметка на карте\n'
                         '• Ориентиры ("возле школы №5")\n\n'
                         '⏱ <b>Сроки рассмотрения:</b> 1-3 рабочих дня\n\n'
                         '❌ <b>Что не принимается:</b>\n'
                         '• Без фото/видео\n• Неточные адреса\n• Повторные заявки\n\n'
                         '📌 Отправьте команду <b>«/report_problem»</b>, чтобы начать отправлять заявку.')


@user.message(Command('report_problem'))
@user.callback_query(F.data == 'categories')
async def cmd_report_problem(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, Message):
        if await find_user(event.from_user.id):
            await event.answer('🚨 <b>Сообщить о проблеме</b>\n\n'
            '<i>Заметили что-то, что нужно исправить?</i>\n'
            'Расскажите нам, и мы оперативно решим проблему!\n\n'
            '▫️▫️▫️▫️▫️▫️▫️▫️▫️\n\n'
            '📌 <b>Как это работает:</b>\n'
            '1️⃣ <b>Выберите категорию</b> (дороги, освещение и др.)\n'
            '2️⃣ <b>Добавьте фото/видео</b> (чтобы лучше понять проблему)\n'
            '3️⃣ <b>Укажите место</b> (адрес или отметка на карте)\n'
            '4️⃣ <b>Опишите проблему</b> (обязательно)\n\n'
            '🔹 <i>Каждая заявка проверяется администрацией</i>\n'
            '🔹 <i>Статус можно отслеживать в профиле</i>\n\n'
            'Выберите категорию ниже чтобы начать 👇', reply_markup=await kb.category())
            await state.set_state(ReportProblem.category)
        else:
            await event.answer('Вам нужно зарегистрироваться!\n\n'
                               'Для того чтобы зарегистрироваться вам нужно нажать на кнопку ниже и следовать всем инструкциям.',
                               reply_markup=kb.register)
    else:
        if await find_user(event.from_user.id):
            await event.answer()
            await event.message.answer('🚨 <b>Сообщить о проблеме</b>\n\n'
                               '<i>Заметили что-то, что нужно исправить?</i>\n'
                               'Расскажите нам, и мы оперативно решим проблему!\n\n'
                               '▫️▫️▫️▫️▫️▫️▫️▫️▫️\n\n'
                               '📌 <b>Как это работает:</b>\n'
                               '1️⃣ <b>Выберите категорию</b> (дороги, освещение и др.)\n'
                               '2️⃣ <b>Добавьте фото/видео</b> (чтобы лучше понять проблему)\n'
                               '3️⃣ <b>Укажите место</b> (адрес или отметка на карте)\n'
                               '4️⃣ <b>Опишите проблему</b> (обязательно)\n\n'
                               '🔹 <i>Каждая заявка проверяется администрацией</i>\n'
                               '🔹 <i>Статус можно отслеживать в профиле</i>\n\n'
                               'Выберите категорию ниже чтобы начать 👇', reply_markup=await kb.category())
            await state.set_state(ReportProblem.category)
        else:
            await event.answer('Вам нужно зарегистрироваться!\n\n'
                               'Для того чтобы зарегистрироваться вам нужно нажать на кнопку ниже и следовать всем инструкциям.',
                               reply_markup=kb.register)


# Callback Обработчики


@user.callback_query(F.data == 'register')
async def clb_register(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('🌟 <b>Давайте познакомимся ближе!</b>\n\n'
                         'Как вас называют друзья? Введите ваше <b>имя</b> — именно так мы будем обращаться к вам! ✨', reply_markup=kb.stop)
    await state.set_state(Register.name)


@user.callback_query(F.data == 'history_bid')
async def clb_get_history_at_bid_user(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('📋 <b>История ваших заявок</b>\n\n'
                                     '<i>В этом разделе вы можете просматривать все свои поданные заявки — их статус, дату создания и краткое описание проблемы.</i>\n\n'
                                     'Что можно сделать:\n'
                                     '• Открыть любую заявку для просмотра деталей\n'
                                     '• Увидеть текущий статус обработки',
                                     reply_markup=await kb.get_history_at_bid_user())


@user.callback_query(F.data.startswith('history_at_bid_'))
async def clb_get_history_at_bid_user(callback: CallbackQuery):
    problem_info = await get_report_problem_id(callback.data.split('_')[3])
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(photo=problem_info.image,
                                        caption='📋 <b>Ваша заявка</b>\n\n'
                                                f'{problem_info.description}\n\n'
                                                f'<b>Адрес: {problem_info.adress}</b>',
                                        reply_markup=await kb.btns_report_problems(problem_info.problem_category_id))


@user.callback_query(F.data.startswith('delete_problem_'))
async def clb_delete_problem(callback: CallbackQuery):
    category_id = callback.data.split('_')[-1]

    await delete_report_problem_user(
        tg_id=callback.from_user.id,
        category_id=category_id
    )

    await callback.answer('Заявка была удалена.')
    await callback.message.delete()

    await callback.message.answer('📋 <b>История ваших заявок</b>\n\n'
                                  '<i>В этом разделе вы можете просматривать все свои поданные заявки — их статус, дату создания и краткое описание проблемы.</i>\n\n'
                                  'Что можно сделать:\n'
                                  '• Открыть любую заявку для просмотра деталей\n'
                                  '• Увидеть текущий статус обработки',
                                  reply_markup=await kb.get_history_at_bid_user())


@user.callback_query(F.data == 'push_notifications')
async def clb_on_off_notifications(callback: CallbackQuery):
    await callback.answer()
    if not await check_user_at_notifications_list(callback.from_user.id):
        await callback.message.edit_text('🔔 <b>Управление уведомлениями</b>\n\n'
                                         '<i>Здесь вы можете настроить, какие уведомления хотите получать:</i>\n\n'
                                         '📲 <b>Доступные опции:</b>\n'
                                         '✅ <b>Новые заявки</b> – статус ваших обращений\n'
                                         '✅ <b>Важные новости</b> – обновления от администрации\n'
                                         '✅ <b>Экстренные оповещения</b> – информация о ЧС\n\n'
                                         '⚙️ <b>Как это работает?</b>\n'
                                         '• Включите нужные уведомления кнопками ниже\n'
                                         '• Изменения сохраняются автоматически\n\n',
                                          reply_markup=kb.on_notifications)
    else:
        await callback.message.edit_text('🔔 <b>Управление уведомлениями</b>\n\n'
                                         '<i>Здесь вы можете настроить, какие уведомления хотите получать:</i>\n\n'
                                         '📲 <b>Доступные опции:</b>\n'
                                         '✅ <b>Новые заявки</b> – статус ваших обращений\n'
                                         '✅ <b>Важные новости</b> – обновления от администрации\n'
                                         '✅ <b>Экстренные оповещения</b> – информация о ЧС\n\n'
                                         '⚙️ <b>Как это работает?</b>\n'
                                         '• Включите нужные уведомления кнопками ниже\n'
                                         '• Изменения сохраняются автоматически\n\n',
                                         reply_markup=kb.off_notifications)


@user.callback_query(F.data == 'on_notifications')
async def clb_on_notifications(callback: CallbackQuery):
    await add_user_at_notifications_list(callback.from_user.id)
    await callback.answer('Теперь вы будете получать уведомления')
    await callback.message.edit_reply_markup(reply_markup=kb.off_notifications)


@user.callback_query(F.data == 'off_notifications')
async def clb_on_notifications(callback: CallbackQuery):
    await remove_user_from_notifications_list(callback.from_user.id)
    await callback.answer('Теперь вы не будете получать уведомления')
    await callback.message.edit_reply_markup(reply_markup=kb.on_notifications)


@user.callback_query(F.data == 'stop')
async def clb_stop(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Вам нужно зарегистрироваться!\n\n'
                         'Для того чтобы зарегистрироваться вам нужно нажать на кнопку ниже и следовать всем инструкциям.',
                         reply_markup=kb.register)
    await state.clear()


@user.callback_query(F.data.startswith('editprofile_'))
@user.callback_query(F.data == 'edit_profile')
async def clb_edit_profile(callback: CallbackQuery):
    user_profile = await find_user(callback.from_user.id)
    await callback.answer()
    await callback.message.edit_text('✏️ <b>Редактирование профиля</b>\n\n'
    '<i>Здесь вы можете обновить свои данные. Выберите, что хотите изменить:</i>\n\n'
    '📌 <b>Текущая информация:</b>\n'
    f'👤 <b>Имя:</b> {user_profile.name}\n'
    f'📛 <b>Фамилия:</b> {user_profile.surname}\n'
    f'📧 <b>E-mail:</b> {user_profile.email}\n'
    f'📞 <b>Телефон:</b> {user_profile.phone}\n', reply_markup=kb.edit_profile)


@user.callback_query(F.data == 'editname')
async def clb_edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Введите ваше <b>новое имя</b> — именно так мы будем обращаться к вам! ✨', reply_markup=kb.back)
    await state.set_state(EditName.name)


@user.callback_query(F.data == 'editsurname')
async def clb_edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Введите вашу <b>новую фамилию</b> — именно так мы будем обращаться к вам! ✨', reply_markup=kb.back)
    await state.set_state(EditSurName.surname)


@user.callback_query(F.data == 'editphone')
async def clb_edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Введите ваш <b>новой номер телефона</b> ✨', reply_markup=kb.back)
    await state.set_state(EditPhone.phone)


@user.callback_query(F.data == 'editemail')
async def clb_edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Введите ваш <b>новой почтовый адресс</b> ✨', reply_markup=kb.back)
    await state.set_state(EditEmail.email)


# State Обработчики


@user.message(Register.name)
async def st_register_name(message: Message, state: FSMContext):
    await send_typing_action(message)
    await message.answer('📛 <b>Завершаем ваш уникальный профиль!</b>\n\n'
                         'Теперь введите <b>фамилию</b> — это нужно для официальных обращений и документов. 📄', reply_markup=kb.stop)
    await state.update_data(name=message.text)
    await state.set_state(Register.surname)


@user.message(Register.surname)
async def st_register_name(message: Message, state: FSMContext):
    await send_typing_action(message)
    await message.answer('📱 <b>Осталось чуть-чуть!</b>\n\n'
                         'Укажите ваш <b>номер телефона</b> — он поможет:\n'
                         '• Быстро восстановить доступ 🔐\n'
                         '• Получать важные уведомления 💌\n\n'
                         '<i>Формат: 7XXXXXXXXXX</i> без знака +', reply_markup=kb.stop)
    await state.update_data(surname=message.text)
    await state.set_state(Register.phone)


@user.message(Register.phone)
async def st_register_name(message: Message, state: FSMContext):
    await send_typing_action(message)
    await message.answer('📬 <b>Финальный штрих!</b>\n\n'
                         'Введите ваш <b>e-mail</b> — на него придут:\n'
                         '• Подтверждение регистрации ✅\n'
                         '• Отчеты по вашим заявкам 📊\n\n'
                         '<i>Пример: name@example.com</i> 🌐', reply_markup=kb.stop)
    await state.update_data(phone=message.text)
    await state.set_state(Register.email)


@user.message(Register.email)
async def st_register_name(message: Message, state: FSMContext):
    await send_typing_action(message)
    await message.answer('Вы были успешно авторизованны!')
    await state.update_data(email=message.text)
    data = await state.get_data()
    await add_user(message.from_user.id, data['name'], data['surname'], data['phone'], data['email'])
    await state.clear()


@user.callback_query(ReportProblem.category, F.data.startswith('category_'))
async def st_report_problem_category(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')[1]
    await callback.answer()
    await state.update_data(category=data)
    await callback.message.edit_text('Категория выбрана ✅\n\n'
    '📸 <b>Прикрепите фото или видео проблемы</b>\n\n'
    '<i>Чтобы заявка была обработана быстрее, пришлите:</i>\n'
    '✔ <b>Четкое фото</b> (крупным планом, хорошее освещение)\n'
    '✔ <b>Короткое видео</b> (до 30 секунд, если нужно показать масштаб)\n\n'
    '────────────────\n'
    '<b>Пример хорошего фото:</b>\n'
    '▫️ Видно всю проблему (например, яму целиком)\n'
    '▫️ Нет лишних объектов в кадре\n'
    '▫️ Снято при дневном свете\n\n'
    '❌ <b>Что не подходит:</b>\n'
    '▫️ Размытые/темные снимки\n'
    '▫️ Скриншоты или отредактированные фото\n'
    '▫️ Видео длиннее 30 секунд', reply_markup=kb.back_in_category)
    await state.set_state(ReportProblem.photo_or_video)


@user.message(ReportProblem.photo_or_video)
async def st_report_problem_photo_or_video(message: Message, state: FSMContext):
    if message.from_user == F.photo:
        await state.update_data(category_photo_or_video=message.photo[-1].file_id)
    elif message.from_user == F.video:
        await state.update_data(category_video_or_video=message.video.file_id)
    else:
        await message.answer('❌ Пожалуйста отправьте мне фото или видео!')
        return
    await message.answer('⚠️ <b>Опишите, что случилось</b>\n\n'
                         'Пожалуйста, кратко расскажите о проблеме. Это поможет нам быстрее ее решить!\n\n'
                         '<b>Что указать:</b>\n'
                         '1. <b>Тип проблемы</b>\n'
                         '   (<i>например: разбитая дорога, сломанный фонарь</i>)\n\n'
                         '2. <b>Масштаб повреждения</b>\n'
                         '   (<i>например: "яма диаметром 1 метр"</i>)\n\n'
                         '3. <b>Опасность для окружающих</b>\n'
                         '   (<i>например: "мешает проезду машин"</i>)\n\n'
                         '<b>Пример хорошего описания:</b>\n'
                         '<i>"На перекрестке ул. Ленина и пр. Мира глубокая яма (около 50 см), в которую уже проваливались колеса машин. '
                         'Очень опасно в темное время суток."</i>',
                         reply_markup=kb.back_in_category)
    await state.set_state(ReportProblem.description)


@user.message(ReportProblem.description)
async def st_report_problem_description(message: Message, state: FSMContext):
    if len(message.text) < 512:
        await state.update_data(category_description=message.text)
        await message.answer('📍 <b>Укажите адрес проблемы</b>\n\n'
        '<b>Как правильно оформить:</b>\n'
        '1. <b>Точный адрес</b> (если знаете):\n'
        '<i>Пример:</i>\n'
        '<code>"ул. Ленина, д. 10, возле подъезда №3"</code>\n'
        '<code>"пр. Победы, между домами 15 и 17"</code>\n\n'
        '2. <b>Или отправьте геолокацию</b> (нажмите 📎 → "Геопозиция")\n\n'
        '3. <b>Ориентиры</b> (если точный адрес неизвестен):\n'
        '<i>Пример:</i>\n'
        '<code>"Рядом с детской площадкой в парке Горького"</code>\n'
        '<code>"У остановки \'Центральный рынок\'"</code>\n\n'
        '────────────────\n'
        '❌ <b>Частые ошибки:</b>\n'
        '✖ <i>"Напротив того магазина"</i> (непонятно где)\n'
        '✖ Только название улицы без номера дома\n'
        '✖ Неточные формулировки\n\n', reply_markup=kb.back_in_category)
        await state.set_state(ReportProblem.adress)
    else:
        await message.answer('❌ Извините но длина описания не может превышать 512 символов')
        return


@user.message(ReportProblem.adress)
async def st_report_problem_address(message: Message, state: FSMContext):
    await state.update_data(category_adress=message.text)
    data = await state.get_data()
    await message.answer('⌛️ Ваша заявка была принята на рассмотрение.')
    await save_report_problem_user(message.from_user.id, data['category_description'], data['category_photo_or_video'],
                                   data['category_adress'], data['category'])
    await state.clear()


@user.message(EditName.name)
async def st_edit_name(message: Message, state: FSMContext):
    await send_typing_action(message)
    await state.update_data(new_name=message.text)
    data = await state.get_data()
    success = await edit_name(message.from_user.id, data['new_name'])
    user = await find_user(message.from_user.id)

    if success:
        await message.answer("Имя успешно обновлено!")
        await message.answer('👤 <b>Личный кабинет</b>\n\n'
                             '<i>Здесь хранятся ваши данные и история обращений</i>\n\n'
                             '📌 <b>Основная информация:</b>\n\n'
                             f'Имя: <b>{user.name}</b>\n'
                             f'Фамилия: <b>{user.surname}</b>\n'
                             f'📧 E-mail: <b>{user.email}</b>\n'
                             f'📞 Телефон: <b>+{user.phone}</b>\n\n'
                             'ℹ️ <b>Как пользоваться:</b>\n'
                             '• Нажмите <b>«Мои заявки»</b> для просмотра всех обращений\n'
                             '• Выберите <b>«Изменить профиль»</b> для корректировки профиля\n'
                             '• Все изменения сохраняются автоматически\n\n'
                             '🔒 <b>Ваши данные защищены</b>\n'
                             '<i>Мы используем их только для связи с вами и обработки заявок</i>',
                             reply_markup=await kb.profile(user))
    else:
        await message.answer("Не удалось обновить имя. Возможно, вы не зарегистрированы.")

    await state.clear()


@user.message(EditSurName.surname)
async def st_edit_name(message: Message, state: FSMContext):
    await send_typing_action(message)
    await state.update_data(new_surname=message.text)
    data = await state.get_data()
    success = await edit_surname(message.from_user.id, data['new_surname'])
    user = await find_user(message.from_user.id)

    if success:
        await message.answer("Фамилия успешно обновлена!")
        await message.answer('👤 <b>Личный кабинет</b>\n\n'
                             '<i>Здесь хранятся ваши данные и история обращений</i>\n\n'
                             '📌 <b>Основная информация:</b>\n\n'
                             f'Имя: <b>{user.name}</b>\n'
                             f'Фамилия: <b>{user.surname}</b>\n'
                             f'📧 E-mail: <b>{user.email}</b>\n'
                             f'📞 Телефон: <b>+{user.phone}</b>\n\n'
                             'ℹ️ <b>Как пользоваться:</b>\n'
                             '• Нажмите <b>«Мои заявки»</b> для просмотра всех обращений\n'
                             '• Выберите <b>«Изменить профиль»</b> для корректировки профиля\n'
                             '• Все изменения сохраняются автоматически\n\n'
                             '🔒 <b>Ваши данные защищены</b>\n'
                             '<i>Мы используем их только для связи с вами и обработки заявок</i>',
                             reply_markup=await kb.profile(user))
    else:
        await message.answer("Не удалось обновить фамилию. Возможно, вы не зарегистрированы.")

    await state.clear()


@user.message(EditPhone.phone)
async def st_edit_name(message: Message, state: FSMContext):
    await send_typing_action(message)
    await state.update_data(new_phone=message.text)
    data = await state.get_data()
    success = await edit_phone(message.from_user.id, data['new_phone'])
    user = await find_user(message.from_user.id)

    if success:
        await message.answer("Номер телефона был успешно обновлен!")
        await message.answer('👤 <b>Личный кабинет</b>\n\n'
                             '<i>Здесь хранятся ваши данные и история обращений</i>\n\n'
                             '📌 <b>Основная информация:</b>\n\n'
                             f'Имя: <b>{user.name}</b>\n'
                             f'Фамилия: <b>{user.surname}</b>\n'
                             f'📧 E-mail: <b>{user.email}</b>\n'
                             f'📞 Телефон: <b>+{user.phone}</b>\n\n'
                             'ℹ️ <b>Как пользоваться:</b>\n'
                             '• Нажмите <b>«Мои заявки»</b> для просмотра всех обращений\n'
                             '• Выберите <b>«Изменить профиль»</b> для корректировки профиля\n'
                             '• Все изменения сохраняются автоматически\n\n'
                             '🔒 <b>Ваши данные защищены</b>\n'
                             '<i>Мы используем их только для связи с вами и обработки заявок</i>',
                             reply_markup=await kb.profile(user))
    else:
        await message.answer("Не удалось обновить номер телефона. Возможно, вы не зарегистрированы.")

    await state.clear()


@user.message(EditEmail.email)
async def st_edit_name(message: Message, state: FSMContext):
    await send_typing_action(message)
    await state.update_data(new_email=message.text)
    data = await state.get_data()
    success = await edit_email(message.from_user.id, data['new_email'])
    user = await find_user(message.from_user.id)

    if success:
        await message.answer("Почтовый адресс был успешно обновлен!")
        await message.answer('👤 <b>Личный кабинет</b>\n\n'
                             '<i>Здесь хранятся ваши данные и история обращений</i>\n\n'
                             '📌 <b>Основная информация:</b>\n\n'
                             f'Имя: <b>{user.name}</b>\n'
                             f'Фамилия: <b>{user.surname}</b>\n'
                             f'📧 E-mail: <b>{user.email}</b>\n'
                             f'📞 Телефон: <b>+{user.phone}</b>\n\n'
                             'ℹ️ <b>Как пользоваться:</b>\n'
                             '• Нажмите <b>«Мои заявки»</b> для просмотра всех обращений\n'
                             '• Выберите <b>«Изменить профиль»</b> для корректировки профиля\n'
                             '• Все изменения сохраняются автоматически\n\n'
                             '🔒 <b>Ваши данные защищены</b>\n'
                             '<i>Мы используем их только для связи с вами и обработки заявок</i>',
                             reply_markup=await kb.profile(user))
    else:
        await message.answer("Не удалось обновить почтовый адресс. Возможно, вы не зарегистрированы.")

    await state.clear()