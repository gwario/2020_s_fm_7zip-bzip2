#!/usr/bin/dash

COMPRESSED_FILE=$1
TEMP_DIR=$2

7z x -tbzip2 $COMPRESSED_FILE -so | 7z x -ttar -si -an -o$TEMP_DIR
