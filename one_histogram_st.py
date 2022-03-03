#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys
import os

# create and return histrogram automatically
def createHist(varname,minval=0, maxval=501):
    binval = 25
    elif "St" in varname:
        h = ROOT.TH1D(varname, varname, binval, 500, 8000)
        #h = ROOT.THD(varname, varname, binval, 2000, 9000)
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

    outDir = os.path.dirname(sys.argv[2]) + '/rootPlots_st/'
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
