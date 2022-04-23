#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from array import array
from WdecayEff import delPhi
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
        h = ROOT.TH1D(varname, varname, binval, 400, 5400)
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
    elif "jetM" in varname:
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
    elif "_pt" in varname:
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
    out_str = "reliso-ptHt_" + os.path.basename(sys.argv[1])
    outFile = ROOT.TFile(outDir + out_str ,"RECREATE")
    #outputDir = os.path.dirname(inFile) + "/efficiency_plot/" + os.path.basename(inFile).split(".root")[0]

# creating very many histrograms
    hists["TightElectrons_reliso-pt_Ht"] = ROOT.TH2D("TightElectrons_reliso-pt_Ht","TightElectrons_reliso-pt_Ht", 25, 400., 5400., 25, 0., 50.)
    hists["TightMuons_reliso-pt_Ht"] = ROOT.TH2D("TightMuons_reliso-pt_Ht","TightMuons_reliso-pt_Ht", 25, 400., 5400., 25, 0., 50.)
    hists["TightElectrons_reliso_Ht"] = ROOT.TH2D("TightElectrons_reliso_Ht","TightElectrons_reliso_Ht", 25, 400., 5400., 25, 0., 0.25)
    hists["TightMuons_reliso_Ht"] = ROOT.TH2D("TightMuons_reliso_Ht","TightMuons_reliso_Ht", 25, 400., 5400., 25, 0., 0.25)

    hists["TightElectrons_reliso-pt_jetM"] = ROOT.TH2D("TightElectrons_reliso-pt_jetM","TightElectrons_reliso-pt_jetM", 13, -0.5, 12.5, 25, 0., 50.)
    hists["TightMuons_reliso-pt_jetM"] = ROOT.TH2D("TightMuons_reliso-pt_jetM","TightMuons_reliso-pt_jetM", 13, -0.5, 12.5, 25, 0., 50.)
    hists["TightElectrons_reliso_jetM"] = ROOT.TH2D("TightElectrons_reliso_jetM","TightElectrons_reliso_jetM", 13, -0.5, 12.5, 25, 0., 0.25)
    hists["TightMuons_reliso_jetM"] = ROOT.TH2D("TightMuons_reliso_jetM","TightMuons_reliso_jetM", 13, -0.5, 12.5, 25, 0., 0.25)

    hists["jetspuppi_Ht"] = createHist("jetspuppi_Ht")
    hists["jetspuppi_Ht_1"] = createHist("jetspuppi_Ht_1")
    hists["jetspuppi_Ht_2"] = createHist("jetspuppi_Ht_2")
    hists["jetspuppi_Ht_3"] = createHist("jetspuppi_Ht_3")

    hists["jetspuppi_Ht_cut"] = createHist("jetspuppi_Ht_cut")
    hists["jetspuppi_Ht_cut_1"] = createHist("jetspuppi_Ht_cut_1")
    hists["jetspuppi_Ht_cut_2"] = createHist("jetspuppi_Ht_cut_2")
    hists["jetspuppi_Ht_cut_3"] = createHist("jetspuppi_Ht_cut_3")

    hists["jetM_1"] = createHist("jetM_1")
    hists["jetM_2"] = createHist("jetM_2")
    hists["jetM_3"] = createHist("jetM_3")

    hists["jetM_cut_1"] = createHist("jetM_cut_1")
    hists["jetM_cut_2"] = createHist("jetM_cut_2")
    hists["jetM_cut_3"] = createHist("jetM_cut_3")

    hists["pid3_pt_1"] = createHistVarBin("pid3_pt_1")
    hists["pid4_pt_1"] = createHistVarBin("pid4_pt_1")
    hists["pid5_pt_1"] = createHistVarBin("pid5_pt_1")
    hists["pidBtag_pt_1"] = createHistVarBin("pidBtag_pt_1")

    hists["pid3_jetM_1"] = createHist("pid3_jetM_1")
    hists["pid4_jetM_1"] = createHist("pid4_jetM_1")
    hists["pid5_jetM_1"] = createHist("pid5_jetM_1")
    hists["pidBtag_jetM_1"] = createHist("pidBtag_jetM_1")

    hists["pid3_pt_2"] = createHistVarBin("pid3_pt_2")
    hists["pid4_pt_2"] = createHistVarBin("pid4_pt_2")
    hists["pid5_pt_2"] = createHistVarBin("pid5_pt_2")
    hists["pidBtag_pt_2"] = createHistVarBin("pidBtag_pt_2")

    hists["pid3_jetM_2"] = createHist("pid3_jetM_2")
    hists["pid4_jetM_2"] = createHist("pid4_jetM_2")
    hists["pid5_jetM_2"] = createHist("pid5_jetM_2")
    hists["pidBtag_jetM_2"] = createHist("pidBtag_jetM_2")

    hists["pid3_pt_3"] = createHistVarBin("pid3_pt_3")
    hists["pid4_pt_3"] = createHistVarBin("pid4_pt_3")
    hists["pid5_pt_3"] = createHistVarBin("pid5_pt_3")
    hists["pidBtag_pt_3"] = createHistVarBin("pidBtag_pt_3")

    hists["pid3_jetM_3"] = createHist("pid3_jetM_3")
    hists["pid4_jetM_3"] = createHist("pid4_jetM_3")
    hists["pid5_jetM_3"] = createHist("pid5_jetM_3")
    hists["pidBtag_jetM_3"] = createHist("pidBtag_jetM_3")
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        gen_weight = event.genweight()
        ht = event.jetHt()

        multiplicity = 0
        jetM = event.jetM()
        for item in event.jetspuppi():
            hists["jetspuppi_Ht"].Fill(ht, gen_weight)
            multiplicity += 1
            if multiplicity == 1:
                hists["jetspuppi_Ht_1"].Fill(ht, gen_weight)
                hists["jetM_1"].Fill(jetM, gen_weight)
            elif multiplicity == 2:
                hists["jetspuppi_Ht_2"].Fill(ht, gen_weight)
                hists["jetM_2"].Fill(jetM, gen_weight)
            elif multiplicity == 3:
                hists["jetspuppi_Ht_3"].Fill(ht, gen_weight)
                hists["jetM_3"].Fill(jetM, gen_weight)

            if multiplicity < 4:
                dRmin = 9999
                dRmin_pt = 0
                dRmin_pid = 0
                for p in event.genparticles():
                    if abs(p.pid()) == 3 or abs(p.pid()) == 4 or abs(p.pid()) == 5:
                        deltaR = ((p.eta() - item.eta()) ** 2 + (delPhi(p.phi(), item.phi())) ** 2) ** 0.5
                        if (deltaR < dRmin) and ( item.pt() / 4 < p.pt() ):
                            dRmin = deltaR
                            dRmin_pt = p.pt()
                            dRmin_pid = p.pid()

                if dRmin < 0.4:
                    if multiplicity == 1:
                        if p.pid() == 3:
                            hists["pid3_pt_1"].Fill(item.pt())
                            hists["pid3_jetM_1"].Fill(jetM)
                        elif p.pid() == 4:
                            hists["pid4_pt_1"].Fill(item.pt())
                            hists["pid4_jetM_1"].Fill(jetM)
                        elif p.pid() == 5:
                            hists["pid5_pt_1"].Fill(item.pt())
                            hists["pid5_jetM_1"].Fill(jetM)
                    elif multiplicity == 2:
                        if p.pid() == 3:
                            hists["pid3_pt_2"].Fill(item.pt())
                            hists["pid3_jetM_2"].Fill(jetM)
                        elif p.pid() == 4:
                            hists["pid4_pt_2"].Fill(item.pt())
                            hists["pid4_jetM_2"].Fill(jetM)
                        elif p.pid() == 5:
                            hists["pid5_pt_2"].Fill(item.pt())
                            hists["pid5_jetM_2"].Fill(jetM)
                    elif multiplicity == 3:
                        if p.pid() == 3:
                            hists["pid3_pt_3"].Fill(item.pt())
                            hists["pid3_jetM_3"].Fill(jetM)
                        elif p.pid() == 4:
                            hists["pid4_pt_3"].Fill(item.pt())
                            hists["pid4_jetM_3"].Fill(jetM)
                        elif p.pid() == 5:
                            hists["pid5_pt_3"].Fill(item.pt())
                            hists["pid5_jetM_3"].Fill(jetM)

                    if item.btag() == 2 or item.btag() == 3 or item.btag() == 6 or item.btag() == 7:
                        if multiplicity == 1:
                            hists["pidBtag_pt_1"].Fill(item.pt())
                            hists["pidBtag_jetM_1"].Fill(jetM)
                        elif multiplicity == 2:
                            hists["pidBtag_pt_2"].Fill(item.pt())
                            hists["pidBtag_jetM_2"].Fill(jetM)
                        elif multiplicity == 3:
                            hists["pidBtag_pt_3"].Fill(item.pt())
                            hists["pidBtag_jetM_3"].Fill(jetM)


            if item.btag() == 2 or item.btag() == 3 or item.btag() == 6 or item.btag() == 7:
                hists["jetspuppi_Ht_cut"].Fill(ht, gen_weight)
                if multiplicity == 1:
                    hists["jetspuppi_Ht_cut_1"].Fill(ht, gen_weight)
                    hists["jetM_cut_1"].Fill(jetM, gen_weight)
                elif multiplicity == 2:
                    hists["jetspuppi_Ht_cut_2"].Fill(ht, gen_weight)
                    hists["jetM_cut_2"].Fill(jetM, gen_weight)
                elif multiplicity == 3:
                    hists["jetspuppi_Ht_cut_3"].Fill(ht, gen_weight)
                    hists["jetM_cut_3"].Fill(jetM, gen_weight)

#tight lepton selection. Only single lepton is required.
        for item in event.electrons():
            if item.idpass() >= 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                if item.isopass() >= 4:
                    hists["TightElectrons_reliso-pt_Ht"].Fill(ht, item.reliso() * item.pt(), gen_weight)
                    hists["TightElectrons_reliso_Ht"].Fill(ht, item.reliso(), gen_weight)
                    hists["TightElectrons_reliso-pt_jetM"].Fill(multiplicity, item.reliso() * item.pt(), gen_weight)
                    hists["TightElectrons_reliso_jetM"].Fill(multiplicity, item.reliso(), gen_weight)
        for item in event.muons():
            if item.idpass() >= 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                if item.isopass() >= 4:
                    hists["TightMuons_reliso-pt_Ht"].Fill(ht, item.reliso() * item.pt(), gen_weight)
                    hists["TightMuons_reliso_Ht"].Fill(ht, item.reliso(), gen_weight)
                    hists["TightMuons_reliso-pt_jetM"].Fill(multiplicity, item.reliso() * item.pt(), gen_weight)
                    hists["TightMuons_reliso_jetM"].Fill(multiplicity, item.reliso(), gen_weight)

    scale_factor = 3000  * float(sys.argv[2]) / float(sys.argv[4])
    for h in hists.keys():
        hists[h].Scale(scale_factor)

    outFile.Write()
    print("OutFile written at {}".format(outFile))

if __name__ == "__main__":
    main()
