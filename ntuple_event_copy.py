#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
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
    phy_obj_str="fatjets"
    ntuple = Ntuple(inFile)
    maxEvents = 5

    fatjet_size = 0
    metpuppi_size = 0
    fatjet_pt = []
    fatjet_eta = []
    fatjet_phi = []
    fatjet_mass = []
    fatjet_tau1 = []
    fatjet_tau2 = []
    fatjet_tau3 = []
    fatjet_tau4 = []
    fatjet_msoftdrop = []

    metpuppi_pt = []
    metpuppi_eta = []

    outFile = ROOT.TFile('trim_example.root',"RECREATE")
    T = ROOT.TTree("myana/mytree", "mytree")
    T.Branch("fatjet_size", fatjet_size, "fatjet_size/I")
    T.Branch("fatjet_pt", fatjet_pt, "fatjet_pt[fatjet_size]/F")
    T.Branch("fatjet_eta", fatjet_eta, "fatjet_eta[fatjet_size]/F")
    T.Branch("fatjet_phi", fatjet_phi, "fatjet_phi[fatjet_size]/F")
    T.Branch("fatjet_mass", fatjet_mass, "fatjet_mass[fatjet_size]/F")
    T.Branch("fatjet_tau1", fatjet_tau1, "fatjet_tau1[fatjet_size]/F")
    T.Branch("fatjet_tau2", fatjet_tau2, "fatjet_tau2[fatjet_size]/F")
    T.Branch("fatjet_tau3", fatjet_tau3, "fatjet_tau3[fatjet_size]/F")
    T.Branch("fatjet_tau4", fatjet_tau4, "fatjet_tau4[fatjet_size]/F")
    T.Branch("fatjet_msoftdrop", fatjet_msoftdrop, "fatjet_msoftdrop[fatjet_size]/F")
    T.Branch("metpuppi_size", metpuppi_size, "metpuppi_size/I")
    T.Branch("metpuppi_pt", metpuppi_pt, "metpuppi_pt[metpuppi_size]/F")
    T.Branch("metpuppi_eta", metpuppi_eta, "metpuppi_eta[metpuppi_size]/F")



    print(ntuple.__dict__)
    for event in ntuple:
        if event.entry() >= maxEvents and maxEvents > 0:
            break

        fatjet_pt = []
        fatjet_eta = []
        fatjet_phi = []
        fatjet_mass = []
        fatjet_tau1 = []
        fatjet_tau2 = []
        fatjet_tau3 = []
        fatjet_tau4 = []
        fatjet_msoftdrop = []

        metpuppi_pt = []
        metpuppi_eta = []
        for p in phy_obj:

            fatjet_pt.append(p.pt())
            fatjet_eta.append(p.eta())
            fatjet_phi.append(p.phi())
            fatjet_mass.append(p.mass())
            fatjet_tau1.append(p.tau1())
            fatjet_tau2.append(p.tau2())
            fatjet_tau3.append(p.tau3())
            fatjet_tau4.append(p.tau4())
            fatjet_msoftdrop(p.msoftdrop())
        fatjet_size = len(fatjet_pt)

        for p in get_phy_obj(event, "metspuppi"):
            metpuppi_pt.append(p.pt())
            metpuppi_eta.append(p.eta())
        metpuppi_size = len(metpuppi_pt)

        T.Fill()

    T.Write()
    outFile.Close()

if __name__ == "__main__":
    main()
