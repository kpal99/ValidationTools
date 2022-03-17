import ROOT
import sys
import os
import math
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

f = ROOT.TFile.Open(sys.argv[1], 'read')
outputDir = sys.argv[1].split('.root')[0]


hists = {}
hists["TightElectrons_pt"] = f.Get("TightElectrons_pt")
hists["TightMuons_pt"] = f.Get("TightMuons_pt")
hists["jetspuppi_pt"] = f.Get("jetspuppi_pt")
hists["Elec_reliso_met"] = f.Get("Elec_reliso_met")
hists["Muon_reliso_met"] = f.Get("Muon_reliso_met")
hists["Elec_reliso_pT"] = f.Get("Elec_reliso_pt")
hists["Muon_reliso_pT"] = f.Get("Muon_reliso_pt")

hists["TightElectrons_pt_cut"] = f.Get("TightElectrons_pt_cut")
hists["TightMuons_pt_cut"] = f.Get("TightMuons_pt_cut")
hists["jetspuppi_pt_cut"] = f.Get("jetspuppi_pt_cut")
hists["Elec_reliso_met_cut"] = f.Get("Elec_reliso_met_cut")
hists["Muon_reliso_met_cut"] = f.Get("Muon_reliso_met_cut")
hists["Elec_reliso_pT_cut"] = f.Get("Elec_reliso_pt_cut")
hists["Muon_reliso_pT_cut"] = f.Get("Muon_reliso_pt_cut")

tex1 = ROOT.TLatex(0.10, 0.95, "#bf{CMS} #it{Phase-2 Simulation Premilinary}")
tex1.SetNDC()
tex1.SetTextAlign(13)
tex1.SetTextFont(42)
tex1.SetTextSize(0.04)
tex1.SetLineWidth(2)

tex2 = ROOT.TLatex(0.71, 0.95, "3000 fb^{-1} (14 TeV)")
tex2.SetNDC()
tex2.SetTextAlign(13)
tex2.SetTextFont(42)
tex2.SetTextSize(0.04)
tex2.SetLineWidth(2)

for key in hists.keys():
    if "reliso" in key:
        canvas = ROOT.TCanvas('canvas','',600,400)
        hists[key].SetTitle("")
        if "met" in key:
            hists[key].GetXaxis().SetTitle("E_{T}^{miss} [GeV]")
        elif "pT" in key:
            hists[key].GetXaxis().SetTitle("p_{T} [GeV]")
        hists[key].GetYaxis().SetTitle("reliso")
        hists[key].Draw("COLZ")
        tex1.Draw()
        tex2.Draw()
        canvas.SaveAs(outputDir + "_" + key + ".png")
        canvas.SaveAs(outputDir + "_" + key + ".pdf")
        canvas.Close()

for key in hists.keys():
    if "_pt_cut" in key:
        canvas = ROOT.TCanvas('canvas','',600,400)
        hists[key].SetLineColor(1)
        hists[key].SetTitle("")
        hists[key].GetXaxis().SetTitle("P_{T} [GeV]")
        hists[key].GetYaxis().SetTitle("Efficiency")
        hists[key].Divide(hists[key.split("_cut")[0]])
        hists[key].Draw("E")
        tex1.Draw()
        tex2.Draw()
        if "Elec" in key:
            canvas.SaveAs(outputDir + "_" + "elecIsolation" + ".png")
            canvas.SaveAs(outputDir + "_" + "elecIsolation" + ".pdf")
        elif "Muon" in key:
            canvas.SaveAs(outputDir + "_" + "muonIsolation" + ".png")
            canvas.SaveAs(outputDir + "_" + "muonIsolation" + ".pdf")
        elif "jetspuppi" in key:
            canvas.SaveAs(outputDir + "_" + "btag" + ".png")
            canvas.SaveAs(outputDir + "_" + "btag" + ".pdf")
        canvas.Close()

    elif "_pt" in key:
        canvas = ROOT.TCanvas('canvas','',600,400)
        canvas.SetLogy()
        hists[key].SetLineColor(1)
        hists[key].SetTitle("")
        hists[key].GetXaxis().SetTitle("P_{T} [GeV]")
        hists[key].GetYaxis().SetTitle("events/bin")
        hists[key].Draw("E")
        tex1.Draw()
        tex2.Draw()
        canvas.SaveAs(outputDir + "_" + key + ".png")
        canvas.SaveAs(outputDir + "_" + key + ".pdf")
        canvas.Close()
