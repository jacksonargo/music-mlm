#!/usr/bin/env bash
set -x

workDir=$(pwd)
while ! [ -d data ]; do
  cd ..
  if [ "$workDir" -eq "$(pwd)" ]; then
    echo "could not find data dir"
    exit 1
  fi
done

for file in data/src/*.pdf; do
  output="data/extraction/$(basename "$file" .pdf | cksum | awk '{print $1}').txt"
  pdftotext "$file" "$output"
done
