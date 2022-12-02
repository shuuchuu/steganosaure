check:
	black --check steganosaure
	isort --check-only steganosaure
	mypy steganosaure
	flake8 --count
	pylint steganosaure

.PHONY: check
