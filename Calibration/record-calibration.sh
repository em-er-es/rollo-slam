#!/bin/bash
if [[ $# -eq 0 ]]; then RUN=$(date '+%d%m%y-%H%M%S'); else RUN="$@"; fi
#bash record.sh 0 calibration-"$RUN" /camera/rgb/camera_info rgb-camera-info /camera/depth/camera_info depth-camera-info /camera/rgb/image_color rgb-image-color /camera/depth/image_raw depth-image /camera/ir/image_raw ir-image # Not possible since ir and rgb cannot be transmitted at the same time
bash record.sh 0 calibration-"$RUN" /camera/rgb/camera_info rgb-camera-info /camera/depth/camera_info depth-camera-info /camera/rgb/image_color rgb-image-color /camera/depth/image_raw depth-image
