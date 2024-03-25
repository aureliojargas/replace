.PHONY: check clean fmt lint test

PYTHON_FILES = replace.py test_replace.py

check: lint test

fmt:
	ruff format $(PYTHON_FILES)

lint:
	ruff check $(PYTHON_FILES)
	ruff format --check --diff $(PYTHON_FILES)

test: clitest
	pytest
	bash ./clitest --progress none README.md

clitest:
	curl --location --remote-name --silent \
	https://raw.githubusercontent.com/aureliojargas/clitest/master/clitest

clean:
	rm -f clitest
