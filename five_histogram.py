#import contextlib2
import ROOT
import sys

def createStack(varname):
    stack_i = ROOT.THStack(varname, "")
    return stack_i

def setTitle(stack_i,varname):
    if "pt" in varname:
        stack_i.GetXaxis().SetTitle("p_{T}[GeV]")
    elif "Ht" in varname:
        stack_i.GetXaxis().SetTitle("H_{T}[GeV]")
    elif "eta" in varname:
        stack_i.GetXaxis().SetTitle("eta")
    elif "phi" in varname:
        stack_i.GetXaxis().SetTitle("phi")
    elif "mass" in varname:
        stack_i.GetXaxis().SetTitle("mass[GeV]")
    elif "multiplicity" in varname:
        stack_i.GetXaxis().SetTitle(varname)
    else:
        stack_i.GetXaxis().SetTitle(varname)

    stack_i.GetYaxis().SetTitle("events/bin")

if len(sys.argv) != 6:
    print "USAGE: {} <TT_M1000.root> <TT_M1500.root> <TOP.root> <EW.root> <QCD.root>".format(sys.argv[0])
    sys.exit(1)
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
f = ROOT.TFile.Open(sys.argv[1], 'read')
g = ROOT.TFile.Open(sys.argv[2], 'read')
h = ROOT.TFile.Open(sys.argv[3], 'read')
i = ROOT.TFile.Open(sys.argv[4], 'read')
j = ROOT.TFile.Open(sys.argv[5], 'read')

hists_f = {}
hists_g = {}
hists_h = {}
hists_i = {}
hists_j = {}
stack = {}

keys = ['jetspuppi_btagmultiplicity', 'metspuppi_pt', 'TightElectrons_pt', 'TightMuons_eta', 'jetspuppi_eta', 'fatjets_tau21[m-softdrop]', 'fatjets_multiplicity', 'jetspuppi_multiplicity', 'TightElectrons_phi', 'TightElectrons_eta', 'fatjets_phi', 'jetspuppi_pt', 'TightMuons_phi', 'jetspuppi_mass', 'fatjets_H2b-multiplicity', 'St', 'TightMuons_mass', 'fatjets_Wtag-multiplicity', 'jetspuppi_phi', 'metspuppi_phi', 'fatjets_pt', 'fatjets_H1b-multiplicity', 'TightMuons_pt', 'fatjets_eta', 'fatjets_msoftdrop[tau21]', 'jetspuppi_Ht', 'TightElectrons_mass']

#reading very many histrograms
for key in keys:
    hists_f[key] = f.Get(key)
    hists_g[key] = g.Get(key)
    hists_h[key] = h.Get(key)
    hists_i[key] = i.Get(key)
    hists_j[key] = j.Get(key)

#outputDir = '/eos/user/k/kpal/www/i4DAPNVShN/all_signal_v2.1/'
outputDir = '/eos/uscms/store/user/kpal/trimmed_files_v2/plots/'
legend = ROOT.TLegend(0.7,0.8,0.91,0.91) #legend in top right corner
for key in hists_f.keys():
    canvas = ROOT.TCanvas('canvas','',700,500)
    stack[key] = createStack(key)

    hists_h[key].SetFillColor(7)
    #hists_h[key].SetLineColor(7)
    stack[key].Add(hists_h[key])
    hists_i[key].SetFillColor(6)
    #hists_i[key].SetLineColor(6)
    stack[key].Add(hists_i[key])
    hists_j[key].SetFillColor(2)
    #hists_j[key].SetLineColor(2)
    stack[key].Add(hists_j[key])
    stack[key].Draw("pfc hist")
    setTitle(stack[key],key)

    if key == "St" or "H2b" in key or "H1b" in key or key == "metspuppi_pt" or "_Ht" in key:
    #if key == "St" or "H2b" in key or "H1b" in key or key == "metspuppi_pt":
        canvas.SetLogy()
    hists_f[key].Scale(100)
    hists_g[key].Scale(1000)
    hists_f[key].SetLineColor(1)
    hists_g[key].SetLineColor(2)
    hists_f[key].Draw("same hist")
    hists_g[key].Draw("same hist")
    legend.AddEntry(hists_f[key],"TT_M1000 x 100")
    legend.AddEntry(hists_g[key],"TT_M1500 x 1000")
    legend.AddEntry(hists_h[key],"TOP")
    legend.AddEntry(hists_i[key],"EW")
    legend.AddEntry(hists_j[key],"QCD")
    legend.Draw()
    canvas.SaveAs(outputDir + key + ".png")
    canvas.SaveAs(outputDir + key + ".pdf")
    canvas.Close()
    legend.Clear()


f.Close()
g.Close()
h.Close()
i.Close()
j.Close()
