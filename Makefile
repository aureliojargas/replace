.PHONY: check clean pylint

clean:
	rm -f clitest

check: clitest pylint
	pylint replace.py
	bash ./clitest --progress none README.md

pylint:
	@command -v $@ >/dev/null 2>&1 && exit 0; \
	pip3 install --user $@ || pip install --user $@

clitest:
	curl --location --remote-name --silent \
	https://raw.githubusercontent.com/aureliojargas/clitest/master/clitest
