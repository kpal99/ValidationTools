#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from ntuple_chain import ntuple_chain
from mytree import TreeProducer
import sys

def main():
    maxEvents = 0

    m_counter = 0
    j_counter = 0
    tight_counter = 0
    total_events  = 0

    inFile = sys.argv[1]
    outputFile = sys.argv[1].split('.root')
    ntuple = Ntuple(inFile)
# using last part of out_str to creating a root file
    out_root = ROOT.TFile(outputFile[0] + '_met.root',"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

# MET cut of pt > 60GeV
# every event has only one METS thus no need to continue within the event.metspuppi loop.
        counter = 0
        for m in event.metspuppi():
            if m.pt() > 60:
                counter += 1
        if counter == 1:
            m_counter += 1
        else:
            continue

        treeProducer.processEvent(event.entry())
        treeProducer.processWeights(event.genweight())
        treeProducer.processVtxs(event.vtxs())
        treeProducer.processElectrons(event.electrons())
        treeProducer.processMuons(event.muons())
        treeProducer.processTightElectrons(event.tightElectrons())
        treeProducer.processTightMuons(event.tightMuons())
        treeProducer.processPuppiJets(event.jetspuppi())
        treeProducer.processFatJets(event.fatjets())
        treeProducer.processPuppiMissingET(event.metspuppi())

        treeProducer.fill()

    treeProducer.write()
    out_root.Close()

    print "Events after MET selection: {} ".format(m_counter)


if __name__ == "__main__":
    main()
