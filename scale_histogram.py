#import contextlib2
import ROOT
import sys
import os


keys = ["St"]
#keys = ['jetspuppi_btagmultiplicity', 'metspuppi_pt', 'TightElectrons_pt', 'TightMuons_eta', 'jetspuppi_eta', 'jetspuppi_eta_1', 'jetspuppi_eta_2', 'jetspuppi_eta_3', 'fatjets_tau21[m-softdrop]', 'fatjets_multiplicity', 'jetspuppi_multiplicity', 'TightElectrons_phi', 'TightElectrons_eta', 'fatjets_phi', 'jetspuppi_pt', 'jetspuppi_pt_1','jetspuppi_pt_2','jetspuppi_pt_3','TightMuons_phi', 'jetspuppi_mass', 'fatjets_H2b-multiplicity', 'St', 'TightMuons_mass', 'fatjets_Wtag-multiplicity', 'jetspuppi_phi', 'metspuppi_phi', 'fatjets_pt', 'fatjets_H1b-multiplicity', 'TightMuons_pt', 'fatjets_eta', 'fatjets_msoftdrop[tau21]', 'jetspuppi_Ht', 'TightElectrons_mass']

hists = {}
outputDir = os.path.dirname(sys.argv[1]) + "/"
filename = os.path.basename(sys.argv[1])
#intLumi = {300, 500, 1000, 2000}
intLumi = {35.9}

for lumi in intLumi:
    f = ROOT.TFile.Open(sys.argv[1], 'read')
    outFile = ROOT.TFile(outputDir + str(lumi) + '/' + filename,"RECREATE")

    scale_factor = lumi / 3000.0
    for key in keys:
        hists[key] = f.Get(key)
        hists[key].Scale(scale_factor)

    f.GetList().Write()
    #print "OutFile written at {}".format(outFile)
    outFile.Close()

    f.Close()
