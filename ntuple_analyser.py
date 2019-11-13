#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import optparse
import itertools

# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple

pdgid = {
    "photon": 22,
    "electron": 11,
    "muon": 13,
    
}
def createHist(opt, varname, params):
    if "pt" in varname:
        h = ROOT.TH1D(varname, "", 50, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("p_{T} [GeV]")
        h.GetYaxis().SetTitle("N")
    if "eta" in varname:
        h = ROOT.TH1D(varname, "", 50, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("#eta")
        h.GetYaxis().SetTitle("N")
    if "phi" in varname:
        h = ROOT.TH1D(varname, "", 50, params["plotPhiRange"][0], params["plotPhiRange"][1])
        h.GetXaxis().SetTitle("#phi")
        h.GetYaxis().SetTitle("N")
    if "mass" in varname:
        h = ROOT.TH1D(varname, "", 50, params["plotMassRange"][0], params["plotMassRange"][1])
        h.GetXaxis().SetTitle("mass [GeV]")
        h.GetYaxis().SetTitle("N")
    if "idpass" in varname:
        h = ROOT.TH1D(varname, "", 20, 0, 20)
        h.GetXaxis().SetTitle("id pass")
        h.GetYaxis().SetTitle("N")
    if "multi" in varname:
        if "full" in opt.outFile:
            h = ROOT.TH1D(varname, "", params["plotNObjRange_Full"][1], params["plotNObjRange_Full"][0], params["plotNObjRange_Full"][1]) 
        else:
            h = ROOT.TH1D(varname, "", params["plotNObjRange_Delp"][1], params["plotNObjRange_Delp"][0], params["plotNObjRange_Delp"][1])
        h.GetXaxis().SetTitle("multiplicity")
        h.GetYaxis().SetTitle("Events")

        
    h.Sumw2()

    return h

def create2dHist(varname, params):
    if "to_pt" in varname and "response" in varname:
        h = ROOT.TProfile(varname, "", 50, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("gen p_{T} [GeV]")
        h.GetYaxis().SetTitle("Reco_pt/Gen_pt")
    if "to_eta" in varname and "response" in varname:
        h = ROOT.TProfile(varname, "", 50, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("gen #eta")
        h.GetYaxis().SetTitle("Reco_pt/Gen_pt")
    if "to_pt" in varname and "efficiency" in varname:
        h = ROOT.TProfile(varname, "", 50, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("gen p_{T} [GeV]")
        h.GetYaxis().SetTitle("gen object matching efficiency")
    if "to_eta" in varname and "efficiency" in varname:
        h = ROOT.TProfile(varname, "", 50, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("gen #eta")
        h.GetYaxis().SetTitle("gen object matching efficiency")
    if "to_pt" in varname and "fakerate" in varname:
        h = ROOT.TProfile(varname, "", 50, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("reco p_{T} [GeV]")
        h.GetYaxis().SetTitle("reco object fakerate")
    if "to_eta" in varname and "fakerate" in varname:
        h = ROOT.TProfile(varname, "", 50, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("reco #eta")
        h.GetYaxis().SetTitle("reco object fakerate")


    h.Sumw2()

    return h

def create2Dmap(varname, params):
    if "efficiency" in varname:
        h = ROOT.TProfile2D(varname, "", 10, params["plotPtRange"][0], params["plotPtRange"][1], 10, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("gen p_{T} [GeV]")
        h.GetYaxis().SetTitle("gen #eta")
    if "fakerate" in varname:
        h = ROOT.TProfile2D(varname, "", 10, params["plotPtRange"][0], params["plotPtRange"][1], 10, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("reco p_{T} [GeV]")
        h.GetYaxis().SetTitle("reco #eta")
        
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
                      default=500000,
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

    ## Set plotting parameters according to physics object
    params = {}
    outputF = ROOT.TFile(opt.outFile, "RECREATE")
    obj = opt.physobject
    if obj=="jet":
        params = {
            "dR": 0.2,
            "ptRatio": 2.0,
            "ptMin": 20,
            "etaSlices": [[0, 1.3], [1.3, 2.5], [2.5, 3], [3, 1e5] ], ## use 1e5 as "Inf"
            "ptSlices": [[20, 50], [50, 100], [100, 200], [200, 400], [400, 1e5] ],
            "plotPtRange": [0, 1500],
            "plotEtaRange": [-5, 5],
            "plotPhiRange": [-5, 5],
            "plotMassRange": [0, 500],
            "plotNObjRange_Delp": [0, 20],
            "plotNObjRange_Full": [0, 50],
            "ids": [],
            "idvals": [],
            }
    elif obj == "photon": 
        params = {
            "dR": 0.2,
            "ptRatio": 100.0,
            "ptMin": 8,
            "etaSlices": [[0, 1.5], [1.5, 3]],
            "ptSlices": [[8, 20], [20, 50], [50, 100], [100, 1e5]],
            "plotPtRange": [0, 250],
            "plotEtaRange": [-4, 4],
            "plotPhiRange": [-4, 4],
            "plotMassRange": [-1, 1],
            "plotNObjRange_Delp": [0, 4],
            "plotNObjRange_Full": [0, 4],
            "ids": ["incl","loose","tight"],
            "idvals": [-9, 0, 3],
            }
    elif obj == "electron" or obj == "muon":
        params = {
            "dR": 0.2,
            "ptRatio": 2.0,
            "ptMin": 20,
            "etaSlices": [[0, 1.3], [1.3, 2.5], [2.5, 3], [3, 1e5] ],
            "ptSlices": [[20, 50], [50, 100], [100, 200], [200, 400], [400, 1e5] ],
            "plotPtRange": [0, 1500],
            "plotEtaRange": [-5, 5],
            "plotPhiRange": [-5, 5],
            "plotMassRange": [0, 500],
            "plotNObjRange_Delp": [0, 20],
            "plotNObjRange_Full": [0, 50],
            "ids": ["loose","tight"],
            "idvals": [0, 3],
            }                
    else: 
        print 'Physics object not recognized! Choose jet, photon, electron, or muon.'            
        exit()

    ## BOOK HISTOGRAMS
    hists = {} 
    hnames = ["pt", "eta", "phi", "mass", "idpass"]
    for hname in hnames:
        hists["gen"+obj+"_"+hname] = createHist(opt, "gen"+obj+"_"+hname,params)
        hists["gen"+obj+"_matched_"+hname] = createHist(opt, "gen"+obj+"_matched_"+hname,params)
    ## add IDs for reco hists
    if len(params["ids"]) > 0: hnames = ['_'.join (strlist) for strlist in list(itertools.product(hnames,params["ids"]))]
    for hname in hnames:
        hists[obj+"_"+hname] = createHist(opt, obj+"_"+hname,params)
        hists[obj+"_matched_"+hname] = createHist(opt, obj+"_matched_"+hname,params)
        
    cutList = ["nocut"]+params["etaSlices"]+params["ptSlices"]

    for cut in cutList:
        hnames = ["multiplicity"]
        if len(params["ids"]) > 0: hnames = ['_'.join (strlist) for strlist in list(itertools.product(hnames,params["ids"]))]
        for hname in hnames:
            hname += "_"+ str(cut[0]) + "to" + str(cut[1])
            hname = ((hname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
            hists[obj+"_"+hname] = createHist(opt, obj+"_"+hname,params)

    for cut in ["nocut"]+params["etaSlices"]:
        hnames = ["matchefficiency_to_pt", "ptresponse_to_pt", "fakerate_to_pt"]
        if len(params["ids"]) > 0: hnames = ['_'.join (strlist) for strlist in list(itertools.product(hnames,params["ids"]))]
        for hname in hnames:
            hname += "_"+ str(cut[0]) + "to" + str(cut[1])
            hname = ((hname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
            hists[obj+"_"+hname] = create2dHist(obj+"_"+hname,params)

    for cut in ["nocut"]+params["ptSlices"]:
        print 'cut = ',cut
        hnames = ["matchefficiency_to_eta", "ptresponse_to_eta", "fakerate_to_eta"]
        if len(params["ids"]) > 0: hnames = ['_'.join (strlist) for strlist in list(itertools.product(hnames,params["ids"]))]
        for hname in hnames:
            hname += "_"+ str(cut[0]) + "to" + str(cut[1])
            hname = ((hname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
            hists[obj+"_"+hname] = create2dHist(obj+"_"+hname,params)

    hnames = ["efficiency2D", "fakerate2D"]
    if len(params["ids"]) > 0: hnames = ['_'.join (strlist) for strlist in list(itertools.product(hnames,params["ids"]))] 
    for hname in hnames:
        hists[obj+"_"+hname] = create2Dmap(obj+"_"+hname,params)
   

    ## LOOP over events
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents %1000) == 0 :
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

        ## Set the reco and generated object collections
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

        ## Initialize multiplicity counters
        multiplicity = {}
        for cut in cutList:
            cutname = str(cut[0]) + "to" + str(cut[1])
            cutname = ((cutname.replace('.','p')).replace('100000p0','Inf')).replace('ntoo','nocut')
            if len(params["ids"]) > 0:
                for qual in params["ids"]: multiplicity[cutname+"_"+qual] = 0                    
            else: multiplicity[cutname] = 0

	p_tvectors = []
        p_idpass = []

        ## Loop over reco objects
        for p in recoobjs:
            if abs(p.eta()) > 5 or p.pt() < params["ptMin"] : continue

            ## Fill reco object hists
            if len(params["ids"]) > 0:
                for iqual in range(len(params["ids"])):
                    if p.idpass() > params["idvals"][iqual]:
                        hists[obj+"_pt_"+params["ids"][iqual]].Fill(p.pt())
                        hists[obj+"_eta_"+params["ids"][iqual]].Fill(p.eta())
                        hists[obj+"_phi_"+params["ids"][iqual]].Fill(p.phi())
                        hists[obj+"_mass_"+params["ids"][iqual]].Fill(p.mass())
                        hists[obj+"_idpass_"+params["ids"][iqual]].Fill(p.idpass())
            else:
                hists[obj+"_pt"].Fill(p.pt())
                hists[obj+"_eta"].Fill(p.eta())
                hists[obj+"_phi"].Fill(p.phi())
                hists[obj+"_mass"].Fill(p.mass())
                hists[obj+"_idpass"].Fill(p.idpass())


            if obj == "jet" and p.pt() < 25 : continue  # for jets
            
            ## Increment multiplicity counters
            if len(params["ids"]) > 0:
                for iqual in range(len(params["ids"])):
                    if p.idpass() > params["idvals"][iqual]: multiplicity["nocut_"+params["ids"][iqual]] += 1
            else: multiplicity["nocut"] += 1
            for cut in params["etaSlices"]:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                if cut[0] < abs(p.eta()) <= cut[1] : 
                    if len(params["ids"]) > 0:
                        for iqual in range(len(params["ids"])): 
                            if p.idpass() > params["idvals"][iqual]: multiplicity[cutname+"_"+params["ids"][iqual]] += 1
                    else: multiplicity[cutname] += 1

            for cut in params["ptSlices"]:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                if  cut[0] <= p.pt() < cut[1]: 
                    if len(params["ids"]) > 0:
                        for iqual in range(len(params["ids"])): 
                            if p.idpass() > params["idvals"][iqual]: multiplicity[cutname+"_"+params["ids"][iqual]] += 1
                    else: multiplicity[cutname] += 1

            ## STORE all reco objects passing basic thresholds (25 hardcoded for jets)
            p_vec = ROOT.TVector3()
            p_vec.SetPtEtaPhi(p.pt(), p.eta(), p.phi())
            p_tvectors.append(p_vec)
            p_idpass.append(p.idpass())
            
        ## LOOP over the GEN objects
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
            minDRindex = -1

            ## Find matched reco object with minimum DR
            for ivec in range(0, len(p_tvectors)):
                deltaR = g_vec.DeltaR(p_tvectors[ivec])
                if deltaR < minDR:
                    minDR = deltaR
                    minDRindex = ivec

            if minDR < params["dR"] and ( 1./params["ptRatio"] < p_tvectors[ivec].Pt()/g.pt() < params["ptRatio"]) : # matched
                match = 1
                matchindex = minDRindex

            ## Work with only matched pairs first:
            if match == 1:
                
                ## Fill matched reco and gen hists
                if len(params["ids"]) > 0:
                    for iqual in range(len(params["ids"])):
                        if p_idpass[matchindex] > params["idvals"][iqual]:
                            hists[obj+"_matched_pt_"+params["ids"][iqual]].Fill(p_tvectors[matchindex].pt())
                            hists[obj+"_matched_eta_"+params["ids"][iqual]].Fill(p_tvectors[matchindex].eta())
                            hists[obj+"_matched_phi_"+params["ids"][iqual]].Fill(p_tvectors[matchindex].phi())
                            hists[obj+"_matched_mass_"+params["ids"][iqual]].Fill(p_tvectors[matchindex].mass())
                else:
                    hists[obj+"_matched_pt"].Fill(p_tvectors[matchindex].Pt())
                    hists[obj+"_matched_eta"].Fill(p_tvectors[matchindex].Eta())
                    hists[obj+"_matched_phi"].Fill(p_tvectors[matchindex].Phi())
                    hists[obj+"_matched_mass"].Fill(p_tvectors[matchindex].Mag()) 
                hists["gen"+obj+"_matched_pt"].Fill(g.pt())
                hists["gen"+obj+"_matched_eta"].Fill(g.eta())
                hists["gen"+obj+"_matched_phi"].Fill(g.phi())
                hists["gen"+obj+"_matched_mass"].Fill(g.mass())
	
                ## Fill ptresponse hists                
                if len(params["ids"]) > 0:
                    for iqual in range(len(params["ids"])):
                        if p_idpass[matchindex] > params["idvals"][iqual]:
                            hists[obj+"_ptresponse_to_eta_"+params["ids"][iqual]].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                            hists[obj+"_ptresponse_to_pt_"+params["ids"][iqual]].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())
                else:
                    hists[obj+"_ptresponse_to_eta"].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                    hists[obj+"_ptresponse_to_pt"].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())

                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] <= g.pt() < cut[1]: 
                        if len(params["ids"]) > 0:
                            for iqual in range(len(params["ids"])):
                                if p_idpass[matchindex] > params["idvals"][iqual]: 
                                    hists[obj+"_ptresponse_to_eta_"+params["ids"][iqual]+"_"+cutname].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                        else: hists[obj+"_ptresponse_to_eta_"+cutname].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                
                for cut in params["etaSlices"]:
                        cutname = str(cut[0]) + "to" + str(cut[1])
                        cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                        if cut[0] < abs(g.eta()) <= cut[1]: 
                            if len(params["ids"]) > 0:
                                for iqual in range(len(params["ids"])):
                                    if p_idpass[matchindex] > params["idvals"][iqual]:
                                        hists[obj+"_ptresponse_to_pt_"+params["ids"][iqual]+"_"+cutname].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())
                            else: hists[obj+"_ptresponse_to_pt_"+cutname].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())
                
                ## fill 0 into fakerate TProfiles for the matched reco object
                ## fakerate: denominator = all reco objects with given quality (0's here for matched, 1's later for unmatched)
                ##           numerator = all unmatched reco objects with given quality (1's later for unmatched)
                if len(params["ids"]) > 0:
                    for iqual in range(len(params["ids"])):
                        if p_idpass[matchindex] > params["idvals"][iqual]:
                            hists[obj+"_fakerate_to_eta_"+params["ids"][iqual]].Fill(p_tvectors[matchindex].Eta(), 0)
                            hists[obj+"_fakerate_to_pt_"+params["ids"][iqual]].Fill(p_tvectors[matchindex].Pt(), 0)
                            hists[obj+"_fakerate2D_"+params["ids"][iqual]].Fill(p_tvectors[matchindex].Pt(),p_tvectors[matchindex].Eta(),0)
                else:
                    hists[obj+"_fakerate_to_eta"].Fill(p_tvectors[matchindex].Eta(), 0)
                    hists[obj+"_fakerate_to_pt"].Fill(p_tvectors[matchindex].Pt(), 0)
                    hists[obj+"_fakerate2D"].Fill(p_tvectors[matchindex].Pt(),p_tvectors[matchindex].Eta(),0)
                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] <= p_tvectors[matchindex].Pt() < cut[1]: 
                        if len(params["ids"]) > 0:
                            for iqual in range(len(params["ids"])):
                                if p_idpass[matchindex] > params["idvals"][iqual]:
                                    hists[obj+"_fakerate_to_eta_"+params["ids"][iqual]+"_" + cutname].Fill(p_tvectors[matchindex].Eta(), 0)
                        else: hists[obj+"_fakerate_to_eta_" + cutname].Fill(p_tvectors[matchindex].Eta(), 0)

                for cut in params["etaSlices"]:
                        cutname = str(cut[0]) + "to" + str(cut[1])
                        cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                        if cut[0] < abs(p_tvectors[matchindex].Eta()) <= cut[1]: 
                            if len(params["ids"]) > 0:
                                for iqual in range(len(params["ids"])):
                                    if p_idpass[matchindex] > params["idvals"][iqual]:
                                        hists[obj+"_fakerate_to_pt_"+params["ids"][iqual]+"_"+cutname].Fill(p_tvectors[matchindex].Pt(), 0)
                            else: hists[obj+"_fakerate_to_pt_"+cutname].Fill(p_tvectors[matchindex].Pt(), 0)

                ## end of matched object stuff

            ## working with matched AND unmatched: fill match status into efficiency TProfiles
            ## efficiency: denominator = all gen objects (0's for unmatched, 0's for matched and reco obj fails quality)
            ##             numerator = all gen objects matched to reco object of given quality (1's for matched and reco obj passes quality) 
            if len(params["ids"]) > 0:
                for iqual in range(len(params["ids"])):                    
                    try: idpass = (p_idpass[matchindex] > params["idvals"][iqual])
                    except IndexError: idpass = False
                    hists[obj+"_matchefficiency_to_eta_"+params["ids"][iqual]].Fill(g.eta(), match*idpass) #0 if either fails, 1 if both
                    hists[obj+"_matchefficiency_to_pt_"+params["ids"][iqual]].Fill(g.pt(), match*idpass)
                    hists[obj+"_efficiency2D_"+params["ids"][iqual]].Fill(g.pt(),g.eta(), match*idpass)
            else:
                hists[obj+"_matchefficiency_to_eta"].Fill(g.eta(), match)
                hists[obj+"_matchefficiency_to_pt"].Fill(g.pt(), match)
                hists[obj+"_efficiency2D"].Fill(g.pt(),g.eta(), match)
            for cut in params["ptSlices"]:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                if cut[0] <= g.pt() < cut[1]: 
                    if len(params["ids"]) > 0:
                        for iqual in range(len(params["ids"])):
                            try: idpass = (p_idpass[matchindex] > params["idvals"][iqual])
                            except IndexError: idpass = False
                            hists[obj+"_matchefficiency_to_eta_"+params["ids"][iqual]+"_" + cutname].Fill(g.eta(), match*idpass)
                    else: hists[obj+"_matchefficiency_to_eta_" + cutname].Fill(g.eta(), match)

            for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] < abs(g.eta()) <= cut[1]: 
                        if len(params["ids"]) > 0:
                            for iqual in range(len(params["ids"])):
                                try: idpass = (p_idpass[matchindex] > params["idvals"][iqual])
                                except IndexError: idpass = False
                                hists[obj+"_matchefficiency_to_pt_"+params["ids"][iqual]+"_"+cutname].Fill(g.pt(), match*idpass)
                        else: hists[obj+"_matchefficiency_to_pt_"+cutname].Fill(g.pt(), match)

            ## remove this matched reco object so later gen objects can't be matched to it
            if matchindex > -1:
                p_tvectors.pop(matchindex)
                p_idpass.pop(matchindex)

            ## end of gen object loop

        ## All the matched reco objects should have been removed from p_tvectors and p_idpass, fill 1 in fakerate for others
        #print "now filling the fakes:",len(p_tvectors)
        for ip in range(len(p_tvectors)):
            if len(params["ids"]) > 0:
                for iqual in range(len(params["ids"])):
                    if p_idpass[ip] > params["idvals"][iqual]:
                        hists[obj+"_fakerate_to_eta_"+params["ids"][iqual]].Fill(p_tvectors[ip].Eta(), 1)
                        hists[obj+"_fakerate_to_pt_"+params["ids"][iqual]].Fill(p_tvectors[ip].Pt(), 1)
                        hists[obj+"_fakerate2D_"+params["ids"][iqual]].Fill(p_tvectors[ip].Pt(),p_tvectors[ip].Eta(),1)
            else:
                hists[obj+"_fakerate_to_eta"].Fill(p_tvectors[ip].Eta(), 1)
                hists[obj+"_fakerate_to_pt"].Fill(p_tvectors[ip].Pt(), 1)
                hists[obj+"_fakerate2D"].Fill(p_tvectors[ip].Pt(),p_tvectors[ip].Eta(),1)
            for cut in params["ptSlices"]:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                if cut[0] <= p_tvectors[ip].Pt() < cut[1]: 
                    if len(params["ids"]) > 0:
                        for iqual in range(len(params["ids"])):
                            if p_idpass[ip] > params["idvals"][iqual]:
                                hists[obj+"_fakerate_to_eta_"+params["ids"][iqual]+"_" + cutname].Fill(p_tvectors[ip].Eta(), 1)
                    else: hists[obj+"_fakerate_to_eta_" + cutname].Fill(p_tvectors[ip].Eta(), 1)

            for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] < abs(p_tvectors[ip].Eta()) <= cut[1]: 
                        if len(params["ids"]) > 0:
                            for iqual in range(len(params["ids"])):
                                if p_idpass[ip] > params["idvals"][iqual]:
                                    hists[obj+"_fakerate_to_pt_"+params["ids"][iqual]+"_"+cutname].Fill(p_tvectors[ip].Pt(), 1)
                        else: hists[obj+"_fakerate_to_pt_"+cutname].Fill(p_tvectors[ip].Pt(), 1)

        ## for each evt
        for cut in cutList:
            hname = "multiplicity"
            cutname = str(cut[0]) + "to" + str(cut[1])
            cutname = ((cutname.replace('.','p')).replace('100000p0','Inf')).replace('ntoo','nocut')
            if len(params["ids"]) > 0: 
                for qual in params["ids"]:
                    hname = "multiplicity_"+qual
                    if cutname != "nocut": hname += "_"+cutname                  
                    hists[obj+"_" + hname].Fill(multiplicity[cutname+"_"+qual])
            else: 
                if cutname != "nocut": hname += "_"+ cutname
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

