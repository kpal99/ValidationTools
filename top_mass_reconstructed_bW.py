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
    if len(sys.argv) != 6:
        print "USAGE: {} <ntuple1> <ntuple2> <top> <ew> <qcd>".format(sys.argv[0])
        sys.exit(0)
    ntuple = []
    ntuple.append( Ntuple(sys.argv[1]) )
    ntuple.append( Ntuple(sys.argv[2]) )
    ntuple.append( Ntuple(sys.argv[3]) )
    ntuple.append( Ntuple(sys.argv[4]) )
    ntuple.append( Ntuple(sys.argv[5]) )
    hists = {}
    maxEvents = 0

# using last part of out_str to creating a root file
    outFile = ROOT.TFile('TTmass_bW.root',"RECREATE")

# creating very many histrograms
    hists["TTmass_signal_1tev"] = createHist("TTmass_signal_1tev", 500)
    hists["TTmass_signal_1_5tev"] = createHist("TTmass_signal_1_5tev", 500)
    hists["top"] = createHist("top", 500)
    hists["ew"] = createHist("ew", 500)
    hists["qcd"] = createHist("qcd", 500)
# iterating through the all events; if value of maxEvents is zero.
    count = 0
    for ntuple1 in ntuple:
        count += 1
        for event in ntuple1:
            if maxEvents > 0 and event.entry() >= maxEvents:
                break

            b_jet = []
            ak4_jet = []

            for item in event.electrons():
                if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.5:
                    lepton = ROOT.TLorentzVector()
                    lepton.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                    break
            for item in event.muons():
                if item.idpass() > 4 and item.pt() > 60 and abs(item.eta()) < 2.4:
                    lepton = ROOT.TLorentzVector()
                    lepton.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                    break

            btag_multiplicity = 0
            for item in event.jetspuppi():
                if item.btag() > 0:
                    btag_multiplicity += 1
                    A = ROOT.TLorentzVector()
                    A.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                    b_jet.append(A)
                if item.btag() <= 0:
                    A = ROOT.TLorentzVector()
                    A.SetPtEtaPhiM(item.pt(), item.eta(), item.phi(), item.mass())
                    ak4_jet.append(A)


            T = ROOT.TLorentzVector()
            T_min = ROOT.TLorentzVector()
            mass_min = 99999
            if btag_multiplicity != 0:
                for item in b_jet:
                    T = lepton + item
                    T_mass = T.M()
                    if T_mass < mass_min:
                        mass_min = T_mass
                        T_min = T

            h2b_count = 0
            h1b_count = 0
            w_count = 0
            for item in event.fatjets():
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

            if h2b_count == 0 and h1b_count == 0:
                if count == 1:
                    hists["TTmass_signal_1tev"].Fill(T_min.M())
                elif count == 2:
                    hists["TTmass_signal_1_5tev"].Fill(T_min.M())
                elif count == 3:
                    hists["top"].Fill(T_min.M())
                elif count == 4:
                    hists["ew"].Fill(T_min.M())
                elif count == 5:
                    hists["qcd"].Fill(T_min.M())


#        print "Lepton: "
#        lepton.Print()
#        print "normal jet array: "
#        for j in ak4_jet:
#            j.Print()
#        print "b quark array: "
#        for b in b_jet:
#            b.Print()
#        print "Higgs array: "
#        for h in higgs:
#            h.Print()


    outFile.Write()
    print "OutFile written at {}".format(outFile)


if __name__ == "__main__":
    main()
