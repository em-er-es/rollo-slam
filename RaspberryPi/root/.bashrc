# ~/.bashrc: executed by bash(1) for non-login shells.

# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
# export LS_OPTIONS='--color=auto'
# eval "`dircolors`"
# alias ls='ls $LS_OPTIONS'
# alias ll='ls $LS_OPTIONS -l'
# alias l='ls $LS_OPTIONS -lA'
#
# Some more alias to avoid making mistakes:
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'

#source /opt/ros/indigo/setup.bash
#source /home/pi/ros_catkin_ws/devel_isolated/setup.bash
#export ROS_IP=$(hostname -I | awk '{print $1}')

ros-rpi() {
source /opt/ros/indigo/setup.bash
source /home/pi/ros_catkin_ws/devel_isolated/setup.bash

#export ROS_IP=$(hostname -I)
export ROS_IP=$(hostname -I | awk '{print $1}')
#export ROS_IP=192.168.0.155
#export ROS_MASTER_URI=http://192.168.0.155:11311
export ROS_MASTER_URI=http://$ROS_IP:11311

#Disable ROS logging - old way
export ROS_PYTHON_LOG_CONFIG_FILE=/dev/null
export ROS_LOG_DIR=/dev/null
export ROSCONSOLE_CONFIG_FILE="$HOME/.ros/rosconsole.conf"

#Start without rosout
#if [ $(ps aux | grep -v grep | grep -c rosmaster) -gt 1 ]; then 
#if [[ -f /tmp/rosmaster ]]; then 
#if [ $(ps aux | grep -v grep | grep -c rosmaster) -gt 1 ] || [[ -f /tmp/rosmaster ]]; then 
#	echo Roscore found. Skipping...;
#else
#	echo Roscore not found. Starting...;
#	rosmaster --core &>/dev/null & # instead of roscore
#	echo Romaster PID $(ps aux | awk '/rosmater/{print $2}') > /tmp/rosmaster
#fi
}

ros-rpi
