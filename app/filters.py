from aiogram.filters import Filter
from aiogram.types import Message

ADMINS = [1870291778]


class ProtectAdmin(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins
