from environs import Env
from pyrogram import Client, filters

from db_redis import check_user, save_url, save_user
from utils import get_result, run_pings

env = Env()
env.read_env()

api_id = env('API_ID')
api_hash = env('API_HASH')
bot_token = env('BOT_TOKEN')


app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token,
)


@app.on_message(filters.command('start'))
async def start_command(client, message):
    user = message.from_user
    save_user(user_id=user.id, username=user.username)
    await message.reply_text(f'Привет {user.username}')


@app.on_message(filters.command('help'))
async def help_command(client, message):
    help_text = '''
/start - начать работу с ботом
/set - установить url для пингования (в формате сайт.рф (без http://))
/list - вывести последние 5 рузультатов
/help - справка
'''
    await message.reply_text(help_text)


@app.on_message(filters.command('set'))
async def set_command(client, message):
    user = message.from_user
    if not check_user(user.id):
        save_user(user_id=user.id, username=user.username)
    args = message.text.split(' ', 1)
    if len(args) < 2:
        await message.reply_text('Используйте команду так: /set <URL>')
        return
    url = args[1]
    save_url(username=user.username, url=url)
    await message.reply_text(f'URL {url} сохранен!')


@app.on_message(filters.command('list'))
async def list_command(client, message):
    user = message.from_user
    ping_list = await get_result(user.id)
    result = ''.join(ping_list)
    await message.reply_text('Вот последние результаты:')
    await message.reply_text(result)


async def main():
    await app.start()
    await run_pings()
    await app.stop()


if __name__ == '__main__':
    app.run(main())
