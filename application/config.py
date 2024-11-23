from pydantic import BaseModel

from application.env import Env


class AppConfig(BaseModel):
    env: Env

    class Config:
        arbitrary_types_allowed = True


def state() -> AppConfig:
    env = Env()
    return AppConfig(env=env)
