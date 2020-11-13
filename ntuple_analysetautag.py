#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import optparse
import itertools
from array import array
import math

    
def findHadronFlav(genparts, jet, dR):

    isbHad = False
    iscHad = False
    for g in genparts: # check if there exists one b-hadron
	gVec = ROOT.TLorentzVector()
        gVec.SetPtEtaPhiM(g.pt(), g.eta(), g.phi(), g.mass())
        if jet.DeltaR(gVec) >= dR:
	    continue
	if 500 < abs(g.pid()) < 600 or 5000 < abs(g.pid()) < 6000:
	    isbHad = True
	    break
        if 400 < abs(g.pid()) < 500 or 4000 < abs(g.pid()) < 5000:
            iscHad = True

    if isbHad:
        return 5
    if iscHad:
        return 4
    return 1 # any not 4 or 5 case  

def findPartonFlav(genparts, jet, dR):

    isbPar = False
    iscPar = False
    for g in genparts: # check if there exists one b-hadron
        gVec = ROOT.TLorentzVector()
        gVec.SetPtEtaPhiM(g.pt(), g.eta(), g.phi(), g.mass())
        if jet.DeltaR(gVec) >= dR:
            continue
        if abs(g.pid()) == 5:
            isbPar = True
            break
        if abs(g.pid()) == 4:
            iscPar = True

    if isbPar:
        return 5
    if iscPar:
        return 4
    return 1 # any not 4 or 5 case

def findTaus(genparts, tau, dR):
    
    isTau = False
    isElec = False
    for g in genparts:
        gVec = ROOT.TLorentzVector()
        gVec.SetPtEtaPhiM(g.pt(), g.eta(), g.phi(), g.mass())
        if tau.DeltaR(gVec) >= dR:
            continue
        if abs(g.pid()) == 15:
            isTau = True
	if abs(g.pid()) == 11:
	    isElec = True
    if isTau:
        return 15
    elif isElec:
	return 11
    else:
	return 1

def doSum(objs, ptCut, etaCut):
    s = 0
    for j in objs:
        if j.pt()> ptCut and abs(j.eta())< etaCut :
	    s += j.pt()
    return s

def doCount(objs, ptCut, etaCut):
    cnt = 0
    for j in objs:
        if j.pt()> ptCut and abs(j.eta())< etaCut :
            cnt += 1
    return cnt

def create2dHist(varname, params, title):
    if "to_pt" in varname and "tagRate" in varname:
        h = ROOT.TProfile(varname, title, 50, params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("jet p_{T} [GeV]")
        h.GetYaxis().SetTitle("tagging efficiency")
    if "to_eta" in varname and "tagRate" in varname:
        h = ROOT.TProfile(varname, title, 50, params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("jet #eta")
        h.GetYaxis().SetTitle("tagging efficiency")

    h.Sumw2()

    return h

def main():
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--inFile',
                      dest='inFile',
                      help='input file [%default]', # /eos/cms/store/group/upgrade/RTB/DelphesFlat_343pre01 
                      default='/eos/cms/store/group/upgrade/RTB/FullsimFlat_110X/TT_TuneCP5_14TeV_200PU.root',
                      type='string')
    parser.add_option('-o', '--outFile',          
                      dest='outFile',       
                      help='output file [%default]',  
                      default='histo_full/val_btag.root',       
                      type='string')
    parser.add_option('-p', '--physObj',          
                      dest='physobject',       
                      help='object to analyze [%default]',
                      default='jetpuppi',
                      type='string')
    parser.add_option('--maxEvents',          
                      dest='maxEvts',
                      help='max number of events [%default]',
                      default=10000,
                      type=int)
    (opt, args) = parser.parse_args()


    inFile = opt.inFile
    print inFile
    ntuple = Ntuple(inFile)
    maxEvents = opt.maxEvts
    tot_nevents = 0
    outputF = ROOT.TFile(opt.outFile, "RECREATE")
    obj = opt.physobject


    params = {
            "dR": 0.2,
            "ptMin": 10,
            "etaSlices": [[0, 1.5], [1.5, 2.5], [2.5, 4] ], ## use 1e5 as "Inf"
            "ptSlices": [[10, 20], [20, 50], [50, 150] ],
            "sliceSplit": 1, # for 2D map, make N divisions of each slice
            "plotPtRange": [0, 250],
            "plotEtaRange": [-5, 5],
	    "ids": [
	        ["looseID",1,"#varepsilon(looseID)"],
		["mediumID",3,"#varepsilon(mediumID)"], 
                ["tightID",7,"#varepsilon(tightID)"],
		],
	    "bitids": [
		["looseID",(1<<0),"#varepsilon(looseID)"],
		["mediumID",(1<<1),"#varepsilon(mediumID)"],
		["tightID",(1<<2),"#varepsilon(tightID)"],
		]

    }

    ## create histo#

    hists = {}

    for cut in ["nocut"]+params["etaSlices"]:
        hnames = ["tautagRate_to_pt", "elecMistagRate_to_pt", "lightMistagRate_to_pt"]
        for hname in hnames:
            for quality in params["bitids"]:
                newname = hname+"_"+quality[0]+"_"+ str(cut[0]) + "to" + str(cut[1])
                newname = ((newname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
                hists[obj+"_"+newname] = create2dHist(obj+"_"+newname,params,quality[2])

    for cut in ["nocut"]+params["ptSlices"]:
        hnames = ["tautagRate_to_eta", "elecMistagRate_to_eta", "lightMistagRate_to_eta"]
        for hname in hnames:
            for quality in params["bitids"]:
                newname = hname+"_"+quality[0]+"_"+ str(cut[0]) + "to" + str(cut[1])
                newname = ((newname.replace('.', 'p')).replace('100000p0','Inf')).replace('_ntoo','')
                hists[obj+"_"+newname] = create2dHist(obj+"_"+newname,params,quality[2])


    ## study
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents %2) == 0 : # 1000
            print '... processed {} events ...'.format(event.entry()+1)
	
	tot_nevents += 1
	genparts = event.genparticles()
	taus = event.taus()
	electrons = event.electrons()

 	## studymet

	for p in taus:
	    if p.pt() < params['ptMin']: continue
	    pVec = ROOT.TLorentzVector()
	    pVec.SetPtEtaPhiM(p.pt(), p.eta(), p.phi(), p.mass())
	    tauFlav = findTaus(genparts, pVec, params['dR'])

	    if tauFlav == 15:
	        for quality in params["bitids"]:
		    isTagged = int(bool(p.isopass() & quality[1]))
		    hists[obj+"_tautagRate_to_eta_"+quality[0]].Fill(p.eta(), isTagged)
	    	    hists[obj+"_tautagRate_to_pt_"+quality[0]].Fill(p.pt(), isTagged)
	        for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] <= p.pt() < cut[1]: 
 		        for quality in params["bitids"]:
                    	    isTagged = int(bool(p.isopass() & quality[1]))
			    hists[obj+"_tautagRate_to_eta_"+quality[0]+"_" + cutname].Fill(p.eta(), isTagged)
                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] < abs(p.eta()) <= cut[1]: 
		        for quality in params["bitids"]:
                            isTagged = int(bool(p.isopass() & quality[1]))
                            hists[obj+"_tautagRate_to_pt_"+quality[0]+"_" + cutname].Fill(p.pt(), isTagged)

	    if tauFlav == 11:
	        for quality in params["bitids"]:
		    isTagged = int(bool(p.isopass() & quality[1]))
		    hists[obj+"_elecMistagRate_to_eta_"+quality[0]].Fill(p.eta(), isTagged)
	    	    hists[obj+"_elecMistagRate_to_pt_"+quality[0]].Fill(p.pt(), isTagged)
	        for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] <= p.pt() < cut[1]: 
 		        for quality in params["bitids"]:
                    	    isTagged = int(bool(p.isopass() & quality[1]))
			    hists[obj+"_elecMistagRate_to_eta_"+quality[0]+"_" + cutname].Fill(p.eta(), isTagged)
                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] < abs(p.eta()) <= cut[1]: 
		        for quality in params["bitids"]:
                            isTagged = int(bool(p.isopass() & quality[1]))
                            hists[obj+"_elecMistagRate_to_pt_"+quality[0]+"_" + cutname].Fill(p.pt(), isTagged)

	    if tauFlav == 1:
	        for quality in params["bitids"]:
		    isTagged = int(bool(p.isopass() & quality[1]))
		    hists[obj+"_lightMistagRate_to_eta_"+quality[0]].Fill(p.eta(), isTagged)
	    	    hists[obj+"_lightMistagRate_to_pt_"+quality[0]].Fill(p.pt(), isTagged)
	        for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] <= p.pt() < cut[1]: 
 		        for quality in params["bitids"]:
                    	    isTagged = int(bool(p.isopass() & quality[1]))
			    hists[obj+"_lightMistagRate_to_eta_"+quality[0]+"_" + cutname].Fill(p.eta(), isTagged)
                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.','p')).replace('100000p0','Inf')
                    if cut[0] < abs(p.eta()) <= cut[1]: 
		        for quality in params["bitids"]:
                            isTagged = int(bool(p.isopass() & quality[1]))
                            hists[obj+"_lightMistagRate_to_pt_"+quality[0]+"_" + cutname].Fill(p.pt(), isTagged)


    outputF.cd()
    for h in hists.keys():
        hists[h].Write()

if __name__ == "__main__":
    main()
