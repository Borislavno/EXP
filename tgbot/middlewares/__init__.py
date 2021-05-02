from aiogram import Dispatcher
from loguru import logger

from .authentification import AccessMiddleware
from .call_answer import CallCacheTime
from .autoremove import AutoRemoveMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(AccessMiddleware())
    dp.middleware.setup(CallCacheTime())
    dp.middleware.setup(AutoRemoveMiddleware())
    logger.info('Middlewares are successfully configured')
