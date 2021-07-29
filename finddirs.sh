#!/bin/bash


for adir in  `ls -l | grep '^d' | gawk '{print $9}'`
do
	anum=`ls $adir | wc | gawk '{print $1}'`
	echo "$adir,$anum" >> fhaha.csv
done
