ValidationTools
===============

This package contains various scripts for analyzing the flat tree output produced in RecoNtuplizer and DelphesNtuplizer.

Table of contents
=================
  * [Clone](#clone)
  * [Initialisation](#initilisation)
  * [Run examples](#run-examples)
  * [Use steer script to do validation for any objects, plot and post](#steerValidation)


Clone
=====

If you do not attempt to contribute to this repository, simply clone it:
```
git clone git@github.com:recotoolsbenchmarks/ValidationTools.git
```

If you aim at contributing to the repository, you need to fork this repository (via the fork button) and then clone the forked repository:
```
git clone git@github.com:YOURGITUSERNAME/ValidationTools.git
cd ValidationTools
git remote add upstream git@github.com:recotoolsbenchmarks/ValidationTools.git
```
You can then regularly update your fork via:
```
git fetch upstream && git merge upstream/master
```

If you want to submit a new feature to ```recotoolsbenchmarks/ValidationTools``` you have to do it via pull-request (PR):
So, first commit and push your changes to ```YOURGITUSERNAME/ValidationTools``` and then make a PR via the github interface.


Initialisation
==============

This package requires python, ROOT and pandas:

```
source /cvmfs/sft.cern.ch/lcg/views/LCG_92/x86_64-centos7-gcc7-opt/setup.(c)sh
./init.sh
```

Setting up a CMSSW environment via cmsenv also works.


Script ran at condor for job submission
=====================================================================

```
#!/bin/bash

tar xf ValidationTools.tar.gz
cd ValidationTools
source /cvmfs/sft.cern.ch/lcg/views/LCG_92/x86_64-centos7-gcc7-opt/setup.sh
./init.sh
python ntuple_event_selection_tight.py $1
python ntuple_event_selection_tight_met.py "$1"_tight.root
python ntuple_event_selection_tight_met_jet.py "$1"_tight_met.root
xrdcp -f "$1"_tight.root root://cmseos.fnal.gov//eos/uscms/store/user/kpal/trimmed_files_v4
xrdcp -f "$1"_tight_met.root root://cmseos.fnal.gov//eos/uscms/store/user/kpal/trimmed_files_v4
xrdcp -f "$1"_tight_met_jet.root root://cmseos.fnal.gov//eos/uscms/store/user/kpal/trimmed_files_v4
```
