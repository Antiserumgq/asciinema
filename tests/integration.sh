#!/bin/bash

set -e

test() {
  echo "Test: $1"
  eval "PYTHONPATH=. python2 -m asciinema $2 >/dev/null || (echo 'failed' && exit 1)"
}

test "help" "-h"
test "version" "-v"
test "auth" "auth"
