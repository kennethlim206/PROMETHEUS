#!/bin/bash -l

#SBATCH --job-name=QUEEN
#SBATCH --time=48:00:00
#SBATCH --output=./processing_scripts/temp/queen-%j.out
#SBATCH --error=./processing_scripts/temp/queen-%j.err
#SBATCH --partition=gc

TASK="$1"
FUNC="$2"

cmd="python ./processing_scripts/queen.py $TASK $FUNC"

echo "$cmd"
eval "$cmd"

