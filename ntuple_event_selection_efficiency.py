#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from ntuple_example_elec  import get_phy_obj
from ntuple_chain import ntuple_chain
import sys


# create and return histrogram automatically
def createHist(varname,maxval=501):
    if "pt" in varname:
        if maxval == 501:
            maxval = 1500
        h = ROOT.TH1D(varname, varname, 100, 0, maxval)
        h.GetXaxis().SetTitle("pT[GeV]")
        var = varname.split('_')
        h.GetYaxis().SetTitle("N_{"+var[0]+"}")
    if "eta" in varname:
        h = ROOT.TH1D(varname, varname, 100, -5, 5)
        h.GetXaxis().SetTitle("eta")
        var = varname.split('_')
        h.GetYaxis().SetTitle("N_{"+var[0]+"}")
    if "phi" in varname:
        h = ROOT.TH1D(varname, varname, 100, -5, -5)
        h.GetXaxis().SetTitle("phi")
        var = varname.split('_')
        h.GetYaxis().SetTitle("N_{"+var[0]+"}")
    if "mass" in varname:
        if 'electron' in str.lower(varname) or 'muon' in str.lower(varname):
            h = ROOT.TH1D(varname, varname, 100, -1 * maxval, maxval)
        else:
            h = ROOT.TH1D(varname, varname, 100, 0, maxval)
        h.GetXaxis().SetTitle("mass[GeV]")
        var = varname.split('_')
        h.GetYaxis().SetTitle("N_{"+var[0]+"}")

    #h.Sumw2()
    return h

def main(num):
    ntuple_array = ntuple_chain(sys.argv[1])
    hists = {}
    maxEvents = 0

    total_events = 0
    m_counter = 0
    j_counter = 0
    loose_counter = 0
    tight_counter = 0

#    outputDir = "../ntuples/"
#    out_str = inFile.split("/")
## using last part of out_str to creating a root file
#    outFile = ROOT.TFile(outputDir + 'EventSelection_' + out_str[len(out_str) - 1],"RECREATE")
#
## creating very many histrograms
#    hists["electrons_pt"] = createHist("electrons_pt", 500)
#    hists["electrons_eta"] = createHist("electrons_eta")
#    hists["electrons_phi"] = createHist("electrons_phi")
#    hists["electrons_mass"] = createHist("electrons_mass", 0.0002)
#    hists["TightElectrons_pt"] = createHist("TightElectrons_pt")
#    hists["TightElectrons_eta"] = createHist("TightElectrons_eta")
#    hists["TightElectrons_phi"] = createHist("TightElectrons_phi")
#    hists["TightElectrons_mass"] = createHist("TightElectrons_mass", 0.0002)
#    hists["muons_pt"] = createHist("muons_pt",500)
#    hists["muons_eta"] = createHist("muons_eta")
#    hists["muons_phi"] = createHist("muons_phi")
#    hists["muons_mass"] = createHist("muons_mass", 0.0002)
#    hists["TightMuons_pt"] = createHist("TightMuons_pt")
#    hists["TightMuons_eta"] = createHist("TightMuons_eta")
#    hists["TightMuons_phi"] = createHist("TightMuons_phi")
#    hists["TightMuons_mass"] = createHist("TightMuons_mass", 0.0002)
#    hists["gammas_pt"] = createHist("gammas_pt", 500)
#    hists["gammas_eta"] = createHist("gammas_eta")
#    hists["gammas_phi"] = createHist("gammas_phi")
#    hists["gammas_mass"] = createHist("gammas_mass", 0.00001)
#    hists["taus_pt"] = createHist("taus_pt")
#    hists["taus_eta"] = createHist("taus_eta")
#    hists["taus_phi"] = createHist("taus_phi")
#    hists["taus_mass"] = createHist("taus_mass",250)
#    hists["jetspuppi_pt"] = createHist("jetspuppi_pt")
#    hists["jetspuppi_eta"] = createHist("jetspuppi_eta")
#    hists["jetspuppi_phi"] = createHist("jetspuppi_phi")
#    hists["jetspuppi_mass"] = createHist("jetspuppi_mass")
#    hists["fatjets_pt"] = createHist("fatjets_pt")
#    hists["fatjets_eta"] = createHist("fatjets_eta")
#    hists["fatjets_phi"] = createHist("fatjets_phi")
#    hists["fatjets_mass"] = createHist("fatjets_mass")
#    hists["metspuppi_pt"] = createHist("metspuppi_pt")
#    hists["metspuppi_phi"] = createHist("metspuppi_phi")

# iterating through the all events; if value of maxEvents is zero.
    for ntuple in ntuple_array:
        total_events += ntuple.nevents()
        for event in ntuple:
            if maxEvents > 0 and event.entry() >= maxEvents:
                break

# MET cut of pt > 60GeV
# every event has only one METS thus no need to continue within the event.metspuppi loop.
            if num == 0 or num == 4 or num == 6:
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
            if num == 1 or num == 4 or num == 6:
                sum_pt = 0
                first = 0
                second = 0
                third = 0
                for j in event.jetspuppi():
                    if first == 0 and j.pt() > 200 and abs(j.eta()) < 2.4:
                        first += 1
                    elif second == 0 and j.pt() > 100 and abs(j.eta()) < 2.4:
                        second += 1
                    elif third == 0 and j.pt() > 50 and abs(j.eta()) < 2.4:
                        third += 1
                    sum_pt += j.pt()
                if first == 1 and second == 1 and third == 1 and sum_pt > 400:
                    j_counter += 1
                else:
                    continue

#tight lepton selectin. Only single lepton is required.
            if num == 2 or num == 5 or num == 6:
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
            if num == 3 or num == 5 or num == 6:
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

##filling histogram of all the remaining intersted varibale for only event which collect
#        for string in ['electrons', 'muons', 'gammas', 'taus', 'jetspuppi', 'fatjets', 'metspuppi']:
#            phy_obj = get_phy_obj(event,string)
#            for p in phy_obj:
#                hists[string + "_pt"].Fill(p.pt())
#                hists[string + "_phi"].Fill(p.phi())
#                if string != 'metspuppi':
#                    hists[string + "_eta"].Fill(p.eta())
#                    hists[string + "_mass"].Fill(p.mass())
#
#        if tight_electron_found == True:
#            string = "TightElectrons"
#            eta_condition = 2.5
#        elif tight_muon_found == True:
#            string = "TightMuons"
#            eta_condition = 2.4
#        string1 = str.lower(string[5:])
#        phy_obj = get_phy_obj(event, string1)
#        for p in phy_obj:
#            if  p.idpass() > 4 and p.pt() > 60 and abs(p.eta()) < eta_condition:
#                hists[string + "_pt"].Fill(p.pt())
#                hists[string + "_phi"].Fill(p.phi())
#                hists[string + "_eta"].Fill(p.eta())
#                hists[string + "_mass"].Fill(p.mass())
#                continue
#
#    outFile.Write()

    if num == 0:
        print "Total Events {}".format(total_events)

    counter_array = [m_counter, j_counter, tight_counter, loose_counter]
    counter_array.sort()
    for i in range(len(counter_array)):
        if counter_array[i] != 0:
            break
    counter_array = counter_array[i:]
    if num == 0:
        msg = "MET"
    elif num == 1:
        msg = "Jet"
    elif num == 2:
        msg = "Tight-lepton"
    elif num == 3:
        msg = "Loose-lepton"
    elif num == 4:
        msg = "MET+Jet"
    elif num == 5:
        msg = "Tight+Loose-lepton"
    elif num == 6:
        msg = "All"
    print "Events after {} selection: {} efficiency: {:.2f}%".format(msg ,counter_array[0], float(counter_array[0]) / total_events * 100)

if __name__ == "__main__":
    for num in range(7):
        main(num)

#Total Events 24999
#Events after MET selection: 19856 efficiency: 79.43%
#Events after Jet selection: 24550 efficiency: 98.20%
#Events after Tight-lepton selection: 8751 efficiency: 35.01%
#Events after Loose-lepton selection: 17979 efficiency: 71.92%
#Events after MET+Jet selection: 19454 efficiency: 77.82%
#Events after Tight+Loose-lepton selection: 6375 efficiency: 25.50%
#Events after All selection: 5418 efficiency: 21.67%
