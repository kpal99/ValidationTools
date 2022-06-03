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
    elif phy_obj_str == 'muons':
        return event.muons()
    elif phy_obj_str == 'electrons':
        return event.electrons()
    elif phy_obj_str == 'taus':
        return event.taus()
    elif phy_obj_str == 'gammas':
        return event.gammas()
    elif phy_obj_str == 'genjets':
        return event.genjets()
    elif phy_obj_str == 'jetschs':
        return event.jetschs()
    elif phy_obj_str == 'jetspuppi':
        return event.jetspuppi()
    elif phy_obj_str == 'jetsAK8':
        return event.jetsAK8()
    elif phy_obj_str == 'fatjets':
        return event.fatjets()
    elif phy_obj_str == 'metspuppi':
        return event.metspuppi()
    elif phy_obj_str == 'metspf':
        return event.metspf()
    elif phy_obj_str == 'lheweights':
        return event.lheweights()
    elif phy_obj_str == 'genparts':
        return event.genparticles()
    sys.exit("-- {} -- not implemented yet".format(phy_obj_str))

def main():
    if len(sys.argv) != 3:
        print "USAGE: %s <input file> <phy_object>".format(sys.argv[0])
        sys.exit(1)
    inFile = sys.argv[1]
    phy_obj_str=sys.argv[2]
    ntuple = Ntuple(inFile)
    maxEvents = 5

    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        if event.entry() > 0:
            print ""
        print '... processing event {} ... with genweight {}'.format(event.entry(), event.genweight())

        if phy_obj_str == "fatjets":
            print 'fatjetM: {:<6}, fatjetH2b: {:<6}, fatjetH1b: {:<6}, fatjetW: {:<6}'.format(event.fatjetM(), event.fatjetH2b() , event.fatjetH1b(), event.fatjetW())

        if phy_obj_str == "jetspuppi":
            print 'jetM: {:<6}, jetBtag: {:<6}, jetHt: {:<6}, jetSt: {:<6}'.format(event.jetM(), event.jetBtag() , event.jetHt(), event.jetSt())

        if phy_obj_str == "St":
            i=0
            for p in event.metspuppi():
                print 'MET.............. PT: {:<6.2f}, Phi: {:<6.2f}'.format(p.pt(), p.phi())
            for p in event.tightElectrons():
                print 'Tight Electron... PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, : Charge: {:<6}, idvar: {:<6}, idpass: {:<6}, reliso: {:<6.2f}, isopass: {:<6}'.format(p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.idpass(), p.reliso(), p.isopass())
            for p in event.tightMuons():
                print 'Tight Muon....... PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, : Charge: {:<6}, idvar: {:<6}, idpass: {:<6}, reliso: {:<6.2f}, isopass: {:<6}'.format(p.pt(), p.eta() , p.phi(), p.mass(), p.charge(), p.idvar(), p.idpass(), p.reliso(), p.isopass())
            print 'jetM: {:<6}, jetBtag: {:<6}, jetHt: {:<6}, jetSt: {:<6}'.format(event.jetM(), event.jetBtag() , event.jetHt(), event.jetSt())
            for p in event.jetspuppi():
                i += 1
                print 'N: {:<6}, PT: {:<6.2f}, Eta: {:<6.2f}, Phi: {:<6.2f}, M: {:<6.2f}, Btag: {:<6.2f}'.format(i, p.pt(), p.eta() , p.phi(), p.mass(), p.btag())
            continue

        phy_obj=get_phy_obj(event,phy_obj_str)
        i=0
        for p in phy_obj:
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
            elif phy_obj_str == "lheweights":
                if i < 10:
                    print 'N: :{:<6}, val: {:<6.2f}'.format(i, p.val())
            elif phy_obj_str == "genparts":
                if (p.pid()) == 11 or abs(p.pid()) == 13:
                    print 'N: {:<6}, pid: {:<6}, status: {:<6}, Pt: {:<6.2f}, eta: {:<6.2f}, Phi: {:<6.2f}, mass: {:<6.2f}, Mother1: {:<6}, Mother2: {:<6}, tochter1: {:<6}, tochter2: {:<6}'.format(i, p.pid(), p.status() , p.pt(), p.eta(), p.phi(), p.mass(), p.m1(), p.m2(), p.d1(), p.d2())
            else:
                print 'N: {:<7}, PT: {:<6.2f}, Phi: {:<6.2f}'.format(event.entry(), p.pt(), p.phi())
            i += 1


if __name__ == "__main__":
    main()
