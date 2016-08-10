#!/bin/bash
RGB_TOPIC="/camera/rgb/image_color"
FRAME_PERIOD=0.1

rosrun image_view extract_images _sec_per_frame:="$FRAME_PERIOD" image:="RGB_TOPIC"
