import uuid
from datetime import datetime, timedelta

from aiohttp import ClientError, ClientTimeout, ClientSession
from loguru import logger

from tgbot.config import QIWI_WALLET_TOKEN


class QIWI:
    """
    Класс для взаимодействия с API
    """
    _TOKEN = QIWI_WALLET_TOKEN
    _HEADERS = {'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {_TOKEN}'}
    _timeout = ClientTimeout(total=3 * 15, connect=15, sock_connect=None, sock_read=None)
    _session = ClientSession(timeout=_timeout)
    __instance = None

    def __new__(cls, *args, **kwargs):
        logger.debug(f'\n\nWALLET START UP\n\n')
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    async def _request(self, method, request_url, **kwargs):
        try:
            async with self._session.request(method=method, url=request_url, headers=kwargs.get('headers'),
                                             ssl_context=kwargs.get('ssl_context'),
                                             params=kwargs.get('params'),
                                             data=kwargs.get('data'),
                                             json=kwargs.get('json')
                                             ) as response:
                return await self._response(response)
        except ClientError as e:
            raise ClientError(e)

    async def _response(self, response):
        if response.status in [200, 201]:
            try:
                response_json = await response.json()
                logger.debug(f'\n\nJSON RESPONSE {response_json}\n\n')
                return response_json
            except AttributeError:
                logger.debug(f'!!!!!!! ERROR RESPONSE !!!!!!!')
                pass
        else:
            logger.error(f'\n\n!!!!!!! ERROR RESPONSE !!!!!!! {response}\n\n')

    async def create_invoice(self, value: int, billid: str = None, **kwargs) -> dict:
        if billid is None:
            billid = uuid.uuid4()
        logger.debug(f'\n\nTRY CREATE INVOCE\n\n')
        method = 'put'
        request_url = f'https://api.qiwi.com/partner/bill/v1/bills/{billid}'
        json_data = dict()
        json_data['amount'] = {'value': value, 'currency': 'RUB'}
        expirationDateTime = datetime.now() + timedelta(hours=1)
        json_data['expirationDateTime'] = expirationDateTime.strftime('%Y-%m-%dT%H:%m:%S+00:00')
        json_data.update(kwargs)
        r = await self._request(method, request_url, headers=self._HEADERS, json=json_data)
        logger.debug(f'\n\nR is {r}\n\n')
        return r

    async def check_invoice(self, billid: str) -> dict:
        method = 'get'
        request_url = f'https://api.qiwi.com/partner/bill/v1/bills/{billid}'
        return await self._request(method, request_url, headers=self._HEADERS)
