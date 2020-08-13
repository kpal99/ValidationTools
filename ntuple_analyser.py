#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import optparse
import itertools
from array import array

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

def create2dHist(varname, params, title):
    if "to_pt" in varname and "response" in varname:
        title = title.replace(")*#varepsilon(#","+")
        title = title.replace("#varepsilon","response")
        h = ROOT.TProfile(varname, title, 50, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("gen p_{T} [GeV]")
        h.GetYaxis().SetTitle("Reco_pt/Gen_pt")
    if "to_eta" in varname and "response" in varname:
        title = title.replace(")*#varepsilon(#","+")
        title = title.replace("#varepsilon","response")
        h = ROOT.TProfile(varname, title, 50, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("gen #eta")
        h.GetYaxis().SetTitle("Reco_pt/Gen_pt")
    if "to_pt" in varname and "efficiency" in varname:
        h = ROOT.TProfile(varname, title, 50, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("gen p_{T} [GeV]")
        h.GetYaxis().SetTitle("gen object matching efficiency")
    if "to_eta" in varname and "efficiency" in varname:
        h = ROOT.TProfile(varname, title, 50, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("gen #eta")
        h.GetYaxis().SetTitle("gen object matching efficiency")
    if "to_pt" in varname and "fakerate" in varname:
        title = title.replace(")*#varepsilon(#","+")
        title = title.replace("#varepsilon","fakerate")
        h = ROOT.TProfile(varname, title, 50, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("reco p_{T} [GeV]")
        h.GetYaxis().SetTitle("reco object fakerate")
    if "to_eta" in varname and "fakerate" in varname:
        title = title.replace(")*#varepsilon(#","+")
        title = title.replace("#varepsilon","fakerate")
        h = ROOT.TProfile(varname, title, 50, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("reco #eta")
        h.GetYaxis().SetTitle("reco object fakerate")


    h.Sumw2()

    return h

def create2Dmap(varname, params, title):
    
    ## use the slices to build a list of bin edges
    ptbins = [item[0] for item in params["ptSlices"]]
    etabins = [item[0] for item in params["etaSlices"]]
    ptbins.append(params["ptSlices"][-1][1])
    etabins.append(params["etaSlices"][-1][1])
    ## set more realistic caps
    if ptbins[-1] > 5e4: ptbins[-1] = ptbins[-2]*2. ## probably somewhere in 200 -- 4000?
    if etabins[-1] > 5e4: etabins[-1] = 5. 

    ptbinsext = []
    for iedge in range(0,len(ptbins)-1):
        binwidth = ptbins[iedge+1]-ptbins[iedge]
        for j in range(0,params["sliceSplit"]): # 0, 1, 2 if sliceSplit = 3
            ptbinsext.append(ptbins[iedge] + int(j*binwidth/params["sliceSplit"])) # low, low+0*width/3, low+width/3, low+2*width/3
    ptbinsext.append(ptbins[-1])

    etabinsext = []
    for iedge in range(0,len(etabins)-1):
        binwidth = etabins[iedge+1]-etabins[iedge]
        for j in range(0,params["sliceSplit"]): # 0, 1, 2 if sliceSplit = 3
            etabinsext.append(etabins[iedge] + int(j*binwidth/params["sliceSplit"])) # low, low+0*width/3, low+width/3, low+2*width/3
    etabinsext.append(etabins[-1])

    ## arrays for ROOT
    xbins = array('d', ptbinsext)
    ybins = array('d', etabinsext)
    if "efficiency" in varname:
        h = ROOT.TProfile2D(varname, title, len(xbins)-1, xbins, len(ybins)-1, ybins)
        h.GetXaxis().SetTitle("gen p_{T} [GeV]")
        h.GetYaxis().SetTitle("gen #eta")
    if "fakerate" in varname:
        title = title.replace(")*#varepsilon(#","+")
        title = title.replace("#varepsilon","fakerate")
        h = ROOT.TProfile2D(varname, title, 10, params["plotPtRange"][0], params["plotPtRange"][1], 10, params["plotEtaRange"][0], params["plotEtaRange"][1])
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
    parser.add_option('--dumptcl',
                      dest='dumptcl',
                      help='use more bins for making tcl file?',
                      action="store_true",
                      default=False)
    (opt, args) = parser.parse_args()


    inFile = opt.inFile
    ntuple = Ntuple(inFile)
    maxEvents = opt.maxEvts
    dumptcl = opt.dumptcl

    tot_nevents = 0
    tot_genpart = 0
    tot_genjet = 0
    tot_electron = 0
    tot_gamma = 0
    tot_muon = 0
    tot_jetchs = 0
    tot_jetpuppi = 0
    tot_tau = 0
    tot_met = 0
    tot_genjetAK8 = 0
    tot_jetAK8 = 0

    ## Set plotting parameters according to physics object
    params = {}
    outputF = ROOT.TFile(opt.outFile, "RECREATE")
    obj = opt.physobject
    if obj=="jet": 
        print "You entered jet as the particle type -- please specify jetchs or jetpuppi"
        exit()
    elif obj=="jetchs" or obj=="jetpuppi":
        params = {
            "dR": 0.2,
            "ptRatio": 2.0,
            "ptMin": 20,
            "etaSlices": [[0, 1.3], [1.3, 2.5], [2.5, 3], [3, 1e5] ], ## use 1e5 as "Inf"
            "ptSlices": [[20, 50], [50, 100], [100, 200], [200, 400], [400, 1e5] ],
            "sliceSplit": 1, # for 2D map, make N divisions of each slice
            "plotPtRange": [0, 1500],
            "plotEtaRange": [-5, 5],
            "plotPhiRange": [-5, 5],
            "plotMassRange": [0, 500],
            "plotNObjRange_Delp": [0, 20],
            "plotNObjRange_Full": [0, 50],
            "ids": [
		## ["nameforplot", numerator idpass threshold, numerator isopass threshold, denominator: 0(all)/1(reco matched)/2(reco+id), "efficiency title"]
                ## NOTE: only efficiency plots get anything with value [3] > 0
                ["reco",-9,-9,0,"#varepsilon(reco)"],                         ## reco (eff, fakerate, response)
                ["looseID",0,-9,0,"#varepsilon(reco)*#varepsilon(looseID)"], ## reco*ID (ID for fakerate)  
                ["tightID",3,-9,0,"#varepsilon(reco)*#varepsilon(tightID)"],
                ["looseIDifReco",0,-9,1,"#varepsilon(looseID)"],
                ["tightIDifReco",3,-9,1,"#varepsilon(tightID)"],      ## IDs on reco-matched gen (eff only)
		], 
            }
        if dumptcl: params["sliceSplit"] = 5
    elif obj == "photon": 
        params = {
            "dR": 0.2,
            "ptRatio": 100.0,
            "ptMin": 8,
            "etaSlices": [[0, 1.5], [1.5, 3]],
            "ptSlices": [[8, 20], [20, 50], [50, 100], [100, 1e5]],
            "sliceSplit": 3,
            "plotPtRange": [0, 250],
            "plotEtaRange": [-4, 4],
            "plotPhiRange": [-4, 4],
            "plotMassRange": [-1, 1],
            "plotNObjRange_Delp": [0, 4],
            "plotNObjRange_Full": [0, 4],
            "ids": [  
                ## ["nameforplot", numerator idpass threshold, numerator isopass threshold, 
                ##  denominator: 0(all)/1(reco matched)/2(reco+id), "x-axis label"]
                ## NOTE: only efficiency plots get anything with value [3] > 0 
                ["reco",-9,-9,0,"#varepsilon(reco)"],                         ## reco (eff, fakerate, response)
                ["looseID",0,-9,0,"#varepsilon(reco)*#varepsilon(looseID)"], ## reco*ID (ID for fakerate)  
                ["tightID",3,-9,0,"#varepsilon(reco)*#varepsilon(tightID)"],
                ["looseIDifReco",0,-9,1,"#varepsilon(looseID)"], 
                ["tightIDifReco",3,-9,1,"#varepsilon(tightID)"],      ## IDs on reco-matched gen (eff only)
                ],
            }
        if dumptcl: params["sliceSplit"] = 5
    elif obj == "electron" or obj == "muon":
        params = {
            "dR": 0.2,
            "ptRatio": 2.0,
            "ptMin": 10,
            "etaSlices": [[0, 1.5], [1.5, 3], [3, 1e5] ],
            "ptSlices": [[10, 20], [20, 50], [50, 100], [100, 1e5] ],
            "sliceSplit": 2,
            "plotPtRange": [0, 250],
            "plotEtaRange": [-5, 5],
            "plotPhiRange": [-5, 5],
            "plotMassRange": [-1, 1],
            "plotNObjRange_Delp": [0, 8],
            "plotNObjRange_Full": [0, 8],
            "ids": [  
                ## ["nameforplot", numerator idpass threshold, numerator isopass threshold, 
                ##  denominator: 0(all)/1(reco matched)/2(reco+id), "efficiency title"]
                ## NOTE: only efficiency plots get anything with value [3] > 0 
                ["reco",-9,-9,0,"#varepsilon(reco)"],                         ## reco (eff, fakerate, response)
                ["looseID",0,-9,0,"#varepsilon(reco)*#varepsilon(looseID)"], ## reco*ID (ID for fakerate)  
                ["tightID",3,-9,0,"#varepsilon(reco)*#varepsilon(tightID)"],
                ["looseISO",-9,0,0,"#varepsilon(reco)*#varepsilon(looseISO)"],   ## reco*ISO (ISO for fakerate) 
                ["tightISO",-9,14,0,"#varepsilon(reco)*#varepsilon(tightISO)"],
                ["looseIDISO",0,0,0,"#varepsilon(reco)*#varepsilon(looseID)*#varepsilon(looseISO)"], ## reco*ID*ISOs (ID+ISO for fakerate)
                ["tightIDISO",3,14,0,"#varepsilon(reco)*#varepsilon(tightID)*#varepsilon(tightISO)"], 
                ["looseIDifReco",0,-9,1,"#varepsilon(looseID)"], 
                ["tightIDifReco",3,-9,1,"#varepsilon(tightID)"],      ## IDs on reco-matched gen (eff only)
                ["looseISOifReco",-9,0,1,"#varepsilon(looseISO)"], 
                ["tightISOifReco",-9,14,1,"#varepsilon(tightISO)"],   ## ISOs on reco-matched gen (eff only) 
                ["looseIDISOifReco",0,0,1,"#varepsilon(looseID)*#varepsilon(looseISO)"], 
                ["tightIDISOifReco",3,14,1,"#varepsilon(tightID)*#varepsilon(tightISO)"], ## ID+ISOs on reco-matched gen (eff only)
                ["looseISOifRecoLooseID",0,0,2,"#varepsilon(looseISO given looseID)"], 
                ["tightISOifRecoLooseID",0,14,2,"#varepsilon(tightISO given looseID)"] ## ISOs on reco+id-matched gen (eff only)
                ], 
            }
        if dumptcl: params["sliceSplit"] = 5                
    else: 
        print 'Physics object not recognized! Choose jetchs, jetpuppi, photon, electron, or muon.'            
        exit()

    ## BOOK HISTOGRAMS
    hists = {} 
    hnames = ["pt", "eta", "phi", "mass", "idpass"]
    for hname in hnames:
        if hname == "idpass": continue
        hists["gen"+obj+"_"+hname] = createHist(opt, "gen"+obj+"_"+hname,params)
        hists["gen"+obj+"_matched_"+hname] = createHist(opt, "gen"+obj+"_matched_"+hname,params)
    ## add IDs for reco hists
    for hname in hnames:
        if len(params["ids"]) == 0:
            hists[obj+"_"+hname] = createHist(opt, obj+"_"+hname,params)
            hists[obj+"_matched_"+hname] = createHist(opt, obj+"_matched_"+hname,params)
        else:
            for quality in params["ids"]:
                if quality[3] > 0: continue
                newname = hname+"_"+quality[0]
                hists[obj+"_"+newname] = createHist(opt, obj+"_"+newname,params)
                hists[obj+"_matched_"+newname] = createHist(opt, obj+"_matched_"+newname,params)
            
    cutList = ["nocut"]+params["etaSlices"]+params["ptSlices"]

    for cut in cutList:
        hname = "multiplicity"
        if len(params["ids"]) == 0:
            hname += "_"+ str(cut[0]) + "to" + str(cut[1])
            hname = ((hname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
            hists[obj+"_"+hname] = createHist(opt, obj+"_"+hname,params)
        else:
            for quality in params["ids"]:
                if quality[3] > 0: continue
                newname = hname+"_"+quality[0]+"_"+ str(cut[0]) + "to" + str(cut[1])
                newname = ((newname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
                hists[obj+"_"+newname] = createHist(opt, obj+"_"+newname,params)

    for cut in ["nocut"]+params["etaSlices"]:
        hnames = ["efficiency_to_pt", "ptresponse_to_pt", "fakerate_to_pt"]
        for hname in hnames:
            if len(params["ids"]) == 0:
                title = "#varepsilon(reco)"
                hname += "_"+ str(cut[0]) + "to" + str(cut[1])
                hname = ((hname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
                hists[obj+"_"+hname] = create2dHist(obj+"_"+hname,params,title)
            else:
                for quality in params["ids"]:
                    if ('ptresponse' in hname or 'fakerate' in hname) and quality[3] > 0: continue
                    newname = hname+"_"+quality[0]+"_"+ str(cut[0]) + "to" + str(cut[1])
                    newname = ((newname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
                    hists[obj+"_"+newname] = create2dHist(obj+"_"+newname,params,quality[4])

    for cut in ["nocut"]+params["ptSlices"]:
        hnames = ["efficiency_to_eta", "ptresponse_to_eta", "fakerate_to_eta"]
        for hname in hnames:
            if len(params["ids"]) == 0:
                title = "#varepsilon(reco)"
                hname += "_"+ str(cut[0]) + "to" + str(cut[1])
                hname = ((hname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
                hists[obj+"_"+hname] = create2dHist(obj+"_"+hname,params,title)
            else:
                for quality in params["ids"]:
                    if ('ptresponse' in hname or 'fakerate' in hname) and quality[3] > 0: continue
                    newname = hname+"_"+quality[0]+"_"+ str(cut[0]) + "to" + str(cut[1])
                    newname = ((newname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
                    hists[obj+"_"+newname] = create2dHist(obj+"_"+newname,params,quality[4])

    hnames = ["efficiency2D", "fakerate2D"]
    for hname in hnames:
        if len(params["ids"]) == 0:
            title = "#varepsilon(reco)"
            hists[obj+"_"+hname] = create2Dmap(obj+"_"+hname,params,title)
        else:
            for quality in params["ids"]:
                if 'fakerate' in hname and quality[3] > 0: continue
                newname = hname+"_"+quality[0]
                hists[obj+"_"+newname] = create2Dmap(obj+"_"+newname,params,quality[4])
   

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
        tot_jetchs += len(event.jetschs())
        tot_jetpuppi += len(event.jetspuppi())
        tot_tau += len(event.taus())
        tot_met += len(event.metspuppi())
        #tot_genjetAK8 += len(event.genjetsAK8())
        #tot_jetAK8 += len(event.jetsAK8())

        ## Set the reco and generated object collections
	if obj=="jetpuppi":
            recoobjs = event.jetspuppi()
            genobjs = event.genjets()
	elif obj=="jetchs":
            recoobjs = event.jetschs()
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
                for quality in params["ids"]:                    
                    if quality[3] == 0: multiplicity[cutname+"_"+quality[0]] = 0                    
            else: multiplicity[cutname] = 0

	p_tvectors = []
        p_idpass = []
        p_isopass = []

        #printgen = False

        ## Loop over reco objects
        for p in recoobjs:
            if abs(p.eta()) > 5 or p.pt() < params["ptMin"] : continue

            ## jets don't have the isopass method
            isopass = -1
            try: isopass = p.isopass() 
            except: pass

            ## Fill reco object hists
            if len(params["ids"]) > 0:
                for quality in params["ids"]:
                    if quality[3] > 0: continue
                    if p.idpass() > quality[1] and isopass > quality[2]:
                        hists[obj+"_pt_"+quality[0]].Fill(p.pt())
                        hists[obj+"_eta_"+quality[0]].Fill(p.eta())
                        hists[obj+"_phi_"+quality[0]].Fill(p.phi())
                        hists[obj+"_mass_"+quality[0]].Fill(p.mass())
                        hists[obj+"_idpass_"+quality[0]].Fill(p.idpass())
            else:
                hists[obj+"_pt"].Fill(p.pt())
                hists[obj+"_eta"].Fill(p.eta())
                hists[obj+"_phi"].Fill(p.phi())
                hists[obj+"_mass"].Fill(p.mass())
                hists[obj+"_idpass"].Fill(p.idpass())


            if obj == "jet" and p.pt() < 25 : continue  # for jets
            
            ## Increment multiplicity counters
            if len(params["ids"]) > 0:
                for quality in params["ids"]:
                    if quality[3] >= 1: continue
                    if p.idpass() > quality[1] and isopass > quality[2]: multiplicity["nocut_"+quality[0]] += 1
            else: multiplicity["nocut"] += 1
            for cut in params["etaSlices"]:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                if cut[0] < abs(p.eta()) <= cut[1] : 
                    if len(params["ids"]) > 0:
                        for quality in params["ids"]:
                            if quality[3] >= 1: continue 
                            if p.idpass() > quality[1] and isopass > quality[2]: multiplicity[cutname+"_"+quality[0]] += 1
                    else: multiplicity[cutname] += 1

            for cut in params["ptSlices"]:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                if  cut[0] <= p.pt() < cut[1]: 
                    if len(params["ids"]) > 0:
                        for quality in params["ids"]: 
                            if quality[3] >= 1: continue
                            if p.idpass() > quality[1] and isopass > quality[2]: multiplicity[cutname+"_"+quality[0]] += 1
                    else: multiplicity[cutname] += 1

            ## STORE all reco objects passing basic thresholds (25 hardcoded for jets)
            p_vec = ROOT.TLorentzVector()
            p_vec.SetPtEtaPhiM(p.pt(), p.eta(), p.phi(), p.mass())
            p_tvectors.append(p_vec)
            p_idpass.append(p.idpass())
            p_isopass.append(isopass)

            # if p.pt() > 96:
            #     print '------------------------'
            #     print "HIGHTPT reco muon:",p.pt(),p.eta(),p.phi(),p.idpass(),p.isopass()
            #     printgen = True

        # for genjet in event.genjets():
        #     if printgen: 
        #         print "gen jet:",genjet.pt(),genjet.eta(),genjet.phi()

        # for jet in event.jets():
        #     if printgen:
        #         print "reco jet:",jet.pt(),jet.eta(),jet.phi()
            
        # for electron in event.electrons():
        #     if printgen:
        #         print "reco electron:",electron.pt(),electron.eta(),electron.phi()

        ## LOOP over the GEN objects
        for g in genobjs:

            ## Cuts on the gen object
            if obj in pdgid:
                if abs(g.pid()) != pdgid[obj]: continue  # check genparticle pid  
                if g.status() != 1: continue
            if abs(g.eta()) > 5 or g.pt() < params["ptMin"] : continue

            ## Fill gen object hists
            hists["gen"+obj+"_pt"].Fill(g.pt())
            hists["gen"+obj+"_eta"].Fill(g.eta())
            hists["gen"+obj+"_phi"].Fill(g.phi())
            hists["gen"+obj+"_mass"].Fill(g.mass())

            g_vec = ROOT.TLorentzVector()
            g_vec.SetPtEtaPhiM(g.pt(), g.eta(), g.phi(), g.mass())
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

            if minDR < params["dR"] and ( 1./params["ptRatio"] < p_tvectors[minDRindex].Pt()/g.pt() < params["ptRatio"]) : # matched
                match = 1
                matchindex = minDRindex

            # if g.pt() > 100:
            #     print "HIGHPT gen muon:",g.pt(),g.eta(),g.phi(),minDR
            #     if match:
            #         print "\t MATCH to reco:",p_tvectors[matchindex].Pt(),p_tvectors[matchindex].Eta(),p_tvectors[matchindex].Phi()
            #     else:
            #         print "\t MATCH FAIL:",minDR,p_tvectors[minDRindex].Pt()/g.pt()
            # else:
            #     if printgen: print "gen muon:",g.pt(),g.eta(),g.phi(),minDR

            ## Work with only matched pairs first:
            if match == 1:
                
                ## Fill matched reco and gen hists
                if len(params["ids"]) > 0:
                    for quality in params["ids"]:
                        if quality[3] >= 1: continue
                        if p_idpass[matchindex] > quality[1] and p_isopass[matchindex] > quality[2]:
                            hists[obj+"_matched_pt_"+quality[0]].Fill(p_tvectors[matchindex].Pt())
                            hists[obj+"_matched_eta_"+quality[0]].Fill(p_tvectors[matchindex].Eta())
                            hists[obj+"_matched_phi_"+quality[0]].Fill(p_tvectors[matchindex].Phi())
                            hists[obj+"_matched_mass_"+quality[0]].Fill(p_tvectors[matchindex].M())
			    hists[obj+"_matched_idpass_"+quality[0]].Fill(p_idpass[matchindex])
                else:
                    hists[obj+"_matched_pt"].Fill(p_tvectors[matchindex].Pt())
                    hists[obj+"_matched_eta"].Fill(p_tvectors[matchindex].Eta())
                    hists[obj+"_matched_phi"].Fill(p_tvectors[matchindex].Phi())
                    hists[obj+"_matched_mass"].Fill(p_tvectors[matchindex].M())
		    hists[obj+"_matched_idpass"].Fill(p_idpass[matchindex]) 
                hists["gen"+obj+"_matched_pt"].Fill(g.pt())
                hists["gen"+obj+"_matched_eta"].Fill(g.eta())
                hists["gen"+obj+"_matched_phi"].Fill(g.phi())
                hists["gen"+obj+"_matched_mass"].Fill(g.mass())
	
                ## Fill ptresponse hists                
                if len(params["ids"]) > 0:
                    for quality in params["ids"]:
                        if quality[3] >= 1: continue
                        if p_idpass[matchindex] > quality[1] and p_isopass[matchindex] > quality[2]:
                            hists[obj+"_ptresponse_to_eta_"+quality[0]].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                            hists[obj+"_ptresponse_to_pt_"+quality[0]].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())
                else:
                    hists[obj+"_ptresponse_to_eta"].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                    hists[obj+"_ptresponse_to_pt"].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())

                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] <= g.pt() < cut[1]: 
                        if len(params["ids"]) > 0:
                            for quality in params["ids"]:
                                if quality[3] >= 1: continue
                                if p_idpass[matchindex] > quality[1] and p_isopass[matchindex] > quality[2]: 
                                    hists[obj+"_ptresponse_to_eta_"+quality[0]+"_"+cutname].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                        else: hists[obj+"_ptresponse_to_eta_"+cutname].Fill(g.eta(), p_tvectors[matchindex].Pt()/g.pt())
                
                for cut in params["etaSlices"]:
                        cutname = str(cut[0]) + "to" + str(cut[1])
                        cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                        if cut[0] < abs(g.eta()) <= cut[1]: 
                            if len(params["ids"]) > 0:
                                for quality in params["ids"]:
                                    if quality[3] >= 1: continue
                                    if p_idpass[matchindex] > quality[1] and p_isopass[matchindex] > quality[2]:
                                        hists[obj+"_ptresponse_to_pt_"+quality[0]+"_"+cutname].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())
                            else: hists[obj+"_ptresponse_to_pt_"+cutname].Fill(g.pt(), p_tvectors[matchindex].Pt()/g.pt())

                ## fill 0 into fakerate TProfiles for the matched reco object
                ## fakerate: denominator = all reco objects with given quality (0's here for matched, 1's later for unmatched)
                ##           numerator = all unmatched reco objects with given quality (1's later for unmatched)
                if len(params["ids"]) > 0:
                    for quality in params["ids"]:
                        if quality[3] >= 1: continue
                        if p_idpass[matchindex] > quality[1] and p_isopass[matchindex] > quality[2]:
                            hists[obj+"_fakerate_to_eta_"+quality[0]].Fill(p_tvectors[matchindex].Eta(), 0)
                            hists[obj+"_fakerate_to_pt_"+quality[0]].Fill(p_tvectors[matchindex].Pt(), 0)
                            hists[obj+"_fakerate2D_"+quality[0]].Fill(p_tvectors[matchindex].Pt(),p_tvectors[matchindex].Eta(),0)
                else:
                    hists[obj+"_fakerate_to_eta"].Fill(p_tvectors[matchindex].Eta(), 0)
                    hists[obj+"_fakerate_to_pt"].Fill(p_tvectors[matchindex].Pt(), 0)
                    hists[obj+"_fakerate2D"].Fill(p_tvectors[matchindex].Pt(),p_tvectors[matchindex].Eta(),0)
                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] <= p_tvectors[matchindex].Pt() < cut[1]: 
                        if len(params["ids"]) > 0:
                            for quality in params["ids"]:
                                if quality[3] >= 1: continue
                                if p_idpass[matchindex] > quality[1] and p_isopass[matchindex] > quality[2]:
                                    hists[obj+"_fakerate_to_eta_"+quality[0]+"_" + cutname].Fill(p_tvectors[matchindex].Eta(), 0)
                        else: hists[obj+"_fakerate_to_eta_" + cutname].Fill(p_tvectors[matchindex].Eta(), 0)

                for cut in params["etaSlices"]:
                        cutname = str(cut[0]) + "to" + str(cut[1])
                        cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                        if cut[0] < abs(p_tvectors[matchindex].Eta()) <= cut[1]: 
                            if len(params["ids"]) > 0:
                                for quality in params["ids"]:
                                    if quality[3] >= 1: continue
                                    if p_idpass[matchindex] > quality[1] and p_isopass[matchindex] > quality[2]:
                                        hists[obj+"_fakerate_to_pt_"+quality[0]+"_"+cutname].Fill(p_tvectors[matchindex].Pt(), 0)
                            else: hists[obj+"_fakerate_to_pt_"+cutname].Fill(p_tvectors[matchindex].Pt(), 0)

                ## end of matched object stuff

            ## working with matched AND unmatched: fill match status into efficiency TProfiles
            ## efficiency when quality[3] == 0:
            ##             denominator = all gen objects: fill 0's for unmatched, 0's for matched and reco obj fails quality, match*idpass*isopass = 0
            ##             numerator = all reco-matched gen objects with given reco quality: fill 1's for matched and reco obj passes quality, match*idpass*isopass = 1
            ## efficiency when quality[3] == 1: 
            ##             denominator = all reco-matched gen objects: if match, fill 0 if matched&!quality, idpass*isopass = 0
            ##             numerator = all reco-matched gen objects with given reco quality: fill 1 if matched&quality, idpass*isopass = 1
            if len(params["ids"]) > 0:
                for quality in params["ids"]:
                    try: idpass = (p_idpass[matchindex] > quality[1])
                    except: idpass = False
                    try: isopass = (p_isopass[matchindex] > quality[2])
                    except: isopass = False
                    if quality[3] >= 1:
                        if match == 1:
                            if quality[3] == 2:
                                if idpass:
                                    hists[obj+"_efficiency_to_eta_"+quality[0]].Fill(g.eta(), isopass) #0 if iso fails, 1 if passes
                                    hists[obj+"_efficiency_to_pt_"+quality[0]].Fill(g.pt(), isopass)
                                    hists[obj+"_efficiency2D_"+quality[0]].Fill(g.pt(),g.eta(), isopass)
                            else:
                                hists[obj+"_efficiency_to_eta_"+quality[0]].Fill(g.eta(), idpass*isopass) #0 if either fails, 1 if both
                                hists[obj+"_efficiency_to_pt_"+quality[0]].Fill(g.pt(), idpass*isopass)
                                hists[obj+"_efficiency2D_"+quality[0]].Fill(g.pt(),g.eta(), idpass*isopass)
                    else:
                        hists[obj+"_efficiency_to_eta_"+quality[0]].Fill(g.eta(), match*idpass*isopass) #0 if any fail, 1 if all
                        hists[obj+"_efficiency_to_pt_"+quality[0]].Fill(g.pt(), match*idpass*isopass)
                        hists[obj+"_efficiency2D_"+quality[0]].Fill(g.pt(),g.eta(), match*idpass*isopass)
            else:
                hists[obj+"_efficiency_to_eta"].Fill(g.eta(), match)
                hists[obj+"_efficiency_to_pt"].Fill(g.pt(), match)
                hists[obj+"_efficiency2D"].Fill(g.pt(),g.eta(), match)
            for cut in params["ptSlices"]:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                if cut[0] <= g.pt() < cut[1]: 
                    if len(params["ids"]) > 0:
                        for quality in params["ids"]:
                            try: idpass = (p_idpass[matchindex] > quality[1])
                            except IndexError: idpass = False
                            try: isopass = (p_isopass[matchindex] > quality[2])
                            except: isopass = False
                            if quality[3] >= 1:
                                if match == 1: 
                                    if quality[3] == 2:
                                        if idpass: hists[obj+"_efficiency_to_eta_"+quality[0]+"_" + cutname].Fill(g.eta(), isopass)
                                    else: hists[obj+"_efficiency_to_eta_"+quality[0]+"_" + cutname].Fill(g.eta(), idpass*isopass)
                            else: hists[obj+"_efficiency_to_eta_"+quality[0]+"_" + cutname].Fill(g.eta(), match*idpass*isopass)
                    else: hists[obj+"_efficiency_to_eta_" + cutname].Fill(g.eta(), match)

            for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] < abs(g.eta()) <= cut[1]: 
                        if len(params["ids"]) > 0:
                            for quality in params["ids"]:
                                try: idpass = (p_idpass[matchindex] > quality[1])
                                except IndexError: idpass = False
                                try: isopass = (p_isopass[matchindex] > quality[2])
                                except: isopass = False
                                if quality[3] >= 1:
                                    if match == 1: 
                                        if quality[3] == 2:
                                            if idpass: hists[obj+"_efficiency_to_pt_"+quality[0]+"_"+cutname].Fill(g.pt(), isopass)
                                        else: hists[obj+"_efficiency_to_pt_"+quality[0]+"_"+cutname].Fill(g.pt(), idpass*isopass)
                                else: hists[obj+"_efficiency_to_pt_"+quality[0]+"_"+cutname].Fill(g.pt(), match*idpass*isopass)
                        else: hists[obj+"_efficiency_to_pt_"+cutname].Fill(g.pt(), match)

            ## remove this matched reco object so later gen objects can't be matched to it
            if matchindex > -1:
                p_tvectors.pop(matchindex)
                p_idpass.pop(matchindex)
                p_isopass.pop(matchindex)

            ## end of gen object loop

        ## All the matched reco objects should have been removed from p_tvectors and p_idpass, fill 1 in fakerate for others
        #print "now filling the fakes:",len(p_tvectors)
        for ip in range(len(p_tvectors)):

            # if p_tvectors[ip].Pt() > 100:
            #     print "HIGHPT unmatched reco:",p_tvectors[ip].Pt(),p_tvectors[ip].Eta(),p_tvectors[ip].Phi()

            if len(params["ids"]) > 0:
                for quality in params["ids"]:
                    if quality[3] >= 1: continue
                    if p_idpass[ip] > quality[1] and p_isopass[ip] > quality[2]:
                        hists[obj+"_fakerate_to_eta_"+quality[0]].Fill(p_tvectors[ip].Eta(), 1)
                        hists[obj+"_fakerate_to_pt_"+quality[0]].Fill(p_tvectors[ip].Pt(), 1)
                        hists[obj+"_fakerate2D_"+quality[0]].Fill(p_tvectors[ip].Pt(),p_tvectors[ip].Eta(),1)
            else:
                hists[obj+"_fakerate_to_eta"].Fill(p_tvectors[ip].Eta(), 1)
                hists[obj+"_fakerate_to_pt"].Fill(p_tvectors[ip].Pt(), 1)
                hists[obj+"_fakerate2D"].Fill(p_tvectors[ip].Pt(),p_tvectors[ip].Eta(),1)
            for cut in params["ptSlices"]:
                cutname = str(cut[0]) + "to" + str(cut[1])
                cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                if cut[0] <= p_tvectors[ip].Pt() < cut[1]: 
                    if len(params["ids"]) > 0:
                        for quality in params["ids"]:
                            if quality[3] >= 1: continue
                            if p_idpass[ip] > quality[1] and p_isopass[ip] > quality[2]:
                                hists[obj+"_fakerate_to_eta_"+quality[0]+"_" + cutname].Fill(p_tvectors[ip].Eta(), 1)
                    else: hists[obj+"_fakerate_to_eta_" + cutname].Fill(p_tvectors[ip].Eta(), 1)

            for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] < abs(p_tvectors[ip].Eta()) <= cut[1]: 
                        if len(params["ids"]) > 0:
                            for quality in params["ids"]:
                                if quality[3] >= 1: continue
                                if p_idpass[ip] > quality[1] and p_isopass[ip] > quality[2]:
                                    hists[obj+"_fakerate_to_pt_"+quality[0]+"_"+cutname].Fill(p_tvectors[ip].Pt(), 1)
                        else: hists[obj+"_fakerate_to_pt_"+cutname].Fill(p_tvectors[ip].Pt(), 1)

        ## for each evt
        for cut in cutList:
            hname = "multiplicity"
            cutname = str(cut[0]) + "to" + str(cut[1])
            cutname = ((cutname.replace('.','p')).replace('100000p0','Inf')).replace('ntoo','nocut')
            if len(params["ids"]) > 0: 
                for quality in params["ids"]:
                    if quality[3] > 0: continue
                    hname = "multiplicity_"+quality[0]
                    if cutname != "nocut": hname += "_"+cutname                  
                    hists[obj+"_" + hname].Fill(multiplicity[cutname+"_"+quality[0]])
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
    print("On average %f chs jets" % (float(tot_jetchs) / tot_nevents))
    print("On average %f puppi jets" % (float(tot_jetpuppi) / tot_nevents))
    print("On average %f taus" % (float(tot_tau) / tot_nevents))
    print("On average %f met" % (float(tot_met) / tot_nevents))
    #print("On average %f generated AK8 jets" % (float(tot_genjetAK8) / tot_nevents))
    #print("On average %f jetsAK8" % (float(tot_jetAK8) / tot_nevents))

if __name__ == "__main__":
    main()

