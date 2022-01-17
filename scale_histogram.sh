#!/bin/bash

for i in {1..20}
do
    python scale_histogram.py `sed "{$i q;d}" all_plots.txt`
done
