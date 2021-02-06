import random
import questionary
from questionary import Separator, Style


class FakeTask:
    def __init__(self):
        self.description = "This is a fake categorization task"
        self.options = ["Foo", "Bar", "Baz"]

    def result(self, option):
        pass


tasks = [FakeTask()]


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


for task in tasks:
    response = questionary.select(
        task.description,
        choices=task.options + [Separator(), "Skip", "Quit"],
        use_shortcuts=True,
        style=style,
    ).ask()

    if response == "Skip":
        continue

    if response == "Quit":
        break

    task.result(response)
