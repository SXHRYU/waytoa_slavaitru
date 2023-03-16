import io
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_files import keyboards as kb
import db
import models
from crud import get_problems, get_tags


class FSMProblemChoose(StatesGroup):
    tag = State()
    difficulty = State()
    problem = State()

    async def problem_choose_cmd(message: types.Message):
        await FSMProblemChoose.tag.set()
        await message.reply("Укажите тему задачи.", reply_markup=kb.navigation_kb)
        tags: list[models.Tag] = await get_tags(db.DatabaseHandle())
        formatted_tags = io.StringIO()
        for tag in tags:
            formatted_tags.write("●" + tag[1] + ";\n")
        formatted_tags.seek(0)

        await message.answer(f"Темы:\n{''.join(formatted_tags.readlines())}")

    async def problem_choose_tag(message: types.Message, state: FSMContext):
        tags: list[models.Tag] = await get_tags(db.DatabaseHandle())
        if message.text == "Отменить":
            await message.reply(
                "Меню.",
                reply_markup=kb.menu_kb
            )
            await state.finish()
        else:
            problems: list[models.Problem] = await get_problems(db.DatabaseHandle())
            difficulties: list[int] = sorted(list(set([i[4] for i in problems])))
            formatted_diffs = io.StringIO()
            for diff in difficulties:
                formatted_diffs.write("●" + str(diff) + ";\n")
            formatted_diffs.seek(0)

            await message.answer(f"Сложности:\n{''.join(formatted_diffs.readlines())}")

            async with state.proxy() as data:
                data["tags"] = [i[1] for i in tags]
                data["tag"] = message.text
                if data["tag"] not in data["tags"]:
                    await message.reply(
                        'Нет такой темы. Попробуйте ещё раз или нажмите "Отменить".'
                    )
                else:
                    await FSMProblemChoose.next()
                    await message.reply(
                        f"Вы выбрали тему '{message.text}'.\nВыберите сложность.",
                        reply_markup=kb.navigation_kb,
                    )

    async def problem_choose_difficulty(message: types.Message, state: FSMContext):
        if message.text == "Отменить":
            await message.reply(
                "Меню.",
                reply_markup=kb.menu_kb
            )
            await state.finish()
        else:
            problems: list[models.Problem] = await get_problems(db.DatabaseHandle())
            difficulties: list[int] = set([i[4] for i in problems])
            async with state.proxy() as data:
                data["diffs"] = difficulties
                data["problems"] = problems
                data["diff"] = int(message.text)
                if data["diff"] not in data["diffs"]:
                    await message.reply(
                        "Нет такой сложности. Попробуйте ещё раз или нажмите Отменить."
                    )
                else:            
                    await message.reply(
                        f"Вы выбрали тему \"{data['tag']}\" и сложность {data['diff']}.\nЗадачи подходящие под эти параметры:",
                    )
                    problems = tuple(
                        filter(lambda i: i[4] == data["diff"], data["problems"])
                    )
                    formatted_problems = io.StringIO()
                    for problem in problems:
                        formatted_problems.write(
                            f'●<a href="{problem[-1]}">{problem[3]}</a>;\n'
                        )
                    formatted_problems.seek(0)
                    await message.answer(f"Сложности:\n{''.join(formatted_problems.readlines())}")
                    await FSMProblemChoose.next()

    async def problem_choose_problem(message: types.Message, state: FSMContext):
        await message.reply("Меню", reply_markup=kb.navigation_kb)
        await state.finish()


def register_FSM_handlers(dp: Dispatcher):
    # fmt: off
    dp.register_message_handler(
        FSMProblemChoose.problem_choose_cmd, text="Выбрать задачу", state=None)
    dp.register_message_handler(
        FSMProblemChoose.problem_choose_tag, state=FSMProblemChoose.tag)
    dp.register_message_handler(
        FSMProblemChoose.problem_choose_difficulty, state=FSMProblemChoose.difficulty)
    dp.register_message_handler(
        FSMProblemChoose.problem_choose_problem, state=FSMProblemChoose.problem)
    # fmt: on
