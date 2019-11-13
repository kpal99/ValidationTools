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
./init.sh
```

Run examples
============

NtupleDataFormat.py provides a wrapper to the ntuple such that it can be used as if it contained classes. An example implementation can be found in NtupleExample.py (ONLY GENPARTICLES AND MUON CLASSES HAVE BEEN IMPLEMENTED FOR NOW, NEED TO INCLUDE MISSING OBJECTS). You need to provide an ntuple ROOT file to it:

```
python ntuple_example.py tree.root

```

Use steer script to do validation for any objects, plot and post
================================================================

steerValidation.sh does analysing, plotting, or posting based on given option. Options can be choose from physics objects ```jet```, ```muon```, ```electron```, ```photon```, or ```plot```, ```post```.
Instruction for setting up cernbox personal webpage can be found here
<https://cernbox-manual.web.cern.ch/cernbox-manual/en/web/personal_website_content.html#create_personal_space>

Run steer script example:
```
./steerValidation.sh -o jet 
``` 
