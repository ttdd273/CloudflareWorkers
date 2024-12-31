#!/bin/bash

dirs=$(find . -maxdepth 1 -type d -name '*worker*')
echo "Running tests for all workers: $dirs"

for dir in $dirs; do
  echo "Testing worker: $dir"
  cd "$dir"
  npm install
  npm test
done