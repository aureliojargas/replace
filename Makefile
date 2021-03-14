.PHONY: check doctester fmt lint test

check: lint test

fmt:
	black replace.py

lint:
	black --check --diff --quiet replace.py
	pylint replace.py

test: doctester
	doctester --prefix '' README.md

doctester:
	@command -v doctester >/dev/null || \
	python3 -m pip install doctester
