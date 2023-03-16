import asyncio
import httpx


def get_URL(page_num: int) -> str:
    return f"https://codeforces.com/problemset/page/{page_num}?order=BY_RATING_DESC&locale=ru"


async def fetch(client: httpx.AsyncClient, page_num: int):
    response = await client.get(get_URL(page_num))
    if response.status_code != 200:
        return response.raise_for_status()
    return response.text


async def fetch_all(client: httpx.AsyncClient, pages: int):
    tasks = []
    for page in range(1, pages + 1):
        task = asyncio.create_task(fetch(client, page))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res
