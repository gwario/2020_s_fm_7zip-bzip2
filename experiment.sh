#!/bin/bash

USAGE="Usage: $0 <reps> <algo> <input>"

if [ $1 -gt 0 ]
then
	REPS="$1"
	echo "Repeating measurement $REPS times..."
else
	echo "Invalid number of repetitions $1!"
	echo $USAGE
	exit
fi

if [ "$2" = "bzip2" ]
then
	ALGO="bzip2"
	ALGO_EXT="bz2"
	echo "Using $ALGO as algorithm..."
elif [ "$2" = "7zip" ]
then
	ALGO="7z"
	ALGO_EXT="7z"
	echo "Using $ALGO as algorithm..."	
else
	echo "Invalid algorithm '$2'!"
	echo $USAGE
	exit
fi

if [ -d "$3" ] || [ -f "$3" ]
then
	FILE_OR_DIR="$3"
	echo "Using $FILE_OR_DIR as input..."
else
	echo "Invalid input '$3'!"
	echo $USAGE
	exit
fi



TEMP_DIR="tmp"
if [ -d "$TEMP_DIR" ]
then
	echo "Temp dir already exist! Remove it manually and retry."
	exit
else
	echo "Creating temp dir..."
	mkdir $TEMP_DIR
fi



echo "Running compression..."
STATS_FILE=$ALGO"_compress_"$FILE_OR_DIR".csv"
# write output file with header
echo "id of repetition;elapsed wall clock time[s];CPU-time (system)[s];CPU-time (user)[s];percentage CPU;maximum resident set size[Kilobytes];file system inputs;file system outputs;command exit code;command" > $STATS_FILE

idx=0
while [ $idx -lt $REPS ]
do
	echo "Repetition $idx..."

	COMPRESSED_FILE=$TEMP_DIR"/"$FILE_OR_DIR"_"$idx"."$ALGO_EXT	

	if [ "$ALGO" = "bzip2" ]
	then
		/bin/time -f "$idx;%e;%S;%U;%P;%M;%I;%O;%x;%C" -a -o "$STATS_FILE" 7z a -ttar $FILE_OR_DIR -so -an | 7z a -t$ALGO $COMPRESSED_FILE -si &>/dev/null
	else
		/bin/time -f "$idx;%e;%S;%U;%P;%M;%I;%O;%x;%C" -a -o "$STATS_FILE" 7z a -t$ALGO $COMPRESSED_FILE $FILE_OR_DIR &>/dev/null
	fi

	sleep 5

	((idx++))
done



echo "Running decompression..."
STATS_FILE=$ALGO"_decompress_"$FILE_OR_DIR".csv"
# write output file with header
echo "id of repetition;elapsed wall clock time[s];CPU-time (system)[s];CPU-time (user)[s];percentage CPU;maximum resident set size[Kilobytes];file system inputs;file system outputs;command exit code;command" > $STATS_FILE

idx=0
while [ $idx -lt $REPS ]
do
	echo "Repetition $idx..."

	COMPRESSED_FILE=$TEMP_DIR"/"$FILE_OR_DIR"_"$idx"."$ALGO_EXT	

	if [ "$ALGO" = "bzip2" ]
	then
		/bin/time -f "$idx;%e;%S;%U;%P;%M;%I;%O;%x;%C" -a -o "$STATS_FILE" 7z x -t$ALGO $COMPRESSED_FILE -so | 7z x -ttar -si -an -o$TEMP_DIR &>/dev/null
	else
		/bin/time -f "$idx;%e;%S;%U;%P;%M;%I;%O;%x;%C" -a -o "$STATS_FILE" 7z x $COMPRESSED_FILE -o$TEMP_DIR &>/dev/null
	fi

	mv $TEMP_DIR"/"$FILE_OR_DIR $TEMP_DIR"/"$FILE_OR_DIR"_"$idx

	sleep 5

	((idx++))
done



# This is partly for compression ration and partly as sanity check
echo "Running file size comparison..."
SIZE_FILE=$ALGO"_"$FILE_OR_DIR"_size.csv"
echo "id of repetition;uncompressed;compressed;decompressed" > $SIZE_FILE

SIZE_UNCOMPRESSED=$(du -b "$FILE_OR_DIR" | grep -Po '^\d+')

idx=0
while [ $idx -lt $REPS ]
do
	echo "Repetition $idx..."

	COMPRESSED_FILE=$TEMP_DIR"/"$FILE_OR_DIR"_"$idx"."$ALGO_EXT
	DECOMPRESSED_FILE=$TEMP_DIR"/"$FILE_OR_DIR"_"$idx

	SIZE_COMPRESSED=$(du -b "$COMPRESSED_FILE" | grep -Po '^\d+')
	SIZE_DECOMPRESSED=$(du -b "$DECOMPRESSED_FILE" | grep -Po '^\d+')

	echo "$idx;$SIZE_UNCOMPRESSED;$SIZE_COMPRESSED;$SIZE_DECOMPRESSED" >> $SIZE_FILE

	((idx++))
done



echo "Experiment finished."
