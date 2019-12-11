#!/bin/bash

while getopts "o:i:s:" opt; do
    case "$opt" in
        o) OUTPATH=$OPTARG
            ;;
	i) INPATH=$OPTARG
	    ;;
	s) SAMPLE=$OPTARG
    esac
done

DELPHESVERSION="delphes3.4.2pre17"
DELPHESCARD="CMS_PhaseII_200PU_v04VAL.tcl"
FULLSIMCAMP="PhaseIIMTDTDRAutumn18MiniAOD"

INITIAL="$(echo $USER | head -c 1)"
WWWDIR=/eos/user/${INITIAL}/${USER}/www/${OUTPATH}

if [ ! -d "${WWWDIR}" ]; then
    mkdir -p ${WWWDIR}
fi

cp index.php ${WWWDIR}
mkdir ${WWWDIR}/efficiencies
mkdir ${WWWDIR}/fakerates
mkdir ${WWWDIR}/ptresponse
mkdir ${WWWDIR}/multiplicity
cp index.php ${WWWDIR}/efficiencies
cp index.php ${WWWDIR}/fakerates
cp index.php ${WWWDIR}/ptresponse
cp index.php ${WWWDIR}/multiplicity

cp ${INPATH}/*.png ${WWWDIR}
mv ${WWWDIR}/*efficiency*.png ${WWWDIR}/efficiencies/
mv ${WWWDIR}/*fakerate*.png ${WWWDIR}/fakerates/
mv ${WWWDIR}/*ptresponse*.png ${WWWDIR}/ptresponse/
mv ${WWWDIR}/*multiplicity*.png ${WWWDIR}/multiplicity/

echo $(date) >> ${WWWDIR}/postlog.txt
echo ${USER} >> ${WWWDIR}/postlog.txt
echo " " >> ${WWWDIR}/postlog.txt
echo ${DELPHESVERSION} >> ${WWWDIR}/postlog.txt
echo ${DELPHESCARD} >> ${WWWDIR}/postlog.txt
echo "FullSim  ${FULLSIMCAMP}" >> ${WWWDIR}/postlog.txt
echo ${SAMPLE} >>  ${WWWDIR}/postlog.txt

echo "Plots posted in ${WWWDIR} "

