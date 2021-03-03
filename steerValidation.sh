#!/bin/bash

# USER wenyu

DELPHESVERSION="delphes3.4.3pre01"
DELPHESCARD="CMS_PhaseII_200PU_v04VAL.tcl"

FULLSIMCAMP="Phase2HLTTDRWinter20RECOMiniAOD"
#FULLSIMCAMP="PhaseIITDRSpring19MiniAOD"
SAMPLE="DYToLL_M-50_TuneCP5_14TeV-pythia8_200PU"

WWWDIR=/eos/user/w/wenyu/www/delphes_validation
CURDIR=20200820/met

while getopts "o:s:" opt; do
    case "$opt" in
        i) INFILE=$OPTARG
            ;;
        o) STORAGE=$OPTARG
            ;;
	p) PARTICLE=$OPTARG
	    ;;
	c) COMMAND=$OPTARG  # analyze, plot, post
    esac
done

WORKDIR=${STORAGE}
if [ -z ${WORKDIR} ]; then
    WORKDIR=${PWD}
fi    
PLOTDIR=plotsMet

case ${COMMAND} in 

    met)

#      input=/eos/cms/store/group/upgrade/RTB/FullsimFlat_110X/DYToLL_M-50_14TeV_HLTTDRWinter20_200PU.root
      input=/eos/cms/store/group/upgrade/RTB/DelphesFlat_343pre01/DYToLL_M-50_TuneCP5_14TeV-pythia8_200PU.root
      output=histo_delp/val_met.root
      python ntuple_analyseMET.py -i ${input} -o ${output} -p met --maxEvents -1

    ;;

    jetpuppi)

#      input=/eos/cms/store/group/upgrade/RTB/DelphesFlat_343pre01/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_200PU.root
#      output=histo_delp/val_jetpuppi.root
      input=/eos/cms/store/group/upgrade/RTB/FullsimFlat_110X/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_200PU.root
      output=histo_full/val_jetpuppi.root
      echo "Running jetpuppi analyser on ${input}, output file ${output} "
      python ntuple_analyser.py -i ${input} -o ${output} -p jetpuppi --maxEvents -1

      ;;

    jetchs)

      input=/eos/cms/store/group/upgrade/RTB/DelphesFlat_343pre01/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_200PU.root
      output=histo_delp/val_jetchs.root
#      input=/eos/cms/store/group/upgrade/RTB/FullsimFlat_110X/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_200PU.root
#      output=histo_full/val_jetchs.root
      echo "Running jetchs analyser on ${input}, output file ${output} "
      python ntuple_analyser.py -i ${input} -o ${output} -p jetchs --maxEvents -1

      ;;

    electron)
     
      input=/afs/cern.ch/work/i/ilmargje/public/delphes/FastSim_DYToMuMuorEleEle_PU200_flattree.root
#      input=/afs/cern.ch/work/i/ilmargje/public/fullsim/FullSim_DYToMuMuorEleEle_PU200_FlatTree.root
      output=histo_delp/val_elec.root
      echo "Running electron analyser on ${input}, output file ${output} "
      python ntuple_analyser.py -i ${input} -o ${output} -p electron --maxEvents 100000

      ;;

    muon)

      input=/afs/cern.ch/work/i/ilmargje/public/delphes/FastSim_DYToMuMuorEleEle_PU200_flattree.root
#      input=/afs/cern.ch/work/i/ilmargje/public/fullsim/FullSim_DYToMuMuorEleEle_PU200_FlatTree.root
      output=histo_delp/val_mu.root
      echo "Running electron analyser on ${input}, output file ${output} "
      python ntuple_analyser.py -i ${input} -o ${output} -p muon --maxEvents 100000

      ;;

    plot)

      python doPlot.py -d histo_delp/val_met.root -f histo_full/val_met.root -o ${PLOTDIR}

      ;;

    post)

      POSTDIR=${WWWDIR}/${CURDIR}
      if [ ! -d "${POSTDIR}" ]; then
        mkdir ${POSTDIR}
      fi

      cp index.php ${POSTDIR}
      cp ${WORKDIR}/${PLOTDIR}/*.png ${POSTDIR}
      cp ${WORKDIR}/${PLOTDIR}/*.png ${POSTDIR}

      echo " " >> ${POSTDIR}/postlog.txt
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
