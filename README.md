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

Run examples
============

NtupleDataFormat.py provides a wrapper to the ntuple such that it can be used as if it contained classes. An example implementation can be found in NtupleExample.py (ONLY GENPARTICLES AND MUON CLASSES HAVE BEEN IMPLEMENTED FOR NOW, NEED TO INCLUDE MISSING OBJECTS). You need to provide an ntuple ROOT file to it:

```
python ntuple_example.py tree.root

```

Analyze, plot, and post
=======================

1. Analyze. Pass arguments for the input file (an nutple) and output file (histograms). The particle can be "jet", "photon", "muon", or "electron". 

```
python -u ntuple_analyser.py -i path/to/input/ntuple.root -o outputplotfile.root -p particle --maxEvents NNNNNNN
```

2. Plot. Pass arguments for the two input files (delphes and fullsim), the output plot directory and the output file format (pdf/png).

```
python -u doPlot.py -f path/to/fullsimplots.root -d path/to/delphesplots.root -o mynewplotdir/ --outFormat pdf
```
If you have run steps 1 and 2 on a computer network other than LXPLUS, copy your plot directories to lxplus and run step 3 from there. 

3. Post (must be run on LXPLUS!). Pass arguments for the directory of plots to be copied, the destination on CERN EOS, and the sample name. The EOS path will be automatically prepended with: /eos/user/userinitial/username/www/. Instruction for setting up cernbox personal webpage can be found here <https://cernbox-manual.web.cern.ch/cernbox-manual/en/web/personal_website_content.html#create_personal_space>
 
```
sh postPlots.sh -i mynewplotdir/ -o delphes_validation/mynewplotdir/ -s PhotonFlat0to150_0PU
```

4. Presentation file. If folders that contain the pdf/png files are stored inside a parent directory and named exactly as: "TauTag", "BTag", "ELMu", "Photon" and "QCD", then pass only that parent directory.

```
python -u doPDF.py --parentpath path/
```

Else, specify each of them such as:

```
python -u doPDF.py -b path/to/Btag_plots/ -e path/to/ELMu_plots/ -g path/to/Photon_plots/ -q path/to/QCD_plots/ -t path/to/TauTag_plots/
```

Use steer script to do validation for any objects, plot and post
================================================================

steerValidation.sh does analysing, plotting, or posting based on given option. Options can be chosen from physics objects ```jet```, or ```plot```, ```post```. When running ```post```, the plots will be copied to the user's cernbox www page.

Instruction for setting up cernbox personal webpage can be found here \
<https://cernbox-manual.web.cern.ch/cernbox-manual/en/web/personal_website_content.html#create_personal_space>

Run steer script example:
```
./steerValidation.sh -o jet 
``` 



Run script to check compatibility between Reco and Delphes flatTrees
=====================================================================

```
python compare_trees.py delphes_flat_tree.root reco_flat_tree.root
```
