#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys


# create and return histrogram automatically
def createHist(varname,maxval=501):
    if "mass" in varname:
        h = ROOT.TH1D(varname, varname, 100, 0, maxval)
        h.GetXaxis().SetTitle("mass[GeV]")
        var = varname.split('_')
        h.GetYaxis().SetTitle("N_{"+var[0]+"}")
    else:
        h = ROOT.TH1D(varname,varname,100,0,maxval)

    h.Sumw2()
    return h

def main():
    if len(sys.argv) != 2:
        print "USAGE: {} <ntuple>".format(sys.argv[0])
        sys.exit(0)
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 100

    outputFile = sys.argv[1]
    out_str = outputFile.split('.root')
# using last part of out_str to creating a root file
#    outFile = ROOT.TFile(out_str[0] + '_plot.root',"RECREATE")

# creating very many histrograms
    hists["TT_mass"] = createHist("TT_mass", 0.0002)
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        higgs = []
        w_boson = []
        b_quark = []

        btag_multiplicity = 0
        for item in event.jetspuppi():
            if item.btag() > 0:
                btag_multiplicity += 1
                A = ROOT.TLorentzVector()
                A.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                b_quark.append(A)

# multiplicity of fatjet
        fatjet_count = 0
        h2b_count = 0
        h1b_count = 0
        w_count = 0
        for item in event.fatjets():
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
                    A = ROOT.TLorentzVector()
                    A.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                    higgs.append(A)
                elif b_count == 1:
                    h1b_count += 1
                    A = ROOT.TLorentzVector()
                    A.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                    higgs.append(A)
            if item.tau1() != 0:
                if item.pt() > 200 and abs(item.eta()) < 2.4 and 60 <= item.msoftdrop() <= 110 and item.tau2() / item.tau1() < 0.55 and h2b_count == 0 and h1b_count == 0:
                    w_count += 1
                    A = ROOT.TLorentzVector()
                    A.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                    w_boson.append(A)
        print "Event: {}".format(event.entry())
        print "b quark array: "
        for b in b_quark:
            b.Print()
        print "Higgs array: "
        for h in higgs:
            h.Print()
        print "W-boson array: "
        for w in w_boson:
            w.Print()
        print ""

        chi_2 = 9999999999
        temp = ROOT.TLorentzVector()
        if h2b_count > 0 or h1b_count > 0:
            if w_count > 0:
                for w in w_boson:
                    for b in b_qu
            pass

    #outFile.Write()
    #print "OutFile written at {}".format(outFile)


if __name__ == "__main__":
    main()
