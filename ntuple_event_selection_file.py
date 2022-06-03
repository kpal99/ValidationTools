#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from ntuple_chain import ntuple_chain
from mytree import TreeProducer
import sys
import os

def main():
    maxEvents = 0
    tight_counter = 0
    total_events  = 0

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
# using last part of out_str to creating a root file
    out_root= ROOT.TFile('/eos/uscms/store/user/kpal/trimmed_files_v20/' + os.path.basename(sys.argv[1]), "RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        total_events += 1
#tight lepton selection. Only single lepton is required.
        tight_electron_found = False
        tight_muon_found = False
        e_tight_count = 0
        u_tight_count = 0
        for e in event.tightElectrons():
            if e.isopass() >=4 and e.reliso() >= 0:
                e_tight_count += 1
        for u in event.tightMuons():
            if u.isopass() >=4 and u.reliso() >= 0:
                u_tight_count += 1

        if e_tight_count == 0 and u_tight_count == 1:
            tight_muon_found = True
        elif e_tight_count == 1 and u_tight_count == 0:
            tight_electron_found = True
        else:
            continue
        tight_counter += 1


        #tree is being written
        treeProducer.processEvent(event.entry())
        treeProducer.processWeights(event.genweight())
        treeProducer.processVtxs(event.vtxs())
        treeProducer.processElectrons(event.electrons())
        treeProducer.processMuons(event.muons())
        treeProducer.processTightElectrons(event.tightElectrons())
        treeProducer.processTightMuons(event.tightMuons())
        treeProducer.processPuppiJets(event.jetspuppi())
        treeProducer.processJetsMul_(event.jetM(), event.jetBtag(), event.jetHt(), event.jetSt())
        treeProducer.processFatJets(event.fatjets())
        treeProducer.processFatjetsMul_(event.fatjetM(), event.fatjetH2b(), event.fatjetH1b(), event.fatjetW())
        treeProducer.processPuppiMissingET(event.metspuppi())
        treeProducer.fill()

    treeProducer.write()
    out_root.Close()

    print "Total Events                       : {}".format(total_events)
    print "Events after tight-lepton selection: {}".format(tight_counter)

if __name__ == "__main__":
    main()
