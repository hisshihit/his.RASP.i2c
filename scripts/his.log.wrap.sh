#!/bin/bash

pid=$$
date=`date '+%Y%m%d'`
fileprefix="/home/shibata/his.SensorLogs/Log-"
ambiscript="/home/shibata/scripts/his.ambient.py"
envscript="/home/shibata/scripts/his.env2.py"

#
# get Sensor output
#
AMB=`${ambiscript}`
ENV=`${envscript}`

echo $AMB$ENV | sed 's/}{ "place": "home" , "time": "....-..-..T..:..:..Z"//' >> "${fileprefix}${date}.txt"
