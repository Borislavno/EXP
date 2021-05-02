from typing import Dict

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputFile, MediaGroup
from loguru import logger

from tgbot import config
from tgbot.API.parser import Parser
from tgbot.filters.is_link import IsLinkForSearch
from tgbot.keyboards.tools.cb_data import search_pay_cb, show_pay_cb
from tgbot.loader import dp, Wallet
from tgbot.utils.user_data import save_data, get_fund_photos


@dp.message_handler(CommandStart())
async def start_handler(message: types.Message):
    text = 'Привет, я бот, который находит интимные материалы людей\n\n' \
           '🔥 Для того чтобы посмотреть интимные материалы пользователя, ' \
           'просто скинь ссылку на его аккаунт Instagram или ВКонтакте🔥'
    await message.answer(text, disable_web_page_preview=True)


@dp.message_handler(IsLinkForSearch(), content_types=types.ContentTypes.TEXT)
async def get_link_handler(message: types.Message, state: FSMContext):
    if payment := await Wallet.create_invoice(value=config.SEARCH_COST):
        link = message.text.lower().strip()[:128]
        if 'vk.com' in link:
            if parsing_data := await Parser.parsing_vk(link):
                return await Parser.check_parser(parsing_data)
        if 'instagram.com/' in link:
            if parsing_data := await Parser.parsing_vk(link):
                return await Parser.check_parser(parsing_data)
        if parsing_data != None:
            await save_data(state, link, payment['billId'])
            text = f'{parsing_data}' \
                   f'🎁Чтобы проверить пользователя оплатите: {config.SEARCH_COST} р\n' \
                   f'Для оплаты перейдите по кнопке "Перейти к оплате", ' \
                   f'далее нажмите "Оплатил"'
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Перейти к оплате', url=payment['payUrl'])],
                    [InlineKeyboardButton(text='Оплатил', callback_data=search_pay_cb.new(uuid=payment['billId']))],
                ]
            )
        if parsing_data == None:
            text = 'К сожалению, ничего не найдено. Попробуйте еще раз.'
            keyboard = None
    else:
        text = 'К сожалению, сервис в настоящий момент недоступен. Попробуйте позднее.'
        keyboard = None
    logger.debug(f'\n\n{payment}\n\n')
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(search_pay_cb.filter())
async def check_payment_handler(call: CallbackQuery, callback_data: Dict[str, str], state: FSMContext):
    bill_id = callback_data['uuid']
    bill = await Wallet.check_invoice(bill_id)
    if bill and bill['status']['value'] == 'PAID':
        if photos := await get_fund_photos(state, bill['billId']):
            album = MediaGroup()
            for photo in photos:
                album.attach_photo(InputFile(f'{config.PHOTOS_BLUR}/{photo}.jpg'))
            await call.message.answer_media_group(media=album)

            if payment := await Wallet.create_invoice(value=config.SHOW_COST):
                count = len(photos)
                text = f'Найдено {count} фотографий.\n' \
                       f'🎁Чтобы получить качественное изображение оплатите: {config.SHOW_COST} рублей!'
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='Перейти к оплате', url=payment['payUrl'])],
                        [InlineKeyboardButton(text='Оплатил', callback_data=show_pay_cb.new(uuid=payment['billId']))],
                    ]
                )
            else:
                text = 'К сожалению, сервис в настоящий момент недоступен. Попробуйте позднее.'
                keyboard = None
        else:
            text = 'Ничего не найдено. Попробуй поискать по другому пользователю.\n' \
                   'Кидай ссылку пользователя в формате vk.com/***** или instagram.com/*****'
            keyboard = None
    elif bill:
        text = 'Оплата не прошла'
        await call.message.answer(text)

        photos = await get_fund_photos(state, bill['billId'])
        count = len(photos)
        text = f'Найдено {count} фотографий.\n' \
               f'🎁Чтобы получить качественное изображение оплатите: {config.SHOW_COST} рублей!'
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Перейти к оплате', url=bill['payUrl'])],
                [InlineKeyboardButton(text='Оплатил', callback_data=search_pay_cb.new(uuid=bill['billId']))],
            ]
        )
    else:
        text = 'К сожалению, сервис в настоящий момент недоступен. Попробуйте позднее.'
        keyboard = None
    await call.message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)


@dp.callback_query_handler(show_pay_cb.filter())
async def check_show_payment_handler(call: CallbackQuery, callback_data: Dict[str, str], state: FSMContext):
    bill_id = callback_data['uuid']
    bill = await Wallet.check_invoice(bill_id)
    if bill and bill['status']['value'] == 'PAID':
        data = await state.get_data()
        photos = data['user_bills'][bill_id]['photos']
        album = MediaGroup()
        for photo in photos:
            album.attach_photo(InputFile(f'{config.PHOTOS_UNBLUR}/{photo}.jpg'))
        await call.message.answer_media_group(album)

        text = 'Все результаты,что можем тебе предоставить\n' \
               'Кидай ссылку пользователя в формате vk.com/***** или instagram.com/*****, чтобы получить больше фото.'
        keyboard = None
    elif bill:
        text = 'Оплата не прошла.'
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Перейти к оплате', url=bill['payUrl'])],
                [InlineKeyboardButton(text='Оплатил', callback_data=show_pay_cb.new(uuid=bill['billId']))],
            ]
        )
    else:
        text = 'К сожалению, сервис в настоящий момент недоступен. Попробуйте позднее.'
        keyboard = None
    await call.message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)


@dp.message_handler()
async def no_handlers(message: types.Message):
    text = 'Введи ссылку VK или INSTAGRAM в формате vk.com/***** или instagram.com/*****\n' \
           'И я покажу, интимные фото пользователя.'
    await message.answer(text, disable_web_page_preview=True)
