#!/usr/bin/env bash
#Small script to see what iteration the run is on. It's run in the run directory.

NUM=0

for POSTERIOR_FILE in posterior_samples*.dat; do
	NUM=$((NUM+1))
done
echo $NUM
