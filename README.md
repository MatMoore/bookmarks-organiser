# Bookmark organiser

A command line tool to quickly sort bookmarks into categories.

The goal is to turn a long list of unsorted bookmarks (exported from Pocket) into some kind of browseable knowledge base.

This tool handles the first step of grouping bookmarks into high level categories. It prompts you to choose the most appropriate category using an interactive command line interface.

Currently it stores all the data in a SQLite database.

## Design goals

- Enable quick data collection. Completing a task should take seconds.
- Have minimal external dependencies.
- Produce data in a consumable format.
- Be easy to extend to any simple data gathering tasks.

## Non-goals

- Crowdsourcing
- Requiring tasks to be completed more than once

## Setup

Requires python 3.9.

```
pip install -r requirements.txt
```

(TODO: CLI to import bookmarks to categorise)

To start categorising:

```
python bookmark_organiser.py
```

The categories are currently hardcoded in `work.py`.

## Licence

MIT
