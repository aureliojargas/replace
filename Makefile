.PHONY: check clean fmt lint test

check: lint test

fmt:
	black replace.py

lint:
	black --check --diff --quiet replace.py
	ruff replace.py

test: clitest
	bash ./clitest --progress none README.md

clitest:
	curl --location --remote-name --silent \
	https://raw.githubusercontent.com/aureliojargas/clitest/master/clitest

clean:
	rm -f clitest
