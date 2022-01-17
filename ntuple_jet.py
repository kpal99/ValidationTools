#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys


# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple

hists = {}
outputDir = "histo_delp"

def createHist(varname):
    if "pt" in varname:
        h = ROOT.TH1D(varname, varname, 100, 0, 1500)
      h.GetXaxis().SetTitle("pT[GeV]")
      var = varname.split('_')
      h.GetYaxis().SetTitle("N_{"+var[0]+"}")
    if "eta" in varname:
        h = ROOT.TH1D(varname, varname, 100, -2.5, 2.5)
      h.GetXaxis().SetTitle("eta")
      var = varname.split('_')
      h.GetYaxis().SetTitle("N_{"+var[0]+"}")
    if "phi" in varname:
        h = ROOT.TH1D(varname, varname, 100, -5, -5)
      h.GetXaxis().SetTitle("phi")
      var = varname.split('_')
      h.GetYaxis().SetTitle("N_{"+var[0]+"}")
    if "mass" in varname:
        h = ROOT.TH1D(varname, varname, 100, 0, 500)
      h.GetXaxis().SetTitle("mass[GeV]")
      var = varname.split('_')
      h.GetYaxis().SetTitle("N_{"+var[0]+"}")

    h.Sumw2()

    return h

def create2dHist(varname):
    if "to_pt" in varname:
        h = ROOT.TProfile(varname, varname, 100, 0, 1500)
      h.GetXaxis().SetTitle("pT[GeV]")
      h.GetYaxis().SetTitle("Jet.pt/GenJet.pt")
    if "to_eta" in varname:
        h = ROOT.TProfile(varname, varname, 100, -5, 5)
      h.GetXaxis().SetTitle("eta")
      h.GetYaxis().SetTitle("Jet.pt/GenJet.pt")

    h.Sumw2()

    return h


def main():
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)

    maxEvents = 5000

    tot_nevents = 0
    tot_genpart = 0
    tot_genjet = 0
    tot_electron = 0
    tot_gamma = 0
    tot_muon = 0
    tot_jet = 0
    tot_tau = 0
    tot_met = 0
    tot_genjetAK8 = 0
    tot_jetAK8 = 0


    outputF = ROOT.TFile(outputDir + "/" + "val_jet.root","RECREATE")
    hists["jet_pt"] = createHist("jet_pt")
    hists["jet_eta"] = createHist("jet_eta")
    hists["jet_phi"] = createHist("jet_phi")
    hists["jet_mass"] = createHist("jet_mass")
    hists["jet_ptresponse_to_eta"] = create2dHist("jet_ptresponse_to_eta")
    hists["jet_ptresponse_to_pt"] = create2dHist("jet_ptresponse_to_pt")
    hists["jet_ptresponse_to_eta_0to50"] = create2dHist("jet_ptresponse_to_eta_0to50")
    hists["jet_ptresponse_to_eta_50to100"] = create2dHist("jet_ptresponse_to_eta_50to100")
    hists["jet_ptresponse_to_eta_100to200"] = create2dHist("jet_ptresponse_to_eta_100to200")
    hists["jet_ptresponse_to_eta_200to400"] = create2dHist("jet_ptresponse_to_eta_200to400")
    hists["jet_ptresponse_to_eta_400up"] = create2dHist("jet_ptresponse_to_eta_400up")

    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents %100) == 0 :
            print '... processed {} events ...'.format(event.entry()+1)

    jets = event.jets()
    genjets = event.genjets()

    for p in jets:
        jet = ROOT.TVector3()
          jet.SetPtEtaPhi(p.pt(), p.eta(), p.phi())
      if p.eta() > 5 : continue

      for g in genjets:
          gjet = ROOT.TVector3()
        gjet.SetPtEtaPhi(g.pt(), g.eta(), g.phi())
        if g.eta() > 5 : continue

        if jet.DeltaR(gjet) < 0.2:
            hists["jet_ptresponse_to_eta"].Fill(g.eta(), p.pt()/g.pt())
              hists["jet_ptresponse_to_pt"].Fill(g.pt(), p.pt()/g.pt())
              for ptcut1, ptcut2 in [[0, 50], [50, 100], [100, 200], [200,400]]:
                  if ( g.pt() >= ptcut1 and g.pt() < ptcut2 ):
                      hists["jet_ptresponse_to_eta_" + str(ptcut1) + "to" +str(ptcut2)].Fill(g.eta(), p.pt()/g.pt())
              if g.pt() >= 400 :
                  hists["jet_ptresponse_to_eta_400up"].Fill(g.eta(), p.pt()/g.pt())

          hists["jet_pt"].Fill(p.pt())
              hists["jet_eta"].Fill(p.eta())
              hists["jet_phi"].Fill(p.phi())
              hists["jet_mass"].Fill(p.mass())


        tot_nevents += 1
        tot_genpart += len(event.genparticles())
        tot_genjet += len(event.genjets())
        tot_electron += len(event.electrons())
        tot_gamma += len(event.gammas())
        tot_muon += len(event.muons())
        tot_jet += len(event.jets())
        tot_tau += len(event.taus())
        tot_met += len(event.mets())
        tot_genjetAK8 += len(event.genjetsAK8())
        tot_jetAK8 += len(event.jetsAK8())
        # end of one event

    outputF.cd()
    for h in hists.keys():
        hists[h].Write()


    print("Processed %d events" % tot_nevents)
    print("On average %f generator particles" % (float(tot_genpart) / tot_nevents))
    print("On average %f generated jets" % (float(tot_genjet) / tot_nevents))
    print("On average %f electrons" % (float(tot_electron) / tot_nevents))
    print("On average %f photons" % (float(tot_gamma) / tot_nevents))
    print("On average %f muons" % (float(tot_muon) / tot_nevents))
    print("On average %f jets" % (float(tot_jet) / tot_nevents))
    print("On average %f taus" % (float(tot_tau) / tot_nevents))
    print("On average %f met" % (float(tot_met) / tot_nevents))
    print("On average %f generated AK8 jets" % (float(tot_genjetAK8) / tot_nevents))
    print("On average %f jetsAK8" % (float(tot_jetAK8) / tot_nevents))

if __name__ == "__main__":
    main()
