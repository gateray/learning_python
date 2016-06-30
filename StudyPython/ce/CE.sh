#/bin/bash
PYTHONBIN=`which python 2>/dev/null`
if [ `whoami` != "root" ]
then
   echo "This program must be run as root user."
   exit 1
fi

if [ -n "$PYTHONBIN" ]
then
    export PYTHONPATH
else
    echo "Python is not available"
fi

if [ "$#" -gt "0" -a "$1" = "-R" ]; then
   echo "reset AE start"
   rm -f /opt/huadi/ce/CR/*
   if [ -f "/etc/udev/rules.d/70-persistent-net.rules" ];
   then
      rm -f  /etc/udev/rules.d/70-persistent-net.rules
   fi
   if [ -f "/etc/udev/rules.d/30-net_persistent_name.rul" ];
   then
      rm -f  /etc/udev/rules.d/30-net_persistent_name.rul
   fi
   echo "reset CE completed,shutdown computer"
   halt
else
   echo "Init VM netWork start"
   "$PYTHONBIN" /opt/huadi/ce/ce.py
   echo "Init VM netWork has completed."
fi