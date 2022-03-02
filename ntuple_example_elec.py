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
    maxEvents = 0

    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        print '... processing event {} ... with genweight {}'.format(event.entry(), event.genweight())
        phy_obj=get_phy_obj(event,phy_obj_str)
        i=0;
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
            elif phy_obj_str == "electrons":
                print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, : Charge: {:<6}, idvar: {:<6}, idpass: {:<6}, reliso: {:<6.2f}, isopass: {:<6}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.idpass(), p.reliso(), p.isopass())
            elif phy_obj_str == "muons":
                print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, : Charge: {:<6}, idvar: {:<6}, idpass: {:<6}, reliso: {:<6.2f}, isopass: {:<6}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.idpass(), p.reliso(), p.isopass())
            else:
                print 'N: {:<7}, PT: {:<6.2f}, Phi: {:<6.2f}'.format(event.entry(), p.pt(), p.phi())


if __name__ == "__main__":
    main()
