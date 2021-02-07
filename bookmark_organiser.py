import random
import questionary
from questionary import Separator, Style
from categorization_task import CategorizationTaskStore
from work import WorkGenerator
import sqlite3


style = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", "fg:#FF9D00 bold"),
        ("question", ""),
        ("selected", "fg:#5F819D"),
        ("pointer", "fg:#FF9D00 bold"),
        ("answer", "fg:#5F819D bold"),
    ]
)


def prompt(store):
    for task in store.load_tasks():
        response = questionary.select(
            task.description,
            choices=task.options + [Separator(), "Skip", "Quit"],
            use_shortcuts=True,
            style=style,
        ).ask()

        if response == "Skip":
            continue

        if response is None or response == "Quit":
            break

        store.save_result(task.task_id, response)


def get_store(conn):
    conn.row_factory = sqlite3.Row
    store = CategorizationTaskStore(conn.cursor())
    store.create_schema()
    return store


def pocket_export(filename, store):
    generator = WorkGenerator(store)
    generator.from_pocket_export(filename)


if __name__ == "__main__":
    import sys

    with sqlite3.connect("tasks.db") as conn:
        store = get_store(conn)

        # pocket_export(sys.argv[1], store)

        prompt(store)
