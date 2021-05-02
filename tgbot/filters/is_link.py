from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsLinkForSearch(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        link = message.text.lower().strip()
        return 'instagram.com/' in link or 'vk.com/' in link
