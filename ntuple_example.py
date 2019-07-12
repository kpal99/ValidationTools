#!/usr/bin/env python
# import ROOT
from __future__ import print_function
from NtupleDataFormat import Ntuple
import sys


# The purpose of this file is to demonstrate mainly the objects
# that are in the HGCalNtuple

def main():
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)

    maxEvents = 10

    tot_nevents = 0r
    tot_genpart = 0

    for event in ntuple:
        if event.entry() >= maxEvents:
            break
        print("Event", event.entry()+1)
        tot_nevents += 1
        genParts = event.genParticles()
        tot_genpart += len(genParts)

        # for genPart in genParts:
        #     print(tot_nevents, "genPart pt:", genPart.pt()

    print("Processed %d events" % tot_nevents)
    print("On average %f generator particles" % (float(tot_genpart) / tot_nevents))

if __name__ == "__main__":
    main()
