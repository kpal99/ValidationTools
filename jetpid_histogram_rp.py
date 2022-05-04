#import contextlib2
import ROOT
import sys
import os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

def pid1to5():
    if "gluon" in sys.argv[1]:
        return
    f = ROOT.TFile.Open(sys.argv[1], 'read')

    keys = ['pid1_pt_1',   'pid2_pt_1',   'pid3_pt_1',   'pid4_pt_1',   'pid5_pt_1',   'pidBtag_pt_1',
            'pid1_jetM_1', 'pid2_jetM_1', 'pid3_jetM_1', 'pid4_jetM_1', 'pid5_jetM_1', 'pidBtag_jetM_1',
            'pid1_pt_2',   'pid2_pt_2',   'pid3_pt_2',   'pid4_pt_2',   'pid5_pt_2',   'pidBtag_pt_2',
            'pid1_jetM_2', 'pid2_jetM_2', 'pid3_jetM_2', 'pid4_jetM_2', 'pid5_jetM_2', 'pidBtag_jetM_2',
            'pid1_pt_3',   'pid2_pt_3',   'pid3_pt_3',   'pid4_pt_3',   'pid5_pt_3',   'pidBtag_pt_3',
            'pid1_jetM_3', 'pid2_jetM_3', 'pid3_jetM_3', 'pid4_jetM_3', 'pid5_jetM_3', 'pidBtag_jetM_3']

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
        if "Btag" in key:
            canvas = ROOT.TCanvas('canvas','',600,600)

            key_divide = key.split("Btag")
            pid1_key = key_divide[0] + '1' + key_divide[1]
            pid2_key = key_divide[0] + '2' + key_divide[1]
            pid3_key = key_divide[0] + '3' + key_divide[1]
            pid4_key = key_divide[0] + '4' + key_divide[1]
            pid5_key = key_divide[0] + '5' + key_divide[1]

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

            hists[key].SetMaximum(100000000)
            hists[key].SetMinimum(1)
            hists[key].Draw("hist")

            pid123 = hists[pid1_key].Clone()
            pid123.Add(hists[pid2_key])
            pid123.Add(hists[pid3_key])

            hists[pid4_key].SetLineColor(4)
            hists[pid4_key].Draw("E same")

            hists[pid5_key].SetLineColor(5)
            hists[pid5_key].Draw("E same")

            pid123.SetLineColor(6)
            pid123.Draw("E same")

            canvas.cd()
            pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.4)
            pad2.SetTopMargin(0.0)
            pad2.SetBottomMargin(0.3)
            pad2.SetGrid()
            pad2.Draw()
            pad2.cd()
            hist = hists[key].Clone()
            hist.Reset()
            hist.Divide(pid123,hists[key],1,1,"B")
            hist.SetMinimum(0)
            hist.SetMaximum(1.1)
            hist.GetXaxis().SetLabelSize(0.07)
            hist.GetYaxis().SetLabelSize(0.07)
            hist.GetXaxis().SetTitleSize(0.07)
            hist.SetTitle("")
            if 'pt' in key:
                hist.GetXaxis().SetTitle("p_{T} [GeV]")
            elif 'jetM' in key:
                hist.GetXaxis().SetTitle("AK4 jet multiplicity")
            hist.GetYaxis().SetTitle("")

            hist.SetLineColor(6)
            hist.Draw("E")

            hist4 = hists[key].Clone()
            hist4.Reset()
            hist4.Divide(hists[pid4_key],hists[key],1,1,"B")
            hist4.SetLineColor(4)
            hist4.Draw("same E")

            hist5 = hists[key].Clone()
            hist5.Reset()
            hist5.Divide(hists[pid5_key],hists[key],1,1,"B")
            hist5.SetLineColor(5)
            hist5.Draw("same E")

            canvas.cd()

            legend1 = ROOT.TLegend(0.7,0.92,0.86,0.8)
            legend1.SetBorderSize(0)
            legend1.AddEntry(pid123,         "PID 1-3 genpart", "l")
            legend1.AddEntry(hists[pid4_key],"PID 4 genpart", "l")
            legend1.AddEntry(hists[pid5_key],"PID 5 genpart", "l")
            legend1.AddEntry(hists[key],     "b-tagged jet", "l")
            legend1.Draw()

            tex1.Draw()
            tex2.Draw()
            canvas.SaveAs(outputDir + "_" + key + ".png")
            canvas.SaveAs(outputDir + "_" + key + ".pdf")
            canvas.Close()
    f.Close()

def pid1to5fraction():
    if "gluon" in sys.argv[1]:
        return
    f = ROOT.TFile.Open(sys.argv[1], 'read')

    keys = ['pid1_pt_1',   'pid2_pt_1',   'pid3_pt_1',   'pid4_pt_1',   'pid5_pt_1',   'pidBtag_pt_1',
            'pid1_jetM_1', 'pid2_jetM_1', 'pid3_jetM_1', 'pid4_jetM_1', 'pid5_jetM_1', 'pidBtag_jetM_1',
            'pid1_pt_2',   'pid2_pt_2',   'pid3_pt_2',   'pid4_pt_2',   'pid5_pt_2',   'pidBtag_pt_2',
            'pid1_jetM_2', 'pid2_jetM_2', 'pid3_jetM_2', 'pid4_jetM_2', 'pid5_jetM_2', 'pidBtag_jetM_2',
            'pid1_pt_3',   'pid2_pt_3',   'pid3_pt_3',   'pid4_pt_3',   'pid5_pt_3',   'pidBtag_pt_3',
            'pid1_jetM_3', 'pid2_jetM_3', 'pid3_jetM_3', 'pid4_jetM_3', 'pid5_jetM_3', 'pidBtag_jetM_3']

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
        if "Btag" in key:
            canvas = ROOT.TCanvas('canvas','',600,600)

            key_divide = key.split("Btag")
            pid1_key = key_divide[0] + '1' + key_divide[1]
            pid2_key = key_divide[0] + '2' + key_divide[1]
            pid3_key = key_divide[0] + '3' + key_divide[1]
            pid4_key = key_divide[0] + '4' + key_divide[1]
            pid5_key = key_divide[0] + '5' + key_divide[1]

            canvas.cd()
            pad1 = ROOT.TPad("pad1","pad1",0,0.4,1,1)
            pad1.SetLogy()
            pad1.SetBottomMargin(0)
            pad1.Draw()
            pad1.cd()
            hists[key].SetLineColor(1)
            hists[key].SetLineWidth(0)
            hists[key].Reset()
            hists[key].SetTitle("")
            hists[key].GetXaxis().SetLabelSize(0.05)
            hists[key].GetYaxis().SetLabelSize(0.05)
            hists[key].GetYaxis().SetTitleSize(0.05)
            hists[key].GetYaxis().SetTitle("events/bin")

            hists[key].SetMaximum(100000000)
            hists[key].SetMinimum(1)
            hists[key].Draw("hist")

            pid123 = hists[pid1_key].Clone()
            pid123 = hists[pid2_key].Clone()
            pid123 = hists[pid3_key].Clone()

            hists[pid4_key].SetLineColor(4)
            hists[pid4_key].Draw("E same")

            hists[pid5_key].SetLineColor(5)
            hists[pid5_key].Draw("E same")

            pid123.SetLineColor(6)
            pid123.Draw("E same")

            pidAll = pid123.Clone()
            pidAll.Add(hists[pid4_key])
            pidAll.Add(hists[pid5_key])

            canvas.cd()
            pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.4)
            pad2.SetTopMargin(0.0)
            pad2.SetBottomMargin(0.3)
            pad2.SetGrid()
            pad2.Draw()
            pad2.cd()
            hist = pidAll.Clone()
            hist.Reset()
            hist.Divide(pid123,pidAll,1,1,"B")
            hist.SetMinimum(0)
            hist.SetMaximum(1.1)
            hist.GetXaxis().SetLabelSize(0.07)
            hist.GetYaxis().SetLabelSize(0.07)
            hist.GetXaxis().SetTitleSize(0.07)
            hist.SetTitle("")
            if 'pt' in key:
                hist.GetXaxis().SetTitle("p_{T} [GeV]")
            elif 'jetM' in key:
                hist.GetXaxis().SetTitle("AK4 jet multiplicity")
            hist.GetYaxis().SetTitle("")

            hist.SetLineColor(6)
            hist.Draw("E")

            hist4 = pidAll.Clone()
            hist4.Reset()
            hist4.Divide(hists[pid4_key],pidAll,1,1,"B")
            hist4.SetLineColor(4)
            hist4.Draw("same E")

            hist5 = pidAll.Clone()
            hist5.Reset()
            hist5.Divide(hists[pid5_key],pidAll,1,1,"B")
            hist5.SetLineColor(5)
            hist5.Draw("same E")

            canvas.cd()

            legend1 = ROOT.TLegend(0.7,0.92,0.86,0.8)
            legend1.SetBorderSize(0)
            legend1.AddEntry(pid123,         "PID 1-3 genpart", "l")
            legend1.AddEntry(hists[pid4_key],"PID 4 genpart", "l")
            legend1.AddEntry(hists[pid5_key],"PID 5 genpart", "l")
            legend1.Draw()

            tex1.Draw()
            tex2.Draw()
            canvas.SaveAs(outputDir + "_fraction_" + key + ".png")
            canvas.SaveAs(outputDir + "_fraction_" + key + ".pdf")
            canvas.Close()
    f.Close()
def pid21():
    if "gluon" in sys.argv[1]:
        pass
    else:
        return

    f = ROOT.TFile.Open(sys.argv[1], 'read')

    keys = ['pid21_pt_1',   'pidBtag_pt_1',
            'pid21_jetM_1', 'pidBtag_jetM_1',
            'pid21_pt_2',   'pidBtag_pt_2',
            'pid21_jetM_2', 'pidBtag_jetM_2',
            'pid21_pt_3',   'pidBtag_pt_3',
            'pid21_jetM_3', 'pidBtag_jetM_3']

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
        if "Btag" in key:
            canvas = ROOT.TCanvas('canvas','',600,600)

            key_divide = key.split("Btag")
            pid21_key = key_divide[0] + '21' + key_divide[1]

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

            hists[key].SetMaximum(100000000)
            hists[key].SetMinimum(1)
            hists[key].Draw("hist")

            hists[pid21_key].SetLineWidth(2)
            hists[pid21_key].SetLineColor(6)
            hists[pid21_key].Draw("E same")

            canvas.cd()
            pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.4)
            pad2.SetTopMargin(0.0)
            pad2.SetBottomMargin(0.3)
            pad2.SetGrid()
            pad2.Draw()
            pad2.cd()
            hist = hists[key].Clone()
            hist.Reset()
            hist.Divide(hists[key],hists[pid21_key],1,1,"B")
            hist.SetMinimum(0)
            hist.SetMaximum(1.1)
            hist.GetXaxis().SetLabelSize(0.07)
            hist.GetYaxis().SetLabelSize(0.07)
            hist.GetXaxis().SetTitleSize(0.07)
            hist.SetTitle("")
            if 'pt' in key:
                hist.GetXaxis().SetTitle("p_{T} [GeV]")
            elif 'jetM' in key:
                hist.GetXaxis().SetTitle("AK4 jet multiplicity")
            hist.GetYaxis().SetTitle("")
            hist.Draw("E")

            canvas.cd()

            legend1 = ROOT.TLegend(0.6,0.92,0.86,0.85)
            legend1.SetBorderSize(0)
            legend1.AddEntry(hists[pid21_key],"PID 21 (g) genpart", "l")
            legend1.AddEntry(hists[key],     "b-tagged jet", "l")
            legend1.Draw()

            tex1.Draw()
            tex2.Draw()
            canvas.SaveAs(outputDir + "_" + key + ".png")
            canvas.SaveAs(outputDir + "_" + key + ".pdf")
            canvas.Close()
    f.Close()

if len(sys.argv) != 2:
    print "USAGE: {} <plot_file>".format(sys.argv[0])
    sys.exit(1)

if __name__ == "__main__":
    pid1to5()
    pid1to5fraction()
    pid21()
