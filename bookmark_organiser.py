import random


class FakeTask:
    def __init__(self):
        self.description = "This is a fake categorization task"
        self.options = ["Foo", "Bar", "Baz"]
        self.options_normalised = [self.normalise(option) for option in self.options]

    def result(self, option):
        pass

    def normalise(self, option):
        return option.lower()

    def validate_option(self, response):
        return self.normalise(response) in self.options_normalised


tasks = [FakeTask()]


def prompt(task):
    print(task.description)
    print(task.options)
    print("Select an option:")

    while True:
        response = input("> ")
        if task.validate_option(response):
            task.result(response)
            break
        else:
            print(f'Invalid option "{response}". Valid options are {task.options}')


for task in tasks:
    prompt(task)
