#!/usr/bin/env bash

set -e

year_month=$(date '+%Y-%m')
full_date=$(date '+%Y-%m-%d_%H-%M-%S')
hugo_fn=post/${year_month}/${full_date}.md
new_fn=content/${hugo_fn}
fn=${new_fn}

# hugo new post//.md

while getopts "o:nt:" opt; do
  case $opt in
    n)
      echo "create new post with name ${filename}"
      hugo new ${hugo_fn}
      ;;
    o)
      echo "replace old filename $OPTARG title..."
      fn=content/$OPTARG
      ;;
    t)
      echo "replace with title $OPTARG"
      sed -i "s/^title: \".*\"$/title: \"$OPTARG\"/g" ${fn}
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
