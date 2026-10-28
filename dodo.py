DOIT_CONFIG = {
    "backend": "json",
    "default_tasks": ["check"],
    "dep_file": ".doit.json",
    "verbosity": 2,
}


def task_check():
    return {
        "actions": [
            "uv run ruff check src/steganosaure tests",
            "uv run ruff format --check src/steganosaure tests",
            "uv run pyrefly check src/steganosaure tests",
        ],
    }


def task_test():
    return {
        "actions": [
            "uv run pytest",
        ],
    }
