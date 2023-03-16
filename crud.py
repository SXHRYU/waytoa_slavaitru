import db
import models
from env import CONTESTS, PROBLEMS, TAGS


async def add_problems_to_db(
    problemset: set[models.Problem], db_handle: db.DatabaseHandle
) -> set[models.Problem]:
    for problem in problemset:
        await db_handle.insert(table=PROBLEMS, **problem.__dict__)
    return problemset


async def add_contests_to_db(
    contestset: set[models.Contest], db_handle: db.DatabaseHandle
) -> set[models.Contest]:
    for contest in contestset:
        await db_handle.insert(table=CONTESTS, **contest.__dict__)
    return contestset


async def add_tags_to_db(
    tagset: set[models.Tag], db_handle: db.DatabaseHandle
) -> set[models.Tag]:
    for tag in tagset:
        await db_handle.insert(table=TAGS, **tag.__dict__)
    return tagset


async def get_tags(db_handle: db.DatabaseHandle, **values) -> tuple[models.Tag]:
    return await db_handle.select(table=TAGS, **values)


async def get_problems(db_handle: db.DatabaseHandle, **values) -> tuple[models.Problem]:
    return await db_handle.select(table=PROBLEMS, **values)
