import ROOT
import sys
import os
import math
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

def main():
    f = ROOT.TFile.Open(sys.argv[1], 'read')
    outputDir = sys.argv[1].split('.root')[0]

    hists = {}
    hists["TightElectrons_reliso-pt_Ht"] = f.Get("TightElectrons_reliso-pt_Ht")
    hists["TightMuons_reliso-pt_Ht"] = f.Get("TightMuons_reliso-pt_Ht")
    hists["TightElectrons_reliso_Ht"] = f.Get("TightElectrons_reliso_Ht")
    hists["TightMuons_reliso_Ht"] = f.Get("TightMuons_reliso_Ht")

    hists["TightElectrons_reliso-pt_jetM"] = f.Get("TightElectrons_reliso-pt_jetM")
    hists["TightMuons_reliso-pt_jetM"] = f.Get("TightMuons_reliso-pt_jetM")
    hists["TightElectrons_reliso_jetM"] = f.Get("TightElectrons_reliso_jetM")
    hists["TightMuons_reliso_jetM"] = f.Get("TightMuons_reliso_jetM")

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
        canvas = ROOT.TCanvas('canvas','',600,400)
        pad1 = ROOT.TPad("pad1","pad1",0,0,1,1)
        pad1.SetRightMargin(0.13)
        pad1.Draw()
        pad1.cd()
        profile = hists[key].ProfileX()
        hists[key].SetTitle("")
        hists[key].SetMaximum(45000)

        if "Ht" in key:
            hists[key].GetXaxis().SetTitle("H_{T} [GeV]")
        elif "jetM" in key:
            hists[key].GetXaxis().SetTitle("AK4 jet multiplicity")

        if "pt" in key:
            hists[key].GetYaxis().SetTitle("reliso #times P_{T} [GeV]")
        else:
            hists[key].GetYaxis().SetTitle("reliso ")

        hists[key].Draw("COLZ")
        profile.Draw("same")
        canvas.cd()
        tex1.Draw()
        tex2.Draw()
        canvas.SaveAs(outputDir + "_" + key + ".png")
        canvas.SaveAs(outputDir + "_" + key + ".pdf")
        canvas.Close()

def ptHt_lepton_QCD():
    if "pt_Ht" in sys.argv[1]:
        pass
    else:
        return

    f = ROOT.TFile.Open(sys.argv[1], 'read')
    outputDir = sys.argv[1].split('.root')[0]

    hists = {}
    hists["TightElectrons_pt_Ht"] = f.Get("TightElectrons_pt_Ht")
    hists["TightMuons_pt_Ht"] = f.Get("TightMuons_pt_Ht")
    hists["TightElectrons_pt_Ht_cut"] = f.Get("TightElectrons_pt_Ht_cut")
    hists["TightMuons_pt_Ht_cut"] = f.Get("TightMuons_pt_Ht_cut")

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
        if "_cut" in key:
            canvas = ROOT.TCanvas('canvas','',600,400)
            pad1 = ROOT.TPad("pad1","pad1",0,0,1,1)
            pad1.SetRightMargin(0.13)
            pad1.Draw()
            pad1.cd()

            hist = hists[key].Clone()
            hist.Reset()
            key_divide = key.split("_cut")[0]
            hist.Divide(hists[key],hists[key_divide],1,1,"B")

            hist.SetTitle("")
            hist.SetMaximum(1.0)

            if "Ht" in key:
                hist.GetXaxis().SetTitle("H_{T} [GeV]")
            elif "jetM" in key:
                hist.GetXaxis().SetTitle("AK4 jet multiplicity")

            if "pt" in key:
                hist.GetYaxis().SetTitle("P_{T} [GeV]")
            else:
                hist.GetYaxis().SetTitle("reliso ")

            hist.Draw("COLZ")
            canvas.cd()
            tex1.Draw()
            tex2.Draw()
            canvas.SaveAs(outputDir + "_" + key + ".png")
            canvas.SaveAs(outputDir + "_" + key + ".pdf")
            canvas.Close()

if __name__ == "__main__":
    #main()
    ptHt_lepton_QCD()
