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
    if "pt" in varname:
        h = ROOT.TH1D(varname, varname, 50, 0., 250.)
        h.GetXaxis().SetTitle("p_{T} [GeV]")
        h.GetYaxis().SetTitle("N_{#gamma}")
    if "DR" in varname:
        h = ROOT.TH1D(varname, varname, 50, 0., 2*math.pi)
        h.GetXaxis().SetTitle("min #Delta(R) [GeV]")
        h.GetYaxis().SetTitle("N_{#gamma}")
    if "eta" in varname:
        h = ROOT.TH1D(varname, varname, 50, -4., 4.)
        h.GetXaxis().SetTitle("#eta")
        h.GetYaxis().SetTitle("N_{#gamma}")
    if "phi" in varname:
        h = ROOT.TH1D(varname, varname, 50, -4., 4.)
        h.GetXaxis().SetTitle("#phi")
        h.GetYaxis().SetTitle("N_{#gamma}")
    if "mass" in varname:
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

    maxEvents = 50000

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
    hists["gamma_reco_phi"] = createHist("gamma_reco_phi")
    hists["gamma_reco_mass"] = createHist("gamma_reco_mass")
    hists["gamma_reco_minDR"] = createHist("gamma_reco_minDR")
    hists["gamma_gen_eta"] = createHist("gamma_gen_eta")
    hists["gamma_gen_pt"] = createHist("gamma_gen_pt")
    hists["gamma_genmatched_eta"] = createHist("gamma_genmatched_eta")
    hists["gamma_genmatched_pt"] = createHist("gamma_genmatched_pt")

    ## all, no criteria
    hists["gamma_reco_eta"] = createHist("gamma_reco_eta")
    hists["gamma_reco_pt"] = createHist("gamma_reco_pt")
    hists["gamma_recomatched_eta"] = createHist("gamma_recomatched_eta")
    hists["gamma_recomatched_pt"] = createHist("gamma_recomatched_pt")
    hists["gamma_recounmatched_eta"] = createHist("gamma_recounmatched_eta")
    hists["gamma_recounmatched_pt"] = createHist("gamma_recounmatched_pt")
    hists["gamma_ptresponse_to_eta"] = create2dHist("gamma_ptresponse_to_eta")
    hists["gamma_ptresponse_to_pt"] = create2dHist("gamma_ptresponse_to_pt")

    ## loose photon ID, dummy iso
    hists["gamma_LD_reco_eta"] = createHist("gamma_LD_reco_eta")
    hists["gamma_LD_reco_pt"] = createHist("gamma_LD_reco_pt")
    hists["gamma_LD_recomatched_eta"] = createHist("gamma_LD_recomatched_eta")
    hists["gamma_LD_recomatched_pt"] = createHist("gamma_LD_recomatched_pt")
    hists["gamma_LD_recounmatched_eta"] = createHist("gamma_LD_recounmatched_eta")
    hists["gamma_LD_recounmatched_pt"] = createHist("gamma_LD_recounmatched_pt")
    hists["gamma_LD_ptresponse_to_eta"] = create2dHist("gamma_LD_ptresponse_to_eta")
    hists["gamma_LD_ptresponse_to_pt"] = create2dHist("gamma_LD_ptresponse_to_pt")

    ## loose photon ID, loose+ iso
    hists["gamma_LL_reco_eta"] = createHist("gamma_LL_reco_eta")
    hists["gamma_LL_reco_pt"] = createHist("gamma_LL_reco_pt")
    hists["gamma_LL_recomatched_eta"] = createHist("gamma_LL_recomatched_eta")
    hists["gamma_LL_recomatched_pt"] = createHist("gamma_LL_recomatched_pt")
    hists["gamma_LL_recounmatched_eta"] = createHist("gamma_LL_recounmatched_eta")
    hists["gamma_LL_recounmatched_pt"] = createHist("gamma_LL_recounmatched_pt")

    ## loose photon ID, medium+ iso
    hists["gamma_LM_reco_eta"] = createHist("gamma_LM_reco_eta")
    hists["gamma_LM_reco_pt"] = createHist("gamma_LM_reco_pt")
    hists["gamma_LM_recomatched_eta"] = createHist("gamma_LM_recomatched_eta")
    hists["gamma_LM_recomatched_pt"] = createHist("gamma_LM_recomatched_pt")
    hists["gamma_LM_recounmatched_eta"] = createHist("gamma_LM_recounmatched_eta")
    hists["gamma_LM_recounmatched_pt"] = createHist("gamma_LM_recounmatched_pt")

    ## tight photon ID, dummy iso
    hists["gamma_TD_reco_eta"] = createHist("gamma_TD_reco_eta")
    hists["gamma_TD_reco_pt"] = createHist("gamma_TD_reco_pt")
    hists["gamma_TD_recomatched_eta"] = createHist("gamma_TD_recomatched_eta")
    hists["gamma_TD_recomatched_pt"] = createHist("gamma_TD_recomatched_pt")
    hists["gamma_TD_recounmatched_eta"] = createHist("gamma_TD_recounmatched_eta")
    hists["gamma_TD_recounmatched_pt"] = createHist("gamma_TD_recounmatched_pt")
    hists["gamma_TD_ptresponse_to_eta"] = create2dHist("gamma_TD_ptresponse_to_eta")
    hists["gamma_TD_ptresponse_to_pt"] = create2dHist("gamma_TD_ptresponse_to_pt")

    ## tight photon ID, loose+ iso
    hists["gamma_TL_reco_eta"] = createHist("gamma_TL_reco_eta")
    hists["gamma_TL_reco_pt"] = createHist("gamma_TL_reco_pt")
    hists["gamma_TL_recomatched_eta"] = createHist("gamma_TL_recomatched_eta")
    hists["gamma_TL_recomatched_pt"] = createHist("gamma_TL_recomatched_pt")
    hists["gamma_TL_recounmatched_eta"] = createHist("gamma_TL_recounmatched_eta")
    hists["gamma_TL_recounmatched_pt"] = createHist("gamma_TL_recounmatched_pt")

    ## tight photon ID, medium+ iso
    hists["gamma_TM_reco_eta"] = createHist("gamma_TM_reco_eta")
    hists["gamma_TM_reco_pt"] = createHist("gamma_TM_reco_pt")
    hists["gamma_TM_recomatched_eta"] = createHist("gamma_TM_recomatched_eta")
    hists["gamma_TM_recomatched_pt"] = createHist("gamma_TM_recomatched_pt")
    hists["gamma_TM_recounmatched_eta"] = createHist("gamma_TM_recounmatched_eta")
    hists["gamma_TM_recounmatched_pt"] = createHist("gamma_TM_recounmatched_pt")

    ## tight photon ID, tight+ iso
    hists["gamma_TT_reco_eta"] = createHist("gamma_TT_reco_eta")
    hists["gamma_TT_reco_pt"] = createHist("gamma_TT_reco_pt")
    hists["gamma_TT_recomatched_eta"] = createHist("gamma_TT_recomatched_eta")
    hists["gamma_TT_recomatched_pt"] = createHist("gamma_TT_recomatched_pt")
    hists["gamma_TT_recounmatched_eta"] = createHist("gamma_TT_recounmatched_eta")
    hists["gamma_TT_recounmatched_pt"] = createHist("gamma_TT_recounmatched_pt")

    ## tight photon ID, verytight iso
    hists["gamma_TV_reco_eta"] = createHist("gamma_TV_reco_eta")
    hists["gamma_TV_reco_pt"] = createHist("gamma_TV_reco_pt")
    hists["gamma_TV_recomatched_eta"] = createHist("gamma_TV_recomatched_eta")
    hists["gamma_TV_recomatched_pt"] = createHist("gamma_TV_recomatched_pt")
    hists["gamma_TV_recounmatched_eta"] = createHist("gamma_TV_recounmatched_eta")
    hists["gamma_TV_recounmatched_pt"] = createHist("gamma_TV_recounmatched_pt")


    # hists["gamma_ptresponse_to_eta_0to50"] = create2dHist("gamma_ptresponse_to_eta_0to50")
    # hists["gamma_ptresponse_to_eta_50to100"] = create2dHist("gamma_ptresponse_to_eta_50to100")
    # hists["gamma_ptresponse_to_eta_100to200"] = create2dHist("gamma_ptresponse_to_eta_100to200")
    # hists["gamma_ptresponse_to_eta_200to400"] = create2dHist("gamma_ptresponse_to_eta_200to400")
    # hists["gamma_ptresponse_to_eta_400up"] = create2dHist("gamma_ptresponse_to_eta_400up")

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
            if igen.pid() != 22 or igen.status() != mystatus or igen.pt() == 0 or abs(igen.eta()) > 5: continue
            gengammacount += 1

            hists["gamma_gen_pt"].Fill(igen.pt())
            hists["gamma_gen_eta"].Fill(igen.eta())

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

            # for igen in genparts:
            #     gencounter += 1
            #     if igen.pid() != 22 or igen.status() != mystatus or igen.pt() == 0 or abs(igen.eta()) > 5: continue

            #     tvec_gengamma = ROOT.TVector3()
            #     tvec_gengamma.SetPtEtaPhi(igen.pt(), igen.eta(), igen.phi()) 

            #     if tvec_gamma.DeltaR(tvec_gengamma) < minDR:
            #         minDR = tvec_gamma.DeltaR(tvec_gengamma)
            #         minDRindex = gencounter
            #         #print "DR =",minDR,"and pt",igen.pt()
                    
            if minDR < 0.2: matched = True 
            #if matched: print "Mathced with minDR",minDR,"and index",minDRindex,"and pt",genparts[minDRindex].pt()

            hists["gamma_reco_pt"].Fill(igamma.pt())
            hists["gamma_reco_eta"].Fill(igamma.eta())
            hists["gamma_reco_phi"].Fill(igamma.phi())
            hists["gamma_reco_mass"].Fill(igamma.mass())
            hists["gamma_reco_minDR"].Fill(minDR)

            if igamma.idpass() > 0:
                hists["gamma_LD_reco_pt"].Fill(igamma.pt())
                hists["gamma_LD_reco_eta"].Fill(igamma.eta())
                if igamma.isopass() > 0:
                    hists["gamma_LL_reco_pt"].Fill(igamma.pt())
                    hists["gamma_LL_reco_eta"].Fill(igamma.eta())
                if igamma.isopass() > 8:
                    hists["gamma_LM_reco_pt"].Fill(igamma.pt())
                    hists["gamma_LM_reco_eta"].Fill(igamma.eta())

            if igamma.idpass() > 3:
                hists["gamma_TD_reco_pt"].Fill(igamma.pt())
                hists["gamma_TD_reco_eta"].Fill(igamma.eta())
                if igamma.isopass() > 0:
                    hists["gamma_TL_reco_pt"].Fill(igamma.pt())
                    hists["gamma_TL_reco_eta"].Fill(igamma.eta())
                if igamma.isopass() > 9:
                    hists["gamma_TM_reco_pt"].Fill(igamma.pt())
                    hists["gamma_TM_reco_eta"].Fill(igamma.eta())
                if igamma.isopass() > 13:
                    hists["gamma_TT_reco_pt"].Fill(igamma.pt())
                    hists["gamma_TT_reco_eta"].Fill(igamma.eta())
                if igamma.isopass() == 15:
                    hists["gamma_TV_reco_pt"].Fill(igamma.pt())
                    hists["gamma_TV_reco_eta"].Fill(igamma.eta())
                

            if matched:
                hists["gamma_recomatched_pt"].Fill(igamma.pt())
                hists["gamma_recomatched_eta"].Fill(igamma.eta())
                hists["gamma_genmatched_pt"].Fill(tvecs_gengamma[minDRindex].Pt())
                hists["gamma_genmatched_eta"].Fill(tvecs_gengamma[minDRindex].Eta())
                hists["gamma_ptresponse_to_eta"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                hists["gamma_ptresponse_to_pt"].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())

                if igamma.idpass() > 0:
                    hists["gamma_LD_recomatched_pt"].Fill(igamma.pt())
                    hists["gamma_LD_recomatched_eta"].Fill(igamma.eta())
                    hists["gamma_LD_ptresponse_to_eta"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                    hists["gamma_LD_ptresponse_to_pt"].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                    if igamma.isopass() > 0:
                        hists["gamma_LL_recomatched_pt"].Fill(igamma.pt())
                        hists["gamma_LL_recomatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() > 8:
                        hists["gamma_LM_recomatched_pt"].Fill(igamma.pt())
                        hists["gamma_LM_recomatched_eta"].Fill(igamma.eta())

                if igamma.idpass() > 3:
                    hists["gamma_TD_recomatched_pt"].Fill(igamma.pt())
                    hists["gamma_TD_recomatched_eta"].Fill(igamma.eta())
                    hists["gamma_TD_ptresponse_to_eta"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                    hists["gamma_TD_ptresponse_to_pt"].Fill(tvecs_gengamma[minDRindex].Pt(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                    if igamma.isopass() > 0:
                        hists["gamma_TL_recomatched_pt"].Fill(igamma.pt())
                        hists["gamma_TL_recomatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() > 9:
                        hists["gamma_TM_recomatched_pt"].Fill(igamma.pt())
                        hists["gamma_TM_recomatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() > 13:
                        hists["gamma_TT_recomatched_pt"].Fill(igamma.pt())
                        hists["gamma_TT_recomatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() == 15:
                        hists["gamma_TV_recomatched_pt"].Fill(igamma.pt())
                        hists["gamma_TV_recomatched_eta"].Fill(igamma.eta())

                # for ptcut1, ptcut2 in [[0, 50], [50, 100], [100, 200], [200,400]]:
                #     if ( tvecs_gengamma[minDRindex].Pt() >= ptcut1 and tvecs_gengamma[minDRindex].Pt() < ptcut2 ): 
                #         hists["gamma_ptresponse_to_eta_" + str(ptcut1) + "to" +str(ptcut2)].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())
                #     if igen.pt() >= 400 :
                #         hists["gamma_ptresponse_to_eta_400up"].Fill(tvecs_gengamma[minDRindex].Eta(), igamma.pt()/tvecs_gengamma[minDRindex].Pt())              
            else:
                hists["gamma_recounmatched_pt"].Fill(igamma.pt())
                hists["gamma_recounmatched_eta"].Fill(igamma.eta())
                if igamma.idpass() > 0:
                    hists["gamma_LD_recounmatched_pt"].Fill(igamma.pt())
                    hists["gamma_LD_recounmatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() > 0:
                        hists["gamma_LL_recounmatched_pt"].Fill(igamma.pt())
                        hists["gamma_LL_recounmatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() > 8:
                        hists["gamma_LM_recounmatched_pt"].Fill(igamma.pt())
                        hists["gamma_LM_recounmatched_eta"].Fill(igamma.eta())

                if igamma.idpass() > 3:
                    hists["gamma_TD_recounmatched_pt"].Fill(igamma.pt())
                    hists["gamma_TD_recounmatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() > 0:
                        hists["gamma_TL_recounmatched_pt"].Fill(igamma.pt())
                        hists["gamma_TL_recounmatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() > 9:
                        hists["gamma_TM_recounmatched_pt"].Fill(igamma.pt())
                        hists["gamma_TM_recounmatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() > 13:
                        hists["gamma_TT_recounmatched_pt"].Fill(igamma.pt())
                        hists["gamma_TT_recounmatched_eta"].Fill(igamma.eta())
                    if igamma.isopass() == 15:
                        hists["gamma_TV_recounmatched_pt"].Fill(igamma.pt())
                        hists["gamma_TV_recounmatched_eta"].Fill(igamma.eta())

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
