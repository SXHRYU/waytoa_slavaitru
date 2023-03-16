from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bot_files.handlers import FSM_handlers, general_handlers
from env import BOT_TOKEN
import asyncio


storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


# Registers all the handlers defined in bot_files package.
FSM_handlers.register_FSM_handlers(dp)
general_handlers.register_general_handlers(dp)


async def on_startup(_):
    """Prints to stdout when the bot has started, passing by the logs."""
    return print("Bot started.")


async def on_shutdown(_):
    """Prints to stdout when the bot has stopped, passing by the logs."""
    return print("Bot stopped.")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )
