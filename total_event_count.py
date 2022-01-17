#import contextlib2
import ROOT
import sys
from bin.NtupleDataFormat import Ntuple

if len(sys.argv) < 2:
    print "USAGE: {} <ntuple(s)>".format(sys.argv[0])
    sys.exit(1)
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
for arg in sys.argv[1:]:
    ntuple = Ntuple(arg)
    print "{:<90}    {:<20}".format(arg, ntuple.nevents() + 1)
