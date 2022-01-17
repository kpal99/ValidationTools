#import contextlib2
import ROOT
import sys

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
f = ROOT.TFile.Open(sys.argv[1], 'read')
g = ROOT.TFile.Open(sys.argv[2], 'read')

#reading very many histrograms
hists = f.Get("St")
hists_g = g.Get("St")

outputDir = '/eos/uscms/store/user/kpal/rp/'
outputFile = sys.argv[1]
out_str = outputFile.split('.root')
filename = out_str[0].split('/')
hh = filename[ len(filename) - 1 ]
h = hh.split('_plot')[0]

legend = ROOT.TLegend(0.64,0.89,0.89,0.75)
canvas = ROOT.TCanvas('canvas','',900,900)
rp = ROOT.TRatioPlot(hists, hists_g)
hists.SetLineColor(3)
hists.Draw("hist")
hists_g.Draw("same hist")
legend.AddEntry(hists,h)
legend.AddEntry(hists_g,"bkg")
rp.Draw()
legend.Draw()
canvas.SaveAs(outputDir + h + ".png")
canvas.SaveAs(outputDir + h + ".pdf")
canvas.SaveAs(outputDir + h + ".root")
canvas.Close()
legend.Clear()


f.Close()
g.Close()
