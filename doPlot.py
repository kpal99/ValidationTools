import ROOT as rt
import os

rt.gROOT.SetBatch(True) ## avoid figures pop out to screen

printoutdir = "plots"
inputFile_d = rt.TFile.Open("histo_delp/val_jet.root")
inputFile_f = rt.TFile.Open("histo_full/val_jet.root")

hist_names = ["jet_pt", "jet_eta", "jet_phi", "jet_mass",
"jet_ptresponse_to_eta","jet_ptresponse_to_pt", 
"jet_ptresponse_to_eta_0to50","jet_ptresponse_to_eta_50to100","jet_ptresponse_to_eta_100to200",
"jet_ptresponse_to_eta_200to400","jet_ptresponse_to_eta_400up", 
 ]

for name in hist_names:
    canv_name = name
    canv = rt.TCanvas(canv_name, canv_name, 900, 600)
    hd = inputFile_d.Get(name)
    hf = inputFile_f.Get(name)
    hd.Draw()
    hd.SetLineColor(rt.kRed)
    hd.SetStats(rt.kFALSE)
    hf.Draw("same")
    hf.SetLineColor(rt.kBlue)
    legend = rt.TLegend(.4,.2,.7,.35)
    legend.SetTextSize(0.03)
    legend.SetBorderSize(0) 
    legend.AddEntry(hd,"Delphes","l")
    legend.AddEntry(hf,"FullSim","l")
    legend.Draw()
    canv.Print(printoutdir+ "/" + canv_name +".png")


