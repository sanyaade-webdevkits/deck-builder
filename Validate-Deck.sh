#!/bin/sh

# This software is owned by Cooliris, Inc., copyright 2011, and licensed to you under the
# Software License Agreement for the Decks by Cooliris Template Files and Sample Code available at
# http://www.decksapp.com/sample-code-license/

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
