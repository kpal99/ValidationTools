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

    maxEvents = 2

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

    for event in ntuple:
        if event.entry() >= maxEvents:
            break
        print '... processing event {} ...'.format(event.entry()+1)

        print ' '
        print' -------------- new event -----------------'
        print ' '

        ###### loop over gen particles ######

        print ''
        print '  -- gen parts --'
        print ''

        print(event.genweight())
        genparts = event.genparticles()
        i=0
        for p in genparts:

            eta = p.eta()

            etap = eta
            if eta > 10:
               etap = 999.
            if eta < -10:
               etap = -999.
            if abs(p.pid()) == 13:
            #if 1:
                pass #print 'N: {:<5}, St: {:<5}, PID: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  M1: {:<5}, M2: {:<5}, D1: {:<5}, D2: {:<5}'.format(i, p.status(), p.pid(), p.pt(), etap, p.phi(), p.mass(), p.m1(), p.m2(), p.d1(), p.d2())
            i+=1


        print ''
        print '  -- muons  --'
        print ''

        muons = event.muons()
        i=0
        for p in muons:


            pass #print 'N: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  Charge: {:<5}, IdVar: {:<5.2f}, IsoVar: {:<5.2f}, IdPass: {:08b}, IsoPass: {:08b}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.reliso(), p.idpass(), p.isopass() )


        tot_nevents += 1
        tot_genpart += len(event.genparticles())
        tot_genjet += len(event.genjets())
        tot_electron += len(event.electrons())
        tot_gamma += len(event.gammas())
        tot_muon += len(event.muons())
        tot_jetschs += len(event.jetschs())
        tot_jetspuppi += len(event.jetspuppi())
        #tot_jetsAK8 += len(event.jetsAK8())
        tot_tau += len(event.taus())
        tot_metspf += len(event.metspf())
        tot_metspuppi += len(event.metspuppi())



        # for genPart in genParts:
        #     print(tot_nevents, "genPart pt:", genPart.pt()

    print("Processed %d events" % tot_nevents)
    print("On average %f generator particles" % (float(tot_genpart) / tot_nevents))
    print("On average %f generated jets" % (float(tot_genjet) / tot_nevents))
    print("On average %f electrons" % (float(tot_electron) / tot_nevents))
    print("On average %f photons" % (float(tot_gamma) / tot_nevents))
    print("On average %f muons" % (float(tot_muon) / tot_nevents))
    print("On average %f jetschs" % (float(tot_jetschs) / tot_nevents))
    print("On average %f jetspuppi" % (float(tot_jetspuppi) / tot_nevents))
    #print("On average %f jetsAK8" % (float(tot_jetAK8) / tot_nevents))
    print("On average %f taus" % (float(tot_tau) / tot_nevents))
    print("On average %f metspf" % (float(tot_metspf) / tot_nevents))
    print("On average %f metspuppi" % (float(tot_metspuppi) / tot_nevents))

if __name__ == "__main__":
    main()
