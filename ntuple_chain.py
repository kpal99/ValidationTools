#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys

def ntuple_chain(string_file):
    txtFile = open(string_file, 'r')
    lines = txtFile.readlines()
    ntuple_array = []
    for line in lines:
        #print line.strip()
        ntuple_array.append(Ntuple(line.strip()))
    return ntuple_array


def main():
    tot_event = 0
    ntuple_array = ntuple_chain(sys.argv[1])
    for ntuple in ntuple_array:
        tot_event += ntuple.nevents() + 1

    print "Total Events {}".format(tot_event)

if __name__ == "__main__":
    main()
