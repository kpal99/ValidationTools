#!/bin/bash

# USER wenyu

DELPHESVERSION="delphes3.4.2pre17"
DELPHESCARD="CMS_PhaseII_200PU_v04VAL.tcl"

FULLSIMCAMP="PhaseIIMTDTDRAutumn18MiniAOD"
SAMPLE="QCD..."

WWWDIR=/eos/user/w/wenyu/www/delphes_validation
CURDIR=20190830

while getopts "o:s:" opt; do
    case "$opt" in
        o) COMMAND=$OPTARG
            ;;
        s) STORAGE=$OPTARG
            ;;
    esac
done

WORKDIR=${STORAGE}
if [ -z ${WORKDIR} ]; then
    WORKDIR=${PWD}
fi    
PLOTDIR=plots

case ${COMMAND} in 

    jet)

      input=../DelphesNtuplizer/ntuples/QCD_Pt-15To7000_Autumn18_1et2.root
      output=histo_delp/val.root

      echo "Running jet analyser on ${input}, output file ${output} "
      python ntuple_analyser.py -i ${input} -o ${output} -p jet --maxEvents 100

      ;;

    plot)

      python doPlot.py ${PLOTDIR}

      ;;

    post)

      POSTDIR=${WWWDIR}/${CURDIR}
      if [ ! -d "${POSTDIR}" ]; then
        mkdir ${POSTDIR}
      fi

      cp ${WWWDIR}/index.php ${POSTDIR}
      cp ${WORKDIR}/${PLOTDIR}/*.png ${POSTDIR}

      echo $(date) >> ${POSTDIR}/postlog.txt
      echo ${USER} >> ${POSTDIR}/postlog.txt
      echo " " >> ${POSTDIR}/postlog.txt
      echo ${DELPHESVERSION} >> ${POSTDIR}/postlog.txt
      echo ${DELPHESCARD} >> ${POSTDIR}/postlog.txt
      echo "FullSim  ${FULLSIMCAMP}" >> ${POSTDIR}/postlog.txt
      echo ${SAMPLE} >>  ${POSTDIR}/postlog.txt

      echo "Plots posted in ${POSTDIR} "

      ;;

esac
