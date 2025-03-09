#!/bin/bash
set -e

# If no filenames are passed, exit gracefully
if [ $# -eq 0 ]; then
  exit 0
fi

# Collect normalized unique directories containing the modified files
DIRS_ARRAY=()
for file in "$@"; do
  dir=$(dirname "$file")
  # Normalize directory names to absolute paths
  dir=$(cd "$dir" && pwd -P)
  DIRS_ARRAY+=("$dir")
done

# Remove duplicates from DIRS_ARRAY
IFS=$'\n' read -r -d '' -a DIRS_UNIQUE < <(printf "%s\n" "${DIRS_ARRAY[@]}" | sort -u && printf '\0')

# Initialize a variable to track if any check fails
FAILED=0

# For each unique directory, run 'poetry lock --check'
for dir in "${DIRS_UNIQUE[@]}"; do
  # Only proceed if pyproject.toml exists in the directory
  if [ -f "$dir/pyproject.toml" ]; then
    echo "Checking pyproject.toml against poetry.lock in $dir"
    pushd "$dir" > /dev/null
    if ! poetry check --lock; then
      echo "Error: poetry.lock is not up to date in $dir"
      FAILED=1
    fi
    popd > /dev/null
  fi
done

# Exit with failure if any check failed
if [ "$FAILED" -ne 0 ]; then
  echo "Please run 'poetry lock' in the directories above and commit the changes."
  exit 1
fi
