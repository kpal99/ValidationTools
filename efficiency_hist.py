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
    if len(sys.argv) != 5:
        print("USAGE: {} <ntuple> <cross-section(fb)> <total event> <Initial genweight>".format(sys.argv[0]))
        sys.exit(1)

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0
    outDir = os.path.dirname(sys.argv[1]) + '/rootPlots/test/'
    out_str = "efficiency_scaled_" + os.path.basename(sys.argv[1])
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
    hists["jetspuppi_btagmultiplicity"] = createHist("jetspuppi_btagmultiplicity")

    hists["jetspuppi_pt_1"] = createHistVarBin("jetspuppi_pt_1",0,2000)
    hists["jetspuppi_pt_cut_1"] = createHistVarBin("jetspuppi_pt_cut_1",0,2000)
    hists["jetspuppi_eta_1"] = createHist("jetspuppi_eta_1")
    hists["jetspuppi_idpass_1"] = createHist("jetspuppi_idpass_1")

    hists["jetspuppi_pt_2"] = createHistVarBin("jetspuppi_pt_2",0,2000)
    hists["jetspuppi_pt_cut_2"] = createHistVarBin("jetspuppi_pt_cut_2",0,2000)
    hists["jetspuppi_eta_2"] = createHist("jetspuppi_eta_2")
    hists["jetspuppi_idpass_2"] = createHist("jetspuppi_idpass_2")

    hists["jetspuppi_pt_3"] = createHistVarBin("jetspuppi_pt_3",0,2000)
    hists["jetspuppi_pt_cut_3"] = createHistVarBin("jetspuppi_pt_cut_3",0,2000)
    hists["jetspuppi_eta_3"] = createHist("jetspuppi_eta_3")
    hists["jetspuppi_idpass_3"] = createHist("jetspuppi_idpass_3")

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        gen_weight = event.genweight()

        multiplicity = 0
        for item in event.jetspuppi():
            hists["jetspuppi_pt"].Fill(item.pt(), gen_weight)
            hists["jetspuppi_eta"].Fill(item.eta(), gen_weight)
            hists["jetspuppi_idpass"].Fill(item.idpass(), gen_weight)
            multiplicity += 1
            if multiplicity == 1:
                hists["jetspuppi_pt_1"].Fill(item.pt(), gen_weight)
                hists["jetspuppi_eta_1"].Fill(item.eta(), gen_weight)
                hists["jetspuppi_idpass_1"].Fill(item.idpass(), gen_weight)
            elif multiplicity == 2:
                hists["jetspuppi_pt_2"].Fill(item.pt(), gen_weight)
                hists["jetspuppi_eta_2"].Fill(item.eta(), gen_weight)
                hists["jetspuppi_idpass_2"].Fill(item.idpass(), gen_weight)
            elif multiplicity == 3:
                hists["jetspuppi_pt_3"].Fill(item.pt(), gen_weight)
                hists["jetspuppi_eta_3"].Fill(item.eta(), gen_weight)
                hists["jetspuppi_idpass_3"].Fill(item.idpass(), gen_weight)

            if item.btag() == 2 or item.btag() == 3 or item.btag() == 6 or item.btag() == 7:
                hists["jetspuppi_pt_cut"].Fill(item.pt(), gen_weight)
                if multiplicity == 1:
                    hists["jetspuppi_pt_cut_1"].Fill(item.pt(), gen_weight)
                elif multiplicity == 2:
                    hists["jetspuppi_pt_cut_2"].Fill(item.pt(), gen_weight)
                elif multiplicity == 3:
                    hists["jetspuppi_pt_cut_3"].Fill(item.pt(), gen_weight)

        hists["jetspuppi_multiplicity"].Fill(multiplicity, gen_weight)
#tight lepton selection. Only single lepton is required.
        elec_mul = 0
        muon_mul = 0
        for item in event.electrons():
            if item.idpass() >= 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                hists["TightElectrons_pt"].Fill(item.pt(), gen_weight)
                hists["TightElectrons_eta"].Fill(item.eta(), gen_weight)
                hists["TightElectrons_idpass"].Fill(item.idpass(), gen_weight)
                if item.isopass() >= 4:
                    hists["TightElectrons_pt_cut"].Fill(item.pt(), gen_weight)
                elec_mul += 1
        for item in event.muons():
            if item.idpass() >= 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                hists["TightMuons_pt"].Fill(item.pt(), gen_weight)
                hists["TightMuons_eta"].Fill(item.eta(), gen_weight)
                hists["TightMuons_idpass"].Fill(item.idpass(), gen_weight)
                if item.isopass() >= 4:
                    hists["TightMuons_pt_cut"].Fill(item.pt(), gen_weight)
                muon_mul += 1

        hists["TightElectrons_count"].Fill(elec_mul, gen_weight)
        hists["TightMuons_count"].Fill(muon_mul, gen_weight)
        hists["TightLeptons_count"].Fill(muon_mul + elec_mul, gen_weight)

#        print "no. of electrons in original tuple: {}".format(len(event.electrons()))
#        print "no. of muons in original tuple: {}".format(len(event.muons()))
#        print "no. of selected electrons in original tuple: {}".format(elec_mul)
#        print "no. of selected muons in original tuple: {}".format(muon_mul)
#        print ""

    scale_factor = 3000  * float(sys.argv[2]) / float(sys.argv[4])
    for h in hists.keys():
        hists[h].Scale(scale_factor)

    outFile.Write()
    print("OutFile written at {}".format(outFile))

if __name__ == "__main__":
    main()
