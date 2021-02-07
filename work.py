"""
Create tasks and store them in the database
Turn bookmark export files into a set of categorization tasks.
"""
from bs4 import BeautifulSoup


class WorkGenerator:
    CATEGORIES = [
        "Uncategorized non-tech",
        "Uncategorized tech",
        "Systems, maintainence, testing, delivery",
        "Tech industry, leadership, career advice",
        "Govtech",
        "Data",
        "Backend",
        "Frontend and accessibility",
        "Tools",
    ]

    def __init__(self, store):
        self.store = store

    def from_pocket_export(self, filename):
        with open(filename) as fp:
            soup = BeautifulSoup(fp, "html.parser")
            for anchor in soup.find_all("a"):
                tags = anchor["tags"]
                if tags:
                    description = f"{anchor.string} (tags: {tags})"
                else:
                    description = anchor.string

                task = self.store.create_task(
                    description=description,
                    options=WorkGenerator.CATEGORIES,
                    metadata={
                        "href": anchor["href"],
                        "time_added": anchor["time_added"],
                    },
                )
