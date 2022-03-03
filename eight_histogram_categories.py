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

if len(sys.argv) != 2:
    print "USAGE: {} <diraddress containing (rootPlots/plots in different categories)>".format(sys.argv[0])
    sys.exit(1)

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

hists_f = ROOT.TH1D("","",8,-0.5,7.5)
hists_g = ROOT.TH1D("","",8,-0.5,7.5)
hists_h = ROOT.TH1D("","",8,-0.5,7.5)
hists_i = ROOT.TH1D("","",8,-0.5,7.5)
hists_j = ROOT.TH1D("","",8,-0.5,7.5)
hists_k = ROOT.TH1D("","",8,-0.5,7.5)
hists_l = ROOT.TH1D("","",8,-0.5,7.5)
hists_m = ROOT.TH1D("","",8,-0.5,7.5)

categories = ["_1b", "_2b", "_3b", "w1b", "w2b", "w3b", "h1b", "h2b"]
Categories = ["H0W0b1", "H0W0b2", "H0W0b3", "H0W1b1", "H0W1b2", "H0W1b3", "H1b1", "H1b2"]
iCount = 1
for category in categories:
    f = ROOT.TFile.Open(sys.argv[1] + "/" + category + "/rootPlots/TT_M1000.root", 'read')
    g = ROOT.TFile.Open(sys.argv[1] + "/" + category + "/rootPlots/TT_M1500.root", 'read')
    h = ROOT.TFile.Open(sys.argv[1] + "/" + category + "/rootPlots/TT_M2000.root", 'read')
    i = ROOT.TFile.Open(sys.argv[1] + "/" + category + "/rootPlots/TT_M2500.root", 'read')
    j = ROOT.TFile.Open(sys.argv[1] + "/" + category + "/rootPlots/TT_M3000.root", 'read')
    k = ROOT.TFile.Open(sys.argv[1] + "/" + category + "/rootPlots/top.root", 'read')
    l = ROOT.TFile.Open(sys.argv[1] + "/" + category + "/rootPlots/ew.root", 'read')
    m = ROOT.TFile.Open(sys.argv[1] + "/" + category + "/rootPlots/qcd.root", 'read')

    hists_f.SetBinContent(iCount,f.Get("St").Integral(0,101))
    hists_g.SetBinContent(iCount,g.Get("St").Integral(0,101))
    hists_h.SetBinContent(iCount,h.Get("St").Integral(0,101))
    hists_i.SetBinContent(iCount,i.Get("St").Integral(0,101))
    hists_j.SetBinContent(iCount,j.Get("St").Integral(0,101))
    hists_k.SetBinContent(iCount,k.Get("St").Integral(0,101))
    hists_l.SetBinContent(iCount,l.Get("St").Integral(0,101))
    hists_m.SetBinContent(iCount,m.Get("St").Integral(0,101))
    iCount += 1

#outputDir = '/eos/user/k/kpal/www/i4DAPNVShN/all_signal_v2.1/'
#outputDir = '/eos/uscms/store/user/kpal/trimmed_files_v2/smallBins/plots/'
outputDir = os.path.dirname(sys.argv[1]) + '/'
#outputDir = os.path.dirname(sys.argv[8]) +'/plotsNewQCDsamples/'

key = ""
#print(key)
canvas = ROOT.TCanvas('canvas','',600,400)
stack = createStack(key)

hists_k.SetFillColor(7)
hists_k.SetLineWidth(0)
stack.Add(hists_k)
hists_l.SetFillColor(6)
hists_l.SetLineWidth(0)
stack.Add(hists_l)
hists_m.SetFillColor(2)
hists_m.SetLineWidth(0)
stack.Add(hists_m)


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

hists_f.Scale(20)
hists_g.Scale(200)
hists_h.Scale(2000)
hists_i.Scale(20000)
hists_j.Scale(200000)

hists_f.SetLineColor(1)
hists_f.SetLineStyle(2)
hists_g.SetLineColor(2)
hists_g.SetLineStyle(2)
hists_h.SetLineColor(1)
hists_i.SetLineColor(2)
hists_j.SetLineColor(3)



if "eta" in key:
    legend = ROOT.TLegend(0.70,0.89,0.99,0.67)
    legend1 = ROOT.TLegend(0.13,0.89,0.28,0.71)
elif "St" in key or "Ht" in key:
    legend = ROOT.TLegend(0.70,0.89,0.99,0.67)
    legend1 = ROOT.TLegend(0.91,0.67,0.99,0.55)
    #legend = ROOT.TLegend(0.59,0.89,0.89,0.70)
    #legend1 = ROOT.TLegend(0.45,0.89,0.59,0.71)
elif "deltaR" in key:
    legend = ROOT.TLegend(0.15,0.89,0.47,0.67)
    legend1 = ROOT.TLegend(0.15,0.67,0.47,0.55)
else:
    legend = ROOT.TLegend(0.70,0.89,0.99,0.71)
    legend1 = ROOT.TLegend(0.13,0.89,0.28,0.71)
    #legend = ROOT.TLegend(0.55,0.89,0.89,0.67)
    #legend1 = ROOT.TLegend(0.55,0.67,0.89,0.55)
legend.SetBorderSize(0)
legend1.SetBorderSize(0)
legend.AddEntry(hists_f,"T'#bar{T'} (1.0 TeV) x 20", "l")
legend.AddEntry(hists_g,"T'#bar{T'} (1.5 TeV) x 200", "l")
legend.AddEntry(hists_h,"T'#bar{T'} (2.0 TeV) x 2000", "l")
legend.AddEntry(hists_i,"T'#bar{T'} (2.5 TeV) x 20000", "l")
legend.AddEntry(hists_j,"T'#bar{T'} (3.0 TeV) x 200000", "l")
legend1.AddEntry(hists_m,"QCD", "f")
legend1.AddEntry(hists_l,"EW", "f")
legend1.AddEntry(hists_k,"TOP", "f")

canvas.SetLogy()
iCount = 1
stack.Draw("pfc hist")
for category in categories:
    stack.GetXaxis().SetBinLabel(iCount, Categories[iCount - 1])
    iCount += 1
stack.SetMinimum(100.)
stack.SetMaximum(10000000.)
hists_f.Draw("same hist")
hists_g.Draw("same hist")
hists_h.Draw("same hist")
hists_i.Draw("same hist")
hists_j.Draw("same hist")
setTitle(stack,key)
tex1.Draw()
tex2.Draw()
legend.Draw()
legend1.Draw()
canvas.SaveAs(outputDir + "category" + ".png")
canvas.SaveAs(outputDir + "category" + ".pdf")
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
