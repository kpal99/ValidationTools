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
    loose_counter = 0
    tight_counter = 0
    total_events  = 0

    outputFile = sys.argv[1]
# using last part of out_str to creating a root file
    out_root = ROOT.TFile(outputFile + '_EventSelection.root',"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for ntuple in ntuple_array:
        total_events += ntuple.nevents() + 1
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

#        print ""
#        print "event {}".format(event.entry()+1)
#        print ""

# Jet selection cut
# pt of jets are descendingly sorted already for each event. So, checking if first jet has pt>200, then second jet has pt>100, at last third jet has pt>50
            sum_pt = 0
            first = 0
            second = 0
            third = 0
            multiplicity = 0
            btag_multiplicity = 0
            for j in event.jetspuppi():
                if first == 0 and j.pt() > 200 and abs(j.eta()) < 2.4:
                    first += 1
                elif second == 0 and j.pt() > 100 and abs(j.eta()) < 2.4:
                    second += 1
                elif third == 0 and j.pt() > 50 and abs(j.eta()) < 2.4:
                    third += 1
                if j.pt() > 30 and abs(j.eta()) < 2.4:
                    sum_pt += j.pt()
            if first == 1 and second == 1 and third == 1 and sum_pt > 400:
                j_counter += 1
            else:
                continue

#tight lepton selection. Only single lepton is required.
            tight_electron_found = False
            tight_muon_found = False
            e_tight_count = 0
            u_tight_count = 0
            for e in event.electrons():
                if e.idpass() > 4 and e.pt() > 60 and abs(e.eta()) < 2.5:
                    e_tight_count += 1
            for u in event.muons():
                if u.idpass() > 4 and u.pt() > 60 and abs(u.eta()) < 2.4:
                    u_tight_count += 1
            if e_tight_count == 0 and u_tight_count == 1:
                tight_counter += 1
                tight_muon_found = True
            elif e_tight_count == 1 and u_tight_count == 0:
                tight_counter += 1
                tight_electron_found = True
            else:
                continue

#loose lepton selection, no loose lepton is required.
            u_loose_count = 0
            e_loose_count = 0
            for e in event.electrons():
                if e.idpass() > 0 and e.idpass() < 3 and e.pt() > 10 and abs(e.eta()) < 2.5:
                    e_loose_count += 1
            for u in event.muons():
                if u.idpass() > 0 and u.idpass() < 3 and u.pt() > 10 and abs(u.eta()) < 2.4:
                    u_loose_count += 1
            if e_loose_count == 0 and u_loose_count == 0:
                loose_counter += 1
            else:
                continue

            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())

            treeProducer.fill()

    treeProducer.write()
    out_root.Close()

    print "Total Events {}".format(total_events)
    print "Events after MET selection: {} ".format(m_counter)
    print "Events after Jets selection: {}".format(j_counter)
    print "Events after tight-lepton selection: {}".format(tight_counter)
    print "Events after loose-lepton selection: {}".format(loose_counter)


if __name__ == "__main__":
    main()
