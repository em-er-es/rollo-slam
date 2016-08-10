#!/bin/bash
IR_TOPIC="/camera/ir/image_raw"
FRAME_PERIOD=0.1

rosrun image_view extract_images _sec_per_frame:="$FRAME_PERIOD" image:="IR_TOPIC"
