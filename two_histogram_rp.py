#import contextlib2
import ROOT
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
f = ROOT.TFile.Open(sys.argv[1], 'read')
g = ROOT.TFile.Open(sys.argv[2], 'read')

#reading very many histrograms
hists_f = f.Get("St")
hists_g = g.Get("St")

hists_f.Scale(1./hists_f.Integral())
hists_g.Scale(1./hists_g.Integral())
outputDir = '/eos/uscms/store/user/kpal/rp/'
h1 = os.path.basename(sys.argv[1]).split('_plot.root')[0]
g1 = os.path.basename(sys.argv[2]).split('_plot.root')[0]

legend = ROOT.TLegend(0.64,0.89,0.89,0.75)
canvas = ROOT.TCanvas('canvas','',900,900)
canvas.SetLogy()
rp = ROOT.TRatioPlot(hists_f, hists_g)
hists_f.SetLineColor(3)
hists_f.Draw("hist")
hists_g.Draw("same hist")
legend.AddEntry(hists_f,h1)
legend.AddEntry(hists_g,g1)
rp.Draw()
legend.Draw()
canvas.SaveAs(outputDir + h1 + ".png")
canvas.SaveAs(outputDir + h1 + ".pdf")
canvas.SaveAs(outputDir + h1 + ".root")
canvas.Close()
legend.Clear()

f.Close()
g.Close()
