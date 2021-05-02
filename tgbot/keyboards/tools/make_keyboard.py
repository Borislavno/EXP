from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


async def make_inline_keyboard(buttons: list, row_width: int = 3, method: str = 'add'):
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    if len(buttons) >= 1:
        if method == 'add':
            for button in buttons:
                keyboard.add(
                    InlineKeyboardButton(text=button[0], callback_data=button[1])
                )
        elif method == 'insert':
            for button in buttons:
                keyboard.insert(
                    InlineKeyboardButton(text=button[0], callback_data=button[1])
                )
        elif method == 'row':
            for button in buttons:
                keyboard.row(
                    InlineKeyboardButton(text=button[0], callback_data=button[1])
                )
    return keyboard


async def make_reply_keyboard(buttons: list, resize_keyboard: bool = True, one_time_keyboard: bool = None,
                              selective: bool = None, row_width: int = 2, method: str = 'add'):
    keyboard = ReplyKeyboardMarkup(None, resize_keyboard, one_time_keyboard, selective, row_width)
    if len(buttons) >= 1:
        if method == 'add':
            for button in buttons:
                keyboard.add(
                    KeyboardButton(text=button)
                )
        elif method == 'insert':
            for button in buttons:
                keyboard.insert(
                    KeyboardButton(text=button)
                )
        elif method == 'row':
            for button in buttons:
                keyboard.row(
                    KeyboardButton(text=button)
                )
    return keyboard
