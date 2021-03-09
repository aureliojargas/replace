.PHONY: check clean lint test

check: lint test

lint:
	black --check --diff --quiet replace.py
	pylint replace.py

test: clitest
	bash ./clitest --progress none README.md

clitest:
	curl --location --remote-name --silent \
	https://raw.githubusercontent.com/aureliojargas/clitest/master/clitest

clean:
	rm -f clitest
