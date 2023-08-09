import asyncio
from datetime import datetime

import aiofiles
import aiohttp

from db_redis import get_all_users, get_url, get_username


async def ping_url(url: str):
    '''
    Отсылаем запрос на URL и возврвщвем код ответа
    '''
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'http://{url}') as response:
                return response.status
        except Exception as e:
            print(e)


async def save_result_to_file(user, result):
    '''
    Записываем результат ping url в файл
    '''
    username = get_username(user)
    url = get_url(username)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    async with aiofiles.open(f'data/ping_results_{user}.txt', mode='a', buffering=1) as file:
        await file.write(f'[{timestamp}] url: {url}, status code: {result}\n')


async def get_result(user) -> list:
    '''
    Читаем все записи по результатам пинга и возвращаем последние 5
    '''
    results = []
    try:
        async with aiofiles.open(f'data/ping_results_{user}.txt', mode='r', buffering=1) as file:
            results = await file.readlines()
    except FileNotFoundError:
        pass
    return results[-5:]


async def pings():
    ''''
    Для всех пользователей, проверяем наличие записи с URL,
    если URL, пингуем и сохраняем результат
    '''
    users = get_all_users()
    ping_tasks = []

    for user in users:
        username = get_username(user)
        url = get_url(username)
        if url:
            ping_task = asyncio.create_task(ping_url(url))
            ping_tasks.append((user, ping_task))

    for user, ping_task in ping_tasks:
        result = await ping_task
        await save_result_to_file(user=user, result=result)


async def run_pings():
    '''
    Запускаем пинг url на постоянное основе
    '''
    while True:
        await pings()
        await asyncio.sleep(60)
