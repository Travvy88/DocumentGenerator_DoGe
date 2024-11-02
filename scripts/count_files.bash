#!/bin/bash

count_files() {
  if [ -z "$1" ]; then
    echo "No argument provided" >&2
    return 1
  fi
  if [ ! -d "$1" ]; then
    echo "Argument is not a directory" >&2
    return 1
  fi
  find "$1" -type f | wc -l
}

count_files "$@"