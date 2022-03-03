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
    elif "St" in varname:
        h = ROOT.TH1D(varname, varname, binval, 500, 8000)
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

def main():
    if len(sys.argv) != 5:
        print("USAGE: {} <ntuple> <cross-section(fb)> <total event> <Initial genweight>".format(sys.argv[0]))
        sys.exit(1)

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0

    outDir = os.path.dirname(sys.argv[1]) + '/rootPlots/'
    out_str = os.path.basename(sys.argv[1])
# using last part of out_str to creating a root file
    outFile = ROOT.TFile(outDir + out_str,"RECREATE")

# creating very many histrograms
    hists["TightElectrons_pt"] = createHist("TightElectrons_pt",50,1050)
    hists["TightElectrons_eta"] = createHist("TightElectrons_eta")
    hists["TightElectrons_phi"] = createHist("TightElectrons_phi")
    hists["TightElectrons_mass"] = createHist("TightElectrons_mass",0, 0.0002)
    hists["TightMuons_pt"] = createHist("TightMuons_pt",50,1050)
    hists["TightMuons_eta"] = createHist("TightMuons_eta")
    hists["TightMuons_phi"] = createHist("TightMuons_phi")
    hists["TightMuons_mass"] = createHist("TightMuons_mass",0, 0.0002)
    hists["jetspuppi_pt"] = createHist("jetspuppi_pt",0,2000)
    #hists["jetspuppi_pt_1"] = createHist("jetspuppi_pt_1",200,1800)
    #hists["jetspuppi_pt_2"] = createHist("jetspuppi_pt_2",100,1200)
    #hists["jetspuppi_pt_3"] = createHist("jetspuppi_pt_3",50,600)
    hists["jetspuppi_pt_1"] = createHist("jetspuppi_pt_1",200,3200)
    hists["jetspuppi_pt_2"] = createHist("jetspuppi_pt_2",100,2100)
    hists["jetspuppi_pt_3"] = createHist("jetspuppi_pt_3",50,1050)
    hists["jetspuppi_eta"] = createHist("jetspuppi_eta")
    hists["jetspuppi_eta_1"] = createHist("jetspuppi_eta_1")
    hists["jetspuppi_eta_2"] = createHist("jetspuppi_eta_2")
    hists["jetspuppi_eta_3"] = createHist("jetspuppi_eta_3")
    hists["jetspuppi_phi"] = createHist("jetspuppi_phi")
    hists["jetspuppi_mass"] = createHist("jetspuppi_mass",0,100)
    hists["jetspuppi_multiplicity"] = createHist("jetspuppi_multiplicity")
    hists["jetspuppi_btagmultiplicity"] = createHist("jetspuppi_btagmultiplicity")
    hists["jetspuppi_Ht"] = createHist("jetspuppi_Ht")
    hists["St"] = createHist("St")
    hists["fatjets_pt"] = createHist("fatjets_pt",200,2075)
    #hists["fatjets_pt"] = createHist("fatjets_pt",1500)
    hists["fatjets_eta"] = createHist("fatjets_eta")
    hists["fatjets_phi"] = createHist("fatjets_phi")
    #hists["fatjets_msoftdrop[tau21]"] = createHist("fatjets_msoftdrop[tau21]",400)
    hists["fatjets_msoftdrop[tau21]"] = createHist("fatjets_msoftdrop[tau21]",0,300)
    hists["fatjets_tau21[m-softdrop]"] = createHist("fatjets_tau21[m-softdrop]",0,1)
    hists["fatjets_multiplicity"] = createHist("fatjets_multiplicity")
    hists["fatjets_H2b-multiplicity"] = createHist("fatjets_H2b-multiplicity")
    hists["fatjets_H1b-multiplicity"] = createHist("fatjets_H1b-multiplicity")
    hists["fatjets_Wtag-multiplicity"] = createHist("fatjets_Wtag-multiplicity")
    #hists["metspuppi_pt"] = createHist("metspuppi_pt",2000)
    hists["metspuppi_pt"] = createHist("metspuppi_pt",50,1300)
    hists["metspuppi_phi"] = createHist("metspuppi_phi")
    hists["deltaR"] = createHist("deltaR")
    hists["deltaRmin"] = createHist("deltaRmin",0,5)

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break


        gen_weight = event.genweight()

        #local_weight += gen_weight
        for item in event.metspuppi():
            hists["metspuppi_pt"].Fill(item.pt(), gen_weight)
            hists["metspuppi_phi"].Fill(item.phi(), gen_weight)

        ak4_jet = []
        for item in event.jetspuppi():
            hists["jetspuppi_pt"].Fill(item.pt(), gen_weight)
            hists["jetspuppi_eta"].Fill(item.eta(), gen_weight)
            hists["jetspuppi_phi"].Fill(item.phi(), gen_weight)
            hists["jetspuppi_mass"].Fill(item.mass(), gen_weight)
            ak4_jet.append([item.pt(), item.eta()])
        hists["jetspuppi_pt_1"].Fill(ak4_jet[0][0], gen_weight)     #filling highest pt jet
        hists["jetspuppi_eta_1"].Fill(ak4_jet[0][1], gen_weight)    #filling highest pt jet's eta
        hists["jetspuppi_pt_2"].Fill(ak4_jet[1][0], gen_weight)
        hists["jetspuppi_eta_2"].Fill(ak4_jet[1][1], gen_weight)
        hists["jetspuppi_pt_3"].Fill(ak4_jet[2][0], gen_weight)
        hists["jetspuppi_eta_3"].Fill(ak4_jet[2][1], gen_weight)

        hists["jetspuppi_multiplicity"].Fill(event.jetM(), gen_weight)
        hists["jetspuppi_btagmultiplicity"].Fill(event.jetBtag(), gen_weight)
        hists["jetspuppi_Ht"].Fill(event.jetHt(), gen_weight)
        hists["St"].Fill(event.jetSt(), gen_weight)

#tight lepton selection. Only single lepton is required.
        for item in event.tightElectrons():
            hists["TightElectrons_pt"].Fill(item.pt(), gen_weight)
            hists["TightElectrons_eta"].Fill(item.eta(), gen_weight)
            hists["TightElectrons_phi"].Fill(item.phi(), gen_weight)
            hists["TightElectrons_mass"].Fill(item.mass(), gen_weight)
        for item in event.tightMuons():
            hists["TightMuons_pt"].Fill(item.pt(), gen_weight)
            hists["TightMuons_eta"].Fill(item.eta(), gen_weight)
            hists["TightMuons_phi"].Fill(item.phi(), gen_weight)
            hists["TightMuons_mass"].Fill(item.mass(), gen_weight)

# multiplicity of fatjet
        fatjet_count = 0
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
                hists["fatjets_pt"].Fill(item.pt(), gen_weight)
                hists["fatjets_eta"].Fill(item.eta(), gen_weight)
                hists["fatjets_phi"].Fill(item.phi(), gen_weight)
                if item.tau1() != 0:
                    if item.tau2() / item.tau1() < 0.55:
                        hists["fatjets_msoftdrop[tau21]"].Fill(item.msoftdrop(), gen_weight)
                    if 60 <= item.msoftdrop() <= 110:
                        hists["fatjets_tau21[m-softdrop]"].Fill( item.tau2() / item.tau1() , gen_weight)

        hists["fatjets_multiplicity"].Fill(event.fatjetM(), gen_weight)
        hists["fatjets_H2b-multiplicity"].Fill(event.fatjetH2b(), gen_weight)
        hists["fatjets_H1b-multiplicity"].Fill(event.fatjetH1b(), gen_weight)
        hists["fatjets_Wtag-multiplicity"].Fill(event.fatjetW(), gen_weight)

        delRmin = []
        if fatjet_count > 1:
            for i in range(len(jet_eta)):
                deltaR =  ((lead_jet_eta - jet_eta[i])**2 + (lead_jet_phi - jet_phi[i])**2)**0.5
                delRmin.append(deltaR)
                hists["deltaR"].Fill(deltaR, gen_weight)
            delRmin.sort()
            hists["deltaRmin"].Fill(delRmin[0], gen_weight)

    scale_factor = 3000  * float(sys.argv[2]) / float(sys.argv[4])
    for h in hists.keys():
        hists[h].Scale(scale_factor)
    outFile.Write()
    print("OutFile written at {}".format(outFile))

if __name__ == "__main__":
    main()
