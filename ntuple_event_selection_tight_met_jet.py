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
    out_root = ROOT.TFile(outputFile[0] + '_jet.root',"RECREATE")   #outfile is created
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

# Jet selection cut
# pt of jets are descendingly sorted already for each event. So, checking if first jet has pt>200, then second jet has pt>100, at last third jet has pt>50
        lepton_eta = 0
        lepton_phi = 0
        for item in event.electrons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                lepton_eta = item.eta()
                lepton_phi = item.phi()
                break
        for item in event.muons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                lepton_eta = item.eta()
                lepton_phi = item.phi()
                break

        sum_pt = 0
        pt_array = []
        multiplicity = 0
        for j in event.jetspuppi():
            if j.pt() > 30 and abs(j.eta()) < 2.4:
                delR = ( ( lepton_eta - j.eta() ) ** 2 + ( lepton_phi - j.phi() ) ** 2 ) ** 0.5
                if delR >= 0.4:
                    pt_array.append(j.pt())
                    sum_pt += j.pt()
                    multiplicity += 1
        if multiplicity > 2 and pt_array[0] > 200 and pt_array[1] > 100 and pt_array[2] > 50 and sum_pt > 400:
            j_counter += 1
        else:
            continue


        #tree is being written
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

    print "Events after Jets selection: {}".format(j_counter)


if __name__ == "__main__":
    main()
