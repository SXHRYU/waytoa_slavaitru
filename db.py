from typing import Sequence
import psycopg
from env import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)


class DatabaseHandle:
    aconn: psycopg.AsyncConnection = psycopg.AsyncConnection

    def __init__(
        self,
        host: str = DB_HOST,
        db_name: str = DB_NAME,
        db_password: str = DB_PASSWORD,
        db_port: int = DB_PORT,
        db_user: str = DB_USER,
    ) -> None:
        self.host = host
        self.dbname = db_name
        self.password = db_password
        self.port = db_port
        self.user = db_user


    async def insert(self, *, table: str, **values):
        item = ValueNormaliser.normalise(values)
        if isinstance(item, Sequence):
            for value in item:
                async with await self.aconn.connect(**self.__dict__) as aconn:
                    async with aconn.cursor() as acur:
                        await acur.execute(
                            f'INSERT INTO {table} ({", ".join(value.keys())}) VALUES {tuple(value.values())} RETURNING *;'
                        )
        else:
            async with await self.aconn.connect(**self.__dict__) as aconn:
                async with aconn.cursor() as acur:
                    await acur.execute(
                        f'INSERT INTO {table} ({", ".join(item.keys())}) VALUES {tuple(item.values())} RETURNING *;'
                    )

    async def select(self, *, table: str, **kwargs):
        # This leads to "SELECT * FROM WHERE True" to select all valeus.
        if not kwargs:
            kwargs = True
        async with await self.aconn.connect(**self.__dict__) as aconn:
            async with aconn.cursor() as acur:
                await acur.execute(f"SELECT * FROM {table} WHERE {kwargs};")
                return await acur.fetchall()


class ValueNormaliser:
    @classmethod
    def normalise(cls, item):
        items = []
        for key, value in item.items():
            if isinstance(value, Sequence):
                multiple_values = value.split(",")
                if len(multiple_values) > 1 and key != "name":
                    for m_value in multiple_values:
                        copy = {keys: items for keys, items in item.items()}
                        copy[key] = m_value
                        items.append(copy)
        if items:
            for item in items:
                for key, value in item.items():
                    if value is None:
                        item[key] = "NULL"
                    elif isinstance(value, str) and "'" in value:
                        item[key] = item[key].replace("'", "`")
            return items
        else:
            for key, value in item.items():
                if value is None:
                    item[key] = "NULL"
                elif isinstance(value, str) and "'" in value:
                    item[key] = item[key].replace("'", "`")
            return item