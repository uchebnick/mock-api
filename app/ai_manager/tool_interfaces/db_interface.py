import sqlite3
from typing import Any

class DBInterface:
    def __init__(self, db_path: str = 'app/db.sqlite3'):
        self.db_path = db_path

    def execute_query(self, query: str, params: tuple = ()) -> str:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if query.strip().lower().startswith("select"):
                    rows = cursor.fetchall()
                    result = '\n'.join([str(row) for row in rows])
                else:
                    conn.commit()
                    result = f"Query executed successfully. Rows affected: {cursor.rowcount}"
                return result
        except Exception as e:
            return f"DB error: {e}"

    def get_commands(self):
        commands = {
            "execute_query": self.execute_query
        }
        return commands


