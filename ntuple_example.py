#!/usr/bin/env python
# import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys


# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple

def main():
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)

    maxEvents = 100

    tot_nevents = 0
    tot_genpart = 0
    tot_genjet = 0
    tot_electron = 0
    tot_gamma = 0
    tot_muon = 0
    tot_jetschs = 0
    tot_jetspuppi = 0
    tot_jetsAK8 = 0
    tot_tau = 0
    tot_metspf = 0
    tot_metspuppi = 0

    print("total events",ntuple.nevents())
    for event in ntuple:
        if event.entry() >= maxEvents:
            break
        #print '... processing event {} ... with genweight {}'.format(event.entry(), event.genweight())

        i=0
        #for p in event.tightElectrons():
            #print 'Electron N: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  Charge: {:<5}, IdVar: {:<5.2f}, IsoVar: {:<5.2f}, IdPass: {:08b}, IsoPass: {:08b}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.reliso(), p.idpass(), p.isopass() )
         #   pass
        #for p in event.tightMuons():
         #   print 'Muon     N: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  Charge: {:<5}, IdVar: {:<5.2f}, IsoVar: {:<5.2f}, IdPass: {:08b}, IsoPass: {:08b}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.reliso(), p.idpass(), p.isopass() )
            #print p.pt()
          #  pass

        #print(event.jetM(), event.jetBtag(), event.jetHt(), event.jetSt())
        print(event.fatjetM(), event.fatjetH2b(), event.fatjetH1b(), event.fatjetW())



if __name__ == "__main__":
    main()
