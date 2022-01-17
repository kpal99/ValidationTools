#!/usr/bin/env python
# import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from ntuple_event_selection import createHist
import ROOT
import sys

# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple
def get_phy_obj(event,phy_obj_str):
    if phy_obj_str == 'muons':
        return event.muons()
    if phy_obj_str == 'electrons':
        return event.electrons()
    if phy_obj_str == 'taus':
        return event.taus()
    if phy_obj_str == 'gammas':
        return event.gammas()
    if phy_obj_str == 'genjets':
        return event.genjets()
    if phy_obj_str == 'jetschs':
        return event.jetschs()
    if phy_obj_str == 'jetspuppi':
        return event.jetspuppi()
    if phy_obj_str == 'jetsAK8':
        return event.jetsAK8()
    if phy_obj_str == 'fatjets':
        return event.fatjets()
    if phy_obj_str == 'metspuppi':
        return event.metspuppi()
    if phy_obj_str == 'metspf':
        return event.metspf()
    sys.exit("-- {} -- not implemented yet".format(phy_obj_str))

def main():
    if len(sys.argv) != 2:
        print "USAGE: %s <input file>".format(sys.argv[0])
        sys.exit(1)
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    maxEvents = 0

    hist = createHist("delta R", 0.4)
    phy_obj_str = "fatjets"
    #print(ntuple.__dict__)
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break


        #print ''
        #print '... processing event {} ...'.format(event.entry()+1)


        phy_obj=get_phy_obj(event,phy_obj_str)
        i=0; #print(phy_obj.__dict__)

        for p in phy_obj:
            i += 1
            #print '  -- {}  --'.format(phy_obj_str)
            #print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, Tau1: {:<6.2f}, Tau2: {:<6.2f}, Tau3: {:<6.2f}, Tau4: {:<6.2f}, m-SD: {:<6.2f}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.tau1(), p.tau2(), p.tau3(), p.tau4(), p.msoftdrop())
            #print '  -- subjets --'
            ij = 0
            for j in get_phy_obj(event,"jetspuppi"):
                ij += 1
                deltaR =  ((p.eta() - j.eta())**2 + (p.phi() - j.phi())**2)**0.5
                hist.Fill(deltaR)
                    #print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, Btag: {:<6.2f}, delta R: {:<6}'.format(ij, j.pt(), j.eta() , j.phi(), j.mass(), j.btag(),deltaR)
            #print ''
    outputDir = '/eos/user/k/kpal/www/'
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(1111111)
    canvas = ROOT.TCanvas('canvas','',700,500)
    hist.SetLineColor(3)
    hist.Draw("hist")
    canvas.SaveAs(outputDir + "deltaR1.pdf")
    canvas.Close()

if __name__ == "__main__":
    main()
