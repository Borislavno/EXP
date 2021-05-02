from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot import middlewares, filters
from tgbot.API.qiwi_wallet import QIWI
from tgbot.config import TGBOT_TOKEN
from tgbot.utils.logger import setup_logger

# Setup logging
setup_logger("DEBUG")

# Setup storage
storage = MemoryStorage()

# Setup bot
bot = Bot(token=TGBOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

# Setup middlewares
middlewares.setup(dp)

# Setup filters
filters.setup(dp)

# Setup Wallet
Wallet = QIWI()
