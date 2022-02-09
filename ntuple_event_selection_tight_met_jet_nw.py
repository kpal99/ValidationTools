#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from ntuple_chain import ntuple_chain
from mytree import TreeProducer
import sys

def main():
    ntuple_array = ntuple_chain(sys.argv[1])
    maxEvents = 10

    m_counter = 0
    j_counter = 0
    tight_counter = 0
    loose_counter = 0
    total_events  = 0

    outputFile = sys.argv[1]
# using last part of out_str to creating a root file

# iterating through the all events; if value of maxEvents is zero.
    file_counter = 0
    files = len(ntuple_array)
    for ntuple in ntuple_array:
        file_counter += 1
        print"Processing {}/{}".format(file_counter,files)
        total_events += ntuple.nevents()
        for event in ntuple:
            if maxEvents > 0 and event.entry() >= maxEvents:
                break

            vertex_count = 0
            for v in event.vtxs():
                vertex_count += 1
                if vertex_count == 1:
                    print "vertex_z {} ".format(v.z())

#tight lepton selection. Only single lepton is required.
            tight_electron_found = False
            tight_muon_found = False
            e_tight_count = 0
            u_tight_count = 0
            e_loose_count = 0
            u_loose_count = 0
            for e in event.electrons():
                if ( e.idpass() == 1 ) and e.pt() > 10 and abs(e.eta()) < 2.5:
                    e_loose_count +=1
                if e.idpass() >= 4 and e.pt() > 60 and abs(e.eta()) < 2.5:
                    e_tight_count += 1
                    lepton_eta = e.eta()
                    lepton_phi = e.phi()
            for u in event.muons():
                if ( u.idpass() == 1  ) and u.pt() > 10 and abs(u.eta()) < 2.4:
                    u_loose_count +=1
                if u.idpass() >= 4 and u.pt() > 60 and abs(u.eta()) < 2.4:
                    u_tight_count += 1
                    lepton_eta = u.eta()
                    lepton_phi = u.phi()

            print "n_TightElectrons: {} \t n_LooseElectrons: {}".format(e_tight_count,e_loose_count)
            print "n_TightMuons: {} \t n_LooseMuons: {}".format(u_tight_count,u_loose_count)

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

            counter = 0
            for m in event.metspuppi():
                if m.pt() > 60:
                    counter += 1
            if counter == 1:
                m_counter += 1
            else:
                continue

            sum_pt = 0
            pt_array = []
            multiplicity = 0
            for j in event.jetspuppi():
                if j.pt() > 30 and abs(j.eta()) < 2.4:
                    pt_array.append(j.pt())
                    sum_pt += j.pt()
                    multiplicity += 1
            if multiplicity > 2 and pt_array[0] > 200 and pt_array[1] > 100 and pt_array[2] > 50 and sum_pt > 400:
                j_counter += 1
            else:
                continue

    print "Total Events {}".format(total_events)
    print "Events after tight-lepton selection: {}".format(tight_counter)
    print "Events after tight-lepton-looseVeto selection: {}".format(loose_counter)
    print "Events after MET selection: {} ".format(m_counter)
    print "Events after Jet selection: {} ".format(j_counter)

if __name__ == "__main__":
    main()
