#!/bin/bash -l

#SBATCH --job-name=INTERPRETER_SUBMITTER
#SBATCH --time=00:05:00
#SBATCH --output=./processing_scripts/temp/submitter-%j.out
#SBATCH --error=./processing_scripts/temp/submitter-%j.err
#SBATCH --partition=gc

task="$1"
func="$2"

cmd="python ./processing_scripts/interpreter.py $task $func"

echo "$cmd"
eval "$cmd"