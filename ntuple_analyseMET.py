#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import optparse
import itertools
from array import array
import math

def findZ(genparts):
    v= ROOT.TVector2(0, 0)
    for g in genparts:
        if abs(g.pid())==23: 
	    d1 = g.d1()
	    gd1 = genparts[d1]
 	    if ( abs(gd1.pid())==11 or abs(gd1.pid()==13) ):
	        v.SetMagPhi(g.pt(),g.phi())
		return v
    return v

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

def createMetHist(varname, xTitle, nBinsX, xMin, xMax):
    h = ROOT.TH1D(varname, "", nBinsX, xMin, xMax)
    h.GetXaxis().SetTitle(xTitle)
    h.GetYaxis().SetTitle("Events")
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
    outputF = ROOT.TFile(opt.outFile, "RECREATE")

    ## create histo
    metHists = {}
    metHists['ht'] = createMetHist('ht', "H_{T} [GeV]", 50, 0, 500)
    metHists['ht_pt30_eta4'] = createMetHist('ht_pt30_eta4', "H_{T} [GeV]", 50, 0, 500)
    metHists['ht_pt30_eta3'] = createMetHist('ht_pt30_eta3', "H_{T} [GeV]", 50, 0, 500)
    metHists['vtx_size'] = createMetHist('vtx_size', "N_{PV}", 180, 90, 270)
    metHists['jet_size'] = createMetHist('jet_size', "N_{jet}", 15, 0, 15)
    metHists['jet_size_pt30_eta4'] = createMetHist('jet_size_pt30_eta4', "N_{jet}", 15, 0, 15)
    metHists['jet_size_pt30_eta3'] = createMetHist('jet_size_pt30_eta3', "N_{jet}", 15, 0, 15)
    metHists['z_pt'] = createMetHist('z_pt', "p_{T}(Z) [GeV]", 150, 0, 150)
    metHists['met'] = createMetHist('met', "p_{T,miss} [GeV]", 300, 0, 300)
    metHists['met_p'] = createMetHist('met_p', "parallel p_{T,miss} [GeV]", 150, 0, 150)
    metHists['met_t'] = createMetHist('met_t', "transverse p_{T,miss} [GeV]", 150, 0, 150)
    metHists['u_p'] = createMetHist('u_p', "u_{p} [GeV]", 150, 0, 150)

    twodvarList=['ht','ht_pt30_eta4','ht_pt30_eta3','vtx_size','jet_size','jet_size_pt30_eta4','jet_size_pt30_eta3']
    varList = ['z_pt', 'met', 'met_p', 'met_t', 'u_p']
    varAllList = varList +twodvarList
    for v in varList:
        for twodv in twodvarList:
            metHists[v+'_VS_'+twodv] = ROOT.TProfile(v+'_VS_'+twodv, "", metHists[v].GetNbinsX(), 0, metHists[v].GetXaxis().GetBinUpEdge(metHists[v].GetNbinsX()))
	    metHists[v+'_VS_'+twodv].GetXaxis().SetTitle(metHists[v].GetXaxis().GetTitle())
	    metHists[v+'_VS_'+twodv].GetYaxis().SetTitle(metHists[twodv].GetXaxis().GetTitle())

    ## study
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents %2) == 0 :
            print '... processed {} events ...'.format(event.entry()+1)

	tot_nevents += 1
        genparts = event.genparticles()
        jets = event.jetspuppi()
        mets = event.metspuppi()

 	## studymet
        z = findZ(genparts)
        z_pt = z.Mod()
	if not (z_pt>0.00001): continue
  	ht = doSum(jets, 0., 5000.)
	ht_pt30_eta4 = doSum(jets, 30., 4.)
	ht_pt30_eta3 = doSum(jets, 30., 3.)
	met_v = ROOT.TVector2(0,0)
	met_v.SetMagPhi(mets[0].pt(),mets[0].phi())
	met = mets[0].pt()
	met_p = met_v.Proj(z).Mod()
	met_t =	met_v.Norm(z).Mod()	
	u_p = (z+met_v).Proj(z).Mod()
	jet_size_pt30_eta4 = doCount(jets, 30., 4.)
	jet_size_pt30_eta3 = doCount(jets, 30., 3.)
	jet_size = len(jets)
	vtx_size = event.vtxSize()
 	npuV = event.npuVertices()
	trueInt = event.trueInteractions()

	var = {}
        var['ht'] = ht
        var['ht_pt30_eta4'] =ht_pt30_eta4
 	var['ht_pt30_eta3'] =ht_pt30_eta3
	var['vtx_size'] = vtx_size
 	var['jet_size'] = jet_size 
	var['jet_size_pt30_eta4'] = jet_size_pt30_eta4
	var['jet_size_pt30_eta3'] = jet_size_pt30_eta3
	var['z_pt'] = z_pt
	var['met'] = met
	var['met_p'] = met_p
	var['met_t'] = met_t
 	var['u_p']= u_p

	for v in varAllList:
	    metHists[v].Fill(var[v])

	for v in varList:
            for twodv in twodvarList:
	        metHists[v+'_VS_'+twodv].Fill(var[v], var[twodv])
	    
    ## write event level var hists
    outputF.cd()
    for h in metHists.keys():
	metHists[h].Write()


if __name__ == "__main__":
    main()
