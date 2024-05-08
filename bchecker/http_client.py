from random import uniform

import httpx
from user_agent import generate_user_agent as user_agent

from .utils import Colors


class HttpClient(Colors):
    def __init__(self, proxy_url=None, timeout=uniform(10, 15)) -> None:
        self._base_agent = {"User-Agent": user_agent()}
        self._client = httpx.AsyncClient(
            headers=self._base_agent, proxy=proxy_url, timeout=timeout
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self._client.aclose()

    async def _build_request(self, method, url, **kwargs):
        try:
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPError as exc:
            raise RuntimeError(
                f"{type(exc).__name__}: {self.RED}{exc}{self.END}"
            ) from exc

    async def get(self, url, **kwargs):
        return await self._build_request("GET", url, **kwargs)

    async def post(self, url, **kwargs):
        return await self._build_request("POST", url, **kwargs)
