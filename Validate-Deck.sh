#!/bin/sh
set -e
BASE_DIRECTORY=`dirname "$0"`

# First argument must be deck directory
if [[ "$1" == "" ]]
then
  TOOL=`basename "$0"`
  echo "Usage: $TOOL deck-directory"
  exit 1
fi
INPUT="$1"

# Validate deck (run Python in 32 bits on Mac OS X 10.6 to allow Quartz bindings)
export VERSIONER_PYTHON_PREFER_32_BIT=yes
"${BASE_DIRECTORY}/Deck-Validator.py" "${INPUT}"
