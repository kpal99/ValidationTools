#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from array import array
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
    elif "idpass" in varname:
        h = ROOT.TH1D(varname, varname, 8, -0.5, 7.5)
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

def createHistVarBin(varname,minval=0, maxval=501):
    if "Tight" in varname:
        varBin = [50, 100, 150, 200, 250, 300, 400, 500, 650, 800]
        h = ROOT.TH1D(varname, varname, len(varBin)-1, array('d',varBin))
    elif "jetspuppi_pt" in varname:
        varBin = [0, 50, 100, 150, 200, 250, 300, 400, 500, 650, 800, 1000, 1200]
        h = ROOT.TH1D(varname, varname, len(varBin)-1, array('d',varBin))
    else:
        h = ROOT.TH1D(varname,varname,binval,minval,maxval)

    h.Sumw2()
    return h

def main():
    if len(sys.argv) != 2:
        print("USAGE: {} <ntuple>".format(sys.argv[0]))
        sys.exit(1)

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0
    outDir = os.path.dirname(sys.argv[1]) + '/rootPlots/test/'
    out_str = "efficiency_" + os.path.basename(sys.argv[1])
    outFile = ROOT.TFile(outDir + out_str ,"RECREATE")
    #outputDir = os.path.dirname(inFile) + "/efficiency_plot/" + os.path.basename(inFile).split(".root")[0]


# creating very many histrograms
    hists["TightElectrons_pt"] = createHistVarBin("TightElectrons_pt",50,1050)
    hists["TightElectrons_pt_cut"] = createHistVarBin("TightElectrons_pt_cut",50,1050)
    hists["TightElectrons_eta"] = createHist("TightElectrons_eta")
    hists["TightElectrons_idpass"] = createHist("TightElectrons_idpass")

    hists["TightMuons_pt"] = createHistVarBin("TightMuons_pt",50,1050)
    hists["TightMuons_pt_cut"] = createHistVarBin("TightMuons_pt_cut",50,1050)
    hists["TightMuons_eta"] = createHist("TightMuons_eta")
    hists["TightMuons_idpass"] = createHist("TightMuons_idpass")

    hists["TightMuons_count"] = ROOT.TH1D("TightMuons_count","TightMuons_count",3,-0.5,2.5)
    hists["TightElectrons_count"] = ROOT.TH1D("TightElectrons_count","TightElectrons_count",3,-0.5,2.5)
    hists["TightLeptons_count"] = ROOT.TH1D("TightLeptons_count","TightLeptons_count",3,-0.5,2.5)

    hists["jetspuppi_pt"] = createHistVarBin("jetspuppi_pt",0,2000)
    hists["jetspuppi_pt_cut"] = createHistVarBin("jetspuppi_pt_cut",0,2000)
    hists["jetspuppi_eta"] = createHist("jetspuppi_eta")
    hists["jetspuppi_idpass"] = createHist("jetspuppi_idpass")
    hists["jetspuppi_multiplicity"] = createHist("jetspuppi_multiplicity")

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        #local_weight += gen_weight
        multiplicity = 0
        for item in event.jetspuppi():
            hists["jetspuppi_pt"].Fill(item.pt())
            hists["jetspuppi_eta"].Fill(item.eta())
            hists["jetspuppi_idpass"].Fill(item.idpass())
            multiplicity += 1
            if item.btag() == 2 or item.btag() == 3 or item.btag() == 6 or item.btag() == 7:
                hists["jetspuppi_pt_cut"].Fill(item.pt())
        hists["jetspuppi_multiplicity"].Fill(multiplicity)

#tight lepton selection. Only single lepton is required.

        elec_mul = 0
        muon_mul = 0
        for item in event.electrons():
            if item.idpass() >= 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                hists["TightElectrons_pt"].Fill(item.pt())
                hists["TightElectrons_eta"].Fill(item.eta())
                hists["TightElectrons_idpass"].Fill(item.idpass())
                if item.isopass() >= 4:
                    hists["TightElectrons_pt_cut"].Fill(item.pt())
                elec_mul += 1
        for item in event.muons():
            if item.idpass() >= 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                hists["TightMuons_pt"].Fill(item.pt())
                hists["TightMuons_eta"].Fill(item.eta())
                hists["TightMuons_idpass"].Fill(item.idpass())
                if item.isopass() >= 4:
                    hists["TightMuons_pt_cut"].Fill(item.pt())
                muon_mul += 1

        hists["TightElectrons_count"].Fill(elec_mul)
        hists["TightMuons_count"].Fill(muon_mul)
        hists["TightLeptons_count"].Fill(muon_mul + elec_mul)

#        print "no. of electrons in original tuple: {}".format(len(event.electrons()))
#        print "no. of muons in original tuple: {}".format(len(event.muons()))
#        print "no. of selected electrons in original tuple: {}".format(elec_mul)
#        print "no. of selected muons in original tuple: {}".format(muon_mul)
#        print ""

    outFile.Write()
    print("OutFile written at {}".format(outFile))

if __name__ == "__main__":
    main()
