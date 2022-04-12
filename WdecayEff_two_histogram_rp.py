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
        'TightMuons_pt','TightMuons_pt_cut']

hists = {}
for key in keys:
    hists[key] = f.Get(key)

outputDir = sys.argv[1].split('.root')[0]

tex1 = ROOT.TLatex(0.10, 0.97, "#bf{CMS} #it{Phase-2 Simulation Premilinary}")
tex1.SetNDC()
tex1.SetTextAlign(13)
tex1.SetTextFont(42)
tex1.SetTextSize(0.03)
tex1.SetLineWidth(2)

tex2 = ROOT.TLatex(0.69, 0.97, "3000 fb^{-1} (14 TeV)")
tex2.SetNDC()
tex2.SetTextAlign(13)
tex2.SetTextFont(42)
tex2.SetTextSize(0.03)
tex2.SetLineWidth(2)

for key in hists.keys():
    if "_pt_cut" in key and "Tight" in key:
        canvas = ROOT.TCanvas('canvas','',600,600)

        key_divide = key.split("_cut")[0] + key.split("_cut")[1]

        canvas.cd()
        pad1 = ROOT.TPad("pad1","pad1",0,0.4,1,1)
        pad1.SetLogy()
        pad1.SetBottomMargin(0)
        pad1.Draw()
        pad1.cd()
        hists[key].SetLineColor(1)
        hists[key].SetLineWidth(2)
        hists[key].SetTitle("")
        hists[key].GetXaxis().SetLabelSize(0.05)
        hists[key].GetYaxis().SetLabelSize(0.05)
        hists[key].GetYaxis().SetTitleSize(0.05)
        hists[key].GetYaxis().SetTitle("events/bin")

        maximum = 0
        for i in range(hists[key].GetNbinsX()):
            binContent = hists[key_divide].GetBinContent(i)
            if maximum < binContent:
                maximum = binContent

        hists[key].SetMaximum(5 * maximum)
        hists[key].SetMinimum(1)
        hists[key].Draw("hist")
        hists[key_divide].Draw("E same")

        canvas.cd()
        pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.4)
        pad2.SetTopMargin(0.0)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()
        hist = hists[key].Clone()
        hist.Reset()
        hist.Divide(hists[key],hists[key_divide],1,1,"B")
        hist.SetMinimum(0)
        hist.SetMaximum(1.1)
        hist.GetXaxis().SetLabelSize(0.07)
        hist.GetYaxis().SetLabelSize(0.07)
        hist.GetXaxis().SetTitleSize(0.07)
        hist.SetTitle("")
        hist.GetXaxis().SetTitle("P_{T} [GeV]")
        hist.GetYaxis().SetTitle("")
        hist.Draw("E")

        canvas.cd()

        legend1 = ROOT.TLegend(0.15,0.92,0.9,0.89)
        legend1.SetNColumns(2)
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
