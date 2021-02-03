#!/bin/bash

date
hostname

source /cvmfs/sft.cern.ch/lcg/views/LCG_92/x86_64-centos7-gcc7-opt/setup.sh

FILEIN=${1}
FILEOUT=${2}
TCL=${3}
PARTICLE=${4}
IDLIST=${5}
OUTDIR=${6}

echo "FILEIN = ${FILEIN}"
echo "FILEOUT = ${FILEOUT}"
echo "TCL = ${TCL}"
echo "PARTICLE = ${PARTICLE}"
echo "IDLIST = ${IDLIST}"
echo "OUTDIR = ${OUTDIR}"

mkdir bin
mv NtupleDataFormat.py __init__.py bin/

for ifile in $IDLIST; do

    echo "Running ntuple analyzer"
    if [[ ${TCL} == "True" ]]
    then 
	echo "Using TCL settings"
	if [[ ${PARTICLE} == "all" ]]
	then
	    echo "MUONS:"
	    python -u ntuple_analyser.py -p muon -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_muon_${ifile}.root --dumptcl
	    echo "ELECTRONS:"
	    python -u ntuple_analyser.py -p electron -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_electron_${ifile}.root --dumptcl
	    echo "PHOTONS:"
	    python -u ntuple_analyser.py -p photon -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_photon_${ifile}.root --dumptcl
	    echo "JETS:"
	    python -u ntuple_analyser.py -p jetpuppi -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_jet_${ifile}.root --dumptcl
	    echo "MET:"
	    python -u ntuple_analyser.py -p met -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_met_${ifile}.root --dumptcl
	    
	else
	    python -u ntuple_analyser.py -p ${PARTICLE} -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_${ifile}.root --dumptcl
	fi
    else
	if [[ ${PARTICLE} == "all" ]]
	then
	    echo "MUONS:"
	    python -u ntuple_analyser.py -p muon -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_muon_${ifile}.root
	    echo "ELECTRONS:"
	    python -u ntuple_analyser.py -p electron -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_electron_${ifile}.root
	    echo "PHOTONS:"
	    python -u ntuple_analyser.py -p photon -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_photon_${ifile}.root
	    echo "JETS":
	    python -u ntuple_analyser.py -p jetpuppi -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_jet_${ifile}.root
	    echo "MET":
	    python -u ntuple_analyser.py -p met -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_met_${ifile}.root
	else
	    python -u ntuple_analyser.py -p ${PARTICLE} -i root://eoscms.cern.ch/${FILEIN}_${ifile}.root -o ${FILEOUT}_${ifile}.root
	fi
    fi
done

echo "HADDING:"
hadd -k ${FILEOUT}.root ${FILEOUT}_*.root

echo "Copying the file to eos"

if [[ -f ${FILEOUT}.root ]]
then
    xrdcp ${FILEOUT}.root root://eoscms.cern.ch/${OUTDIR}/${FILEOUT}.root
    XRDEXIT=$?
    if [[ $XRDEXIT -ne 0 ]]; then
	echo "exit code $XRDEXIT, failure in xrdcp of ROOT"
	rm *.root *.py
	exit $XRDEXIT
    fi
else
    echo "ERROR: can't find ${FILEOUT} to copy"
fi

rm *.root *.py

