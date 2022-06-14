#import contextlib2
import ROOT
import sys
import os

def scale_hist(sys1):
    keys = ["St"]
    #keys = ["St_signal","St_top","St_ew","St_qcd","data_obs"]
#keys = ['jetspuppi_btagmultiplicity', 'metspuppi_pt', 'TightElectrons_pt', 'TightMuons_eta', 'jetspuppi_eta', 'jetspuppi_eta_1', 'jetspuppi_eta_2', 'jetspuppi_eta_3', 'fatjets_tau21[m-softdrop]', 'fatjets_multiplicity', 'jetspuppi_multiplicity', 'TightElectrons_phi', 'TightElectrons_eta', 'fatjets_phi', 'jetspuppi_pt', 'jetspuppi_pt_1','jetspuppi_pt_2','jetspuppi_pt_3','TightMuons_phi', 'jetspuppi_mass', 'fatjets_H2b-multiplicity', 'St', 'TightMuons_mass', 'fatjets_Wtag-multiplicity', 'jetspuppi_phi', 'metspuppi_phi', 'fatjets_pt', 'fatjets_H1b-multiplicity', 'TightMuons_pt', 'fatjets_eta', 'fatjets_msoftdrop[tau21]', 'jetspuppi_Ht', 'TightElectrons_mass']

    hists = {}
    #outputDir = os.path.dirname(sys1) + "/"
    #filename = os.path.basename(sys1)
    outputDir = "/eos/uscms/store/user/kpal/trimmed_files_v20.2/"
    filename = sys1.split("_v20.2")[1]

    #intLumi = {10, 35.9 ,300, 500, 1000, 2000, 3000, 10000, 30000, 100000, 300000, 1000000, 3000000, 10000000, 30000000}
    intLumi = {100000000, 300000000}
    #intLumi = {10}

    for lumi in intLumi:
        f = ROOT.TFile.Open(sys.argv[1], 'read')
        outFile = ROOT.TFile(outputDir + str(lumi) + filename,"RECREATE")

        scale_factor = lumi / 3000.0
        for key in keys:
            hists[key] = f.Get(key)
            hists[key].Scale(scale_factor)

        f.GetList().Write()
        print "OutFile written at {}".format(outFile)
        outFile.Close()

        f.Close()

def main():
    if len(sys.argv) < 2:
        print "USAGE: {} rootfile(s) with hist".format(sys.argv[0])
        sys.exit(1)
    for filename in sys.argv[1:]:
        scale_hist(filename)

if __name__ == "__main__":
    main()
