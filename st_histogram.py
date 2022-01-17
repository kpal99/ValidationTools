#import contextlib2
import ROOT
import sys
import os

if len(sys.argv) != 5:
    print "USAGE: {} <TT_M1500.root> <TOP.root> <EW.root> <QCD.root>".format(sys.argv[0])
    sys.exit(1)
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
f = ROOT.TFile.Open(sys.argv[1], 'read')
g = ROOT.TFile.Open(sys.argv[2], 'read')
h = ROOT.TFile.Open(sys.argv[3], 'read')
i = ROOT.TFile.Open(sys.argv[4], 'read')

#reading very many histrograms
hist_f = f.Get("St")
hist_g = g.Get("St")
hist_h = h.Get("St")
hist_i = i.Get("St")
#hist_j = ROOT.TH1D("data_obs","data_obs",100,0,7000)
hist_j = ROOT.TH1D("data_obs","data_obs",50,500,7500)

#outputDir = os.path.dirname(sys.argv[4]) + '/'
outputDir = os.path.dirname(sys.argv[4]) + '/plotsNewQCDsamples/'
a=sys.argv[1].split('TT')
outFile = ROOT.TFile(outputDir + 'St' + a[1] ,"RECREATE")
hist_j.Add(hist_f)
hist_j.Add(hist_g)
hist_j.Add(hist_h)
hist_j.Add(hist_i)
hist_f.SetName("St_signal"); hist_f.Write("St_signal",ROOT.TObject.kWriteDelete)
hist_g.SetName("St_top"); hist_g.Write("St_top",ROOT.TObject.kWriteDelete)
hist_h.SetName("St_ew"); hist_h.Write("St_ew",ROOT.TObject.kWriteDelete)
hist_i.SetName("St_qcd"); hist_i.Write("St_qcd",ROOT.TObject.kWriteDelete)
hist_j.SetName("data_obs"); hist_j.Write("data_obs",ROOT.TObject.kWriteDelete)
outFile.Write()

outFile.Close()
f.Close()
g.Close()
h.Close()
i.Close()
