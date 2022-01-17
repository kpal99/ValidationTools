#!/bin/bash
filename=$1
sed -i -e 's/mgm01//' $filename
sed -i -e 's/:1094//' $filename
