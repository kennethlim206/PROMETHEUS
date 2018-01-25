#!/bin/bash -l

#SBATCH --job-name=SUBMIT_INTERPRETER
#SBATCH --time=00:05:00
#SBATCH --output=./processing_scripts/temp/submitter.out
#SBATCH --error=./processing_scripts/temp/submitter.err
#SBATCH --partition=gc

$task = "$1"
$function = "$2"

$cmd = "python ./processing_scripts/interpreter.py $task $function"

echo "$cmd"
eval "$cmd"