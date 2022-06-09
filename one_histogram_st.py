#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from array import array
import sys
import os

# create and return histrogram automatically
def createHist(varname,minval=0, maxval=501):
    binval = 25
    if "St" in varname:
        varBin = []
        minval = 500
        increment = 200
        add2 = 7000
        if "h1b" in sys.argv[1]:
            compare = 5000
            add1 = 6000
        elif "h2b" in sys.argv[1]:
            compare = 4400
            add1 = 5000
        elif "w3b" in sys.argv[1]:
            compare = 3600
            add1 = 4800
        elif "w2b" in sys.argv[1]:
            compare = 3600
            add1 = 5000
        elif "w1b" in sys.argv[1]:
            compare = 3000
            add1 = 4600
        elif "_3b" in sys.argv[1]:
            compare = 4200
            add1 = 4900
        elif "_2b" in sys.argv[1]:
            compare = 4200
            add1 = 4900
        elif "_1b" in sys.argv[1]:
            compare = 3800
            add1 = 4300
        else:
            compare = 5400
            add1 = 6000
        while minval < compare:
            varBin.append(minval)
            minval += increment
        varBin.append(add1)
        varBin.append(add2)
        h = ROOT.TH1D(varname, varname, len(varBin)-1, array('d',varBin))
    else:
        h = ROOT.TH1D(varname,varname,binval,minval,maxval)
    h.Sumw2()
    return h

def main():
    if len(sys.argv) != 5:
        print("USAGE: {} <ntuple> <cross-section(fb)> <total event> <Initial genweight>".format(sys.argv[0]))
        sys.exit(1)

    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    hists = {}
    maxEvents = 0

    outDir = os.path.dirname(sys.argv[1]) + '/rootPlots_st/'
    out_str = os.path.basename(sys.argv[1])
    outFile = ROOT.TFile(outDir + out_str,"RECREATE")

# creating histrogram
    hists["St"] = createHist("St")

# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        gen_weight = event.genweight()
        hists["St"].Fill(event.jetSt(), gen_weight)

    scale_factor = 3000  * float(sys.argv[2]) / float(sys.argv[4])
    for h in hists.keys():
        hists[h].Scale(scale_factor)
    outFile.Write()
    print("OutFile written at {}".format(outFile))

if __name__ == "__main__":
    main()
