#! /bin/sh


root=$1
target_dir=$2

find "$root" -type f -name '*.zip' | while read file; do
    unzip -j -d "$target_dir" "$file"
done
