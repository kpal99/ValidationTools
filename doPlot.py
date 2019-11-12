import ROOT as rt
import os, sys, optparse

rt.gROOT.SetBatch(True) ## avoid figures pop out to screen

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--inFileDelphes',
                  dest='inFileD',
                  help='path to input file delphes [%default]',  
                  default='histo_delp/val_jet.root',                                                                                                           
                  type='string')
parser.add_option('-f', '--inFileFullsim',
                  dest='inFileF',
                  help='path to input file fullsim [%default]',  
                  default='histo_full/val_jet.root',                                                                                                           
                  type='string')
parser.add_option('-o', '--outDir',          
                  dest='printoutdir',       
                  help='output dir for plots [%default]',  
                  default=None,       
                  type='string')
(opt, args) = parser.parse_args()

inFileD = opt.inFileD
inFileF = opt.inFileF
printoutdir = opt.printoutdir

if not os.path.exists(printoutdir):
    os.system('mkdir -p %s'%printoutdir)

inputFile_d = rt.TFile.Open(inFileD)
inputFile_f = rt.TFile.Open(inFileF)

hist_names = []
# hist_names += [ # select hists to print -- CAN be empty -> will take all 
# "jet_pt", "jet_eta", "jet_phi", "jet_mass",
# "jet_ptresponse_to_eta","jet_ptresponse_to_pt", 
# "jet_ptresponse_to_eta_20to50","jet_ptresponse_to_eta_50to100","jet_ptresponse_to_eta_100to200",
# "jet_ptresponse_to_eta_200to400","jet_ptresponse_to_eta_400up", 
# "jet_multiplicity", "jet_multiplicity_20to50", "jet_multiplicity_50to100", "jet_multiplicity_100to200",
# "jet_multiplicity_200to400", "jet_multiplicity_400up",
# "jet_multiplicity_0to1p3", "jet_multiplicity_1p3to2p5", "jet_multiplicity_2p5to3", "jet_multiplicity_3up",
# "jet_matchefficiency_to_eta",
# "jet_matchefficiency_to_eta_20to50", "jet_matchefficiency_to_eta_50to100", "jet_matchefficiency_to_eta_100to200",
# "jet_matchefficiency_to_eta_200to400", "jet_matchefficiency_to_eta_400up",
# "jet_matchefficiency_to_pt", "jet_matchefficiency_to_pt_0to1p3", "jet_matchefficiency_to_pt_1p3to2p5", "jet_matchefficiency_to_pt_2p5to3", "jet_matchefficiency_to_pt_3up",

#  ]

if not hist_names: 
    keys = inputFile_d.GetListOfKeys()
    hist_names = [x.GetName() for x in keys] 
    hist_names.sort()

for name in hist_names:
    canv_name = name
    canv = rt.TCanvas(canv_name, canv_name, 900, 600)
    hd = inputFile_d.Get(name)
    hf = inputFile_f.Get(name)

    if 'efficiency2D' in name or 'fakerate2D' in name:
        rt.gStyle.SetPaintTextFormat("1.2f")
        hd.SetStats(rt.kFALSE)
        hd.Draw("colz texte")
        canv.Print(printoutdir+"/"+canv_name+"_delphes.png")
        hf.SetStats(rt.kFALSE)
        hf.Draw("colz texte")
        canv.Print(printoutdir+"/"+canv_name+"_fullsim.png")
    else:
        hf.SetLineColor(rt.kBlue)
        hf.SetMarkerStyle(21)
        hf.SetMarkerColor(rt.kBlue)
        hf.SetStats(rt.kFALSE)
        hf.Draw("same")
        hd.SetLineColor(rt.kRed)
        hd.SetMarkerStyle(20)
        hd.SetMarkerColor(rt.kRed)
        hd.SetStats(rt.kFALSE)
        hd.SetMaximum(max(hd.GetMaximum(),hf.GetMaximum())*1.1)
        hd.SetMinimum(min(hd.GetMinimum(),hf.GetMinimum())*0.9)
        hd.Draw("same")
        legend = rt.TLegend(.9,.9,.99,.99)
        legend.SetTextSize(0.03)
        legend.SetBorderSize(0) 
        legend.AddEntry(hd,"Delphes","l")
        legend.AddEntry(hf,"FullSim","l")
        legend.Draw()
        canv.Print(printoutdir+ "/" + canv_name +".png")


