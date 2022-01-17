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

    m_counter = 0
    j_counter = 0
    tight_counter = 0
    total_events  = 0

    outputFile = sys.argv[1]
# using last part of out_str to creating a root file
    out_root = ROOT.TFile(outputFile + '_tight.root',"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for ntuple in ntuple_array:
        total_events += ntuple.nevents() + 1
        for event in ntuple:
            if maxEvents > 0 and event.entry() >= maxEvents:
                break

#tight lepton selection. Only single lepton is required.
            tight_electron_found = False
            tight_muon_found = False
            e_tight_count = 0
            u_tight_count = 0
            for e in event.electrons():
                if e.idpass() > 4 and e.pt() > 60 and abs(e.eta()) < 3.0:
                    e_tight_count += 1
            for u in event.muons():
                if u.idpass() > 4 and u.pt() > 60 and abs(u.eta()) < 2.8:
                    u_tight_count += 1
            if e_tight_count == 0 and u_tight_count == 1:
                tight_counter += 1
                tight_muon_found = True
            elif e_tight_count == 1 and u_tight_count == 0:
                tight_counter += 1
                tight_electron_found = True
            else:
                continue

            treeProducer.processEvent(event.entry())
            treeProducer.processWeights(event.genweight())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())

            treeProducer.fill()

    treeProducer.write()
    out_root.Close()

    print "Total Events {}".format(total_events)
    print "Events after tight-lepton selection: {}".format(tight_counter)

if __name__ == "__main__":
    main()
