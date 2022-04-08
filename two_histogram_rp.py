#import contextlib2
import ROOT
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

if len(sys.argv) != 2:
    print "USAGE: {} <plot_file>".format(sys.argv[0])
    sys.exit(1)

f = ROOT.TFile.Open(sys.argv[1], 'read')

keys = ['TightElectrons_pt','TightElectrons_pt_cut',
        'TightMuons_pt','TightMuons_pt_cut',
        'jetspuppi_pt_1','jetspuppi_pt_cut_1',
        'jetspuppi_pt_2','jetspuppi_pt_cut_2',
        'jetspuppi_pt_3','jetspuppi_pt_cut_3']

hists = {}
for key in keys:
    hists[key] = f.Get(key)

outputDir = sys.argv[1].split('.root')[0]

tex1 = ROOT.TLatex(0.10, 0.96, "#bf{CMS} #it{Phase-2 Simulation Premilinary}")
tex1.SetNDC()
tex1.SetTextAlign(13)
tex1.SetTextFont(42)
tex1.SetTextSize(0.03)
tex1.SetLineWidth(2)

tex2 = ROOT.TLatex(0.68, 0.96, "3000 fb^{-1} (14 TeV)")
tex2.SetNDC()
tex2.SetTextAlign(13)
tex2.SetTextFont(42)
tex2.SetTextSize(0.03)
tex2.SetLineWidth(2)

for key in hists.keys():
    if "_pt_cut" in key and "Tight" in key:
        canvas = ROOT.TCanvas('canvas','',600,600)
        canvas.SetLogy()

        key_divide = key.split("_cut")[0] + key.split("_cut")[1]

        rp = ROOT.TRatioPlot(hists[key], hists[key_divide])
        hists[key].SetLineColor(1)
        hists[key].SetLineWidth(2)
        hists[key].SetTitle("")
        hists[key].GetXaxis().SetTitle("P_{T} [GeV]")
        hists[key].GetYaxis().SetTitle("events/bin")

        maximum = 0
        for i in range(hists[key].GetNbinsX()):
            binContent = hists[key_divide].GetBinContent(i)
            if maximum < binContent:
                maximum = binContent

        rp.Draw()
        rp.GetUpperRefYaxis().SetRangeUser(0, 1)
        rp.GetUpperRefYaxis().SetRangeUser(1, 2 * maximum)

        legend1 = ROOT.TLegend(0.55,0.90,0.89,0.80)
        legend1.SetBorderSize(0)
        legend1.AddEntry(hists[key],"w/o reliso cut", "l")
        legend1.AddEntry(hists[key_divide],"w reliso 0.1(0.15) cut", "l")
        legend1.Draw()

        tex1.Draw()
        tex2.Draw()
        canvas.SaveAs(outputDir + "_" + key + ".png")
        canvas.SaveAs(outputDir + "_" + key + ".pdf")
        canvas.Close()

    if "jetspuppi_pt_cut_" in key:
        canvas = ROOT.TCanvas('canvas','',600,600)
        canvas.SetLogy()

        key_divide = key.split("_cut")[0] + key.split("_cut")[1]

        rp = ROOT.TRatioPlot(hists[key], hists[key_divide])
        hists[key].SetLineColor(1)
        hists[key].SetLineWidth(2)
        hists[key].SetTitle("")
        hists[key].GetXaxis().SetTitle("P_{T} [GeV]")
        hists[key].GetYaxis().SetTitle("events/bin")

        maximum = 0
        for i in range(hists[key].GetNbinsX()):
            binContent = hists[key_divide].GetBinContent(i)
            if maximum < binContent:
                maximum = binContent

        rp.Draw()
        rp.GetUpperRefYaxis().SetRangeUser(0, 1)
        rp.GetUpperRefYaxis().SetRangeUser(1, 2 * maximum)

        legend1 = ROOT.TLegend(0.55,0.45,0.89,0.35)
        legend1.SetBorderSize(0)
        legend1.AddEntry(hists[key],"w/o reliso cut", "l")
        legend1.AddEntry(hists[key_divide],"w reliso 0.1(0.15) cut", "l")
        legend1.Draw()

        tex1.Draw()
        tex2.Draw()
        canvas.SaveAs(outputDir + "_" + key + ".png")
        canvas.SaveAs(outputDir + "_" + key + ".pdf")
        canvas.Close()

f.Close()
