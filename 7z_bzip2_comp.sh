#!/usr/bin/dash

FILE_OR_DIR=$1
COMPRESSED_FILE=$2

7z a -ttar $FILE_OR_DIR -so -an | 7z a -tbzip2 $COMPRESSED_FILE -si
