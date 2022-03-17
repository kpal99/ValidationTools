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
        tex1.Clear()
        tex2.Clear()

for key in hists.keys():
    if "_pt_cut" in key:
        canvas = ROOT.TCanvas('canvas','',600,400)
        hists_eff = hists[key].Clone()
        hists_eff.Reset()
        for i in range(hists_eff.GetNbinsX() + 1):
            try:
                eff = hists[key].GetBinContent(i) / hists[key.split("_cut")[0]].GetBinContent(i)
                eff_err = math.sqrt(hists[key].GetBinContent(i) * eff * (1 - eff))
            except ZeroDivisionError:
                eff = 0
                eff_err = 0
            hists_eff.SetBinContent(i,eff)
            hists_eff.SetBinError(i,eff_err)
        hists_eff.SetLineColor(1)
        hists_eff.SetTitle("")
        hists_eff.GetXaxis().SetTitle("P_{T} [GeV]")
        hists_eff.GetYaxis().SetTitle("Efficiency")
        hists_eff.Draw("E")
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
        tex1.Clear()
        tex2.Clear()

    elif "_pt" in key:
        canvas = ROOT.TCanvas('canvas','',600,400)
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
        tex1.Clear()
        tex2.Clear()
