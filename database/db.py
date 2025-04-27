import enum
import os
from typing import List, Optional

import psycopg2
import psycopg2.extras
import psycopg2.sql as pgsql


psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)


def sql_fetchall(sql: str, args: Optional[tuple] = None) -> List[dict]:
    with psycopg2.connect(os.getenv("DB")) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            result = cur.fetchall()
            return [
                dict(zip(map((lambda x: x.name), cur.description), i)) for i in result
            ]


def sql_fetchone(sql: str, args: Optional[tuple] = None) -> Optional[dict]:
    with psycopg2.connect(os.getenv("DB")) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            result = cur.fetchone()
            if result is None:
                return
            return dict(zip(map((lambda x: x.name), cur.description), result))


class DatabaseStore(enum.Enum):
    users = "users"
    action = "action"

    def get_key(self, key) -> str:
        return f"{self.value}|{key}"

    def _get_by_key(self, key: str):
        result = sql_fetchone(
            "select value from kv where key = %s;",
            (self.get_key(key),),
        )
        return result

    def get_by_key(self, key: str | int):
        result = self._get_by_key(str(key))
        if result is None:
            return
        return {"key": key, **result["value"]}

    # def get_all(self):
    #     return sql_fetchall("select * from {};".format(pgsql.Identifier(self.value)))

    def upsert(self, key: str, value: dict) -> str:
        return self._upsert(key, value)

    def _upsert(self, key: str, value: dict) -> str:
        with psycopg2.connect(os.getenv("DB")) as conn:
            with conn.cursor() as cur:
                sql = pgsql.SQL(
                    """
                        insert into kv(key, value) 
                        values (%s ,%s)
                        on conflict (key) do update 
                        set value = excluded.value
                        returning key;
                    """
                )
                cur.execute(
                    sql,
                    (
                        self.get_key(key),
                        value,
                    ),
                )
                return cur.fetchone()[0]
