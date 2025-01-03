#!/bin/bash

dirs=$(find . -maxdepth 1 -type d -name '*worker*')
echo "Running tests for all workers: $dirs"

# We will disable watch mode
for dir in $dirs; do
  echo "Testing worker: $dir"
  cd "$dir"
  npm ci
  npm test -- --run
done