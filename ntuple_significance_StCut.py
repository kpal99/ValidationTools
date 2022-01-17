#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from mytree import TreeProducer
import sys

def main():
    if len(sys.argv) != 2:
        print "USAGE: {} <ntuple(s)>".format(sys.argv[0])
        sys.exit(0)
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0

    outputFile = sys.argv[1]
    out_str = outputFile.split('.root')
# using last part of out_str to creating a root file
    out_root = ROOT.TFile(out_str[0] + '_St.root',"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        for item in event.metspuppi():
            St = item.pt()

        sum_pt = 0
        for item in event.jetspuppi():
            sum_pt += item.pt()
        St += sum_pt

#tight lepton selection. Only single lepton is required.
        for item in event.electrons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                St += item.pt()
                break
        for item in event.muons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                St += item.pt()
                break
        if St >= 2000:
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())

            treeProducer.fill()

    treeProducer.write()
    out_root.Close()

if __name__ == "__main__":
    main()
