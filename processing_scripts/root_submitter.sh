#!/bin/bash -l

task="$1"
func="$2"

dep=$(grep "<DEPENDENCY>" ./processing_scripts/temp/dependency.txt)

IFS=" "
read -ra array <<< "$dep"

dep="${array[1]}"

if [ "$dep" = "" ]
then
	cmd="sbatch ./processing_scripts/submitter.sh $task $func"
else
	cmd="sbatch --dependency=afterok:$dep ./processing_scripts/submitter.sh $task $func"
fi

echo "$cmd"
eval "$cmd"