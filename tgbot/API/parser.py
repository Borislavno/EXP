from aiohttp import ClientTimeout, ClientSession, ClientError
from bs4 import BeautifulSoup
from loguru import logger


class Parser:
    _HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    _timeout = ClientTimeout(total=2 * 2, connect=15, sock_connect=None, sock_read=None)
    _session = ClientSession(timeout=_timeout)
    __instance = None

    def __new__(cls, *args, **kwargs):
        # logger.debug(f'\n\nWALLET START UP\n\n')
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
                # logger.debug(f'\n\nJSON RESPONSE {response_json}\n\n')
                return response_json
            except AttributeError:
                logger.debug(f'!!!!!!! ERROR RESPONSE !!!!!!!')
                pass
            except:
                response_text = await response.text()
                return response_text
        else:
            return None

    async def parsing_instagram(self, link: str):
        if link[-1] == '/':
            request_url = f'https://{link}?__a=1'
        else:
            request_url = f'https://{link}/?__a=1'
        method = 'get'
        r = await self._request(method, request_url, headers=self._HEADERS)
        return r

    async def parsing_vk(self, link: str):
        request_url = 'http://' + link
        method = 'get'
        r = await self._request(method, request_url, headers=self._HEADERS)
        return r

    async def check_parser(self, answer):
        if type(answer) == dict:
            user = answer['graphql']['user']['username']
            name = answer['graphql']['user']['full_name']
            biography = answer['graphql']['user']['biography']
            text = f'Пользователь: {user}\nИмя пользователя: {name}\nО себе: {biography}'
            return text
        if type(answer) == str:
            pars = BeautifulSoup(answer, 'html.parser')
            parsed = pars.find_all('title')
            text = ''
            for one in parsed:
                text = text + str(one)
            end = len(text) - 20
            text = f'Пользователь {text[7:int(end)]}'
            return text
