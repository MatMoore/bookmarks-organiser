"""
For a categorization task the user has to select a category from a set of options.
Tasks and responses are stored in a SQLite database.
"""

from typing import NamedTuple
from typing import List, Optional
import json


class CategorizationTask(NamedTuple):
    task_id: int
    description: str
    metadata: str
    options: List[str]
    category: Optional[str]


class CategorizationTaskStore:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_task(self, description, options, metadata=None):
        metadata = metadata or {}
        self.cursor.execute(
            """
            insert into categorization_task (description, options, metadata) values (:description, :options, :metadata)
            """,
            {
                "description": description,
                "options": json.dumps(options),
                "metadata": json.dumps(metadata),
            },
        )

        return CategorizationTask(
            task_id=self.cursor.lastrowid,
            description=description,
            options=options,
            metadata=metadata,
            category=None,
        )

    def load_tasks(self, include_completed=False):
        if include_completed:
            self.cursor.execute(
                """
              select ROWID, description, options, category, metadata
              from categorization_task
              """
            )
        else:
            self.cursor.execute(
                """
              select ROWID, description, options, category, metadata
              from categorization_task
              where category is null
              """
            )

        result = []
        for row in self.cursor.fetchall():
            metadata = json.loads(row["metadata"]) if row["metadata"] else {}
            result.append(
                CategorizationTask(
                    task_id=row["ROWID"],
                    description=row["description"],
                    options=json.loads(row["options"]),
                    metadata=metadata,
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

    def update_metadata(self, task_id, metadata):
        self.cursor.execute(
            """
            update categorization_task set metadata=:metadata where ROWID=:task_id
            """,
            {"task_id": task_id, "metadata": json.dumps(metadata)},
        )

    def create_schema(self):
        self.cursor.execute(
            """
            create table if not exists categorization_task (
              description text not null,
              options text not null,
              category text,
              metadata text
            );
            """
        )


if __name__ == "__main__":
    import sqlite3

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    store = CategorizationTaskStore(conn.cursor())
    store.create_schema()
    print(store.create_task(description="desc", options=["a", "b", "c"]))
    print(store.create_task(description="desc2", options=["a2", "b2", "c2"]))
    store.save_result(1, "c")
    print(store.load_tasks(include_completed=True))
