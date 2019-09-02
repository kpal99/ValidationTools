#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import optparse

# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple


def createHist(varname):
    if "pt" in varname:
      h = ROOT.TH1D(varname, "", 100, 0, 1500)
      h.GetXaxis().SetTitle("pT[GeV]")
      h.GetYaxis().SetTitle("N_{jet}")
    if "eta" in varname:
      h = ROOT.TH1D(varname, "", 100, -5, -5)
      h.GetXaxis().SetTitle("eta")
      h.GetYaxis().SetTitle("N_{jet}")
    if "phi" in varname:
      h = ROOT.TH1D(varname, "", 100, -5, -5)
      h.GetXaxis().SetTitle("phi")
      h.GetYaxis().SetTitle("N_{jet}")
    if "mass" in varname:
      h = ROOT.TH1D(varname, "", 100, 0, 500)
      h.GetXaxis().SetTitle("mass[GeV]")
      h.GetYaxis().SetTitle("N_{jet}")
    if "multi" in varname:
      if "full" in outputDir:
         h = ROOT.TH1D(varname, "", 50, 0, 50) 
      else:
	 h = ROOT.TH1D(varname, "", 20, 0, 20)
      h.GetXaxis().SetTitle("jet multiplicity")
      h.GetYaxis().SetTitle("Events")


    h.Sumw2()

    return h

def create2dHist(varname):
    if "to_pt" in varname and "response" in varname:
      h = ROOT.TProfile(varname, "", 100, 0, 1500)
      h.GetXaxis().SetTitle("pT[GeV]")
      h.GetYaxis().SetTitle("Jet.pt/GenJet.pt")
    if "to_eta" in varname and "response" in varname:
      h = ROOT.TProfile(varname, "", 100, -5, 5)
      h.GetXaxis().SetTitle("eta")
      h.GetYaxis().SetTitle("Jet.pt/GenJet.pt")
    if "to_pt" in varname and "efficiency" in varname:
      h = ROOT.TProfile(varname, "", 100, 0, 1500)
      h.GetXaxis().SetTitle("pT[GeV]")
      h.GetYaxis().SetTitle("genjet matching efficiency")
    if "to_eta" in varname and "efficiency" in varname:
      h = ROOT.TProfile(varname, "", 100, -5, 5)
      h.GetXaxis().SetTitle("eta")
      h.GetYaxis().SetTitle("genjet matching efficiency")


    h.Sumw2()

    return h

def runJet(event, hists):

        jets = event.jets()
        genjets = event.genjets()
        if len(jets) < 1 or len(genjets) <1 : 
	  return hists
      #  jet_multi = {}
      #  for cutname in ["nocut",
      #                  "0to1p3", "1p3to2p5", "2p5to3","3up",
      #                  "20to50", "50to100", "100to200", "200to400", "400up",
      #                  ]:
      #    jet_multi[cutname] = 0

      #  for g in genjets:  # match reco to gen
      #    if abs(g.eta()) > 5 or g.pt() <20 : continue
      #    match = 0
      #    gjet = ROOT.TVector3()
      #    gjet.SetPtEtaPhi(g.pt(), g.eta(), g.phi())

      #    for p in jets:
      #      if abs(p.eta()) > 5 or p.pt() <20 : continue
      #      jet = ROOT.TVector3()
      #      jet.SetPtEtaPhi(p.pt(), p.eta(), p.phi())
      #      if jet.DeltaR(gjet) < 0.2 and ( g.pt()/2 < p.pt() < g.pt()*2) :  # match found
      #        match = 1

      #    hists["jet_matchefficiency_to_eta"].Fill(g.eta(), match)
      #    hists["jet_matchefficiency_to_pt"].Fill(g.pt(), match)
      #    for ptcut1, ptcut2 in [[20, 50], [50, 100], [100, 200], [200,400]]:
      #      if ( g.pt() >= ptcut1 and g.pt() < ptcut2 ):
      #        hists["jet_matchefficiency_to_eta_" + str(ptcut1) + "to" +str(ptcut2)].Fill(g.eta(), match)
      #    if g.pt() >= 400 :
      #      hists["jet_matchefficiency_to_eta_400up"].Fill(g.eta(), match)
      #    if abs(g.eta()) <= 1.3 : hists["jet_matchefficiency_to_pt_0to1p3"].Fill(g.pt(), match)
      #    elif 1.3< abs(g.eta()) <= 2.5 : hists["jet_matchefficiency_to_pt_1p3to2p5"].Fill(g.pt(), match)
      #    elif 2.5< abs(g.eta()) <= 3 : hists["jet_matchefficiency_to_pt_2p5to3"].Fill(g.pt(), match)
      #    elif abs(g.eta()) > 3 : hists["jet_matchefficiency_to_pt_3up"].Fill(g.pt(), match)

        for p in jets: # match gen to reco
          if abs(p.eta()) > 5 or p.pt() <20 : continue
	  ## jet multiplicity
       #   if p.pt() > 25 :
       #     jet_multi["nocut"] += 1
       #     if abs(p.eta()) <= 1.3 : jet_multi["0to1p3"] += 1
       #     elif 1.3< abs(p.eta()) <= 2.5 : jet_multi["1p3to2p5"] += 1
       #     elif 2.5< abs(p.eta()) <= 3 : jet_multi["2p5to3"] += 1
       #     elif abs(p.eta()) > 3 : jet_multi["3up"] += 1
       #     for ptcut1, ptcut2 in [[20, 50], [50, 100], [100, 200], [200,400]]:
       #       if ( p.pt() >= ptcut1 and p.pt() < ptcut2 ):
       #         jet_multi[str(ptcut1) + "to" +str(ptcut2)] += 1
       #       if p.pt() >= 400 :
       #         jet_multi["400up"] += 1

          jet = ROOT.TVector3()
          jet.SetPtEtaPhi(p.pt(), p.eta(), p.phi())

          for g in genjets:
            gjet = ROOT.TVector3()
            gjet.SetPtEtaPhi(g.pt(), g.eta(), g.phi())
            if abs(g.eta()) > 5 or g.pt() <20 : continue
            if jet.DeltaR(gjet) < 0.2 and ( g.pt()/2 < p.pt() < g.pt()*2) :  # match found

            # fill for each matched jet
#              hists["jet_ptresponse_to_eta"].Fill(g.eta(), p.pt()/g.pt())
#              hists["jet_ptresponse_to_pt"].Fill(g.pt(), p.pt()/g.pt())
#              for ptcut1, ptcut2 in [[20, 50], [50, 100], [100, 200], [200,400]]:
#                if ( g.pt() >= ptcut1 and g.pt() < ptcut2 ):
#                  hists["jet_ptresponse_to_eta_" + str(ptcut1) + "to" +str(ptcut2)].Fill(g.eta(), p.pt()/g.pt())
#
#              if g.pt() >= 400 :
#                  hists["jet_ptresponse_to_eta_400up"].Fill(g.eta(), p.pt()/g.pt())

              hists["jet_pt"].Fill(p.pt())
              hists["jet_eta"].Fill(p.eta())
              hists["jet_phi"].Fill(p.phi())
              hists["jet_mass"].Fill(p.mass())
#              hists["genjet_pt"].Fill(g.pt())
#              hists["genjet_eta"].Fill(g.eta())
#              hists["genjet_phi"].Fill(g.phi())
#              hists["genjet_mass"].Fill(g.mass())
#
#
#        # fill for each evt
#        hists["jet_multiplicity"].Fill(jet_multi["nocut"])
#        for cutname in [
#                        "0to1p3", "1p3to2p5", "2p5to3","3up",
#                        "20to50", "50to100", "100to200", "200to400", "400up"
#                        ]:
#          hists["jet_multiplicity_" + cutname ].Fill(jet_multi[cutname])

        return hists


def main():

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--inFile',
                      dest='inFile',
                      help='input file [%default]',  
                      default=None,                                                                                                           
                      type='string')
    parser.add_option('-o', '--outFile',          
                      dest='outFile',       
                      help='output file [%default]',  
                      default='histo_delp/val.root',       
                      type='string')
    parser.add_option('-p', '--physObj',          
                      dest='physobject',       
                      help='object to analyze [%default]',
                      default='jet',
                      type='string')
    parser.add_option('--maxEvents',          
                      dest='maxEvts',
                      help='max number of events [%default]',
                      default=4976,
                      type=int)
    (opt, args) = parser.parse_args()


    inFile = opt.inFile
    ntuple = Ntuple(inFile)
    maxEvents = opt.maxEvts

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


    outputF = ROOT.TFile(opt.outFile, "RECREATE")
    obj = opt.physobject
    hists = {} 
    for hname in ["pt", "eta", "phi", "mass",
		]:
      hists[obj+"_"+hname] = createHist(obj+"_"+hname)

#    for hname in ["genjet_pt", "genjet_eta", "genjet_phi", "genjet_mass", 
#		  "jet_multiplicity", "jet_multiplicity_0to1p3", "jet_multiplicity_1p3to2p5", "jet_multiplicity_2p5to3", "jet_multiplicity_3up",
#		  "jet_multiplicity_20to50", "jet_multiplicity_50to100", "jet_multiplicity_100to200", 
#		  "jet_multiplicity_200to400", "jet_multiplicity_400up"
#		]:
#      hists[hname] = createHist(hname)

#    for hname in ["jet_matchefficiency_to_eta",
#                  "jet_matchefficiency_to_eta_20to50", "jet_matchefficiency_to_eta_50to100", "jet_matchefficiency_to_eta_100to200",
#                  "jet_matchefficiency_to_eta_200to400", "jet_matchefficiency_to_eta_400up",
#		  "jet_matchefficiency_to_pt", "jet_matchefficiency_to_pt_0to1p3", "jet_matchefficiency_to_pt_1p3to2p5", "jet_matchefficiency_to_pt_2p5to3", "jet_matchefficiency_to_pt_3up",
#		  "jet_ptresponse_to_eta", "jet_ptresponse_to_eta_20to50", "jet_ptresponse_to_eta_50to100",
#		  "jet_ptresponse_to_eta_100to200", "jet_ptresponse_to_eta_200to400", "jet_ptresponse_to_eta_400up",
#		  "jet_ptresponse_to_pt"
#		]:
#      hists[hname] = create2dHist(hname)

    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents %100) == 0 :
          print '... processed {} events ...'.format(event.entry()+1)

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

	if obj=="jet":	hists = runJet(event, hists)

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
