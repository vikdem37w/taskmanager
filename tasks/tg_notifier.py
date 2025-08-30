from environs import Env
from aiogram import Bot, Dispatcher, F
import asyncio
import requests

env = Env()
env.read_env()

TELEGRAM_KEY = env("TELEGRAM_KEY")

async def main():
    pass

if __name__ == "__main__":
    main()