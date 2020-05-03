#!/bin/bash
# Script to copy files to remote nodes
# to run type ./copy2clearLab [file1] [file2] [file3] [...]

for FILE1 in "$@"
do
scp mpiuser@192.168.110.133:/home/mpiuser/code/cc_project/$FILE1 mpiuser8@129.114.25.78:/home/mpiuser8/code/cc_project/$FILE1
done
