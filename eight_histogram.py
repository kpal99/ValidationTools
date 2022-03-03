#import contextlib2
import ROOT
import sys
import os

def createStack(varname):
    stack_i = ROOT.THStack(varname, "")
    return stack_i

def setTitle(stack_i,varname):
    if "pt" in varname:
        stack_i.GetXaxis().SetTitle("p_{T} [GeV]")
        per = stack_i.GetXaxis().GetXmax() - stack_i.GetXaxis().GetXmin()
        per /= stack_i.GetXaxis().GetNbins()
        stack_i.GetYaxis().SetTitle("events/"+ str(int(per)) +"GeV")
    elif "Ht" in varname:
        stack_i.GetXaxis().SetTitle("H_{T} [GeV]")
        per = stack_i.GetXaxis().GetXmax() - stack_i.GetXaxis().GetXmin()
        per /= stack_i.GetXaxis().GetNbins()
        stack_i.GetYaxis().SetTitle("events/"+ str(int(per)) +"GeV")
    elif "St" in varname:
        stack_i.GetXaxis().SetTitle("S_{T} [GeV]")
        per = stack_i.GetXaxis().GetXmax() - stack_i.GetXaxis().GetXmin()
        per /= stack_i.GetXaxis().GetNbins()
        stack_i.GetYaxis().SetTitle("events/"+ str(int(per)) +"GeV")
    elif "eta" in varname:
        stack_i.GetXaxis().SetTitle("#eta")
        per = stack_i.GetXaxis().GetXmax() - stack_i.GetXaxis().GetXmin()
        per /= stack_i.GetXaxis().GetNbins()
        stack_i.GetYaxis().SetTitle("events/"+ str(round(per,2)) +"#eta")
    elif "phi" in varname:
        stack_i.GetXaxis().SetTitle("phi")
        per = stack_i.GetXaxis().GetXmax() - stack_i.GetXaxis().GetXmin()
        per /= stack_i.GetXaxis().GetNbins()
        stack_i.GetYaxis().SetTitle("events/"+ str(round(per,2)) +"rad")
    elif "mass" in varname:
        stack_i.GetXaxis().SetTitle("mass [GeV]")
        per = stack_i.GetXaxis().GetXmax()
        per /= stack_i.GetXaxis().GetNbins()
        stack_i.GetYaxis().SetTitle("events/"+ str(int(per)) +"GeV")
    elif "multiplicity" in varname:
        stack_i.GetXaxis().SetTitle(varname)
        stack_i.GetYaxis().SetTitle("events/bin")
    else:
        stack_i.GetXaxis().SetTitle(varname)
        stack_i.GetYaxis().SetTitle("events/bin")

if len(sys.argv) != 9:
    print "USAGE: {} <TT_M1000_plot> <TT_M1500_plot>  <TT_M2000_plot> <TT_M2500_plot> <TT_M3000_plot> <TOP_plot> <EW_plot> <QCD_plot>".format(sys.argv[0])
    sys.exit(1)

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

f = ROOT.TFile.Open(sys.argv[1], 'read')
g = ROOT.TFile.Open(sys.argv[2], 'read')
h = ROOT.TFile.Open(sys.argv[3], 'read')
i = ROOT.TFile.Open(sys.argv[4], 'read')
j = ROOT.TFile.Open(sys.argv[5], 'read')
k = ROOT.TFile.Open(sys.argv[6], 'read')
l = ROOT.TFile.Open(sys.argv[7], 'read')
m = ROOT.TFile.Open(sys.argv[8], 'read')

hists_f = {}
hists_g = {}
hists_h = {}
hists_i = {}
hists_j = {}
hists_k = {}
hists_l = {}
hists_m = {}
stack = {}

keys = ['jetspuppi_btagmultiplicity', 'metspuppi_pt', 'TightElectrons_pt', 'TightMuons_eta', 'jetspuppi_eta', 'jetspuppi_eta_1', 'jetspuppi_eta_2', 'jetspuppi_eta_3', 'fatjets_tau21[m-softdrop]', 'fatjets_multiplicity', 'jetspuppi_multiplicity', 'TightElectrons_phi', 'TightElectrons_eta', 'fatjets_phi', 'jetspuppi_pt', 'jetspuppi_pt_1','jetspuppi_pt_2','jetspuppi_pt_3','TightMuons_phi', 'jetspuppi_mass', 'fatjets_H2b-multiplicity', 'St', 'TightMuons_mass', 'fatjets_Wtag-multiplicity', 'jetspuppi_phi', 'metspuppi_phi', 'fatjets_pt', 'fatjets_H1b-multiplicity', 'TightMuons_pt', 'fatjets_eta', 'fatjets_msoftdrop[tau21]', 'jetspuppi_Ht', 'TightElectrons_mass', 'deltaR','deltaRmin']

#reading very many histrograms
for key in keys:
    hists_f[key] = f.Get(key)
    hists_g[key] = g.Get(key)
    hists_h[key] = h.Get(key)
    hists_i[key] = i.Get(key)
    hists_j[key] = j.Get(key)
    hists_k[key] = k.Get(key)
    hists_l[key] = l.Get(key)
    hists_m[key] = m.Get(key)

#outputDir = '/eos/user/k/kpal/www/i4DAPNVShN/all_signal_v2.1/'
#outputDir = '/eos/uscms/store/user/kpal/trimmed_files_v2/smallBins/plots/'
outputDir = os.path.dirname(sys.argv[8]) +'/plots' + os.path.basename(sys.argv[8]).split(".root")[0].split("qcd")[1] + '/'
#outputDir = os.path.dirname(sys.argv[8]) +'/plotsNewQCDsamples/'

scale_factor = 20
for key in hists_f.keys():
    #print(key)
    canvas = ROOT.TCanvas('canvas','',600,400)
    stack[key] = createStack(key)

    hists_k[key].SetFillColor(7)
    hists_k[key].SetLineWidth(0)
    stack[key].Add(hists_k[key])
    hists_l[key].SetFillColor(6)
    hists_l[key].SetLineWidth(0)
    stack[key].Add(hists_l[key])
    hists_m[key].SetFillColor(2)
    hists_m[key].SetLineWidth(0)
    stack[key].Add(hists_m[key])
    stack[key].Draw("pfc hist")
    if key == "St":
        stack[key].SetMinimum(.01)
        #stack[key].SetMaximum(10000000.)
    setTitle(stack[key],key)

    if key == "St" or "multiplicity" in key or "deltaR" in key or "_pt" in key or "_Ht" in key or "metspuppi_pt" in key :
    #if key == "St" or "H2b" in key or "H1b" in key or key == "metspuppi_pt":
        canvas.SetLogy()
        tex1 = ROOT.TLatex(0.10, 0.95, "#bf{CMS} #it{Phase-2 Simulation Premilinary}")
    else:
        tex1 = ROOT.TLatex(0.155555, 0.95, "#bf{CMS} #it{Phase-2 Simulation Premilinary}")

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

    hists_f[key].Scale(scale_factor)
    hists_g[key].Scale(scale_factor * 10)
    hists_h[key].Scale(scale_factor * 100)
    hists_i[key].Scale(scale_factor * 1000)
    hists_j[key].Scale(scale_factor * 10000)

    hists_f[key].SetLineColor(1)
    hists_f[key].SetLineStyle(2)
    hists_g[key].SetLineColor(2)
    hists_g[key].SetLineStyle(2)
    hists_h[key].SetLineColor(1)
    hists_i[key].SetLineColor(2)
    hists_j[key].SetLineColor(3)

    hists_f[key].Draw("same hist")
    hists_g[key].Draw("same hist")
    hists_h[key].Draw("same hist")
    hists_i[key].Draw("same hist")
    hists_j[key].Draw("same hist")


    if "eta" in key:
        legend = ROOT.TLegend(0.70,0.89,0.99,0.67)
        legend1 = ROOT.TLegend(0.13,0.89,0.28,0.71)
    elif "St" in key or "Ht" in key:
        legend = ROOT.TLegend(0.70,0.89,0.99,0.67)
        legend1 = ROOT.TLegend(0.91,0.67,0.99,0.55)
        #legend = ROOT.TLegend(0.59,0.89,0.89,0.70)
        #legend1 = ROOT.TLegend(0.45,0.89,0.59,0.71)
    elif "deltaR" in key:
        legend = ROOT.TLegend(0.12,0.89,0.42,0.67)
        legend1 = ROOT.TLegend(0.12,0.67,0.26,0.55)
    else:
        legend = ROOT.TLegend(0.55,0.89,0.89,0.67)
        legend1 = ROOT.TLegend(0.75,0.67,0.89,0.55)
    legend.SetBorderSize(0)
    legend1.SetBorderSize(0)
    legend.AddEntry(hists_f[key],"T'#bar{T'} (1.0 TeV) x " + str(scale_factor), "l")
    legend.AddEntry(hists_g[key],"T'#bar{T'} (1.5 TeV) x " + str(scale_factor * 10), "l")
    legend.AddEntry(hists_h[key],"T'#bar{T'} (2.0 TeV) x " + str(scale_factor * 100), "l")
    legend.AddEntry(hists_i[key],"T'#bar{T'} (2.5 TeV) x " + str(scale_factor * 1000), "l")
    legend.AddEntry(hists_j[key],"T'#bar{T'} (3.0 TeV) x " + str(scale_factor * 10000), "l")
    legend1.AddEntry(hists_m[key],"QCD", "f")
    legend1.AddEntry(hists_l[key],"EW", "f")
    legend1.AddEntry(hists_k[key],"TOP", "f")
    tex1.Draw()
    tex2.Draw()
    legend.Draw()
    legend1.Draw()
    canvas.SaveAs(outputDir + key + ".png")
    canvas.SaveAs(outputDir + key + ".pdf")
    canvas.Close()
    legend.Clear()
    legend1.Clear()
    tex1.Clear()
    tex2.Clear()


f.Close()
g.Close()
h.Close()
i.Close()
j.Close()
k.Close()
l.Close()
m.Close()
