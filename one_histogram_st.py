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
        h = ROOT.TH1D(varname, varname, 100, 0, 10000)
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

def main():
    if len(sys.argv) != 4:
        print "USAGE: {} <ntuple> <cross-section(fb)> <total event>".format(sys.argv[0])
        sys.exit(0)
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0

    #outputFile = sys.argv[1]
    #out_str = outputFile.split('.root')
    out_str = os.path.basename(sys.argv[1]).split('.root')
    #outDir = '/eos/uscms/store/user/kpal/trimmed_files_v2/smallBins/'
    outDir = os.path.dirname(sys.argv[1]) + '/st/'
# using last part of out_str to creating a root file
    outFile = ROOT.TFile(outDir + out_str[0] + '_plot.root',"RECREATE")

# creating very many histrograms
    hists["St"] = createHist("St")
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break


        for item in event.metspuppi():
            St = item.pt()


        sum_pt = 0
        for item in event.jetspuppi():
            sum_pt += item.pt()
        St += sum_pt

#tight lepton selection. Only single lepton is required.
        for item in event.electrons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                St += item.pt()
#                lepton = ROOT.TLorentzVector()
#                lepton.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                break
        for item in event.muons():
            if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                St += item.pt()
#                lepton = ROOT.TLorentzVector()
#                lepton.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                break
        hists["St"].Fill(St,event.genweight())

    scale_factor = 3000 * float(sys.argv[2]) / float(sys.argv[3])
    for h in hists.keys():
        hists[h].Scale(scale_factor)
    outFile.Write()
    print "OutFile written at {}".format(outFile)

if __name__ == "__main__":
    main()
