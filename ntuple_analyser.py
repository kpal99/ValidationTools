#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import optparse

# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple


def createHist(opt, varname):
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
      if "full" in opt.outFile:
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
      hists[obj+"_"+hname] = createHist(opt, obj+"_"+hname)
      hists["gen"+obj+"_"+hname] = createHist(opt, "gen"+obj+"_"+hname)
      hists[obj+"_matched_"+hname] = createHist(opt, obj+"_matched_"+hname)
      hists["gen"+obj+"_matched_"+hname] = createHist(opt, "gen"+obj+"_matched_"+hname)

    for hname in [
		  "multiplicity", "multiplicity_0to1p3", "multiplicity_1p3to2p5", "multiplicity_2p5to3", "multiplicity_3up",
		  "multiplicity_20to50", "multiplicity_50to100", "multiplicity_100to200", 
		  "multiplicity_200to400", "multiplicity_400up"
		]:
      hists[obj+"_"+hname] = createHist(opt, obj+"_"+hname)

    for hname in ["matchefficiency_to_eta",
                  "matchefficiency_to_eta_20to50", "matchefficiency_to_eta_50to100", "matchefficiency_to_eta_100to200",
                  "matchefficiency_to_eta_200to400", "matchefficiency_to_eta_400up",
		  "matchefficiency_to_pt", "matchefficiency_to_pt_0to1p3", "matchefficiency_to_pt_1p3to2p5", "matchefficiency_to_pt_2p5to3", "matchefficiency_to_pt_3up",
		  "ptresponse_to_eta", "ptresponse_to_eta_20to50", "ptresponse_to_eta_50to100",
		  "ptresponse_to_eta_100to200", "ptresponse_to_eta_200to400", "ptresponse_to_eta_400up",
		  "ptresponse_to_pt"
		]:
      hists[obj+"_"+hname] = create2dHist(obj+"_"+hname)


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

	if obj=="jet":
	   objs = event.jets()
           genobjs = event.genjets()
	elif obj == "photon" :
	   objs = event.gammas()
           genobjs = event.genparticles()

        if len(objs) < 1 or len(genobjs) <1 : continue
        multiplicity = {}
        for cutname in ["nocut",
                        "0to1p3", "1p3to2p5", "2p5to3","3up",
                        "20to50", "50to100", "100to200", "200to400", "400up",
                        ]:
          multiplicity[cutname] = 0


	p_tvectors = []

        for p in objs: # match gen to reco
          if p.eta() > 5 or p.pt() <20 : continue
	    hists[obj+"_pt"].Fill(p.pt())
	    hists[obj+"_eta"].Fill(p.eta())
	    hists[obj+"_phi"].Fill(p.phi())
	    hists[obj+"_mass"].Fill(p.mass())

          if p.pt() > 25 :
            multiplicity["nocut"] += 1
            if abs(p.eta()) <= 1.3 : multiplicity["0to1p3"] += 1
            elif 1.3< abs(p.eta()) <= 2.5 : multiplicity["1p3to2p5"] += 1
            elif 2.5< abs(p.eta()) <= 3 : multiplicity["2p5to3"] += 1
            elif abs(p.eta()) > 3 : multiplicity["3up"] += 1
            for ptcut1, ptcut2 in [[20, 50], [50, 100], [100, 200], [200,400]]:
              if ( p.pt() >= ptcut1 and p.pt() < ptcut2 ):
                multiplicity[str(ptcut1) + "to" +str(ptcut2)] += 1
            if p.pt() >= 400 :
              multiplicity["400up"] += 1

          p_vec = ROOT.TVector3()
          p_vec.SetPtEtaPhi(p.pt(), p.eta(), p.phi())
          p_tvectors.append(p_vec)


	for g in genobjs:  # match reco to gen
          if abs(g.eta()) > 5 or g.pt() <20 : continue
	  hists["gen"+obj+"_pt"].Fill(g.pt())
	  hists["gen"+obj+"_eta"].Fill(g.eta())
          hists["gen"+obj+"_phi"].Fill(g.phi())
          hists["gen"+pbj+"_mass"].Fill(g.mass())
	  g_vec = ROOT.TVector3()
	  g_vec.SetPtEtaPhi(g.pt(), g.eta(), g.phi())
	  match = 0

	  for ivec in range(0, len(p_tvectors)):

	    if g_vec.DeltaR(p_tvectors[ivec]) < 0.2 and (g.pt()/2 < p_tvectors[ivec].Pt() < g.pt()*2) : # matched
	      match = 1
              hists[obj+"_matchefficiency_to_eta"].Fill(g.eta(), match)
              hists[obj+"_matchefficiency_to_pt"].Fill(g.pt(), match)
              for ptcut1, ptcut2 in [[20, 50], [50, 100], [100, 200], [200,400]]:
                if ( g.pt() >= ptcut1 and g.pt() < ptcut2 ):
                  hists[obj+"_matchefficiency_to_eta_" + str(ptcut1) + "to" +str(ptcut2)].Fill(g.eta(), match)
              if g.pt() >= 400 :
                hists[obj+"_matchefficiency_to_eta_400up"].Fill(g.eta(), match)
              if abs(g.eta()) <= 1.3 : hists[obj+"_matchefficiency_to_pt_0to1p3"].Fill(g.pt(), match)
              elif 1.3< abs(g.eta()) <= 2.5 : hists[obj+"_matchefficiency_to_pt_1p3to2p5"].Fill(g.pt(), match)
              elif 2.5< abs(g.eta()) <= 3 : hists[obj+"_matchefficiency_to_pt_2p5to3"].Fill(g.pt(), match)
              elif abs(g.eta()) > 3 : hists[obj+"_matchefficiency_to_pt_3up"].Fill(g.pt(), match)

              hists[obj+"_matched_pt"].Fill(p_tvectors[ivec].Pt())
              hists[obj+"_matched_eta"].Fill(p_tvectors[ivec].Eta())
              hists[obj+"_matched_phi"].Fill(p_tvectors[ivec].Phi())
              hists[obj+"_matched_mass"].Fill(p_tvectors[ivec].Mag()) # ?
              hists["gen"+obj+"_matched_pt"].Fill(g.pt())
              hists["gen"+obj+"_matched_eta"].Fill(g.eta())
              hists["gen"+obj+"_matched_phi"].Fill(g.phi())
              hists["gen"+obj+"_matched_mass"].Fill(g.mass())
	
              hists[obj+"_ptresponse_to_eta"].Fill(g.eta(), p_tvectors[ivec].Pt()/g.pt())
              hists[obj+"_ptresponse_to_pt"].Fill(g.pt(), p_tvectors[ivec].Pt()/g.pt())
              for ptcut1, ptcut2 in [[20, 50], [50, 100], [100, 200], [200,400]]:
                if ( g.pt() >= ptcut1 and g.pt() < ptcut2 ):
                  hists[obj+"_ptresponse_to_eta_" + str(ptcut1) + "to" +str(ptcut2)].Fill(g.eta(), p_tvectors[ivec].Pt()/g.pt())
              if g.pt() >= 400 :
                  hists[obj+"_ptresponse_to_eta_400up"].Fill(g.eta(), p_tvectors[ivec].Pt()/g.pt())


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
