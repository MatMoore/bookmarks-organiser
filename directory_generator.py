import sqlite3
import sys
from string import Template
from categorization_task import CategorizationTaskStore

link_template = Template(
    """## [$link_text]($link_href)
$link_description"""
)


def format_link_description(description):
    description = description.strip()

    if not description:
        return ""

    paragraphs = description.strip().split("\n\n")
    quotes = [f"> {p}" for p in paragraphs]
    return "\n>\n".join(quotes) + "\n"


assert len(sys.argv) > 0
category = sys.argv[1]

with sqlite3.connect("tasks.db") as conn:
    conn.row_factory = sqlite3.Row
    store = CategorizationTaskStore(conn.cursor())

    for task in store.fetch_tasks_by_category(category):
        link_text = task.description
        link_href = task.metadata["href"]
        link_description = format_link_description(task.metadata.get("description", ""))

        print(
            link_template.substitute(
                link_text=link_text,
                link_href=link_href,
                link_description=link_description,
            )
        )
