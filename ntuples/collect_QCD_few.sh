#!/bin/bash
num=0
filename=QCD_short.txt

while getopts "n:s:" option
do
    case $option in
        n) num=$OPTARG
    esac
    case $option in
        s) filename=$OPTARG
    esac
done
xrdfs root://cmseos.fnal.gov/ ls -u /store/user/snowmass/Snowmass2021/DelphesNtuplizer/QCD_HT200to300_BGenFilter_TuneCUEP8M2T4_14TeV-madgraphMLM-pythia8_200PU | head -$num > $filename
xrdfs root://cmseos.fnal.gov/ ls -u /store/user/snowmass/Snowmass2021/DelphesNtuplizer/QCD_HT500to700_BGenFilter_TuneCUEP8M2T4_14TeV-madgraphMLM-pythia8_200PU | head -$num >> $filename
xrdfs root://cmseos.fnal.gov/ ls -u /store/user/snowmass/Snowmass2021/DelphesNtuplizer/QCD_HT700to1000_BGenFilter_TuneCUEP8M2T4_14TeV-madgraphMLM-pythia8_200PU | head -$num >> $filename
xrdfs root://cmseos.fnal.gov/ ls -u /store/user/snowmass/Snowmass2021/DelphesNtuplizer/QCD_HT1000to1500_BGenFilter_TuneCUEP8M2T4_14TeV-madgraphMLM-pythia8_200PU | head -$num >> $filename
xrdfs root://cmseos.fnal.gov/ ls -u /store/user/snowmass/Snowmass2021/DelphesNtuplizer/QCD_HT1500to2000_BGenFilter_TuneCUEP8M2T4_14TeV-madgraphMLM-pythia8_200PU | head -$num >> $filename
xrdfs root://cmseos.fnal.gov/ ls -u /store/user/snowmass/Snowmass2021/DelphesNtuplizer/QCD_HT2000toInf_BGenFilter_TuneCUEP8M2T4_14TeV-madgraphMLM-pythia8_200PU | head -$num >> $filename

sed -i -e 's/mgm01//' $filename
sed -i -e 's/:1094//' $filename
