#!/bin/bash
FILES=sample_*

REPS=70

echo "Getting system information..."
CPU_INFO=$(cat /proc/cpuinfo | head -n5 | tail -n1)
CPU_N_CORES=$(cat /proc/cpuinfo | head -n11 | tail -n1)
echo "CPU: "${CPU_INFO#*:}" x "${CPU_N_CORES#*:}
RAM_INFO=$(cat /proc/meminfo | head -n1)
echo "RAM: "${RAM_INFO#*:}
echo "Operating system: "$(uname -a)
echo "File size measurement: "$(du --version | head -n1)
echo "Time measurement: "$(/bin/time --version 2>&1)
echo "Compression tool: "$(7z | head -n2 | tail -n1)
echo
echo "Running experiments on: "
echo $FILES
echo

for f in $FILES
do
	echo "Running experiment for $f..."

  	./experiment.sh $REPS lzma $f
	rm -r tmp
	sleep 5
	./experiment.sh $REPS bzip2 $f
	rm -r tmp
	sleep 5

	echo "Experiment for $f finished."
done

echo "All exeriments finished."
