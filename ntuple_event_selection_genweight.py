#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from ntuple_chain import ntuple_chain
from mytree import TreeProducer
import sys

def main():
    ntuple_array = ntuple_chain(sys.argv[1])
    maxEvents = 0

    outputFile = sys.argv[1]
# using last part of out_str to creating a root file
    out_root = ROOT.TFile(outputFile + '_genweight.root',"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for ntuple in ntuple_array:
        for event in ntuple:
            if maxEvents > 0 and event.entry() >= maxEvents:
                break

            treeProducer.processWeights(event.genweight())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()

if __name__ == "__main__":
    main()
