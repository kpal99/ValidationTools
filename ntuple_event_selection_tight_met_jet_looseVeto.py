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

    m_counter = 0
    j_counter = 0
    loose_counter = 0
    total_events  = 0

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    filename = os.path.basename(inFile)
    out_str = '/eos/uscms/store/user/kpal/trimmed_files_v2.2/'
# using last part of out_str to creating a root file
    out_root = ROOT.TFile(out_str + filename,"RECREATE")   #outfile is created
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    total_events += ntuple.nevents()
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

#tight lepton selection. Only single lepton is required.
        tight_electron_found = False
        tight_muon_found = False
        e_tight_count = 0
        u_tight_count = 0
        e_loose_count = 0
        u_loose_count = 0
        for e in event.electrons():
            if ( e.idpass() == 1 or e.idpass() == 2 ) and e.pt() > 10 and abs(e.eta()) < 2.5:
                e_loose_count +=1
        for u in event.muons():
            if ( u.idpass() == 1 or u.idpass() == 2 ) and u.pt() > 10 and abs(u.eta()) < 2.4:
                u_loose_count +=1
        if e_loose_count > 0 or u_loose_count > 0:
            continue
        loose_counter += 1

        treeProducer.processEvent(event.entry())
        #treeProducer.processWeights(event.genweight())
        treeProducer.processElectrons(event.electrons())
        treeProducer.processMuons(event.muons())
        treeProducer.processPuppiJets(event.jetspuppi())
        treeProducer.processFatJets(event.fatjets())
        treeProducer.processPuppiMissingET(event.metspuppi())

        treeProducer.fill()

    treeProducer.write()
    out_root.Close()

    print "Total event before additonal cut: {}".format(total_events)
    print "Events after loose-leptonVeto   : {}".format(loose_counter)

if __name__ == "__main__":
    main()
