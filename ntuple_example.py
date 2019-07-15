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

    maxEvents = 10

    tot_nevents = 0
    tot_genpart = 0
    tot_muon = 0

    for event in ntuple:
        if event.entry() >= maxEvents:
            break
        print '... processed {} events ...'.format(event.entry()+1)

        print ' '
        print' -------------- new event -----------------'
        print ' '

        ###### loop over gen particles ######

        print ''
        print '  -- gen parts --'
        print ''
        
        genParts = event.genParticles()
        i=0
        for p in genParts:
        
            eta = p.eta()

            etap = eta
            if eta > 10:
               etap = 999.
            if eta < -10:
               etap = -999.

            print 'N: {:<5}, St: {:<5}, PID: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  M1: {:<5}, M2: {:<5}, D1: {:<5}, D2: {:<5}'.format(i, p.status(), p.pid(), p.pt(), etap, p.phi(), p.mass(), p.m1(), p.m2(), p.d1(), p.d2())
            i+=1


        print ''
        print '  -- muons  --'
        print ''

        muons = event.muons()
        i=0
        for p in muons:


            print 'N: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  Charge: {:<5}, IdVar: {:<5.2f}, IsoVar: {:<5.2f}, IdPass: {:08b}, IsoPass: {:08b}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.reliso(), p.idpass(), p.isopass() )


        tot_nevents += 1
        tot_genpart += len(genParts)
        tot_muon += len(muons)

        # for genPart in genParts:
        #     print(tot_nevents, "genPart pt:", genPart.pt()

    print("Processed %d events" % tot_nevents)
    print("On average %f generator particles" % (float(tot_genpart) / tot_nevents))
    print("On average %f muons" % (float(tot_muon) / tot_nevents))

if __name__ == "__main__":
    main()
