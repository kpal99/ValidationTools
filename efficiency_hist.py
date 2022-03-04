#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import os

# create and return histrogram automatically
def createHist(varname,minval=0, maxval=501):
    binval = 25
    if "pt" in varname:
        if maxval == 501:
            maxval = 800
        h = ROOT.TH1D(varname, varname, binval, minval, maxval)
    elif "Ht" in varname:
        h = ROOT.TH1D(varname, varname, binval, 400, 7900)
        #h = ROOT.TH1D(varname, varname, binval, 500, 8000)
    elif "St" in varname:
        h = ROOT.TH1D(varname, varname, binval, 500, 8000)
        #h = ROOT.TH1D(varname, varname, binval, 2000, 9000)
    elif "eta" in varname:
        h = ROOT.TH1D(varname, varname, binval, -3, 3)
    elif "phi" in varname:
        h = ROOT.TH1D(varname, varname, binval, -3.5, 3.5)
    elif "mass" in varname:
        if 'electron' in str.lower(varname) or 'muon' in str.lower(varname):
            h = ROOT.TH1D(varname, varname, binval, -1 * maxval, maxval)
        else:
            h = ROOT.TH1D(varname, varname, binval, minval, maxval)
    elif "msoftdrop" in varname:
        h = ROOT.TH1D(varname, varname, binval, minval, maxval)
    elif "-multiplicity" in varname:
        h = ROOT.TH1D(varname, varname, 6, -0.5, 5.5)
    elif "multiplicity" in varname:
        h = ROOT.TH1D(varname, varname, 13, -0.5, 12.5)
    elif "deltaR" == varname:
        h = ROOT.TH1D(varname, varname, binval, 0, 5)
    else:
        h = ROOT.TH1D(varname,varname,binval,minval,maxval)

    h.Sumw2()
    return h

def globalWeight(inDir, in_str):
    inFile1 = inDir + "genweight/" + in_str

    ntuple1 = Ntuple(inFile1)
    gw = 0
    for event in ntuple1:
        gw += event.genweight()
    return gw

def main():
    if len(sys.argv) != 2:
        print("USAGE: {} <ntuple>".format(sys.argv[0]))
        sys.exit(1)

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0
    outDir = os.path.dirname(sys.argv[1]) + '/rootPlots/'
    out_str = "efficiency_" + os.path.basename(sys.argv[1])
    outFile = ROOT.TFile(outDir + out_str ,"RECREATE")
    #outputDir = os.path.dirname(inFile) + "/efficiency_plot/" + os.path.basename(inFile).split(".root")[0]


# creating very many histrograms
    hists["TightElectrons_pt"] = createHist("TightElectrons_pt",50,1050)
    hists["TightMuons_pt"] = createHist("TightMuons_pt",50,1050)
    hists["jetspuppi_pt"] = createHist("jetspuppi_pt",0,2000)
    hists["Elec_reliso_met"] = ROOT.TH2D("Elec_reliso_met","Elec_reliso_met", 40, 50., 500., 40, 0, 2.)
    hists["Muon_reliso_met"] = ROOT.TH2D("Muon_reliso_met","Muon_reliso_met", 40, 50., 500., 40, 0, 2.)
    hists["TightElectrons_pt_cut"] = createHist("TightElectrons_pt_cut",50,1050)
    hists["TightMuons_pt_cut"] = createHist("TightMuons_pt_cut",50,1050)
    hists["jetspuppi_pt_cut"] = createHist("jetspuppi_pt_cut",0,2000)
    hists["Elec_reliso_met_cut"] = ROOT.TH2D("Elec_reliso_met_cut","Elec_reliso_met_cut", 40, 50., 500., 40, 0, 2.)
    hists["Muon_reliso_met_cut"] = ROOT.TH2D("Muon_reliso_met_cut","Muon_reliso_met_cut", 40, 50., 500., 40, 0, 2.)

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        #local_weight += gen_weight
        for item in event.metspuppi():
            met = item.pt()

        for item in event.jetspuppi():
            hists["jetspuppi_pt"].Fill(item.pt())
            if item.btag() == 2 or item.btag() == 3:
                hists["jetspuppi_pt_cut"].Fill(item.pt())

#tight lepton selection. Only single lepton is required.
        for item in event.electrons():
            if item.idpass() >= 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                hists["TightElectrons_pt"].Fill(item.pt())
                hists["Elec_reliso_met"].Fill(met, item.reliso())
                if item.isopass() >= 4:
                    hists["TightElectrons_pt_cut"].Fill(item.pt())
                    hists["Elec_reliso_met_cut"].Fill(met, item.reliso())
                break
        for item in event.muons():
            if item.idpass() >= 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                hists["TightMuons_pt"].Fill(item.pt())
                hists["Muon_reliso_met"].Fill(met, item.reliso())
                if item.isopass() >= 4:
                    hists["TightMuons_pt_cut"].Fill(item.pt())
                    hists["Muon_reliso_met_cut"].Fill(met, item.reliso())
                break

    outFile.Write()
    print("OutFile written at {}".format(outFile))

if __name__ == "__main__":
    main()
