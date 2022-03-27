#!/bin/bash

declare -A old_interfaces new_interfaces

function query_interfaces() {
    INTFS=$(xmllint --xpath '/domain/devices/interface/mac/@address | /domain/devices/interface/alias/@name' $1 | grep -oP '(?<=").*(?=")')
    temp_str=''
    i=0

    for value in $INTFS
    do
      if [ $((i % 2)) -ne 0 ]
      then
        if [ -z "$2" ]; then
          old_interfaces[$value]=$temp_str
        else
          new_interfaces[$value]=$temp_str
        fi
      else
        temp_str=$value
      fi
      i=$[i + 1]
    done
}

query_interfaces $1
query_interfaces $2 0

for i in "${!old_interfaces[@]}"
do
  if [ ${old_interfaces[$i]} != ${new_interfaces[$i]} ]; then
    echo "Interface $i value changed to ${new_interfaces[$i]} from ${old_interfaces[$i]}"
  fi
done
