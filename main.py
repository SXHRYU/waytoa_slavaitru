import asyncio
import httpx
import crud
import db
import fetching
import models
import parsing


HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


async def main():
    base_html = httpx.get(fetching.get_URL(1)).text
    page_count = parsing.get_page_count(base_html)

    async with httpx.AsyncClient(headers=HEADERS) as client:
        htmls = await fetching.fetch_all(client, page_count)

    db_handle = db.DatabaseHandle()

    problems: set[models.Problem] = set()
    for index, html in enumerate(htmls):
        problemset = parsing.get_problemset(html)
        for problem in problemset:
            problems.add(problem)
        print(f"Page {index+1} done.")
    tags: set[models.Tag] = parsing.get_tagset(html)

    _tags_in_db = await crud.get_tags(db_handle)
    tags_in_db = []
    for tag in _tags_in_db:
        tags_in_db.append(models.Tag(id=tag[0], name=tag[1]))
    tags_not_in_db = tags.difference(tags_in_db)
    await crud.add_tags_to_db(tags_not_in_db, db_handle)

    problems_in_db = set([i for i in await crud.get_problems(db_handle)])
    problems_to_add_in_db = set()
    for problem in problems:
        problems_to_add_in_db.add(problem.id)
    problems_not_in_db = problems_to_add_in_db.difference(problems_in_db)

    
    await crud.add_problems_to_db(problems_not_in_db, db_handle)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
