from bin.NtupleDataFormat import Ntuple
from efficiency_hist import createHistVarBin
from one_histogram import createHist
import sys
import math
import os
import ROOT

def delPhi(a,b):
    c = a - b
    if c >= math.pi:
        c -= 2*math.pi
    if c <= -math.pi:
        c += 2*math.pi
    return c

def main():
    if len(sys.argv) != 2:
        print "USAGE: %s <input file>".format(sys.argv[0])
        sys.exit(1)

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0

    outDir = '/eos/uscms/store/user/kpal/trimmed_files_v6/rootPlots/test/'
    out_str = "efficiency_WtoLNu-ch_" + os.path.basename(sys.argv[1])
    outFile = ROOT.TFile(outDir + out_str ,"RECREATE")

# creating very many histrograms
    hists["TightElectrons_pt"] = createHistVarBin("TightElectrons_pt",50,1050)
    hists["TightElectrons_pt_cut"] = createHistVarBin("TightElectrons_pt_cut",50,1050)

    hists["TightMuons_pt"] = createHistVarBin("TightMuons_pt",50,1050)
    hists["TightMuons_pt_cut"] = createHistVarBin("TightMuons_pt_cut",50,1050)

    hists["TightMuons_count"] = ROOT.TH1D("TightMuons_count","TightMuons_count",3,-0.5,2.5)
    hists["TightElectrons_count"] = ROOT.TH1D("TightElectrons_count","TightElectrons_count",3,-0.5,2.5)
    hists["TightLeptons_count"] = ROOT.TH1D("TightLeptons_count","TightLeptons_count",3,-0.5,2.5)

    hists["deltaRmin"] = createHist("deltaRmin",0,5)

    for event in ntuple:

        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        for p in event.tightElectrons():
            lep_eta = p.eta()
            lep_phi = p.phi()
        for p in event.tightMuons():
            lep_eta = p.eta()
            lep_phi = p.phi()

        dRmin = 9999
        for p in event.genparticles():
            if abs(p.pid()) == 3 or abs(p.pid()) == 4 or abs(p.pid()) == 5:
                deltaR = ((p.eta() - lep_eta) ** 2 + (delPhi(p.phi(), lep_phi)) ** 2) ** 0.5
                if deltaR < dRmin:
                    dRmin = deltaR

        if dRmin < 0.4:
            continue
        hists["deltaRmin"].Fill(dRmin)

#tight lepton selection. Only single lepton is required.
        elec_mul = 0
        muon_mul = 0
        for item in event.tightElectrons():
                hists["TightElectrons_pt"].Fill(item.pt())
                if item.isopass() >= 4:
                    hists["TightElectrons_pt_cut"].Fill(item.pt())
                elec_mul += 1
        for item in event.tightMuons():
                hists["TightMuons_pt"].Fill(item.pt())
                if item.isopass() >= 4:
                    hists["TightMuons_pt_cut"].Fill(item.pt())
                muon_mul += 1

        hists["TightElectrons_count"].Fill(elec_mul)
        hists["TightMuons_count"].Fill(muon_mul)
        hists["TightLeptons_count"].Fill(muon_mul + elec_mul)

    outFile.Write()
    print("OutFile written at {}".format(outFile))

if __name__ == "__main__":
    main()
