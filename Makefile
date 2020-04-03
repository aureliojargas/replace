.PHONY: black check clean pylint

check: black clitest pylint
	black --check --diff --quiet replace.py
	pylint replace.py
	bash ./clitest --progress none README.md

black pylint:
	@command -v $@ >/dev/null || \
	pip3 install --user $@ || \
	pip3 install $@ || \
	pip install --user $@ || \
	pip install $@

clitest:
	curl --location --remote-name --silent \
	https://raw.githubusercontent.com/aureliojargas/clitest/master/clitest

clean:
	rm -f clitest
