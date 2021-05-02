from aiogram.utils import exceptions
from loguru import logger

from tgbot.loader import dp
from tgbot.utils import send_messages
from tgbot.config import TG_ADMINS_ID


@dp.errors_handler(exception=exceptions.TelegramAPIError)
async def retry_after_error(update, exception):
    logger.exception(f'\n\n WARNING TG Exception: {exception} \nUpdate: {update}\n\n')
    await send_messages(TG_ADMINS_ID[0], f'WARNING TG Exception: {exception} \nUpdate: {update}')
    return True
