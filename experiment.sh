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



RESULT_PREFIX="result"



echo "Running compression..."
STATS_FILE=$RESULT_PREFIX"_"$FILE_OR_DIR"_compress_"$ALGO".csv"
# write output file with header
echo "id of repetition;elapsed wall clock time[s];CPU-time (system)[s];CPU-time (user)[s];percentage CPU;maximum resident set size[Kilobytes];file system inputs;file system outputs;command exit code;command" > $STATS_FILE

idx=0
while [ $idx -lt $REPS ]
do
	echo "Repetition $idx..."

	COMPRESSED_FILE=$TEMP_DIR"/"$idx"_"$FILE_OR_DIR"."$ALGO_EXT

	if [ "$ALGO" = "bzip2" ]
	then
		/bin/time -f "$idx;%e;%S;%U;%P;%M;%I;%O;%x;%C" -a -o "$STATS_FILE" ./7z_bzip2_comp.sh $FILE_OR_DIR $COMPRESSED_FILE &>/dev/null
	else
		/bin/time -f "$idx;%e;%S;%U;%P;%M;%I;%O;%x;%C" -a -o "$STATS_FILE" ./7z_7z_comp.sh $COMPRESSED_FILE $FILE_OR_DIR &>/dev/null
	fi

	sleep 5

	((idx++))
done



echo "Running decompression..."
STATS_FILE=$RESULT_PREFIX"_"$FILE_OR_DIR"_decompress_"$ALGO".csv"
# write output file with header
echo "id of repetition;elapsed wall clock time[s];CPU-time (system)[s];CPU-time (user)[s];percentage CPU;maximum resident set size[Kilobytes];file system inputs;file system outputs;command exit code;command" > $STATS_FILE

idx=0
while [ $idx -lt $REPS ]
do
	echo "Repetition $idx..."

	COMPRESSED_FILE=$TEMP_DIR"/"$idx"_"$FILE_OR_DIR"."$ALGO_EXT	

	if [ "$ALGO" = "bzip2" ]
	then
		/bin/time -f "$idx;%e;%S;%U;%P;%M;%I;%O;%x;%C" -a -o "$STATS_FILE" ./7z_bzip2_decomp.sh $COMPRESSED_FILE $TEMP_DIR &>/dev/null
	else
		/bin/time -f "$idx;%e;%S;%U;%P;%M;%I;%O;%x;%C" -a -o "$STATS_FILE" ./7z_7z_decomp.sh $COMPRESSED_FILE $TEMP_DIR &>/dev/null
	fi

	TEMP_DECOMPRESSED_FILE=$TEMP_DIR"/"$FILE_OR_DIR
	DECOMPRESSED_FILE=$TEMP_DIR"/"$idx"_"$FILE_OR_DIR
	
	mv $TEMP_DECOMPRESSED_FILE $DECOMPRESSED_FILE

	sleep 5

	((idx++))
done



# This is partly for compression ration and partly as sanity check
echo "Running file size comparison..."
SIZE_FILE=$RESULT_PREFIX"_"$FILE_OR_DIR"_size_"$ALGO".csv"
echo "id of repetition;uncompressed;compressed;decompressed" > $SIZE_FILE

SIZE_UNCOMPRESSED=$(du -sb "$FILE_OR_DIR" | grep -Po '^\d+')

idx=0
while [ $idx -lt $REPS ]
do
	echo "Repetition $idx..."
	
	COMPRESSED_FILE=$TEMP_DIR"/"$idx"_"$FILE_OR_DIR"."$ALGO_EXT
	DECOMPRESSED_FILE=$TEMP_DIR"/"$idx"_"$FILE_OR_DIR

	SIZE_COMPRESSED=$(du -sb "$COMPRESSED_FILE" | grep -Po '^\d+')
	SIZE_DECOMPRESSED=$(du -sb "$DECOMPRESSED_FILE" | grep -Po '^\d+')

	echo "$idx;$SIZE_UNCOMPRESSED;$SIZE_COMPRESSED;$SIZE_DECOMPRESSED" >> $SIZE_FILE

	((idx++))
done



echo "Experiment finished."
