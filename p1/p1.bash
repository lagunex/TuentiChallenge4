#!/bin/bash
#
# Because the input and the student list have the same format, we can use
# grep directly to look for matches.
#
# When a match is found, it will come one per line with all the student's info.
# Therefore we use cut to extract the name, sort and finally tr to write 
# the names in a single line.
#
# Finally, sed is used to handle the case of no matches and to remove the
# trailing ',' added by tr
#
# The code is written to enforce readability and teaching
#
STUDENTS_DIR=$HOME/tuenti/p1 # this shouldn't be hard-coded in prod enviroments
T=0
while read line; do
  if [ $T -gt 0 ]; then # we ignore the first line
    grep "$line" $STUDENTS_DIR/students |\
    cut -d, -f1 |\
    sort |\
    tr '\n' ',' |\
    xargs echo "Case #$T:" |\
    sed -re 's/:$/: NONE/g' \
        -e 's/,$//g'
  fi
  T=$(($T+1))
done

