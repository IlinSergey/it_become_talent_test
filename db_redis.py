import redis

redis_connect = redis.Redis(host='localhost', port=6379, decode_responses=True)


def save_user(user_id: int, username: str) -> None:
    redis_connect.set(user_id, username)


def check_user(user_id: int) -> int:
    return redis_connect.exists(user_id)


def get_username(user_id: int) -> str:
    return redis_connect.get(user_id)


def save_url(username: str, url: str) -> None:
    redis_connect.set(username, url)


def get_all_users() -> list:
    users_list = redis_connect.keys()
    return users_list


def get_url(username: str) -> str:
    url = redis_connect.get(username)
    return url
