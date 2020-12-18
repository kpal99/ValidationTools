#!/bin/bash

date
hostname

source /cvmfs/sft.cern.ch/lcg/views/LCG_92/x86_64-centos7-gcc7-opt/setup.csh

FILEIN=${1}
FILEOUT=${2}
TCL=${3}
PARTICLE=${4}
OUTDIR=${5}

mkdir bin
mv NtupleDataFormat.py __init__.py bin/

echo "Running ntuple analyzer"
if [[ ${TCL} ]]
then 
    python -u ntuple_analyser.py -p ${PARTICLE} -i ${FILEIN} -o ${FILEOUT} --dumptcl
else
    python -u ntuple_analyser.py -p ${PARTICLE} -i ${FILEIN} -o ${FILEOUT}
fi

echo "Copying the file to eos"

if [[ -f ${FILEOUT} ]]
then
    xrdcp ${FILEOUT} root://eoscms.cern.ch/${OUTDIR}/${FILEOUT}
    XRDEXIT=$?
    if [[ $XRDEXIT -ne 0 ]]; then
	echo "exit code $XRDEXIT, failure in xrdcp of ROOT"
	exit $XRDEXIT
    fi
else
    echo "ERROR: can't find ${FILEOUT} to copy"
fi

rm *.root *.py
