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
    tight_counter = 0
    loose_counter = 0
    total_events  = 0
    gen_weight = 0.

# using last part of out_str to creating a root file
    outputFile = sys.argv[1]
    ntuple = Ntuple(sys.argv[1])
    out_root = ROOT.TFile('/eos/uscms/store/user/kpal/trimmed_files_v6/' + os.path.basename(sys.argv[1]),"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        gen_weight += event.genweight()
#tight lepton selection. Only single lepton is required.
        tight_electron_found = False
        tight_muon_found = False
        e_tight_count = 0
        u_tight_count = 0
        e_loose_count = 0
        u_loose_count = 0
        for e in event.electrons():
            if e.idpass() == 1 and e.pt() > 10 and abs(e.eta()) < 2.5:
                e_loose_count +=1
            if e.idpass() >= 4 and e.pt() > 60 and abs(e.eta()) < 2.5:
                e_tight_count += 1
                lepton_pt = e.pt()
                lepton_eta = e.eta()
                lepton_phi = e.phi()
                lepton_mass = e.mass()
                lepton_charge = e.charge()
                lepton_idvar = e.idvar()
                lepton_reliso = e.reliso()
                lepton_idpass = e.idpass()
                lepton_isopass = e.isopass()
        for u in event.muons():
            if u.idpass() == 1 and u.pt() > 10 and abs(u.eta()) < 2.4:
                u_loose_count +=1
            if u.idpass() >= 4 and u.pt() > 60 and abs(u.eta()) < 2.4:
                u_tight_count += 1
                lepton_pt = u.pt()
                lepton_eta = u.eta()
                lepton_phi = u.phi()
                lepton_mass = u.mass()
                lepton_charge = u.charge()
                lepton_idvar = u.idvar()
                lepton_reliso = u.reliso()
                lepton_idpass = u.idpass()
                lepton_isopass = u.isopass()
        if e_tight_count == 0 and u_tight_count == 1:
            tight_muon_found = True
        elif e_tight_count == 1 and u_tight_count == 0:
            tight_electron_found = True
        else:
            continue
        tight_counter += 1

        if e_loose_count > 0 or u_loose_count > 0:
            continue
        loose_counter += 1

        treeProducer.processTightElectrons_(tight_electron_found, lepton_pt, lepton_eta, lepton_phi, lepton_mass, lepton_charge, lepton_idvar, lepton_reliso, lepton_idpass, lepton_isopass)
        treeProducer.processTightMuons_(tight_muon_found, lepton_pt, lepton_eta, lepton_phi, lepton_mass, lepton_charge, lepton_idvar, lepton_reliso, lepton_idpass, lepton_isopass)
        treeProducer.processEvent(event.entry())
        treeProducer.processWeights(event.genweight())
        treeProducer.processVtxs(event.vtxs())
        treeProducer.processElectrons(event.electrons())
        treeProducer.processMuons(event.muons())
        treeProducer.processPuppiJets(event.jetspuppi())
        treeProducer.processJetsMul_(event.jetM(), event.jetBtag(), event.jetHt(), event.jetSt())
        treeProducer.processFatJets(event.fatjets())
        treeProducer.processFatjetsMul_(event.fatjetM(), event.fatjetH2b(), event.fatjetH1b(), event.fatjetW())
        treeProducer.processPuppiMissingET(event.metspuppi())

        treeProducer.fill()

    treeProducer.write()
    out_root.Close()

    print "Total Events                                 : {}".format(ntuple.nevents())
    print "Total genweight                              : {}".format(gen_weight)
    print "Events after tight-lepton selection          : {}".format(tight_counter)
    print "Events after tight-lepton-looseVeto selection: {}".format(loose_counter)

if __name__ == "__main__":
    main()
