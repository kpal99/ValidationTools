#!/usr/bin/env python
import ROOT, math
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys


# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple

hists = {}
outputDir = "."#histo_delphes"

def createHist(varname):
    if "_pt" in varname or "_pt-eta" in varname:
        h = ROOT.TH1D(varname, varname, 50, 0., 250.)
        h.GetXaxis().SetTitle("p_{T} [GeV]")
        h.GetYaxis().SetTitle("N_{#gamma}")
    elif "DR" in varname:
        h = ROOT.TH1D(varname, varname, 50, 0., 2*math.pi)
        h.GetXaxis().SetTitle("min #Delta(R) [GeV]")
        h.GetYaxis().SetTitle("N_{#gamma}")
    elif ("_eta" in varname or "_eta-pt" in varname):
        h = ROOT.TH1D(varname, varname, 50, -4., 4.)
        h.GetXaxis().SetTitle("#eta")
        h.GetYaxis().SetTitle("N_{#gamma}")
    elif "phi" in varname:
        h = ROOT.TH1D(varname, varname, 50, -4., 4.)
        h.GetXaxis().SetTitle("#phi")
        h.GetYaxis().SetTitle("N_{#gamma}")
    elif "mass" in varname:
        h = ROOT.TH1D(varname, varname, 50, -2., 2.)
        h.GetXaxis().SetTitle("mass [GeV]")
        h.GetYaxis().SetTitle("N_{#gamma}")

    h.Sumw2()

    return h

def create2dHist(varname):
    if "to_pt" in varname:
        h = ROOT.TProfile(varname, varname, 50, 0., 250.)
        h.GetXaxis().SetTitle("p_{T} [GeV]")
        h.GetYaxis().SetTitle("Gamma.pt/GenGamma.pt")
    if "to_eta" in varname:
        h = ROOT.TProfile(varname, varname, 50, -4., 4.)
        h.GetXaxis().SetTitle("#eta")
        h.GetYaxis().SetTitle("Gamma.pt/GenGamma.pt")

    h.Sumw2()

    return h


def main():
    inFile = sys.argv[1]    
    outFile = sys.argv[2]
    ntuple = Ntuple(inFile)
    
    mystatus = 1 ## photon flat statuses are all 1
    # if 'GluGluH' in inFile: mystatus = 23  ## wayyy too few :(

    maxEvents = 500000

    tot_nevents = 0
    tot_genpart = 0
    tot_gengamma = 0
    tot_electron = 0
    tot_gamma = 0
    tot_muon = 0
    tot_jet = 0
    tot_tau = 0
    tot_met = 0
    tot_genjetAK8 = 0
    tot_jetAK8 = 0


    outputF = ROOT.TFile(outputDir + "/" + outFile + ".root","RECREATE")

    print("Starting!")
    ## efficiency denominators
    hists["gamma_gen_eta"] = createHist("gamma_gen_eta")
    hists["gamma_gen_eta-pt8to20"] = createHist("gamma_gen_eta-pt8to20") 
    hists["gamma_gen_eta-pt20to50"] = createHist("gamma_gen_eta-pt20to50")
    hists["gamma_gen_eta-pt50to100"] = createHist("gamma_gen_eta-pt50to100")
    hists["gamma_gen_eta-pt100up"] = createHist("gamma_gen_eta-pt100up") 
    hists["gamma_gen_pt"] = createHist("gamma_gen_pt")
    hists["gamma_gen_pt-eta0to1p5"] = createHist("gamma_gen_pt-eta0to1p5")
    hists["gamma_gen_pt-eta1p5to3p0"] = createHist("gamma_gen_pt-eta1p5to3p0")
    ## efficiency numerators
    hists["gamma_genmatched_eta"] = createHist("gamma_genmatched_eta")
    hists["gamma_genmatched_eta-pt8to20"] = createHist("gamma_genmatched_eta-pt8to20") 
    hists["gamma_genmatched_eta-pt20to50"] = createHist("gamma_genmatched_eta-pt20to50")
    hists["gamma_genmatched_eta-pt50to100"] = createHist("gamma_genmatched_eta-pt50to100")
    hists["gamma_genmatched_eta-pt100up"] = createHist("gamma_genmatched_eta-pt100up") 
    hists["gamma_genmatched_pt"] = createHist("gamma_genmatched_pt")
    hists["gamma_genmatched_pt-eta0to1p5"] = createHist("gamma_genmatched_pt-eta0to1p5")
    hists["gamma_genmatched_pt-eta1p5to3p0"] = createHist("gamma_genmatched_pt-eta1p5to3p0")
    hists["gamma_Loose_genmatched_eta"] = createHist("gamma_Loose_genmatched_eta")
    hists["gamma_Loose_genmatched_eta-pt8to20"] = createHist("gamma_Loose_genmatched_eta-pt8to20") 
    hists["gamma_Loose_genmatched_eta-pt20to50"] = createHist("gamma_Loose_genmatched_eta-pt20to50")
    hists["gamma_Loose_genmatched_eta-pt50to100"] = createHist("gamma_Loose_genmatched_eta-pt50to100")
    hists["gamma_Loose_genmatched_eta-pt100up"] = createHist("gamma_Loose_genmatched_eta-pt100up") 
    hists["gamma_Loose_genmatched_pt"] = createHist("gamma_Loose_genmatched_pt")
    hists["gamma_Loose_genmatched_pt-eta0to1p5"] = createHist("gamma_Loose_genmatched_pt-eta0to1p5")
    hists["gamma_Loose_genmatched_pt-eta1p5to3p0"] = createHist("gamma_Loose_genmatched_pt-eta1p5to3p0")
    hists["gamma_Tight_genmatched_eta"] = createHist("gamma_Tight_genmatched_eta")
    hists["gamma_Tight_genmatched_eta-pt8to20"] = createHist("gamma_Tight_genmatched_eta-pt8to20") 
    hists["gamma_Tight_genmatched_eta-pt20to50"] = createHist("gamma_Tight_genmatched_eta-pt20to50")
    hists["gamma_Tight_genmatched_eta-pt50to100"] = createHist("gamma_Tight_genmatched_eta-pt50to100")
    hists["gamma_Tight_genmatched_eta-pt100up"] = createHist("gamma_Tight_genmatched_eta-pt100up") 
    hists["gamma_Tight_genmatched_pt"] = createHist("gamma_Tight_genmatched_pt")
    hists["gamma_Tight_genmatched_pt-eta0to1p5"] = createHist("gamma_Tight_genmatched_pt-eta0to1p5")
    hists["gamma_Tight_genmatched_pt-eta1p5to3p0"] = createHist("gamma_Tight_genmatched_pt-eta1p5to3p0")

    ## reco extra info
    hists["gamma_reco_phi"] = createHist("gamma_reco_phi")
    hists["gamma_reco_mass"] = createHist("gamma_reco_mass")
    hists["gamma_reco_minDR"] = createHist("gamma_reco_minDR")
    hists["gamma_recomatched_eta"] = createHist("gamma_recomatched_eta")
    hists["gamma_recomatched_pt"] = createHist("gamma_recomatched_pt")
    hists["gamma_Loose_recomatched_eta"] = createHist("gamma_Loose_recomatched_eta")
    hists["gamma_Loose_recomatched_pt"] = createHist("gamma_Loose_recomatched_pt")
    hists["gamma_Tight_recomatched_eta"] = createHist("gamma_Tight_recomatched_eta")
    hists["gamma_Tight_recomatched_pt"] = createHist("gamma_Tight_recomatched_pt")

    ## fakerate denominators
    hists["gamma_reco_eta"] = createHist("gamma_reco_eta")
    hists["gamma_reco_eta-pt8to20"] = createHist("gamma_reco_eta-pt8to20") 
    hists["gamma_reco_eta-pt20to50"] = createHist("gamma_reco_eta-pt20to50")
    hists["gamma_reco_eta-pt50to100"] = createHist("gamma_reco_eta-pt50to100")
    hists["gamma_reco_eta-pt100up"] = createHist("gamma_reco_eta-pt100up") 
    hists["gamma_reco_pt"] = createHist("gamma_reco_pt")
    hists["gamma_reco_pt-eta0to1p5"] = createHist("gamma_reco_pt-eta0to1p5")
    hists["gamma_reco_pt-eta1p5to3p0"] = createHist("gamma_reco_pt-eta1p5to3p0")
    hists["gamma_Loose_reco_eta"] = createHist("gamma_Loose_reco_eta")
    hists["gamma_Loose_reco_eta-pt8to20"] = createHist("gamma_Loose_reco_eta-pt8to20") 
    hists["gamma_Loose_reco_eta-pt20to50"] = createHist("gamma_Loose_reco_eta-pt20to50")
    hists["gamma_Loose_reco_eta-pt50to100"] = createHist("gamma_Loose_reco_eta-pt50to100")
    hists["gamma_Loose_reco_eta-pt100up"] = createHist("gamma_Loose_reco_eta-pt100up") 
    hists["gamma_Loose_reco_pt"] = createHist("gamma_Loose_reco_pt")
    hists["gamma_Loose_reco_pt-eta0to1p5"] = createHist("gamma_Loose_reco_pt-eta0to1p5")
    hists["gamma_Loose_reco_pt-eta1p5to3p0"] = createHist("gamma_Loose_reco_pt-eta1p5to3p0")
    hists["gamma_Tight_reco_eta"] = createHist("gamma_Tight_reco_eta")
    hists["gamma_Tight_reco_eta-pt8to20"] = createHist("gamma_Tight_reco_eta-pt8to20") 
    hists["gamma_Tight_reco_eta-pt20to50"] = createHist("gamma_Tight_reco_eta-pt20to50")
    hists["gamma_Tight_reco_eta-pt50to100"] = createHist("gamma_Tight_reco_eta-pt50to100")
    hists["gamma_Tight_reco_eta-pt100up"] = createHist("gamma_Tight_reco_eta-pt100up") 
    hists["gamma_Tight_reco_pt"] = createHist("gamma_Tight_reco_pt")
    hists["gamma_Tight_reco_pt-eta0to1p5"] = createHist("gamma_Tight_reco_pt-eta0to1p5")
    hists["gamma_Tight_reco_pt-eta1p5to3p0"] = createHist("gamma_Tight_reco_pt-eta1p5to3p0")
    ## fakerate numerators
    hists["gamma_recounmatched_eta"] = createHist("gamma_recounmatched_eta")
    hists["gamma_recounmatched_eta-pt8to20"] = createHist("gamma_recounmatched_eta-pt8to20") 
    hists["gamma_recounmatched_eta-pt20to50"] = createHist("gamma_recounmatched_eta-pt20to50")
    hists["gamma_recounmatched_eta-pt50to100"] = createHist("gamma_recounmatched_eta-pt50to100")
    hists["gamma_recounmatched_eta-pt100up"] = createHist("gamma_recounmatched_eta-pt100up") 
    hists["gamma_recounmatched_pt"] = createHist("gamma_recounmatched_pt")
    hists["gamma_recounmatched_pt-eta0to1p5"] = createHist("gamma_recounmatched_pt-eta0to1p5")
    hists["gamma_recounmatched_pt-eta1p5to3p0"] = createHist("gamma_recounmatched_pt-eta1p5to3p0")
    hists["gamma_Loose_recounmatched_eta"] = createHist("gamma_Loose_recounmatched_eta")
    hists["gamma_Loose_recounmatched_eta-pt8to20"] = createHist("gamma_Loose_recounmatched_eta-pt8to20") 
    hists["gamma_Loose_recounmatched_eta-pt20to50"] = createHist("gamma_Loose_recounmatched_eta-pt20to50")
    hists["gamma_Loose_recounmatched_eta-pt50to100"] = createHist("gamma_Loose_recounmatched_eta-pt50to100")
    hists["gamma_Loose_recounmatched_eta-pt100up"] = createHist("gamma_Loose_recounmatched_eta-pt100up") 
    hists["gamma_Loose_recounmatched_pt"] = createHist("gamma_Loose_recounmatched_pt")
    hists["gamma_Loose_recounmatched_pt-eta0to1p5"] = createHist("gamma_Loose_recounmatched_pt-eta0to1p5")
    hists["gamma_Loose_recounmatched_pt-eta1p5to3p0"] = createHist("gamma_Loose_recounmatched_pt-eta1p5to3p0")
    hists["gamma_Tight_recounmatched_eta"] = createHist("gamma_Tight_recounmatched_eta")
    hists["gamma_Tight_recounmatched_eta-pt8to20"] = createHist("gamma_Tight_recounmatched_eta-pt8to20") 
    hists["gamma_Tight_recounmatched_eta-pt20to50"] = createHist("gamma_Tight_recounmatched_eta-pt20to50")
    hists["gamma_Tight_recounmatched_eta-pt50to100"] = createHist("gamma_Tight_recounmatched_eta-pt50to100")
    hists["gamma_Tight_recounmatched_eta-pt100up"] = createHist("gamma_Tight_recounmatched_eta-pt100up") 
    hists["gamma_Tight_recounmatched_pt"] = createHist("gamma_Tight_recounmatched_pt")
    hists["gamma_Tight_recounmatched_pt-eta0to1p5"] = createHist("gamma_Tight_recounmatched_pt-eta0to1p5")
    hists["gamma_Tight_recounmatched_pt-eta1p5to3p0"] = createHist("gamma_Tight_recounmatched_pt-eta1p5to3p0")

    ## ptresponses
    hists["gamma_ptresponse_to_eta"] = create2dHist("gamma_ptresponse_to_eta")
    hists["gamma_ptresponse_to_eta-pt8to20"] = create2dHist("gamma_ptresponse_to_eta-pt8to20") 
    hists["gamma_ptresponse_to_eta-pt20to50"] = create2dHist("gamma_ptresponse_to_eta-pt20to50")
    hists["gamma_ptresponse_to_eta-pt50to100"] = create2dHist("gamma_ptresponse_to_eta-pt50to100")
    hists["gamma_ptresponse_to_eta-pt100up"] = create2dHist("gamma_ptresponse_to_eta-pt100up") 
    hists["gamma_ptresponse_to_pt"] = create2dHist("gamma_ptresponse_to_pt")
    hists["gamma_ptresponse_to_pt-eta0to1p5"] = create2dHist("gamma_ptresponse_to_pt-eta0to1p5")
    hists["gamma_ptresponse_to_pt-eta1p5to3p0"] = create2dHist("gamma_ptresponse_to_pt-eta1p5to3p0")
    hists["gamma_Loose_ptresponse_to_eta"] = create2dHist("gamma_Loose_ptresponse_to_eta")
    hists["gamma_Loose_ptresponse_to_eta-pt8to20"] = create2dHist("gamma_Loose_ptresponse_to_eta-pt8to20") 
    hists["gamma_Loose_ptresponse_to_eta-pt20to50"] = create2dHist("gamma_Loose_ptresponse_to_eta-pt20to50")
    hists["gamma_Loose_ptresponse_to_eta-pt50to100"] = create2dHist("gamma_Loose_ptresponse_to_eta-pt50to100")
    hists["gamma_Loose_ptresponse_to_eta-pt100up"] = create2dHist("gamma_Loose_ptresponse_to_eta-pt100up") 
    hists["gamma_Loose_ptresponse_to_pt"] = create2dHist("gamma_Loose_ptresponse_to_pt")
    hists["gamma_Loose_ptresponse_to_pt-eta0to1p5"] = create2dHist("gamma_Loose_ptresponse_to_pt-eta0to1p5")
    hists["gamma_Loose_ptresponse_to_pt-eta1p5to3p0"] = create2dHist("gamma_Loose_ptresponse_to_pt-eta1p5to3p0")
    hists["gamma_Tight_ptresponse_to_eta"] = create2dHist("gamma_Tight_ptresponse_to_eta")
    hists["gamma_Tight_ptresponse_to_eta-pt8to20"] = create2dHist("gamma_Tight_ptresponse_to_eta-pt8to20") 
    hists["gamma_Tight_ptresponse_to_eta-pt20to50"] = create2dHist("gamma_Tight_ptresponse_to_eta-pt20to50")
    hists["gamma_Tight_ptresponse_to_eta-pt50to100"] = create2dHist("gamma_Tight_ptresponse_to_eta-pt50to100")
    hists["gamma_Tight_ptresponse_to_eta-pt100up"] = create2dHist("gamma_Tight_ptresponse_to_eta-pt100up") 
    hists["gamma_Tight_ptresponse_to_pt"] = create2dHist("gamma_Tight_ptresponse_to_pt")
    hists["gamma_Tight_ptresponse_to_pt-eta0to1p5"] = create2dHist("gamma_Tight_ptresponse_to_pt-eta0to1p5")
    hists["gamma_Tight_ptresponse_to_pt-eta1p5to3p0"] = create2dHist("gamma_Tight_ptresponse_to_pt-eta1p5to3p0")

    print("Booked histograms, looping...")

    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents %100) == 0 :
            print '... processed {} events ...'.format(event.entry()+1)

        gammas = event.gammas()
        genparts = event.genparticles()

        gengammacount = 0
        tvecs_gengamma = []
        for igen in genparts:
            if igen.pid() != 22 or igen.status() != mystatus or igen.pt() < 8 or abs(igen.eta()) > 5: continue
            gengammacount += 1

            hists["gamma_gen_pt"].Fill(igen.pt())
            hists["gamma_gen_eta"].Fill(igen.eta())

            ## efficiency denominators
            for ptcut1, ptcut2 in [[8, 20], [20, 50], [50, 100]]:
                if ( igen.pt() >= ptcut1 and igen.pt() < ptcut2 ): 
                    hists["gamma_gen_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(igen.eta())
            if igen.pt() >= 100 :
                hists["gamma_gen_eta-pt100up"].Fill(igen.eta())
            for etacut1, etacut2 in [[0,1.5],[1.5,3.0]]:
                if ( abs(igen.eta()) >= etacut1 and abs(igen.eta()) < etacut2 ):
                    hists["gamma_gen_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(igen.pt())            

            tvec = ROOT.TVector3()
            tvec.SetPtEtaPhi(igen.pt(), igen.eta(), igen.phi()) 
            tvecs_gengamma.append(tvec)

	for igamma in gammas:
            tvec_gamma = ROOT.TVector3()
            tvec_gamma.SetPtEtaPhi(igamma.pt(), igamma.eta(), igamma.phi())
            if abs(igamma.eta()) > 5 : continue

            matched = False
            minDR = 999.9
            minDRindex = -1

            for ivec in range(0,len(tvecs_gengamma)):
                if tvec_gamma.DeltaR(tvecs_gengamma[ivec]) < minDR:
                    minDR = tvec_gamma.DeltaR(tvecs_gengamma[ivec])
                    minDRindex = ivec
                    
            if minDR < 0.2: matched = True 
            #if matched: print "Mathced with minDR",minDR,"and index",minDRindex,"and pt",genparts[minDRindex].Pt()

            hists["gamma_reco_pt"].Fill(igamma.pt())
            hists["gamma_reco_eta"].Fill(igamma.eta())
            hists["gamma_reco_phi"].Fill(igamma.phi())
            hists["gamma_reco_mass"].Fill(igamma.mass())
            hists["gamma_reco_minDR"].Fill(minDR)
            if igamma.idpass() > 0:
                hists["gamma_Loose_reco_pt"].Fill(igamma.pt())
                hists["gamma_Loose_reco_eta"].Fill(igamma.eta())
            if igamma.idpass() > 3:
                hists["gamma_Tight_reco_pt"].Fill(igamma.pt())
                hists["gamma_Tight_reco_eta"].Fill(igamma.eta())                

            ## fakerate denominators
            for ptcut1, ptcut2 in [[8, 20], [20, 50], [50, 100]]:
                if ( igamma.pt() >= ptcut1 and igamma.pt() < ptcut2 ): 
                    hists["gamma_reco_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(igamma.eta())
                    if igamma.idpass() > 0: hists["gamma_Loose_reco_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(igamma.eta())
                    if igamma.idpass() > 3: hists["gamma_Tight_reco_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(igamma.eta())
            if igamma.pt() >= 100 :
                hists["gamma_reco_eta-pt100up"].Fill(igamma.eta())
                if igamma.idpass() > 0: hists["gamma_Loose_reco_eta-pt100up"].Fill(igamma.eta())
                if igamma.idpass() > 3: hists["gamma_Tight_reco_eta-pt100up"].Fill(igamma.eta())
            for etacut1, etacut2 in [[0,1.5],[1.5,3.0]]:
                if ( abs(igamma.eta()) >= etacut1 and abs(igamma.eta()) < etacut2 ):
                    hists["gamma_reco_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(igamma.pt())            
                    if igamma.idpass() > 0: hists["gamma_Loose_reco_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(igamma.pt())            
                    if igamma.idpass() > 3: hists["gamma_Tight_reco_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(igamma.pt())            


            if matched:
                hists["gamma_recomatched_pt"].Fill(igamma.pt())
                hists["gamma_recomatched_eta"].Fill(igamma.eta())
                hists["gamma_genmatched_pt"].Fill(tvecs_gengamma[minDRindex].Pt())
                hists["gamma_genmatched_eta"].Fill(tvecs_gengamma[minDRindex].Eta())
                hists["gamma_ptresponse_to_eta"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                hists["gamma_ptresponse_to_pt"].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                if igamma.idpass() > 0:
                    hists["gamma_Loose_recomatched_pt"].Fill(igamma.pt())
                    hists["gamma_Loose_recomatched_eta"].Fill(igamma.eta())
                    hists["gamma_Loose_genmatched_pt"].Fill(tvecs_gengamma[minDRindex].Pt())
                    hists["gamma_Loose_genmatched_eta"].Fill(tvecs_gengamma[minDRindex].Eta())
                    hists["gamma_Loose_ptresponse_to_eta"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                    hists["gamma_Loose_ptresponse_to_pt"].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                if igamma.idpass() > 3:
                    hists["gamma_Tight_recomatched_pt"].Fill(igamma.pt())
                    hists["gamma_Tight_recomatched_eta"].Fill(igamma.eta())
                    hists["gamma_Tight_genmatched_pt"].Fill(tvecs_gengamma[minDRindex].Pt())
                    hists["gamma_Tight_genmatched_eta"].Fill(tvecs_gengamma[minDRindex].Eta())
                    hists["gamma_Tight_ptresponse_to_eta"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                    hists["gamma_Tight_ptresponse_to_pt"].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())

                ## efficiency numerators, ptresponses
                for ptcut1, ptcut2 in [[8, 20], [20, 50], [50, 100]]:
                    if ( tvecs_gengamma[minDRindex].Pt() >= ptcut1 and tvecs_gengamma[minDRindex].Pt() < ptcut2 ): 
                        hists["gamma_genmatched_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(tvecs_gengamma[minDRindex].Eta())
                        hists["gamma_ptresponse_to_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                        if igamma.idpass() > 0: 
                            hists["gamma_Loose_genmatched_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(tvecs_gengamma[minDRindex].Eta())
                            hists["gamma_Loose_ptresponse_to_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                        if igamma.idpass() > 3: 
                            hists["gamma_Tight_genmatched_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(tvecs_gengamma[minDRindex].Eta())
                            hists["gamma_Tight_ptresponse_to_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())

                if tvecs_gengamma[minDRindex].Pt() >= 100 :
                    hists["gamma_genmatched_eta-pt100up"].Fill(tvecs_gengamma[minDRindex].Eta())
                    hists["gamma_ptresponse_to_eta-pt100up"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                    if igamma.idpass() > 0: 
                        hists["gamma_Loose_genmatched_eta-pt100up"].Fill(tvecs_gengamma[minDRindex].Eta())
                        hists["gamma_Loose_ptresponse_to_eta-pt100up"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                    if igamma.idpass() > 3: 
                        hists["gamma_Tight_genmatched_eta-pt100up"].Fill(tvecs_gengamma[minDRindex].Eta())
                        hists["gamma_Tight_ptresponse_to_eta-pt100up"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                for etacut1, etacut2 in [[0,1.5],[1.5,3.0]]:
                    if ( abs(tvecs_gengamma[minDRindex].Eta()) >= etacut1 and abs(tvecs_gengamma[minDRindex].Eta()) < etacut2 ):
                        hists["gamma_genmatched_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(tvecs_gengamma[minDRindex].Pt())            
                        hists["gamma_ptresponse_to_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                        if igamma.idpass() > 0: 
                            hists["gamma_Loose_genmatched_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(tvecs_gengamma[minDRindex].Pt())            
                            hists["gamma_Loose_ptresponse_to_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                        if igamma.idpass() > 3: 
                            hists["gamma_Tight_genmatched_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(tvecs_gengamma[minDRindex].Pt())            
                            hists["gamma_Tight_ptresponse_to_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())

              
            else:
                hists["gamma_recounmatched_pt"].Fill(igamma.pt())
                hists["gamma_recounmatched_eta"].Fill(igamma.eta())
                if igamma.idpass() > 0:
                    hists["gamma_Loose_recounmatched_pt"].Fill(igamma.pt())
                    hists["gamma_Loose_recounmatched_eta"].Fill(igamma.eta())
                if igamma.idpass() > 3:
                    hists["gamma_Tight_recounmatched_pt"].Fill(igamma.pt())
                    hists["gamma_Tight_recounmatched_eta"].Fill(igamma.eta())

                ## fakerate numerators
                for ptcut1, ptcut2 in [[8, 20], [20, 50], [50, 100]]:
                    if ( igamma.pt() >= ptcut1 and igamma.pt() < ptcut2 ): 
                        hists["gamma_recounmatched_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(igamma.eta())
                        if igamma.idpass() > 0: hists["gamma_Loose_recounmatched_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(igamma.eta())
                        if igamma.idpass() > 3: hists["gamma_Tight_recounmatched_eta-pt" + str(ptcut1) + "to" +str(ptcut2)].Fill(igamma.eta())
                if igamma.pt() >= 100 :
                    hists["gamma_recounmatched_eta-pt100up"].Fill(igamma.eta())
                    if igamma.idpass() > 0: hists["gamma_Loose_recounmatched_eta-pt100up"].Fill(igamma.eta())
                    if igamma.idpass() > 3: hists["gamma_Tight_recounmatched_eta-pt100up"].Fill(igamma.eta())
                for etacut1, etacut2 in [[0,1.5],[1.5,3.0]]:
                    if ( abs(igamma.eta()) >= etacut1 and abs(igamma.eta()) < etacut2 ):
                        hists["gamma_recounmatched_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(igamma.pt())            
                        if igamma.idpass() > 0: hists["gamma_Loose_recounmatched_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(igamma.pt()) 
                        if igamma.idpass() > 3: hists["gamma_Tight_recounmatched_pt-eta"+str(etacut1).replace('.','p')+"to"+str(etacut2).replace('.','p')].Fill(igamma.pt()) 

            # remove this matched gen photon so that future reco photons can't match to it. 
            # would be better to find the closest reco photon to each gen photon maybe...
            if minDRindex > -1: tvecs_gengamma.pop(minDRindex)

        tot_nevents += 1
        tot_genpart += len(event.genparticles())
        tot_gengamma += gengammacount
        tot_electron += len(event.electrons()) 
        tot_gamma += len(event.gammas())   
        tot_muon += len(event.muons())   
        tot_jet += len(event.jets())   
        tot_tau += len(event.taus())   
        tot_met += len(event.mets())   
	# tot_genjetAK8 += len(event.genjetsAK8()) ## not in my trees
        # tot_jetAK8 += len(event.jetsAK8())
        # end of one event

    outputF.cd()
    for h in hists.keys(): hists[h].Write()


    print("Processed %d events" % tot_nevents)
    print("On average %f generator particles" % (float(tot_genpart) / tot_nevents))
    print("On average %f generated photons" % (float(tot_gengamma) / tot_nevents))
    print("On average %f electrons" % (float(tot_electron) / tot_nevents))
    print("On average %f photons" % (float(tot_gamma) / tot_nevents))
    print("On average %f muons" % (float(tot_muon) / tot_nevents))
    print("On average %f jets" % (float(tot_jet) / tot_nevents))
    print("On average %f taus" % (float(tot_tau) / tot_nevents))
    print("On average %f met" % (float(tot_met) / tot_nevents))
    # print("On average %f generated AK8 jets" % (float(tot_genjetAK8) / tot_nevents))
    # print("On average %f jetsAK8" % (float(tot_jetAK8) / tot_nevents))

if __name__ == "__main__":
    main()
