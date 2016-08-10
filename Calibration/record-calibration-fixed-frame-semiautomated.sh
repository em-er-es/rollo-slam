#!/bin/bash
if [[ $# -eq 0 ]]; then RUN=fixed-frame-$(date '+%d%m%y--%H%M%S'); else RUN="$@"; fi
FRAME_PERIOD=0.1
SLEEP_DELAY_EST=1
SLEEP_TOPIC=2
SLEEP_LOOP=1
#TOPICS=('/camera/depth/image_raw' '/camera/ir/image_raw' '/camera/rgb/image_color' '/camera/rgd/image_raw')
#TOPICS=('/camera/ir/image_raw' '/camera/rgb/image_color' '/camera/rgd/image_mono' '/camera/depth/image_raw') #image_mono doesn't work, might be delay related
TOPICS=('/camera/ir/image_raw' '/camera/rgb/image_color' '/camera/depth/image_raw')

mkdir -p "$RUN" && cd "$RUN"

while :; do
	i=0
#	for TOPIC in ('/camera/depth_registered/sw_registered/image_raw' '/camera/ir/image_raw' '/camera/rgb/image_color' '/camera/rgd/image_raw'); do
	for TOPIC in ${TOPICS[@]}; do
		LDIR="$(echo "$TOPIC" | sed 's#^/##;s#/#-#g')-$(date '+%H%M%S')"
		mkdir -p "$LDIR"; cd "$LDIR"
#		rosrun image_view extract_images _sec_per_frame:="$FRAME_PERIOD" image:="$TOPIC" &
#		PID=$!; PIDS[i]=$PID;
#		PIDS[i]=$#; PID=${PIDS[i]}
		if [[ "$TOPIC" == "/camera/depth/image_raw" ]]; then
			pwd
			rosrun image_view image_view image:="$TOPIC" &
			PID=$!; PIDS[i]=$PID;
			xdotool mousemove 0 0
			xdotool mousemove_relative -- 200 200
			sleep $SLEEP_DELAY_EST
#Automated approach
#Probably need mousedown/up events to function properly
#			for i in $(seq $(((SLEEP_TOPIC-SLEEP_DELAY_EST)*10))); do
#				xdotool click 2;
#				xdotool click 2;
#				echo Click
#				sleep $FRAME_PERIOD;
#			done
			read -n 1 -p "Capture depth images by clicking the mouse button in the image_view window, then press any key to continue loop"
		else
			rosrun image_view extract_images _sec_per_frame:="$FRAME_PERIOD" image:="$TOPIC" &
			PID=$!; PIDS[i]=$PID;
			sleep $SLEEP_DELAY_EST
#			PIDS[i]=$#; PID=${PIDS[i]}
#		
		fi
		cd ..
#		sleep $SLEEP_TOPIC
#		kill -9 ${PIDS[i]}
		kill -9 $PID
		i=$((i+1))
	done
	sleep $SLEEP_LOOP
	tree
	read -n 1 -p "Press any key for next snapshot burst, press q to exit and k to kill forefully and exit" KEY
	if [[ "$KEY" == "q" ]]; then exit 0;
	elif [[ "$KEY" == "k" ]]; then 
		for ROSPID in ${PIDS[@]}; do kill -9 $ROSPID; done
		ROSPIDS=$(ps aux | awk '/image_view/{print $2}');
		for ROSPID in $ROSPIDS; do kill -9 $ROSPID; done
		exit 0;
	fi
done
