.PHONY: check clean

check: clitest
	black --check --diff --quiet replace.py
	pylint replace.py
	bash ./clitest --progress none README.md

clitest:
	curl --location --remote-name --silent \
	https://raw.githubusercontent.com/aureliojargas/clitest/master/clitest

clean:
	rm -f clitest
