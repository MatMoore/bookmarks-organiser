import requests
import sqlite3
from bs4 import BeautifulSoup
from categorization_task import CategorizationTaskStore

with sqlite3.connect("tasks.db") as conn:
    conn.row_factory = sqlite3.Row
    store = CategorizationTaskStore(conn.cursor())

    for i, task in enumerate(store.load_tasks(include_completed=True)):
        if i % 100 == 0:
            conn.commit()

        metadata = task.metadata

        if "description" in metadata:
            continue

        url = metadata["href"]
        print(url)

        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            continue

        dom = BeautifulSoup(response.text, "html.parser")
        description = dom.find("meta", attrs={"name": "description"})
        content = description.get("content") if description else ""

        if not content or len(content) > 1000:
            continue

        metadata["description"] = content
        store.update_metadata(task.task_id, metadata)
