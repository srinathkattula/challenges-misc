#!/bin/bash

for i in $(seq 1 6); do
  output=$(cat in$i.txt | python ./run.py)
  output_ref=$(cat output$i.txt)

  if test "${output}" != "${output_ref}"; then
    echo "Test $i failed"
    echo "Output:"
    echo $output
    echo "Ref:"
    echo $output_ref
  else
    echo "Test $i OK"
  fi


done
