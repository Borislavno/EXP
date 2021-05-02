import random

from aiogram.dispatcher import FSMContext
from loguru import logger


async def is_has_photo() -> int:
    return random.randint(0, 5)


async def get_blur_photos(count: int) -> list:
    return random.sample(range(1, 51), count)


async def save_data(state: FSMContext, link: str, bill_id: str):
    data: dict = await state.get_data()
    links: dict = data.get('links') or dict()
    user_bills: dict = data.get('user_bills') or dict()
    logger.debug(f'\n\n'
                 f'data {type(data)} {data}\n'
                 f'links {type(links)} {links}\n'
                 f'user_bills {type(user_bills)} {user_bills}'
                 f'\n\n')
    if user_bills:
        if old_bill_id := links.get(link):
            logger.debug(f'\nold_bill_id {old_bill_id}\n')
            old_bill = user_bills[old_bill_id]
            logger.debug(f'\nold_bill {type(old_bill)} {old_bill}\n')
            user_bills[bill_id] = {
                'link': link,
                'fund_count': old_bill.get('fund_count'),
                'photos': old_bill.get('photos')
            }
            logger.debug(f'\nuser_bills {type(user_bills)} {user_bills}\n')
        else:
            links.update({link: bill_id})
    else:
        user_bills[bill_id] = {
            'link': link,
            'fund_count': None,
            'photos': []
        }
        links.update({link: bill_id})
    logger.debug(f'\nsave \n'
                 f'{type(links)} {links}\n'
                 f'{type(user_bills)} {user_bills}')
    await state.update_data(links=links, user_bills=user_bills)


async def get_fund_photos(state: FSMContext, bill_id: str) -> list:
    data: dict = await state.get_data()
    user_bills: dict = data['user_bills']
    bill_data: dict = user_bills[bill_id]
    logger.debug(f'\n\nBILL DATA {bill_data}\n\n')
    if bill_data['fund_count'] is None:
        bill_data['fund_count'] = await is_has_photo()
        logger.debug(f'\n\nfund_count {bill_data["fund_count"]}\n\n')
        if bill_data['fund_count']:
            bill_data['photos'] = await get_blur_photos(bill_data['fund_count'])
            logger.debug(f'\n\nphotos updated { bill_data["photos"]}\n\n')
        user_bills.update(bill_data)
        await state.update_data(user_bills=user_bills)
        return bill_data['photos']
    elif bill_data['photos']:
        return bill_data['photos']
