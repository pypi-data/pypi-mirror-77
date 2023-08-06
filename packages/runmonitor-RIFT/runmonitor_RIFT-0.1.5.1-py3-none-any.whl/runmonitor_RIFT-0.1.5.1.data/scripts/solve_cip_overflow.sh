#!/usr/bin/env bash
#This is the main script to fix the cip -lnL-shift-prevent-overflow. It will check to see what the errorwas in the dagman, then if it's a CIP error, it will see if the error is Effective samples = nan. If so, it will increase the value of the flag by 50, or set it to 50 if not already present, then resubmit the job. It will also move the cip log/err/out files into a directory so that there's no confusion over which files are the most recent.

ERROR_FILE=$(check_error.py)

if [ $ERROR_FILE = "CIP.sub" ]; then
	ITERATION=$(get_iteration.sh)
	if [ $(check_effective_samples_error.py -i $ITERATION) ]; then
		NEW_OVERFLOW=$(get_new_overflow.sh)
		CIP_ARGS=$(python -c'import restore_tools; restore_tools.get_args_without_overflow()')
		NEW_ARGS="$CIP_ARGS --lnL-shift-prevent-overflow $NEW_OVERFLOW \""
		sed -i "s|^arguments = .*|$NEW_ARGS|" CIP.sub
	fi
	
	cd "iteration_"$ITERATION"_cip/logs"
	if [ ! -d "old" ]; then
		mkdir old
	fi
	for d in *; do
		if [ $d != "old" ]; then
			mv $d old
		fi
	done
fi
