#!/bin/bash
if [[ $# -eq 0 ]]; then RUN=fixed-frame-$(date '+%d%m%y--%H%M%S'); else RUN="$@"; fi
FRAME_PERIOD=0.1
SLEEP_DELAY_EST=1
SLEEP_TOPIC=2
SLEEP_LOOP=1
TOPICS=('/camera/ir/image_raw' '/camera/rgb/image_color' '/camera/depth/image_raw')

mkdir -p "$RUN" && cd "$RUN"

i=0
for TOPIC in ${TOPICS[@]}; do
	LDIR="$(echo "$TOPIC" | sed 's#^/##;s#/#-#g')"
	mkdir -p "$LDIR"; cd "$LDIR"
	rosrun image_view extract_images _sec_per_frame:="$FRAME_PERIOD" image:="$TOPIC" &
	PID=$!; PIDS[i]=$PID;
	sleep $SLEEP_DELAY_EST
	cd ..
	i=$((i+1))
done

while :; do
	sleep $SLEEP_LOOP
	tree
	read -n 1 -p "Capture depth images by clicking the mouse button in the image_view window, press q to exit and k to kill forefully and exit" KEY
	if [[ "$KEY" == "q" ]]; then exit 0;
	elif [[ "$KEY" == "k" ]]; then
		for ROSPID in ${PIDS[@]}; do kill -9 $ROSPID; done
		ROSPIDS=$(ps aux | awk '/image_view/{print $2}');
		for ROSPID in $ROSPIDS; do kill -9 $ROSPID; done
		exit 0;
	fi
done
