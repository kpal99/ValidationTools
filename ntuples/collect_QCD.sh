#!/bin/bash
num=0
filename=QCD_bEnriched_HT
while getopts "n:s:" option
do
    case $option in
        n) num=$OPTARG
    esac
    case $option in
        s) filename=$OPTARG
    esac
done
for segment in 200to300 300to500 500to700 700to1000 1000to1500 1500to2000 2000toInf
do
    xrdfs root://cmseos.fnal.gov/ ls -u   /store/user/snowmass/Snowmass2021/DelphesNtuplizer/"$filename$segment"_TuneCUETP8M1_14TeV-madgraphMLM-pythia8_200PU > $filename$segment.txt
    sed -i -e 's/mgm01//' $filename$segment.txt
    sed -i -e 's/:1094//' $filename$segment.txt
done

