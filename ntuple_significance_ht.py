#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys


def main():
    if len(sys.argv) < 3:
        print "USAGE: %s <background file> <Signal file(s)>".format(sys.argv[0])
        sys.exit(1)
    inFile_bkg  = sys.argv[1]
    ntuple_sig = []
    for signal in sys.argv[2:]:
        ntuple_sig.append(Ntuple(signal))
    ntuple_bkg = Ntuple(inFile_bkg)

    maxEvents = 0
    ht_array = range(100,4001,100)
    sig_count = [ [0] * len(ht_array) for i in range(len(ntuple_sig))]
    bkg_count = [0] * len(ht_array)

    file_num = 0
    for ntuple_sig1 in ntuple_sig:
        for event in ntuple_sig1:
            if event.entry() >= maxEvents and maxEvents > 0:
                break

            sum_pt = 0
            for item in event.jetspuppi():
                sum_pt += item.pt()
            ht = sum_pt
            for i in range( len(ht_array) ):
                if ht > ht_array[i]:
                    sig_count[file_num][i] += 1

        file_num += 1

    for event in ntuple_bkg:
        if event.entry() >= maxEvents and maxEvents > 0:
            break

        sum_pt = 0
        for item in event.jetspuppi():
            sum_pt += item.pt()
        ht = sum_pt
        for i in range( len(ht_array) ):
            if ht > ht_array[i]:
                bkg_count[i] += 1

    ROOT.gROOT.SetBatch()
    gr = ROOT.TGraphErrors()

    for file_num in range(len(ntuple_sig)):
        canvas = ROOT.TCanvas('canvas','',700,500)
        for i in range( len(ht_array) ):
            significance = sig_count[file_num][i] / (sig_count[file_num][i] + bkg_count[i])**0.5
            delta_significance = significance * ( 1/ sig_count[file_num][i] ** 0.5 + 1/2 * ( sig_count[file_num][i] ** 0.5 + bkg_count[i] ** 0.5 ) / ( sig_count[file_num][i] + bkg_count[i] ) )
            print "{} \t {} \t {}".format(ht_array[i], significance, delta_significance)
            gr.SetPoint(i, ht_array[i],significance)
            gr.SetPointError(i, 0,delta_significance)

        gr.SetTitle("TT M = "+ str(1000 + 500 * file_num) + " GeV")
        gr.GetXaxis().SetTitle("H_{T} [GeV]")
        gr.GetYaxis().SetTitle("significance")
        gr.Draw("ALP")
        canvas.SaveAs("significance_ht"+ str(file_num) + ".png")
        canvas.Close()

if __name__ == "__main__":
    main()
