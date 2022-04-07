import ROOT
import sys
import os
import math
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

if len(sys.argv) != 8:
    print "USAGE: {} <QCD500> <QCD700>  <QCD1000> <QCD1500> <QCD2000> <TT_M1000> <WJetsToLNu>".format(sys.argv[0])
    sys.exit(1)

outputDir = os.path.dirname(sys.argv[1]) + '/efficiency'

qcd500 = ROOT.TFile.Open(sys.argv[1], 'read')
qcd700 = ROOT.TFile.Open(sys.argv[2], 'read')
qcd1000 = ROOT.TFile.Open(sys.argv[3], 'read')
qcd1500 = ROOT.TFile.Open(sys.argv[4], 'read')
qcd2000 = ROOT.TFile.Open(sys.argv[5], 'read')
tt1000 = ROOT.TFile.Open(sys.argv[6], 'read')
wjets = ROOT.TFile.Open(sys.argv[7], 'read')


hists_qcd500 = {}
hists_qcd700 = {}
hists_qcd1000 = {}
hists_qcd1500 = {}
hists_qcd2000 = {}
hists_tt1000 = {}
hists_wjets = {}
keys = ['TightElectrons_pt','TightElectrons_pt_cut',
        'TightMuons_pt','TightMuons_pt_cut',
        'jetspuppi_pt_1','jetspuppi_pt_cut_1',
        'jetspuppi_pt_2','jetspuppi_pt_cut_2',
        'jetspuppi_pt_3','jetspuppi_pt_cut_3']

for key in keys:
    hists_qcd500[key] = qcd500.Get(key)
    hists_qcd700[key] = qcd700.Get(key)
    hists_qcd1000[key] = qcd1000.Get(key)
    hists_qcd1500[key] = qcd1500.Get(key)
    hists_qcd2000[key] = qcd2000.Get(key)
    hists_tt1000[key] = tt1000.Get(key)
    hists_wjets[key] = wjets.Get(key)


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

for key in hists_qcd500.keys():
    if "_pt_cut" in key and "Tight" in key:
        canvas = ROOT.TCanvas('canvas','',600,400)

        hist_qcd500 = hists_qcd500[key].Clone()
        hist_qcd500.Reset()
        hist_qcd500.Divide(hists_qcd500[key],hists_qcd500[key.split("_cut")[0]],1,1,"B")
        hist_qcd500.SetLineColor(1)
        hist_qcd500.SetLineWidth(2)
        hist_qcd500.SetTitle("")
        hist_qcd500.GetXaxis().SetTitle("P_{T} [GeV]")
        hist_qcd500.GetYaxis().SetTitle("Efficiency")
        hist_qcd500.Draw("E")

        hist_qcd700 = hists_qcd700[key].Clone()
        hist_qcd700.Reset()
        hist_qcd700.Divide(hists_qcd700[key],hists_qcd700[key.split("_cut")[0]],1,1,"B")
        hist_qcd700.SetLineColor(2)
        hist_qcd700.SetLineWidth(2)
        hist_qcd700.Draw("E SAME")

        hist_qcd1000 = hists_qcd1000[key].Clone()
        hist_qcd1000.Reset()
        hist_qcd1000.Divide(hists_qcd1000[key],hists_qcd1000[key.split("_cut")[0]],1,1,"B")
        hist_qcd1000.SetLineColor(3)
        hist_qcd1000.SetLineWidth(2)
        hist_qcd1000.Draw("E SAME")

        hist_qcd1500 = hists_qcd1500[key].Clone()
        hist_qcd1500.Reset()
        hist_qcd1500.Divide(hists_qcd1500[key],hists_qcd1500[key.split("_cut")[0]],1,1,"B")
        hist_qcd1500.SetLineColor(4)
        hist_qcd1500.SetLineWidth(2)
        hist_qcd1500.Draw("E SAME")

        hist_qcd2000 = hists_qcd2000[key].Clone()
        hist_qcd2000.Reset()
        hist_qcd2000.Divide(hists_qcd2000[key],hists_qcd2000[key.split("_cut")[0]],1,1,"B")
        hist_qcd2000.SetLineColor(5)
        hist_qcd2000.SetLineWidth(2)
        hist_qcd2000.Draw("E SAME")

        hist_tt1000 = hists_tt1000[key].Clone()
        hist_tt1000.Reset()
        hist_tt1000.Divide(hists_tt1000[key],hists_tt1000[key.split("_cut")[0]],1,1,"B")
        hist_tt1000.SetLineColor(6)
        hist_tt1000.SetLineWidth(2)
        hist_tt1000.Draw("E SAME")

        hist_wjets = hists_wjets[key].Clone()
        hist_wjets.Reset()
        hist_wjets.Divide(hists_wjets[key],hists_wjets[key.split("_cut")[0]],1,1,"B")
        hist_wjets.SetLineColor(7)
        hist_wjets.SetLineWidth(2)
        hist_wjets.Draw("E SAME")

        legend1 = ROOT.TLegend(0.75,0.5,0.95,0.15)
        legend1.SetBorderSize(0)
        legend1.AddEntry(hist_qcd500,"QCD H_{T} 500-700", "l")
        legend1.AddEntry(hist_qcd700,"QCD H_{T} 700-1000", "l")
        legend1.AddEntry(hist_qcd1000,"QCD H_{T} 1000-1500", "l")
        legend1.AddEntry(hist_qcd1500,"QCD H_{T} 1500-2000", "l")
        legend1.AddEntry(hist_qcd2000,"QCD H_{T} 2000-Inf", "l")
        legend1.AddEntry(hist_tt1000,"TT 1000 GeV", "l")
        legend1.AddEntry(hist_wjets,"WJetsToLNu", "l")

        tex1.Draw()
        tex2.Draw()
        legend1.Draw()
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

    if "jetspuppi_pt_cut" in key:
        canvas = ROOT.TCanvas('canvas','',600,400)

        key_divide = key.split("_cut")[0] + key.split("_cut")[1]
        hist_qcd500 = hists_qcd500[key].Clone()
        hist_qcd500.Reset()
        hist_qcd500.Divide(hists_qcd500[key],hists_qcd500[key_divide],1,1,"B")
        hist_qcd500.SetLineColor(1)
        hist_qcd500.SetLineWidth(2)
        hist_qcd500.SetTitle("")
        hist_qcd500.GetXaxis().SetTitle("P_{T} [GeV]")
        hist_qcd500.GetYaxis().SetTitle("Efficiency")
        hist_qcd500.Draw("E")

        hist_qcd700 = hists_qcd700[key].Clone()
        hist_qcd700.Reset()
        hist_qcd700.Divide(hists_qcd700[key],hists_qcd700[key_divide],1,1,"B")
        hist_qcd700.SetLineColor(2)
        hist_qcd700.SetLineWidth(2)
        hist_qcd700.Draw("E SAME")

        hist_qcd1000 = hists_qcd1000[key].Clone()
        hist_qcd1000.Reset()
        hist_qcd1000.Divide(hists_qcd1000[key],hists_qcd1000[key_divide],1,1,"B")
        hist_qcd1000.SetLineColor(3)
        hist_qcd1000.SetLineWidth(2)
        hist_qcd1000.Draw("E SAME")

        hist_qcd1500 = hists_qcd1500[key].Clone()
        hist_qcd1500.Reset()
        hist_qcd1500.Divide(hists_qcd1500[key],hists_qcd1500[key_divide],1,1,"B")
        hist_qcd1500.SetLineColor(4)
        hist_qcd1500.SetLineWidth(2)
        hist_qcd1500.Draw("E SAME")

        hist_qcd2000 = hists_qcd2000[key].Clone()
        hist_qcd2000.Reset()
        hist_qcd2000.Divide(hists_qcd2000[key],hists_qcd2000[key_divide],1,1,"B")
        hist_qcd2000.SetLineColor(5)
        hist_qcd2000.SetLineWidth(2)
        hist_qcd2000.Draw("E SAME")

        hist_tt1000 = hists_tt1000[key].Clone()
        hist_tt1000.Reset()
        hist_tt1000.Divide(hists_tt1000[key],hists_tt1000[key_divide],1,1,"B")
        hist_tt1000.SetLineColor(6)
        hist_tt1000.SetLineWidth(2)
        hist_tt1000.Draw("E SAME")

        hist_wjets = hists_wjets[key].Clone()
        hist_wjets.Reset()
        hist_wjets.Divide(hists_wjets[key],hists_wjets[key_divide],1,1,"B")
        hist_wjets.SetLineColor(7)
        hist_wjets.SetLineWidth(2)
        hist_wjets.Draw("E SAME")

        legend1 = ROOT.TLegend(0.75,0.5,0.95,0.15)
        legend1.SetBorderSize(0)
        legend1.AddEntry(hist_qcd500,"QCD H_{T} 500-700", "l")
        legend1.AddEntry(hist_qcd700,"QCD H_{T} 700-1000", "l")
        legend1.AddEntry(hist_qcd1000,"QCD H_{T} 1000-1500", "l")
        legend1.AddEntry(hist_qcd1500,"QCD H_{T} 1500-2000", "l")
        legend1.AddEntry(hist_qcd2000,"QCD H_{T} 2000-Inf", "l")
        legend1.AddEntry(hist_tt1000,"TT 1000 GeV", "l")
        legend1.AddEntry(hist_wjets,"WJetsToLNu", "l")

        tex1.Draw()
        tex2.Draw()
        legend1.Draw()
        if "jetspuppi" in key:
            canvas.SaveAs(outputDir + "_" + key + ".png")
            canvas.SaveAs(outputDir + "_" + key + ".pdf")
        canvas.Close()
#    else:
#        canvas = ROOT.TCanvas('canvas','',600,400)
#        canvas.SetLogy()
#        hists[key].SetLineColor(1)
#        hists[key].SetTitle("")
#        if "pt" in key:
#            hists[key].GetXaxis().SetTitle("P_{T} [GeV]")
#            hists[key].GetYaxis().SetTitle("events/bin")
#        elif "eta" in key:
#            hists[key].GetXaxis().SetTitle("#eta")
#            hists[key].GetYaxis().SetTitle("events/bin")
#        if "idpass" in key:
#            hists[key].GetXaxis().SetTitle("idpass")
#            hists[key].GetYaxis().SetTitle("events/bin")
#        if "multi" in key:
#            hists[key].GetXaxis().SetTitle("multiplicity")
#            hists[key].GetYaxis().SetTitle("events/bin")
#        hists[key].Draw("hist")
#        tex1.Draw()
#        tex2.Draw()
#        canvas.SaveAs(outputDir + "_" + key + ".png")
#        canvas.SaveAs(outputDir + "_" + key + ".pdf")
#        canvas.Close()
