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
        sum_pt = 0
        pt_array = []
        multiplicity = 0
        btag_multiplicity = 0
        for j in event.jetspuppi():
            if j.pt() > 30 and abs(j.eta()) < 2.4:
                pt_array.append(j.pt())
                sum_pt += j.pt()
                multiplicity += 1
            if j.btag() > 0:
                btag_multiplicity += 1
        if multiplicity > 2 and pt_array[0] > 200 and pt_array[1] > 100 and pt_array[2] > 50 and sum_pt > 400:
            j_counter += 1
        else:
            continue

        St = sum_pt
        for item in event.metspuppi():
            St += item.pt()

        for item in event.tightElectrons():
            St += item.pt()
        for item in event.tightMuons():
            St += item.pt()


        #tree is being written
        treeProducer.processEvent(event.entry())
        treeProducer.processWeights(event.genweight())
        treeProducer.processVtxs(event.vtxs())
        treeProducer.processElectrons(event.electrons())
        treeProducer.processMuons(event.muons())
        treeProducer.processTightElectrons(event.tightElectrons())
        treeProducer.processTightMuons(event.tightMuons())
        treeProducer.processPuppiJets(event.jetspuppi())
        treeProducer.processJetsMul_(multiplicity, btag_multiplicity, sum_pt, St)
        treeProducer.processFatJets(event.fatjets())
        treeProducer.processPuppiMissingET(event.metspuppi())

        treeProducer.fill()

    treeProducer.write()
    out_root.Close()

    print "Events after Jets selection: {}".format(j_counter)


if __name__ == "__main__":
    main()
