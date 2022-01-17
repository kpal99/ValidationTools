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
    filename = out_str[0].split('/')
    dir_str = "/eos/uscms/store/user/kpal/trimmed_files_v3.1/"
# using last part of out_str to creating a root file
    out_root_e = ROOT.TFile(dir_str + "e_channel/" + filename[ len(filename) - 1 ] + '.root',"RECREATE")
    out_root_e.mkdir("myana")
    out_root_e.cd("myana")
    treeProducer_e = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

#tight lepton selection. Only single lepton is required.
        for item in event.electrons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                treeProducer_e.processEvent(event.entry())
                treeProducer_e.processElectrons(event.electrons())
                treeProducer_e.processMuons(event.muons())
                treeProducer_e.processPuppiJets(event.jetspuppi())
                treeProducer_e.processFatJets(event.fatjets())
                treeProducer_e.processPuppiMissingET(event.metspuppi())
                treeProducer_e.fill()
                break

    treeProducer_e.write()
    out_root_e.Close()

    out_root_u = ROOT.TFile(dir_str + "u_channel/" + filename[ len(filename) - 1 ] + '.root',"RECREATE")
    out_root_u.mkdir("myana")
    out_root_u.cd("myana")
    treeProducer_u = TreeProducer()

    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

#tight lepton selection. Only single lepton is required.
        for item in event.muons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                treeProducer_u.processEvent(event.entry())
                treeProducer_u.processElectrons(event.electrons())
                treeProducer_u.processMuons(event.muons())
                treeProducer_u.processPuppiJets(event.jetspuppi())
                treeProducer_u.processFatJets(event.fatjets())
                treeProducer_u.processPuppiMissingET(event.metspuppi())
                treeProducer_u.fill()
                break

    treeProducer_u.write()
    out_root_u.Close()

if __name__ == "__main__":
    main()
