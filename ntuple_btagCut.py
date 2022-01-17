#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from mytree import TreeProducer
import sys

def main():
    if len(sys.argv) != 2:
        print "USAGE: {} <ntuple>".format(sys.argv[0])
        sys.exit(0)
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0

    outputFile = sys.argv[1]
    out_str = outputFile.split('.root')
    filename = out_str[0].split('/')
    dir_str = "/eos/uscms/store/user/kpal/trimmed_files_v3/QCD_Pt/"
# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + filename[ len(filename) - 1 ] + '_btag.root',"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        btag_multiplicity = 0
        for item in event.jetspuppi():
            if item.btag() > 0:
                btag_multiplicity += 1
#tight lepton selection. Only single lepton is required.
        if btag_multiplicity > 1:
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
