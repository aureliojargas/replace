#!/bin/bash

# Turn strict mode on
set -o errexit -o nounset -o pipefail

# Lint
echo "*** Running Pylint..."
pylint replace.py

# Test
echo "*** Running clitest..."
curl -sL https://raw.githubusercontent.com/aureliojargas/clitest/master/clitest |
  bash -s -- --progress none README.md
