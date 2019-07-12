#!/usr/bin/env python
import ROOT, math, sys
from array import array
import itertools

## This example  prints basic information about the tree content ##


#________________________________________________________________________

inputFile = sys.argv[1]

f = ROOT.TFile.Open(inputFile)
tree=f.Get("myana/mytree")
nev = tree.GetEntries()



nev = 5
for iev in range(0,nev) :
    tree.GetEntry(iev)

    if (iev+1)%1000 == 0:
       print ' ... processed {} events ...'.format(iev+1)
       
    print ' '    
    print ' -------------- new event -----------------'
    print ' '    


    ###### loop over gen particles ######

    i = 0
    print ''
    print '  -- gen parts --'
    print ''
    for pid, pt, eta, phi, m, m1, m2, d1, d2, status in itertools.izip(getattr(tree, 'genpart_{}'.format('pid')), 
                                                                       getattr(tree, 'genpart_{}'.format('pt')),
                                                                       getattr(tree, 'genpart_{}'.format('eta')),
                                                                       getattr(tree, 'genpart_{}'.format('phi')),
                                                                       getattr(tree, 'genpart_{}'.format('mass')),
                                                                       getattr(tree, 'genpart_{}'.format('m1')),
                                                                       getattr(tree, 'genpart_{}'.format('m2')),
                                                                       getattr(tree, 'genpart_{}'.format('d1')),
                                                                       getattr(tree, 'genpart_{}'.format('d2')),
                                                                       getattr(tree, 'genpart_{}'.format('status'))):

        etap = eta
        if eta > 10:
           etap = 999.
        if eta < -10:
           etap = -999.
        
        print 'N: {:<5}, St: {:<5}, PID: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  M1: {:<5}, M2: {:<5}, D1: {:<5}, D2: {:<5}'.format(i, status, pid, pt, etap, phi, m, m1, m2, d1, d2) 
        i += 1
        



    ###### loop over reco electrons ######
    i = 0
    
    print ''
    print '  -- electrons --'
    print ''
    for pt, eta, phi, m, charge, idvar, isovar, idpass, isopass in itertools.izip(getattr(tree, 'elec_{}'.format('pt')),
                                                                                  getattr(tree, 'elec_{}'.format('eta')),
                                                                                  getattr(tree, 'elec_{}'.format('phi')),
                                                                                  getattr(tree, 'elec_{}'.format('mass')),
                                                                                  getattr(tree, 'elec_{}'.format('charge')),
                                                                                  getattr(tree, 'elec_{}'.format('idvar')),
                                                                                  getattr(tree, 'elec_{}'.format('reliso')),
                                                                                  getattr(tree, 'elec_{}'.format('idpass')),
                                                                                  getattr(tree, 'elec_{}'.format('isopass'))):


        print 'N: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  Charge: {:<5}, IdVar: {:<5.2f}, IsoVar: {:<5.2f}, IdPass: {:08b}, IsoPass: {:08b}'.format(i, pt, eta , phi, m, charge, idvar, isovar, idpass, isopass )
        i += 1


    ###### loop over reco electrons ######

    i = 0
    
    print ''
    print '  -- muons --'
    print ''
    for pt, eta, phi, m, charge, idvar, isovar, idpass, isopass in itertools.izip(getattr(tree, 'muon_{}'.format('pt')),
                                                                                  getattr(tree, 'muon_{}'.format('eta')),
                                                                                  getattr(tree, 'muon_{}'.format('phi')),
                                                                                  getattr(tree, 'muon_{}'.format('mass')),
                                                                                  getattr(tree, 'muon_{}'.format('charge')),
                                                                                  getattr(tree, 'muon_{}'.format('idvar')),
                                                                                  getattr(tree, 'muon_{}'.format('reliso')),
                                                                                  getattr(tree, 'muon_{}'.format('idpass')),
                                                                                  getattr(tree, 'muon_{}'.format('isopass'))):


        print 'N: {:<5}, PT: {:<5.2f}, Eta: {:<5.2f}, Phi: {:<5.2f}, M: {:<5.2f},  Charge: {:<5}, IdVar: {:<5.2f}, IsoVar: {:<5.2f}, IdPass: {:08b}, IsoPass: {:08b}'.format(i, pt, eta , phi, m, charge, idvar, isovar, idpass, isopass )
        i += 1




