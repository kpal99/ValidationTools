import ROOT, math, sys
from array import array
import itertools
import numpy as np


inputFile1 = sys.argv[1]
inputFile2 = sys.argv[2]

#_______________________________________________________________
def getListOfBranchNames(inputfile):

    f = ROOT.TFile.Open(inputfile)
    tree=f.Get("myana/mytree")
    
    branches = [br.GetName() for br in tree.GetListOfBranches()]
    names = ['_'.join(br.split('_')[1:]) for br in branches]

    return branches    



branches1 = getListOfBranchNames(inputFile1)
branches2 = getListOfBranchNames(inputFile2)

print ''

for b1 in branches1:
    found=False
    for b2 in branches2:
       if b1 == b2:
           found = True

    if found==False:
        print 'missing', b1, 'in reco flat tree'


print ''


for b2 in branches2:
    found=False
    for b1 in branches1:
       if b1 == b2:
           found = True

    if found==False:
        print 'missing', b2, 'in delphes flat tree'

