#!/bin/bash
# if [[ $# -eq 0 ]]; then echo "${@[0]} DURATION LOGMAINNAME TOPIC1 SUFFIX1 [ TOPICN SUFFIXN ] ... \n"; exit 0; fi
if [[ $# -eq 0 ]]; then echo "$(basename "$0") DURATION LOGMAINNAME TOPIC1 SUFFIX1 [ TOPICN SUFFIXN ] ... "; 
	echo "Stored to ros.LOGMAINNAME.CDT.SUFFIX.log"; exit 0; fi
CDT="$(date '+%d%m%y--%H%M%S')";
DURATION=$1;
LOGMAIN="$2";
shift;
shift;
i=0;
while [[ $# -gt 1 ]]; do
	i=$((i+1));
	echo $i;
	TOPIC="$1";
	SUFFIX="$2";
	echo Logging $1 $2;
	rostopic echo "$TOPIC" > ros."$LOGMAIN.$CDT.$SUFFIX".log &
	echo "$TOPIC" \> ros."$LOGMAIN.$CDT.$SUFFIX".log
	shift;
	shift;
done

if [[ $DURATION -lt 0 ]]; then exit;
elif [[ $DURATION -eq 0 ]]; then read -n 1 -p Press any key to stop recording WAIT; pkill -9 rostopic;
else sleep $DURATION;
pkill -9 rostopic;
fi
