import sqlite3
from typing import Any


class DBInterface:
    @classmethod
    def execute_query(
        cls, query: str, params: tuple = (), db_path: str = "app/ai_db.sqlite"
    ) -> str:
        print(query)
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if query.strip().lower().startswith("select"):
                    rows = cursor.fetchall()
                    result = "\n".join([str(row) for row in rows])
                else:
                    conn.commit()
                    result = (
                        f"Query executed successfully. Rows affected: {cursor.rowcount}"
                    )
                print(result)
                return result
        except Exception as e:
            return f"DB error: {e}"

    @classmethod
    def get_commands(cls):
        commands = {"execute_query": cls.execute_query}
        return commands
