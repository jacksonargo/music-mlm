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

echo manifest

# shellcheck disable=SC2188
>data/manifest.txt
for file in data/00_src/*.pdf; do
  output="$(basename "$file" .pdf | cksum | awk '{print $1}').txt"
  echo "$(basename "$output")" "$(basename "$file")">>data/manifest.txt
done

echo stage 01_extraction

mkdir -p data/01_extraction
for file in data/00_src/*.pdf; do
  output="data/01_extraction/$(basename "$file" .pdf | cksum | awk '{print $1}').txt"
  pdftotext -layout "$file" "$output"
done
