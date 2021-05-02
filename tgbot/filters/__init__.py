from aiogram import Dispatcher

from .is_link import IsLinkForSearch


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsLinkForSearch, event_handlers=[dp.message_handlers])
