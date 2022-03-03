#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from ntuple_chain import ntuple_chain
from mytree import TreeProducer
import sys
import os

def main():
    ntuple_array = ntuple_chain(sys.argv[1])
    maxEvents = 0

    m_counter = 0
    j_counter = 0
    tight_counter = 0
    loose_counter = 0
    total_events  = 0
    gen_weight = 0.

# using last part of out_str to creating a root file
    outputFile = sys.argv[1]
    out_root = ROOT.TFile(outputFile + '_preSelected.root',"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

    treeProducer = TreeProducer()

# iterating through the all events; if value of maxEvents is zero.
    for ntuple in ntuple_array:
        for event in ntuple:
            if maxEvents > 0 and event.entry() >= maxEvents:
                break

            gen_weight += event.genweight()
            total_events += 1
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
                if e.idpass() >= 4 and e.isopass() >= 4 and e.pt() > 60 and abs(e.eta()) < 2.5:
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
                if u.idpass() >= 4 and u.isopass() >= 4 and u.pt() > 60 and abs(u.eta()) < 2.4:
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

            St = lepton_pt
# MET cut of pt > 60GeV
            counter = 0
            for m in event.metspuppi():
                if m.pt() > 60:
                    counter += 1
                    St += m.pt()
            if counter == 1:
                m_counter += 1
            else:
                continue

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
                if j.btag() == 2 or j.btag() == 3:
                    btag_multiplicity += 1
            if multiplicity > 2 and pt_array[0] > 200 and pt_array[1] > 100 and pt_array[2] > 50 and sum_pt > 400:
                j_counter += 1
            else:
                continue
            St += sum_pt

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
                    if item.pt() > 300 and 60 <= item.msoftdrop() <= 160:
                        b_count = 0
                        for jtem in event.jetspuppi():
                            if jtem.btag() > 0:
                                deltaR =  ((item.eta() - jtem.eta())**2 + (item.phi() - jtem.phi())**2)**0.5
                                if deltaR < 0.8:
                                    b_count += 1
                        if b_count >= 2:
                            h2b_count += 1
                        elif b_count == 1:
                            h1b_count += 1
                    if item.tau1() != 0:
                        if item.pt() > 200 and abs(item.eta()) < 2.4 and 60 <= item.msoftdrop() <= 110 and item.tau2() / item.tau1() < 0.55 and h2b_count == 0 and h1b_count == 0:
                            w_count += 1
            if h2b_count > 0:
                h1b_count = 0
                w_count = 0
            if h1b_count > 0:
                w_count = 0

            #tree pointers are being set
            treeProducer.processTightElectrons_(tight_electron_found, lepton_pt, lepton_eta, lepton_phi, lepton_mass, lepton_charge, lepton_idvar, lepton_reliso, lepton_idpass, lepton_isopass)
            treeProducer.processTightMuons_(tight_muon_found, lepton_pt, lepton_eta, lepton_phi, lepton_mass, lepton_charge, lepton_idvar, lepton_reliso, lepton_idpass, lepton_isopass)
            treeProducer.processEvent(event.entry())
            treeProducer.processWeights(event.genweight())
            treeProducer.processVtxs(event.vtxs())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processJetsMul_(multiplicity, btag_multiplicity, sum_pt, St)
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processFatjetsMul_(fatjet_count, h2b_count, h1b_count, w_count)
            treeProducer.processPuppiMissingET(event.metspuppi())

            treeProducer.fill()

        treeProducer.write()
        out_root.Close()

    print "Total Events                         : {}".format(total_events)
    print "Total genweight                      : {}".format(gen_weight)
    print "Events after tight-lepton selection  : {}".format(tight_counter)
    print "Events after loose-lepton selection  : {}".format(loose_counter)
    print "Events after MET selection           : {} ".format(m_counter)
    print "Events after Jets selection          : {}".format(j_counter)

if __name__ == "__main__":
    main()
