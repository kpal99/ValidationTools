#!/bin/bash
num=0
filename=QCD_
while getopts "n:s:" option
do
    case $option in
        n) num=$OPTARG
    esac
    case $option in
        s) filename=$OPTARG
    esac
done
for segment in 50to100 100to200 200to300
do
    xrdfs root://cmseos.fnal.gov/ ls -u   /store/user/snowmass/Snowmass2021/DelphesNtuplizer/QCD_HT"$segment"_BGenFilter_TuneCUEP8M2T4_14TeV-madgraphMLM-pythia8_200PU > $filename$segment.txt
    sed -i -e 's/mgm01//' $filename$segment.txt
    sed -i -e 's/:1094//' $filename$segment.txt
done

