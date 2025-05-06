from app.database.models import async_session
from app.database.models import *
from sqlalchemy import select, update, delete, desc


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper


# Работа с юзером


@connection
async def add_user(session, tg_id, name, surname, phone, email):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id, name=name, surname=surname, phone=phone, email=email))
        await session.commit()


@connection
async def get_users(session):
    return await session.scalars(select(User))


@connection
async def get_users_in_notifications_list(session):
    return await session.scalars(select(NotificationsListUsers))


@connection
async def add_user_at_notifications_list(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return

    existing = await session.scalar(
        select(NotificationsListUsers).where(NotificationsListUsers.tg_id == user.id)
    )
    if not existing:
        session.add(NotificationsListUsers(tg_id=tg_id))
        await session.commit()


@connection
async def remove_user_from_notifications_list(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return

    notif_entry = await session.scalar(
        select(NotificationsListUsers).where(NotificationsListUsers.tg_id == user.id)
    )
    if notif_entry:
        await session.delete(notif_entry)
        await session.commit()


@connection
async def check_user_at_notifications_list(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return False

    existing = await session.scalar(
        select(NotificationsListUsers).where(NotificationsListUsers.tg_id == user.id)
    )
    return bool(existing)


@connection
async def find_user(session, tg_id):
    return await session.scalar(select(User).where(User.tg_id == tg_id))


# Изменение категорий
@connection
async def edit_name(session, tg_id, new_name):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return False
    user.name = new_name
    await session.commit()
    return True


@connection
async def edit_surname(session, tg_id, new_surname):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return False
    user.surname = new_surname
    await session.commit()
    return True


@connection
async def edit_phone(session, tg_id, new_phone):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return False
    user.phone = new_phone
    await session.commit()
    return True


@connection
async def edit_email(session, tg_id, new_email):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return False
    user.email = new_email
    await session.commit()
    return True


# Работа с категориями

@connection
async def add_category(session, category_name):
    category = await session.scalar(select(ProblemCategory).where(ProblemCategory.category_name == category_name))

    if category:
        return False

    session.add(ProblemCategory(category_name=category_name))
    await session.commit()
    return True


@connection
async def edit_problem_category_name(session, category, new_category_name):
    category = await session.scalar(select(ProblemCategory).where(ProblemCategory.id == category))
    if not category:
        return False
    category.category_name = new_category_name
    await session.commit()
    return True


@connection
async def save_report_problem_user(session, tg_id, description, image, adress, category_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        return

    await session.scalar(select(HistoryAtBidUser).where(HistoryAtBidUser.user_id == user.id))
    session.add(HistoryAtBidUser(description=description, image=image,
                                     adress=adress, problem_category_id=category_id, user_id=user.id))
    await session.commit()


@connection
async def delete_report_problem_user(session, tg_id, category_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return

    delete_problem = await session.scalar(
        select(HistoryAtBidUser).where(
            HistoryAtBidUser.user_id == user.id,  # если у тебя есть user_id
            HistoryAtBidUser.problem_category_id == category_id
        )
    )

    if delete_problem:
        await session.delete(delete_problem)
        await session.commit()


@connection
async def get_report_problem(session):
    return await session.scalars(select(HistoryAtBidUser))


@connection
async def get_report_problem_id(session, category_id):
    return await session.scalar(select(HistoryAtBidUser).where(HistoryAtBidUser.problem_category_id == category_id))


@connection
async def get_categories(session):
    return await session.scalars(select(ProblemCategory))