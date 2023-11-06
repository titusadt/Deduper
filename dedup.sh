#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=interactive
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G

/usr/bin/time -v ./temi_deduper.py -f sorted_C1_SE_uniqAlign.sam -u STL96.txt -o FinalFINAL_output.txt 