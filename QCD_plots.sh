#!/bin/bash

for var in "$@"
do
    python ntuple_event_selection.py $var > "$var".output
    echo "=== $var ==="
done
