from dataclasses import dataclass
from environs import Env
from typing import Union


@dataclass
class TgBot:
    token: str    # Токен для доступа к боту
    admin_id: int


@dataclass
class Config:
    tg_bot: TgBot


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('TOKEN'),
            admin_id=env('ADMIN')
        )
    )
