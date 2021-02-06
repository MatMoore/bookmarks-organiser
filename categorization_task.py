"""
Turn bookmark export files into a set of categorization tasks.
Each task presents the bookmark and requires the user to select a category.
Tasks and responses are stored in a SQLite database.
"""

from typing import NamedTuple
from typing import List, Optional
import json


class CategorizationTask(NamedTuple):
    task_id: int
    description: str
    options: List[str]
    category: Optional[str]


class CategorizationTaskStore:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_task(self, description, options):
        self.cursor.execute(
            """
            insert into categorization_task (description, options) values (:description, :options)
            """,
            {"description": description, "options": json.dumps(options)},
        )

        return CategorizationTask(
            task_id=self.cursor.lastrowid,
            description=description,
            options=options,
            category=None,
        )

    def load_tasks(self):
        self.cursor.execute(
            """
            select ROWID, description, options, category from categorization_task
            """
        )

        result = []
        for row in self.cursor.fetchall():
            result.append(
                CategorizationTask(
                    task_id=row["ROWID"],
                    description=row["description"],
                    options=json.loads(row["options"]),
                    category=row["category"],
                )
            )
        return result

    def save_result(self, task_id, result):
        self.cursor.execute(
            """
            update categorization_task set category=:result where ROWID=:task_id
            """,
            {"task_id": task_id, "result": result},
        )

    def create_schema(self):
        self.cursor.execute(
            """
            create table if not exists categorization_task (
              description text not null,
              options text not null,
              category text
            );
            """
        )


class BookmarkSortingTaskFormulator:
    @staticmethod
    def from_pocket_export(filename):
        pass


if __name__ == "__main__":
    import sqlite3

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = CategorizationTaskStore(conn.cursor())
    store.create_schema()
    print(store.create_task(description="desc", options=["a", "b", "c"]))
    print(store.create_task(description="desc2", options=["a2", "b2", "c2"]))
    store.save_result(1, "c")
    print(store.load_tasks())
