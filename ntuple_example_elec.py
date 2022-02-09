#!/usr/bin/env python
# import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys


# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple
def get_phy_obj(event,phy_obj_str):
    if phy_obj_str == 'vtxs':
        return event.vtxs()
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
    if len(sys.argv) != 3:
        print "USAGE: %s <input file> <phy_object>".format(sys.argv[0])
        sys.exit(1)
    inFile = sys.argv[1]
    phy_obj_str=sys.argv[2]
    ntuple = Ntuple(inFile)
    maxEvents = 5

    tot_nevents = 0
    tot_genpart = 0
    tot_genjet = 0
    tot_electron = 0
    tot_gamma = 0
    tot_muon = 0
    tot_jetschs = 0
    tot_jetspuppi = 0
    tot_fatjets = 0
    tot_tau = 0
    tot_metspf = 0
    tot_metspuppi = 0
    print(ntuple.__dict__)
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break


        print '... processing event {} ... with genweight {}'.format(event.entry()+1, event.genweight())

        #print ''
        #print '  -- {}  --'.format(phy_obj_str)
        #print ''

        phy_obj=get_phy_obj(event,phy_obj_str)
        i=0;
#print(phy_obj.__dict__)
        for p in phy_obj:
            i += 1
            if phy_obj_str == "fatjets":
                print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, Tau1: {:<6.2f}, Tau2: {:<6.2f}, Tau3: {:<6.2f}, Tau4: {:<6.2f}, m-SD: {:<6.2f}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.tau1(), p.tau2(), p.tau3(), p.tau4(), p.msoftdrop())
            elif phy_obj_str == "vtxs":
                print 'N: {:<6}, Pt2: {:<6.2f}, z: {:<6.2f}, x: {:<6}, y: {:<6}'.format(i, p.pt2() , p.z(), p.x(), p.y())
                if i == 1:
                    break
            elif phy_obj_str == "gammas":
                print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, idvar: {:<6}, isopass: {:<6}'.format(i, p.pt(), p.eta() , p.phi(), p.idvar(), p.isopass())
            elif phy_obj_str == "jetspuppi":
                print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, Btag: {:<6.2f}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.btag())
            elif phy_obj_str == "jetspuppi":
                print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, Btag: {:<6.2f}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.btag())
            elif phy_obj_str == "electrons" or phy_obj_str == "muons":
                print 'event: {:<12}, N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, : Charge: {:<6}, idvar: {:<6}, idpass: {:<6}, reliso: {:<6.2f}, isopass: {:<6}'.format(event.entry()+1, i, p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.idpass(), p.reliso(), p.isopass())
            else:
                print 'N: {:<7}, PT: {:<6.2f}, Phi: {:<6.2f}'.format(i, p.pt(), p.phi())


    tot_nevents += ntuple.nevents() + 1
#        tot_genpart += len(event.genparticles())
#        tot_genjet += len(event.genjets())
#        tot_electron += len(event.electrons())
#        tot_gamma += len(event.gammas())
#        tot_muon += len(event.muons())
#        tot_jetschs += len(event.jetschs())
#        tot_jetspuppi += len(event.jetspuppi())
#        tot_fatjets += len(event.fatjets())
#        tot_tau += len(event.taus())
#        tot_metspf += len(event.metspf())
#        tot_metspuppi += len(event.metspuppi())

        # for genPart in genParts:
        #     print(tot_nevents, "genPart pt:", genPart.pt()

    print("Processed %d events" % tot_nevents)
#    print("On average %f generator particles" % (float(tot_genpart) / tot_nevents))
#    print("On average %f generated jets" % (float(tot_genjet) / tot_nevents))
#    print("On average %f electrons" % (float(tot_electron) / tot_nevents))
#    print("On average %f photons" % (float(tot_gamma) / tot_nevents))
#    print("On average %f muons" % (float(tot_muon) / tot_nevents))
#    print("On average %f jetschs" % (float(tot_jetschs) / tot_nevents))
#    print("On average %f jetspuppi" % (float(tot_jetspuppi) / tot_nevents))
#    print("On average %f fatjets" % (float(tot_fatjets) / tot_nevents))
#    print("On average %f taus" % (float(tot_tau) / tot_nevents))
#    print("On average %f metspf" % (float(tot_metspf) / tot_nevents))
#    print("On average %f metspuppi" % (float(tot_metspuppi) / tot_nevents))

if __name__ == "__main__":
    main()
