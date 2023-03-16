from aiogram import Dispatcher, types
from bot_files import keyboards as kb


# Handlers that don't use Finite State Machine (FSM),
# meaning these commands can be called independent of previous commands
# given that the caller has required rights and not in a FSM command.
async def show_menu_commands(message: types.Message):
    """Displays menu interface to the user.

    This can be invoked by typing either of "Меню" or "Menu" or any unregistered text.

    Returns
    -------
    Message : Awaitable
        Replies to user with the following message (<text>) and
        keyboard (<button>):
        <text>Меню
            <button>"Выбрать задачу"
            <button>"Помощь"

    Notes
    -----
    Everyone who has access to this bot can see the menu buttons.
    """
    await message.answer("Меню", reply_markup=kb.menu_kb)


async def get_help(message: types.Message):
    """Displays help message to the user.

    This can be invoked by typing either of the following:.
    "Help", "Помощь", "/start", "/help"

    Notes
    -----
    Everyone who has access to this bot can see the help message.
    """
    await message.answer(
        # from `help.html`
        (
            "🤖<b>Бот для получения задач CodeForces.</b>\n\n"
            + "<u>Возможные команды:</u>\n"
            + "📄<code>Меню/Menu</code> - команда для перехода в главное меню. Также можно ввести любое сообщение для вывода меню.\n"
            + "🧠<code>Выбрать задачу</code> - команда для выбора задачи по теме и сложности.\n"
            + "❓<code>Помощь/Help</code> - команда для вывода данного сообщения.\n"
        ),
        parse_mode="HTML",
    )


def register_general_handlers(dp: Dispatcher):
    dp.register_message_handler(show_menu_commands, text=["Меню", "Menu"])
    dp.register_message_handler(get_help, commands=["start", "help"])
    dp.register_message_handler(get_help, text=["Помощь", "Help"])
    dp.register_message_handler(show_menu_commands)
