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

echo stage 02_remove_header_footer

mkdir -p data/02_remove_header_footer
for file in data/01_extraction/*txt; do
  output="data/02_remove_header_footer/$(basename "$file")"
  sed 's/.*$//' <"$file" >"$output"
done

echo stage 03_concat_hyphenated

mkdir -p data/03_concat_hyphenated
for file in data/02_remove_header_footer/*txt; do
  output="data/03_concat_hyphenated/$(basename "$file")"
  sed 's/(\w)-\s*[\n\r]//g' <"$file" >"$output"
done
