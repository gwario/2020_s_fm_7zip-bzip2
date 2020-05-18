#!/bin/bash
FILES=sample_*

REPS=70

echo "Running experiments on: "
echo $FILES
echo ""

for f in $FILES
do
	echo "Running experiment for $f..."
	
  	./experiment.sh $REPS 7zip $f
	rm -r tmp
	sleep 5
	./experiment.sh $REPS bzip2 $f
	rm -r tmp
	sleep 5

	echo "Experiment for $f finished."
done

echo "All exeriments finished."
