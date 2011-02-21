#!/bin/sh
set -e
BASE_DIRECTORY=`dirname "$0"`

# First argument must be deck directory
if [[ "$1" == "" ]]
then
  TOOL=`basename "$0"`
  echo "Usage: $TOOL deck-directory [output-directory]"
  exit 1
fi
INPUT="$1"
NAME=`basename "$INPUT"`

# Second argument is destination (use current user's Desktop directory if not specified)
if [[ "$2" == "" ]]
then
  OUTPUT="${HOME}/Desktop/${NAME}.zip"
else
  OUTPUT="$2.zip"
fi

# Clear output
rm -f "${OUTPUT}"

# Copy deck to temporary directory
TEMP="/tmp/${NAME}"
rm -rf "${TEMP}"
if [[ -d "${INPUT}/.svn" ]]
then
  svn export "${INPUT}" "${TEMP}" > /dev/null
else
  cp -r "${INPUT}" "${TEMP}"
fi

# Validate PageKit files
"${BASE_DIRECTORY}/PageKit-Validator.py" "${TEMP}"

# Optimize PNG images
# http://iphonedevwiki.net/index.php/CgBI_file_format
# http://howett.net/pincrush/
PLATFORM=`uname`
if [[ "${PLATFORM}" == "Darwin" ]]
then
  find "${TEMP}" -name *.png -exec "${BASE_DIRECTORY}/pincrush-osx" -i {} +
else
  find "${TEMP}" -name *.png -exec "${BASE_DIRECTORY}/pincrush-linux" -i {} +
fi

# Create zip archive
pushd "${TEMP}" > /dev/null
zip -r "deck.zip" . > /dev/null
popd > /dev/null

# Move to destination
mv "${TEMP}/deck.zip" "${OUTPUT}"

# Clean up
rm -rf "${TEMP}"
