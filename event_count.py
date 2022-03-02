#import contextlib2
import ROOT
import sys
import os

if len(sys.argv) < 2:
    print "USAGE: {} <ntuple(s)_plot>".format(sys.argv[0])
    sys.exit(1)
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
for arg in sys.argv[1:]:
    file1 = ROOT.TFile.Open(arg,'read')
    hist_st = file1.Get("St")
    all_channel = hist_st.Integral(0,101)
    hist_electron = file1.Get("TightElectrons_eta")
    hist_muon = file1.Get("TightMuons_eta")
    electron_channel = hist_electron.Integral(0,101)
    muon_channel = hist_muon.Integral(0,101)
    print "{:<100}    {:<20}     {:<20}     {:<20}".format(os.path.basename(arg), electron_channel , muon_channel, all_channel)
    #print "{:<100}    {:<20}".format(os.path.basename(arg), all_channel)
    file1.Close()
