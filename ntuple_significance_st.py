#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
import sys


def main():
    if len(sys.argv) < 3:
        print "USAGE: %s <background file> <Signal file(s)>".format(sys.argv[0])
        sys.exit(1)
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    bkg = ROOT.TFile.Open(sys.argv[1], 'read')   #opening bkg files
    f = ROOT.TFile.Open(sys.argv[2], 'read')    #opening signal files
    g = ROOT.TFile.Open(sys.argv[3], 'read')
    signal_file = 2             #signal file count

    hist_bkg = bkg.Get("St")            #get St histogram of the bkg file
    hist_sig = []
    hist_sig.append(f.Get("St"))        #appending St histogram of signal file
    hist_sig.append(g.Get("St"))

    maxEvents = 0
    st_array = range(100,6001,100)
    sig_count = [ [0] * len(st_array) for i in range(signal_file)]
    bkg_count = [0] * len(st_array)

    bmax = hist_bkg.GetXaxis().FindBin(6000)

    for i in range( len(st_array) ):
        bmin = hist_bkg.GetXaxis().FindBin(st_array[i])
        bkg_count[i] = hist_bkg.Integral(bmin,bmax)

    for file_num in range(signal_file):
        for i in range( len(st_array) ):
            #if st_array[i] > st:
            bmin = hist_sig[file_num].GetXaxis().FindBin(st_array[i])
            sig_count[file_num][i] = hist_sig[file_num].Integral(bmin,bmax)

    gr = ROOT.TGraphErrors()
    for file_num in range(signal_file):
        canvas = ROOT.TCanvas('canvas','',700,500)
        for i in range( len(st_array) ):
            significance = sig_count[file_num][i] / (sig_count[file_num][i] + bkg_count[i])**0.5
            delta_significance = significance * ( 1/ sig_count[file_num][i] ** 0.5 + 1/2 * ( sig_count[file_num][i] ** 0.5 + bkg_count[i] ** 0.5 ) / ( sig_count[file_num][i] + bkg_count[i] ) )
            print "{} \t {} \t {}".format(st_array[i], significance, delta_significance)
            gr.SetPoint(i, st_array[i],significance)
            gr.SetPointError(i, 0,delta_significance)

        gr.SetTitle("TT M = "+ str(1000 + 500 * file_num) + " GeV")
        gr.GetXaxis().SetTitle("S_{T} [GeV]")
        gr.GetYaxis().SetTitle("significance")
        gr.Draw("ALP")
        canvas.SaveAs("significance"+ str(file_num) + ".png")
        canvas.Close()

if __name__ == "__main__":
    main()
