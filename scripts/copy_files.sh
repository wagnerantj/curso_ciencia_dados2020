#!/bin/bash

file=$1
prefix=$2
start=$3
end=$4
dest=$5
dez=$6
sufix=$7
ex=_Ex
for num in $(seq $start $end)
do
    cp "$file" "$dest/$prefix$ex$dez$num$sufix.json"
done