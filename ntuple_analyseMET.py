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
	    if d1<0: 
#		print "d1 ", d1, " gd1 ", gd1
		continue
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
    metHists['genht_pt30_eta5'] = createMetHist('genht_pt30_eta5', "H_{T} gen [GeV]", 50, 0, 500)
    metHists['npuVtx'] = createMetHist('npuVtx', "npuVertices", 180, 0, 400)
    metHists['genjet_size_pt30_eta5'] = createMetHist('genjet_size_pt30_eta5', "N_{genjet}", 15, 0, 15)
    metHists['z_pt'] = createMetHist('z_pt', "p_{T}(Z) [GeV]", 150, 0, 150)
    metHists['met'] = createMetHist('met', "p_{T,miss} [GeV]", 300, 0, 300)
    metHists['met_p'] = createMetHist('met_p', "parallel p_{T,miss} [GeV]", 150, 0, 150)
    metHists['met_t'] = createMetHist('met_t', "transverse p_{T,miss} [GeV]", 150, 0, 150)
    metHists['u_p'] = createMetHist('u_p', "u_{p} [GeV]", 150, 0, 150)


    twodvarList=['genht_pt30_eta5','npuVtx','genjet_size_pt30_eta5']
    varList = ['z_pt', 'met', 'met_p', 'met_t', 'u_p']
    varAllList = varList +twodvarList
    for v in varList:
        for twodv in twodvarList:
            metHists[v+'_VS_'+twodv] = ROOT.TProfile(v+'_VS_'+twodv, "", metHists[twodv].GetNbinsX(), 0, metHists[twodv].GetXaxis().GetBinUpEdge(metHists[twodv].GetNbinsX()))
	    metHists[v+'_VS_'+twodv].GetXaxis().SetTitle(metHists[twodv].GetXaxis().GetTitle())
	    metHists[v+'_VS_'+twodv].GetYaxis().SetTitle(metHists[v].GetXaxis().GetTitle())

    ## study
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents %1000) == 0 :
            print '... processed {} events ...'.format(event.entry()+1)

	tot_nevents += 1
        genparts = event.genparticles()
        genjets = event.genjets()
        mets = event.metspuppi()

 	## studymet
        z = findZ(genparts)
        z_pt = z.Mod()
	if not (z_pt>0.00001): continue
#  	ht = doSum(jets, 0., 5000.)
#	ht_pt30_eta4 = doSum(jets, 30., 4.)
#	ht_pt30_eta3 = doSum(jets, 30., 3.)
	genht_pt30_eta5 = doSum(genjets, 30., 5.)
	met_v = ROOT.TVector2(0,0)
	met_v.SetMagPhi(mets[0].pt(),mets[0].phi())
	met = mets[0].pt()
	met_p = met_v.Proj(z).Mod()
	met_t =	met_v.Norm(z).Mod()	
	u_p = (z+met_v).Proj(z).Mod()
#	jet_size_pt30_eta4 = doCount(jets, 30., 4.)
#	jet_size_pt30_eta3 = doCount(jets, 30., 3.)
#	jet_size = len(jets)
	genjet_size_pt30_eta5 = doCount(genjets, 30., 5.)
	vtx_size = event.vtxSize()
 	npuVtx = event.npuVertices()
	trueInt = event.trueInteractions()

	var = {}
        var['genht_pt30_eta5'] =genht_pt30_eta5
	var['npuVtx'] = npuVtx
	var['genjet_size_pt30_eta5'] = genjet_size_pt30_eta5
        var['z_pt'] = z_pt
	var['met'] = met
	var['met_p'] = met_p
	var['met_t'] = met_t
 	var['u_p']= u_p

	for v in varAllList:
	    metHists[v].Fill(var[v])

	for v in varList:
            for twodv in twodvarList:
	        metHists[v+'_VS_'+twodv].Fill(var[twodv], var[v])
	    
    ## write event level var hists
    outputF.cd()
    for h in metHists.keys():
	metHists[h].Write()

    for i in twodvarList:
	up_over_qt=outputF.Get("u_p_VS_"+i).Clone()
	up_over_qt.Divide(outputF.Get("z_pt_VS_"+i))
	up_over_qt.Write("up_over_qt_VS_"+i)

	ut=outputF.Get("met_t_VS_"+i).Clone()
	ut_rms= ROOT.TH1F("ut_rms_VS_"+i, "", metHists[i].GetNbinsX(), 0, metHists[i].GetXaxis().GetBinUpEdge(metHists[i].GetNbinsX()))
	ut_rms.GetXaxis().SetTitle(metHists[i].GetXaxis().GetTitle())
	ut_rms.GetYaxis().SetTitle("RMS u_{T}")
	for imtt in range(1,ut.GetNbinsX()+1):
	    ut_rms.SetBinContent(imtt, ut.GetBinError(imtt)*math.sqrt(ut.GetBinEntries(imtt)))
	ut_rms.Write()

	up_plus_qt =outputF.Get("met_p_VS_"+i).Clone()
	up_plus_qt_rms = ROOT.TH1F("up_plus_qt_rms_VS_"+i, "", metHists[i].GetNbinsX(),0,metHists[i].GetXaxis().GetBinUpEdge(metHists[i].GetNbinsX()))
	up_plus_qt_rms.GetXaxis().SetTitle(metHists[i].GetXaxis().GetTitle())
	up_plus_qt_rms.GetYaxis().SetTitle("RMS u_{P}+q_{T}")
	for imtt in range(1,up_plus_qt.GetNbinsX()+1):
	    up_plus_qt_rms.SetBinContent(imtt, up_plus_qt.GetBinError(imtt)*math.sqrt(up_plus_qt.GetBinEntries(imtt)))
	up_plus_qt_rms.Write()

    outputF.Close()

if __name__ == "__main__":
    main()
