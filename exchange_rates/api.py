import aiohttp

from typing import Optional

from .config import config_api


class HTTPRequestError(Exception):
    pass


async def get_latest_exchange_rate_on_pair_btc_rub() -> Optional[float]:

    url = config_api.api_url.get_secret_value()
    key = config_api.api_key.get_secret_value()

    async with aiohttp.ClientSession(headers={'X-Api-Key': key}) as session:

        response = await session.get(url=url)

        if response.status == 200:
            response_json = await response.json()
            return response_json.get('exchange_rate')
        else:
            raise HTTPRequestError(f'HTTP request failed -> {response.status}')
