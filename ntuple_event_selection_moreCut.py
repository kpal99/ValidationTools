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
    additional_ak4 = 0
    btag1= 0
    fatjet2 = 0
    met75 = 0
    deltaR3 = 0
    tight_counter = 0
    total_events  = 0

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    #out_root= ROOT.TFile('/eos/uscms/store/user/kpal/trimmed_files_v7.2/' + os.path.basename(sys.argv[1]), "RECREATE")
    out_root= ROOT.TFile(sys.argv[1].split("_preSelected.root")[0] + "_moreCut.root", "RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

#        total_events += 1
# Jet selection cut
# pt of jets are descendingly sorted already for each event. So, checking if first jet has pt>300, then second jet has pt>150, at last third jet has pt>100
        counter = 0
        pt_array = []
        for j in event.jetspuppi():
            pt_array.append(j.pt())
            counter += 1
            if counter == 3:
                break
        if pt_array[0] > 300 and pt_array[1] > 150 and pt_array[2] > 100:
            j_counter += 1
        else:
            continue

# multiplicity of fatjet
        fatjet_count = 0
        h2b_count = 0
        h1b_count = 0
        w_count = 0
        lead_jet_eta = 0
        lead_jet_phi = 0
        jet_eta = []
        jet_phi = []
        for item in event.fatjets():
            if abs(item.eta()) < 2.4:
                fatjet_count += 1
                if fatjet_count == 1:
                    lead_jet_eta = item.eta()
                    lead_jet_phi = item.phi()
                else:
                    jet_eta.append(item.eta())
                    jet_phi.append(item.phi())

        if event.fatjetH2b() == 0 and event.fatjetH1b() == 0 and event.fatjetW() == 0:
            if event.jetM() > 3:
                pass
            else:
                continue
        additional_ak4 += 1

        if event.jetBtag() > 0:
            btag1 += 1
        else:
            continue

        if fatjet_count >= 2:
            fatjet2 += 1
        else:
            continue

        for item in event.metspuppi():
            met = item.pt()
        if met > 75:
            met75 += 1
        else:
            continue

        delRmin = []
        for i in range(len(jet_eta)):
            deltaR =  ((lead_jet_eta - jet_eta[i])**2 + (lead_jet_phi - jet_phi[i])**2)**0.5
            delRmin.append(deltaR)

        delRmin.sort()
        if delRmin[0] < 3:
            deltaR3 += 1
        else:
            continue


        #tree is being written
        treeProducer.processEvent(event.entry())
        treeProducer.processWeights(event.genweight(),event.lheweights())
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

    #print "Total Events                         : {}".format(total_events)
    print "Events after 3Jet selection          : {}".format(j_counter)
    print "Events after additional ak4 selection: {}".format(additional_ak4)
    print "Events after btag 1 selection        : {}".format(btag1)
    print "Events after 2 fatjet selection      : {}".format(fatjet2)
    print "Events after met 75 selection        : {}".format(met75)
    print "Events after delR < 3 selection      : {}".format(deltaR3)


if __name__ == "__main__":
    main()
