.PHONY: black check clean pylint

clean:
	rm -f clitest

check: black clitest pylint
	black --check --diff --quiet replace.py
	pylint replace.py
	bash ./clitest --progress none README.md

black pylint:
	@command -v $@ >/dev/null 2>&1 && exit 0; \
	pip3 install --user $@ || pip install --user $@

clitest:
	curl --location --remote-name --silent \
	https://raw.githubusercontent.com/aureliojargas/clitest/master/clitest
