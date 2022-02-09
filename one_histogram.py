#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import os

# create and return histrogram automatically
def createHist(varname,minval=0, maxval=501):
    if "pt" in varname:
        if maxval == 501:
            maxval = 800
        h = ROOT.TH1D(varname, varname, 25, minval, maxval)
    elif "Ht" in varname:
        h = ROOT.TH1D(varname, varname, 25, 400, 6400)
        #h = ROOT.TH1D(varname, varname, 25, 500, 8000)
    elif "St" in varname:
        h = ROOT.TH1D(varname, varname, 25, 500, 7500)
        #h = ROOT.TH1D(varname, varname, 25, 2000, 9000)
    elif "eta" in varname:
        h = ROOT.TH1D(varname, varname, 25, -3, 3)
    elif "phi" in varname:
        h = ROOT.TH1D(varname, varname, 25, -3.5, 3.5)
    elif "mass" in varname:
        if 'electron' in str.lower(varname) or 'muon' in str.lower(varname):
            h = ROOT.TH1D(varname, varname, 25, -1 * maxval, maxval)
        else:
            h = ROOT.TH1D(varname, varname, 25, minval, maxval)
    elif "msoftdrop" in varname:
        h = ROOT.TH1D(varname, varname, 25, minval, maxval)
    elif "-multiplicity" in varname:
        h = ROOT.TH1D(varname, varname, 6, -0.5, 5.5)
    elif "multiplicity" in varname:
        h = ROOT.TH1D(varname, varname, 13, -0.5, 12.5)
    else:
        h = ROOT.TH1D(varname,varname,25,minval,maxval)

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
    if len(sys.argv) != 4:
        print "USAGE: {} <ntuple> <cross-section(fb)> <total event>".format(sys.argv[0])
        sys.exit(1)

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0
    local_weight = 0

    #outputFile = sys.argv[1]
    #out_str = outputFile.split('.root')
    out_str = os.path.basename(sys.argv[1]).split('.root')
    #outDir = '/eos/uscms/store/user/kpal/trimmed_files_v2/smallBins/'
    outDir = os.path.dirname(sys.argv[1]) + '/'
    inDir = outDir

    global_weight = float(sys.argv[3]) #globalWeight(inDir, os.path.basename(sys.argv[1]))
# using last part of out_str to creating a root file
    outFile = ROOT.TFile(outDir + out_str[0] + '_plot.root',"RECREATE")

# creating very many histrograms
    hists["TightElectrons_pt"] = createHist("TightElectrons_pt",50,750)
    hists["TightElectrons_eta"] = createHist("TightElectrons_eta")
    hists["TightElectrons_phi"] = createHist("TightElectrons_phi")
    hists["TightElectrons_mass"] = createHist("TightElectrons_mass",0, 0.0002)
    hists["TightMuons_pt"] = createHist("TightMuons_pt",50,750)
    hists["TightMuons_eta"] = createHist("TightMuons_eta")
    hists["TightMuons_phi"] = createHist("TightMuons_phi")
    hists["TightMuons_mass"] = createHist("TightMuons_mass",0, 0.0002)
    hists["jetspuppi_pt"] = createHist("jetspuppi_pt",0,800)
    hists["jetspuppi_pt_1"] = createHist("jetspuppi_pt_1",200,1800)
    hists["jetspuppi_pt_2"] = createHist("jetspuppi_pt_2",100,1200)
    hists["jetspuppi_pt_3"] = createHist("jetspuppi_pt_3",50,600)
    #hists["jetspuppi_pt_1"] = createHist("jetspuppi_pt_1",200,2000)
    #hists["jetspuppi_pt_2"] = createHist("jetspuppi_pt_2",100,1500)
    #hists["jetspuppi_pt_3"] = createHist("jetspuppi_pt_3",50,1000)
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
    hists["fatjets_pt"] = createHist("fatjets_pt",200,1000)
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
    hists["metspuppi_pt"] = createHist("metspuppi_pt",50,750)
    hists["metspuppi_phi"] = createHist("metspuppi_phi")

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break


        gen_weight = event.genweight()
        #local_weight += gen_weight
        for item in event.metspuppi():
            hists["metspuppi_pt"].Fill(item.pt(), gen_weight)
            hists["metspuppi_phi"].Fill(item.phi(), gen_weight)
            St = item.pt()


        b_jet = []
        ak4_jet = []
        sum_pt = 0
        multiplicity = 0
        btag_multiplicity = 0
        for item in event.jetspuppi():
            hists["jetspuppi_pt"].Fill(item.pt(), gen_weight)
            hists["jetspuppi_eta"].Fill(item.eta(), gen_weight)
            hists["jetspuppi_phi"].Fill(item.phi(), gen_weight)
            hists["jetspuppi_mass"].Fill(item.mass(), gen_weight)
            multiplicity += 1
            ak4_jet.append([item.pt(), item.eta()])
            sum_pt += item.pt()
#            A = ROOT.TLorentzVector()
            if item.btag() > 0:
                btag_multiplicity += 1
#                A.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
#                b_jet.append(A)
#            else:
#                A.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
#                ak4_jet.append(A)
        hists["jetspuppi_pt_1"].Fill(ak4_jet[0][0], gen_weight)     #filling highest pt jet
        hists["jetspuppi_eta_1"].Fill(ak4_jet[0][1], gen_weight)    #filling highest pt jet's eta
        hists["jetspuppi_pt_2"].Fill(ak4_jet[1][0], gen_weight)
        hists["jetspuppi_eta_2"].Fill(ak4_jet[1][1], gen_weight)
        hists["jetspuppi_pt_3"].Fill(ak4_jet[2][0], gen_weight)
        hists["jetspuppi_eta_3"].Fill(ak4_jet[2][1], gen_weight)
        hists["jetspuppi_multiplicity"].Fill(multiplicity, gen_weight)
        hists["jetspuppi_btagmultiplicity"].Fill(btag_multiplicity, gen_weight)
        hists["jetspuppi_Ht"].Fill(sum_pt, gen_weight)
        St += sum_pt

#tight lepton selection. Only single lepton is required.
        for item in event.electrons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                hists["TightElectrons_pt"].Fill(item.pt(), gen_weight)
                hists["TightElectrons_eta"].Fill(item.eta(), gen_weight)
                hists["TightElectrons_phi"].Fill(item.phi(), gen_weight)
                hists["TightElectrons_mass"].Fill(item.mass(), gen_weight)
                St += item.pt()
#                lepton = ROOT.TLorentzVector()
#                lepton.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                break
        for item in event.muons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                hists["TightMuons_pt"].Fill(item.pt(), gen_weight)
                hists["TightMuons_eta"].Fill(item.eta(), gen_weight)
                hists["TightMuons_phi"].Fill(item.phi(), gen_weight)
                hists["TightMuons_mass"].Fill(item.mass(), gen_weight)
                St += item.pt()
#                lepton = ROOT.TLorentzVector()
#                lepton.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                break
        hists["St"].Fill(St, gen_weight)

#        T = ROOT.TLorentzVector()
#        T_min = ROOT.TLorentzVector()
#        mass_min = 99999
#        if btag_multiplicity != 0:
#            for item in b_jet:
#                T = lepton + item
#                T_mass = T.M()
#                if T_mass < mass_min:
#                    mass_min = T_mass
#                    T_min = T
#            hists["min_M_l+b"].Fill(T_min.M())
#        else:
#            for item in ak4_jet:
#                T = lepton + item
#                T_mass = T.M()
#                if T_mass < mass_min:
#                    mass_min = T_mass
#                    T_min = T
#            hists["min_M_l+jet"].Fill(T_min.M())

# multiplicity of fatjet
        fatjet_count = 0
        h2b_count = 0
        h1b_count = 0
        w_count = 0
        for item in event.fatjets():
            if abs(item.eta()) < 2.4:
                hists["fatjets_pt"].Fill(item.pt(), gen_weight)
                hists["fatjets_eta"].Fill(item.eta(), gen_weight)
                hists["fatjets_phi"].Fill(item.phi(), gen_weight)
                fatjet_count += 1
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
                    if item.tau2() / item.tau1() < 0.55:
                        hists["fatjets_msoftdrop[tau21]"].Fill(item.msoftdrop(), gen_weight)
                    if 60 <= item.msoftdrop() <= 110:
                        hists["fatjets_tau21[m-softdrop]"].Fill( item.tau2() / item.tau1() , gen_weight)

        if h2b_count > 0:
            h1b_count = 0
            w_count = 0
        if h1b_count > 0:
            w_count = 0
        hists["fatjets_multiplicity"].Fill(fatjet_count, gen_weight)
        hists["fatjets_H2b-multiplicity"].Fill(h2b_count, gen_weight)
        hists["fatjets_H1b-multiplicity"].Fill(h1b_count, gen_weight)
        hists["fatjets_Wtag-multiplicity"].Fill(w_count, gen_weight)

    eff = 1.0 / global_weight
    #print(out_str[0],local_weight, global_weight, eff)
    scale_factor = 3000 * eff * float(sys.argv[2])
    for h in hists.keys():
        hists[h].Scale(scale_factor)
    outFile.Write()
    print "OutFile written at {}".format(outFile)

if __name__ == "__main__":
    main()
