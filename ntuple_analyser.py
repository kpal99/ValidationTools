#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import optparse

# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple

pdgid = {
    "photon": 22,
    "electron": 11,
    "muon": 13,

}
def createHist(opt, varname, params):
    if "pt" in varname:
        h = ROOT.TH1D(varname, "", 100, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("p_{T}[GeV]")
        h.GetYaxis().SetTitle("N")
    if "eta" in varname:
        h = ROOT.TH1D(varname, "", 100, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("#eta")
        h.GetYaxis().SetTitle("N")
    if "phi" in varname:
        h = ROOT.TH1D(varname, "", 100, params["plotPhiRange"][0], params["plotPhiRange"][1])
        h.GetXaxis().SetTitle("#phi")
        h.GetYaxis().SetTitle("N")
    if "mass" in varname:
        h = ROOT.TH1D(varname, "", 100, params["plotMassRange"][0], params["plotMassRange"][1])
        h.GetXaxis().SetTitle("mass[GeV]")
        h.GetYaxis().SetTitle("N")
    if "multi" in varname:
        if "full" in opt.outFile:
            h = ROOT.TH1D(varname, "", 50, params["plotNObjRange_Full"][0], params["plotNObjRange_Full"][1]) 
        else:
            h = ROOT.TH1D(varname, "", 20, params["plotNObjRange_Delp"][0], params["plotNObjRange_Delp"][1])
        h.GetXaxis().SetTitle("multiplicity")
        h.GetYaxis().SetTitle("Events")


    h.Sumw2()

    return h

def create2dHist(varname, params):
    if "to_pt" in varname and "response" in varname:
        h = ROOT.TProfile(varname, "", 100, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("gen p_{T}[GeV]")
        h.GetYaxis().SetTitle("Reco_pt/Gen_pt")
    if "to_eta" in varname and "response" in varname:
        h = ROOT.TProfile(varname, "", 100, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("gen #eta")
        h.GetYaxis().SetTitle("Reco_pt/Gen_pt")
    if "to_pt" in varname and "efficiency" in varname:
        h = ROOT.TProfile(varname, "", 100, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("gen p_{T}[GeV]")
        h.GetYaxis().SetTitle("gen object matching efficiency")
    if "to_eta" in varname and "efficiency" in varname:
        h = ROOT.TProfile(varname, "", 100, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("gen #eta")
        h.GetYaxis().SetTitle("gen object matching efficiency")
    if "to_pt" in varname and "fakerate" in varname:
        h = ROOT.TProfile(varname, "", 100, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("reco p_{T}[GeV]")
        h.GetYaxis().SetTitle("reco object fakerate")
    if "to_eta" in varname and "fakerate" in varname:
        h = ROOT.TProfile(varname, "", 100, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("reco #eta")
        h.GetYaxis().SetTitle("reco object fakerate")


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

    params = {}
    outputF = ROOT.TFile(opt.outFile, "RECREATE")
    obj = opt.physobject
    if obj=="jet":
        params = {
            "dR": 0.2,
            "ptRatio": 2.0,
            "ptMin": 20,
            "etaSlices": [[0, 1.3], [1.3, 2.5], [2.5, 3], [3] ],
            "ptSlices": [[20, 50], [50, 100], [100, 200], [200, 400], [400] ],
            "plotPtRange": [0, 1500],
            "plotEtaRange": [-5, 5],
            "plotPhiRange": [-5, 5],
            "plotMassRange": [0, 500],
            "plotNObjRange_Delp": [0, 20],
            "plotNObjRange_Full": [0, 50],
            "ids": [],
            }
    elif obj == "photon": 
        params = {
            "dR": 0.2,
            "ptRatio": 3.0,
            "ptMin": 8,
            "etaSlices": [[0, 1.5], [1.5, 3]],
            "ptSlices": [[8, 20], [20, 50], [50, 100], [100]],
            "plotPtRange": [0, 200],
            "plotEtaRange": [-4, 4],
            "plotPhiRange": [-4, 4],
            "plotMassRange": [-1, 1],
            "plotNObjRange_Delp": [0, 4],
            "plotNObjRange_Full": [0, 4],
            "ids": ["loose","tight"],
            }
    elif obj == "electron" or obj == "muon":
        params = {
            "dR": 0.2,
            "ptRatio": 2.0,
            "ptMin": 20,
            "etaSlices": [[0, 1.3], [1.3, 2.5], [2.5, 3], [3] ],
            "ptSlices": [[20, 50], [50, 100], [100, 200], [200, 400], [400] ],
            "plotPtRange": [0, 1500],
            "plotEtaRange": [-5, 5],
            "plotPhiRange": [-5, 5],
            "plotMassRange": [0, 500],
            "plotNObjRange_Delp": [0, 20],
            "plotNObjRange_Full": [0, 50],
            "ids": ["loose","tight"],
            }                
    else: 
        print 'Physics object not recognized! Choose jet, photon, electron, or muon.'            
        exit()

    print "Plot parameters:", params

    hists = {} 
    for hname in ["pt", "eta", "phi", "mass"]:
        hists[obj+"_"+hname] = createHist(opt, obj+"_"+hname,params)
        hists["gen"+obj+"_"+hname] = createHist(opt, "gen"+obj+"_"+hname,params)
        hists[obj+"_matched_"+hname] = createHist(opt, obj+"_matched_"+hname,params)
        hists["gen"+obj+"_matched_"+hname] = createHist(opt, "gen"+obj+"_matched_"+hname,params)
        
    cutList = ["nocut"]+params["etaSlices"]+params["ptSlices"]
    print "list for plots:",cutList

    for cut in cutList:
        hname = "multiplicity"
        if len(cut)==2:
            hname += "_"+ str(cut[0]) + "to" + str(cut[1])
        elif len(cut)==1:
            hname += "_"+ str(cut[0]) + "up" 
        hname = hname.replace('.', 'p')
        hists[obj+"_"+hname] = createHist(opt, obj+"_"+hname,params)

    for cut in ["nocut"]+params["etaSlices"]:
        for hname in ["matchefficiency_to_pt", "ptresponse_to_pt", "fakerate_to_pt"]:
            if len(cut)==2:
                hname += "_"+ str(cut[0]) + "to" + str(cut[1])
            elif len(cut)==1:
                hname += "_"+ str(cut[0]) + "up"
            hname = hname.replace('.', 'p')
            hists[obj+"_"+hname] = create2dHist(obj+"_"+hname,params)

    for cut in ["nocut"]+params["ptSlices"]:
        for hname in ["matchefficiency_to_eta", "ptresponse_to_eta", "fakerate_to_eta"]:
            if len(cut)==2:
                hname += "_"+ str(cut[0]) + "to" + str(cut[1])
            elif len(cut)==1:
                hname += "_"+ str(cut[0]) + "up"
            hname = hname.replace('.', 'p')
            hists[obj+"_"+hname] = create2dHist(obj+"_"+hname,params)


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
        #tot_genjetAK8 += len(event.genjetsAK8())
        #tot_jetAK8 += len(event.jetsAK8())

	if obj=="jet":
            recoobjs = event.jets()
            genobjs = event.genjets()
	elif obj == "photon": 
            recoobjs = event.gammas()
            genobjs = event.genparticles()
        elif obj == "electron":
            recoobjs = event.electrons()
            genobjs = event.genparticles()
        elif obj == "muon":
            recoobjs = event.muons()
            genobjs = event.genparticles()
        else: 
            print 'Physics object not recognized! Choose jet, photon, electron, or muon.'            

        if len(recoobjs) < 1 or len(genobjs) <1 : continue

        multiplicity = {}
        for cut in cutList:
            cutname = cut
            if len(cut)==2:
                cutname = str(cut[0]) + "to" + str(cut[1])
            elif len(cut)==1:
                cutname = str(cut[0]) + "up"
            cutname = cutname.replace('.','p')
            multiplicity[cutname] = 0


	p_tvectors = []

        ## Loop over reco objects
        for p in recoobjs:
            if abs(p.eta()) > 5 or p.pt() < params["ptMin"] : continue

            ## Fill reco object hists
            hists[obj+"_pt"].Fill(p.pt())
            hists[obj+"_eta"].Fill(p.eta())
            hists[obj+"_phi"].Fill(p.phi())
            hists[obj+"_mass"].Fill(p.mass())

            if obj == "jet" and p.pt() < 25 : continue  # for jets
            multiplicity["nocut"] += 1
            for cut in params["etaSlices"]:
                if len(cut) ==2:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = cutname.replace('.','p')
                    if cut[0] < abs(p.eta()) <= cut[1] : multiplicity[cutname] += 1
                elif len(cut) == 1:
                    cutname = str(cut[0]) + "up"
                    cutname = cutname.replace('.','p')
                    if abs(p.eta()) > cut[0] : multiplicity[cutname] += 1

            for cut in params["ptSlices"]:
                if len(cut) ==2:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = cutname.replace('.','p')
                    if  cut[0] <= p.pt() < cut[1]: multiplicity[cutname] += 1
                elif len(cut) == 1:
                    cutname = str(cut[0]) + "up"
                    cutname = cutname.replace('.','p')
                    if p.pt() >= cut[0]: multiplicity[cutname] += 1

          ## STORE all reco objects passing basic thresholds (25 hardcoded for jets)
          p_vec = ROOT.TVector3()
          p_vec.SetPtEtaPhi(p.pt(), p.eta(), p.phi())
          p_tvectors.append(p_vec)

        
        ### LOOP over the GEN objects
        for g in genobjs:

            ## Cuts on the gen object
            if obj in pdgid:
                if g.pid() != pdgid[obj]: continue  # check genparticle pid  
            if abs(g.eta()) > 5 or g.pt() < params["ptMin"] : continue

            ## Fill gen object hists
            hists["gen"+obj+"_pt"].Fill(g.pt())
            hists["gen"+obj+"_eta"].Fill(g.eta())
            hists["gen"+obj+"_phi"].Fill(g.phi())
            hists["gen"+obj+"_mass"].Fill(g.mass())

            g_vec = ROOT.TVector3()
            g_vec.SetPtEtaPhi(g.pt(), g.eta(), g.phi())
            match = 0
            matchindex = -1
            minDR = 999

            ## Find matched reco object with minimum DR
            for ivec in range(0, len(p_tvectors)):
                deltaR = g_vec.DeltaR(p_tvectors[ivec])
                if deltaR < params["dR"] and deltaR < minDR and ( 1./params["ptRatio"] < p_tvectors[ivec].Pt()/g.pt() < params["ptRatio"]) : # matched
                    minDR = deltaR
                    match = 1
                    matchindex = ivec

            ## Fill matched reco and gen hists
            hists[obj+"_matched_pt"].Fill(p_tvectors[matchindex].Pt())
            hists[obj+"_matched_eta"].Fill(p_tvectors[matchindex].Eta())
            hists[obj+"_matched_phi"].Fill(p_tvectors[matchindex].Phi())
            hists[obj+"_matched_mass"].Fill(p_tvectors[matchindex].M()) 
            hists["gen"+obj+"_matched_pt"].Fill(g.pt())
            hists["gen"+obj+"_matched_eta"].Fill(g.eta())
            hists["gen"+obj+"_matched_phi"].Fill(g.phi())
            hists["gen"+obj+"_matched_mass"].Fill(g.mass())
	
            ## Fill ptresponse hists
            hists[obj+"_ptresponse_to_eta"].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
            hists[obj+"_ptresponse_to_pt"].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())
            for cut in params["ptSlices"]:
                if len(cut) ==2:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = cutname.replace('.','p')
                    if cut[0] <= g.pt() < cut[1]: hists[obj+"_ptresponse_to_eta_"+cutname].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                elif len(cut) == 1:
                    cutname = str(cut[0]) + "up"
                    cutname = cutname.replace('.','p')
                    if g.pt() >= cut[0] : hists[obj+"_ptresponse_to_eta_"+cutname].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())

            for cut in params["etaSlices"]:
                if len(cut) ==2:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = cutname.replace('.','p')
                    if cut[0] < abs(g.eta()) <= cut[1]: hists[obj+"_ptresponse_to_pt_"+cutname].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())
                elif len(cut) == 1:
                    cutname = str(cut[0]) + "up"
                    cutname = cutname.replace('.','p')
                    if abs(g.eta()) > cut[0] : hists[obj+"_ptresponse_to_pt_"+cutname].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())


            ## fill match status into efficiency TProfiles
            hists[obj+"_matchefficiency_to_eta"].Fill(g.eta(), match)
            hists[obj+"_matchefficiency_to_pt"].Fill(g.pt(), match)
            for cut in params["ptSlices"]:
                if len(cut) ==2:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = cutname.replace('.','p')
                    if cut[0] <= g.pt() < cut[1]: hists[obj+"_matchefficiency_to_eta_" + cutname].Fill(g.eta(), match)
                elif len(cut) == 1:
                    cutname = str(cut[0]) + "up"
                    cutname = cutname.replace('.','p')
                    if g.pt() >= cut[0] : hists[obj+"_matchefficiency_to_eta_" +cutname].Fill(g.eta(), match)

            for cut in params["etaSlices"]:
                if len(cut) ==2:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = cutname.replace('.','p')
                    if cut[0] < abs(g.eta()) <= cut[1]: hists[obj+"_matchefficiency_to_pt_"+cutname].Fill(g.pt(), match)
                elif len(cut) == 1:
                    cutname = str(cut[0]) + "up"
                    cutname = cutname.replace('.','p')          
                    if abs(g.eta()) > cut[0] : hists[obj+"_matchefficiency_to_pt_"+cutname].Fill(g.pt(), match)

            ## Work with the matched reco object if it exists:
            if matchindex > -1:

                ## fill 0 into fakerate TProfiles for the matched reco object
                hists[obj+"_fakerate_to_eta"].Fill(p_tvectors[matchindex].Eta(), 0)
                hists[obj+"_fakerate_to_pt"].Fill(p_tvectors[matchindex].Pt(), 0)
                for cut in params["ptSlices"]:
                    if len(cut) ==2:
                        cutname = str(cut[0]) + "to" + str(cut[1])
                        cutname = cutname.replace('.','p')
                        if cut[0] <= p_tvectors[matchindex].Pt() < cut[1]: hists[obj+"_fakerate_to_eta_" + cutname].Fill(p_tvectors[matchindex].Eta(), 0)
                    elif len(cut) == 1:
                        cutname = str(cut[0]) + "up"
                        cutname = cutname.replace('.','p')
                        if p_tvectors[matchindex].Pt() >= cut[0] : hists[obj+"_fakerate_to_eta_" +cutname].Fill(p_tvectors[matchindex].Eta(), 0)

                for cut in params["etaSlices"]:
                    if len(cut) ==2:
                        cutname = str(cut[0]) + "to" + str(cut[1])
                        cutname = cutname.replace('.','p')
                        if cut[0] < abs(p_tvectors[matchindex].Eta()) <= cut[1]: hists[obj+"_fakerate_to_pt_"+cutname].Fill(p_tvectors[matchindex].Pt(), 0)
                    elif len(cut) == 1:
                        cutname = str(cut[0]) + "up"
                        cutname = cutname.replace('.','p')          
                        if abs(p_tvectors[matchindex].Eta()) > cut[0] : hists[obj+"_fakerate_to_pt_"+cutname].Fill(p_tvectors[matchindex].Pt(), 0)

                ## remove this matched reco object so later gen objects can't be matched to it
                p_tvectors.pop(matchindex)

        ## All the matched reco objects should have been removed from p_tvectors, fill 1 in fakerate for others
        for p in p_tvectors:
            hists[obj+"_fakerate_to_eta"].Fill(p_tvectors[matchindex].Eta(), 1)
            hists[obj+"_fakerate_to_pt"].Fill(p_tvectors[matchindex].Pt(), 1)
            for cut in params["ptSlices"]:
                if len(cut) ==2:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = cutname.replace('.','p')
                    if cut[0] <= p_tvectors[matchindex].Pt() < cut[1]: hists[obj+"_fakerate_to_eta_" + cutname].Fill(p_tvectors[matchindex].Eta(), 1)
                elif len(cut) == 1:
                    cutname = str(cut[0]) + "up"
                    cutname = cutname.replace('.','p')
                    if p_tvectors[matchindex].Pt() >= cut[0] : hists[obj+"_fakerate_to_eta_" +cutname].Fill(p_tvectors[matchindex].Eta(), 1)

            for cut in params["etaSlices"]:
                if len(cut) ==2:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = cutname.replace('.','p')
                    if cut[0] < abs(p_tvectors[matchindex].Eta()) <= cut[1]: hists[obj+"_fakerate_to_pt_"+cutname].Fill(p_tvectors[matchindex].Pt(), 1)
                elif len(cut) == 1:
                    cutname = str(cut[0]) + "up"
                    cutname = cutname.replace('.','p')          
                    if abs(p_tvectors[matchindex].Eta()) > cut[0] : hists[obj+"_fakerate_to_pt_"+cutname].Fill(p_tvectors[matchindex].Pt(), 1)


        ## for each evt
        for cut in cutList:
            cutname = cut
            hname = "multiplicity" # cut == "nocut"
            if len(cut)==2:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = cutname.replace('.','p')
                hname += "_"+ cutname
            elif len(cut)==1:
                cutname = str(cut[0]) + "up"
                cutname = cutname.replace('.','p')
                hname += "_"+ cutname

            hists[obj+"_" + hname].Fill(multiplicity[cutname])

    ## Write all histograms
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
