import ROOT as rt
import os, sys

rt.gROOT.SetBatch(True) ## avoid figures pop out to screen

printoutdir = sys.argv[1]
if not os.path.exists(printoutdir):
    os.system('mkdir -p %s'%printoutdir)

inputFile_d = rt.TFile.Open("histo_delp/val_jet.root")
inputFile_f = rt.TFile.Open("histo_full/val_jet.root")

hist_names = []
hist_names += [ # select hists to print -- CAN be empty -> will take all 
"jet_pt", "jet_eta", "jet_phi", "jet_mass",
"jet_ptresponse_to_eta","jet_ptresponse_to_pt", 
"jet_ptresponse_to_eta_20to50","jet_ptresponse_to_eta_50to100","jet_ptresponse_to_eta_100to200",
"jet_ptresponse_to_eta_200to400","jet_ptresponse_to_eta_400up", 
"jet_multiplicity", "jet_multiplicity_20to50", "jet_multiplicity_50to100", "jet_multiplicity_100to200",
"jet_multiplicity_200to400", "jet_multiplicity_400up",
"jet_multiplicity_0to1p3", "jet_multiplicity_1p3to2p5", "jet_multiplicity_2p5to3", "jet_multiplicity_3up",
"jet_matchefficiency_to_eta",
"jet_matchefficiency_to_eta_20to50", "jet_matchefficiency_to_eta_50to100", "jet_matchefficiency_to_eta_100to200",
"jet_matchefficiency_to_eta_200to400", "jet_matchefficiency_to_eta_400up",
"jet_matchefficiency_to_pt", "jet_matchefficiency_to_pt_0to1p3", "jet_matchefficiency_to_pt_1p3to2p5", "jet_matchefficiency_to_pt_2p5to3", "jet_matchefficiency_to_pt_3up",

 ]

if not hist_names: 
    keys = inputFile_d.GetListOfKeys()
    hist_names = [x.GetName() for x in keys] 
    hist_names.sort()

for name in hist_names:
    canv_name = name
    canv = rt.TCanvas(canv_name, canv_name, 900, 600)
    hd = inputFile_d.Get(name)
    hf = inputFile_f.Get(name)
    hd.SetLineColor(rt.kRed)
    hd.SetStats(rt.kFALSE)
    hf.Draw("same")
    # set ymax if needed
    for sname, maxval in [ ["jet_multiplicity", 1500], ["jet_multiplicity_20to50", 2000], ["jet_multiplicity_50to100", 2500], 
			["jet_multiplicity_100to200", 3000], ["jet_multiplicity_3up", 3500],
			["jet_matchefficiency", 600], ["jet_matchefficiency_3up", 4500], ["jet_ptresponse_to_pt", 1.4],
			["jet_eta", 500], ["jet_phi", 250], ["jet_mass", 5000], 
			]:
	if name == sname : hf.SetMaximum(maxval)
    hf.SetLineColor(rt.kBlue)
    hf.SetStats(rt.kFALSE)
    hd.Draw("same")
    legend = rt.TLegend(.78,.8,.9,.87)
    legend.SetTextSize(0.03)
    legend.SetBorderSize(0) 
    legend.AddEntry(hd,"Delphes","l")
    legend.AddEntry(hf,"FullSim","l")
    legend.Draw()
    canv.Print(printoutdir+ "/" + canv_name +".png")


