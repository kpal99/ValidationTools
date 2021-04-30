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
WWWDIR=/afs/cern.ch/user/s/selvaggi/www/${OUTPATH}

if [ ! -d "${WWWDIR}" ]; then
    mkdir -p ${WWWDIR}
fi

cp index.php ${WWWDIR}
mkdir -p  ${WWWDIR}/efficiencies
mkdir -p  ${WWWDIR}/efficiencies/loose
mkdir -p  ${WWWDIR}/efficiencies/medium
mkdir -p  ${WWWDIR}/efficiencies/tight
mkdir -p  ${WWWDIR}/fakerates
mkdir -p  ${WWWDIR}/fakerates/loose
mkdir -p  ${WWWDIR}/fakerates/medium
mkdir -p  ${WWWDIR}/fakerates/tight
mkdir -p  ${WWWDIR}/resolution
mkdir -p  ${WWWDIR}/resolution/loose
mkdir -p  ${WWWDIR}/resolution/medium
mkdir -p  ${WWWDIR}/resolution/tight
mkdir -p  ${WWWDIR}/ptresponse
mkdir -p  ${WWWDIR}/ptresponse/loose
mkdir -p  ${WWWDIR}/ptresponse/medium
mkdir -p  ${WWWDIR}/ptresponse/tight
mkdir -p  ${WWWDIR}/multiplicity

cp index.php ${WWWDIR}/multiplicity
cp index.php ${WWWDIR}/efficiencies
cp index.php ${WWWDIR}/efficiencies/loose
cp index.php ${WWWDIR}/efficiencies/medium
cp index.php ${WWWDIR}/efficiencies/tight
cp index.php ${WWWDIR}/fakerates
cp index.php ${WWWDIR}/fakerates/loose
cp index.php ${WWWDIR}/fakerates/medium
cp index.php ${WWWDIR}/fakerates/tight
cp index.php ${WWWDIR}/resolution
cp index.php ${WWWDIR}/resolution/loose
cp index.php ${WWWDIR}/resolution/medium
cp index.php ${WWWDIR}/resolution/tight
cp index.php ${WWWDIR}/ptresponse
cp index.php ${WWWDIR}/ptresponse/loose
cp index.php ${WWWDIR}/ptresponse/medium
cp index.php ${WWWDIR}/ptresponse/tight
cp index.php ${WWWDIR}/multiplicity

cp ${INPATH}/*.png ${WWWDIR}
mv ${WWWDIR}/*efficiency*loose*.png ${WWWDIR}/efficiencies/loose/
mv ${WWWDIR}/*efficiency*medium*.png ${WWWDIR}/efficiencies/medium/
mv ${WWWDIR}/*efficiency*tight*.png ${WWWDIR}/efficiencies/tight/
mv ${WWWDIR}/*efficiency*.png ${WWWDIR}/efficiencies/
mv ${WWWDIR}/*fakerate*loose*.png ${WWWDIR}/fakerates/loose/
mv ${WWWDIR}/*fakerate*medium*.png ${WWWDIR}/fakerates/medium/
mv ${WWWDIR}/*fakerate*tight*.png ${WWWDIR}/fakerates/tight/
mv ${WWWDIR}/*fakerate*.png ${WWWDIR}/fakerates/
mv ${WWWDIR}/*loose*resolution*.png ${WWWDIR}/resolution/loose/
mv ${WWWDIR}/*medium*resolution*.png ${WWWDIR}/resolution/medium/
mv ${WWWDIR}/*tight*resolution*.png ${WWWDIR}/resolution/tight/
mv ${WWWDIR}/*resolution*.png ${WWWDIR}/resolution/
mv ${WWWDIR}/*ptresponse*loose*.png ${WWWDIR}/ptresponse/loose/
mv ${WWWDIR}/*ptresponse*medium*.png ${WWWDIR}/ptresponse/medium/
mv ${WWWDIR}/*ptresponse*tight*.png ${WWWDIR}/ptresponse/tight/
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

