#!/usr/bin/env python
import sys
import ROOT
from array import array
from bin.NtupleDataFormat import Ntuple


class TreeProducer:
    def __init__(self):

         self.t = ROOT.TTree( "mytree","TestTree" )
         self.maxn = 9999

         # declare arrays
         self.evt_size = array( 'i', [ 0 ] )

         ## put dummy value for now
         self.true_int         = array( 'i', [ -1 ] )

         ## main MC weight
         self.genweight         = array( 'f', [ 0 ] )
         self.lheweight_size        = array( 'i', [ 0 ] )
         self.lheweight_val         = array( 'f', self.maxn*[ 0. ] )

         self.vtx_size        = array( 'i', [ 0 ] )
         self.vtx_pt2         = array( 'f', self.maxn*[ 0. ] )
         self.vtx_z         = array( 'f', self.maxn*[ 0. ] )
         self.vtx_x         = array( 'f', self.maxn*[ 0. ] )
         self.vtx_y        = array( 'f', self.maxn*[ 0. ] )

         self.elec_size        = array( 'i', [ 0 ] )
         self.elec_pt          = array( 'f', self.maxn*[ 0. ] )
         self.elec_eta         = array( 'f', self.maxn*[ 0. ] )
         self.elec_phi         = array( 'f', self.maxn*[ 0. ] )
         self.elec_mass        = array( 'f', self.maxn*[ 0. ] )
         self.elec_charge      = array( 'i', self.maxn*[ 0 ] )
         self.elec_idvar       = array( 'f', self.maxn*[ 0. ] )
         self.elec_reliso      = array( 'f', self.maxn*[ 0. ] )
         self.elec_idpass      = array( 'i', self.maxn*[ 0 ] )
         self.elec_isopass     = array( 'i', self.maxn*[ 0 ] )

         self.tightElec_size        = array( 'i', [ 0 ] )
         self.tightElec_pt          = array( 'f', self.maxn*[ 0 ] )
         self.tightElec_eta         = array( 'f', self.maxn*[ 0 ] )
         self.tightElec_phi         = array( 'f', self.maxn*[ 0 ] )
         self.tightElec_mass        = array( 'f', self.maxn*[ 0 ] )
         self.tightElec_charge      = array( 'i', self.maxn*[ 0 ] )
         self.tightElec_idvar       = array( 'f', self.maxn*[ 0 ] )
         self.tightElec_reliso      = array( 'f', self.maxn*[ 0 ] )
         self.tightElec_idpass      = array( 'i', self.maxn*[ 0 ] )
         self.tightElec_isopass     = array( 'i', self.maxn*[ 0 ] )

         self.muon_size        = array( 'i', [ 0 ] )
         self.muon_pt          = array( 'f', self.maxn*[ 0. ] )
         self.muon_eta         = array( 'f', self.maxn*[ 0. ] )
         self.muon_phi         = array( 'f', self.maxn*[ 0. ] )
         self.muon_mass        = array( 'f', self.maxn*[ 0. ] )
         self.muon_charge      = array( 'i', self.maxn*[ 0 ] )
         self.muon_idvar       = array( 'f', self.maxn*[ 0. ] )
         self.muon_reliso      = array( 'f', self.maxn*[ 0. ] )
         self.muon_idpass      = array( 'i', self.maxn*[ 0 ] )
         self.muon_isopass     = array( 'i', self.maxn*[ 0 ] )

         self.tightMuon_size        = array( 'i', [ 0 ] )
         self.tightMuon_pt          = array( 'f', self.maxn*[ 0 ] )
         self.tightMuon_eta         = array( 'f', self.maxn*[ 0 ] )
         self.tightMuon_phi         = array( 'f', self.maxn*[ 0 ] )
         self.tightMuon_mass        = array( 'f', self.maxn*[ 0 ] )
         self.tightMuon_charge      = array( 'i', self.maxn*[ 0 ] )
         self.tightMuon_idvar       = array( 'f', self.maxn*[ 0 ] )
         self.tightMuon_reliso      = array( 'f', self.maxn*[ 0 ] )
         self.tightMuon_idpass      = array( 'i', self.maxn*[ 0 ] )
         self.tightMuon_isopass     = array( 'i', self.maxn*[ 0 ] )

         self.jetpuppi_size         = array( 'i', [ 0 ] )
         self.jetpuppi_pt           = array( 'f', self.maxn*[ 0. ] )
         self.jetpuppi_eta          = array( 'f', self.maxn*[ 0. ] )
         self.jetpuppi_phi          = array( 'f', self.maxn*[ 0. ] )
         self.jetpuppi_mass         = array( 'f', self.maxn*[ 0. ] )
         self.jetpuppi_idpass       = array( 'i', self.maxn*[ 0 ] )
         self.jetpuppi_DeepJET      = array( 'f', self.maxn*[ 0. ] )
         self.jetpuppi_btag         = array( 'i', self.maxn*[ 0 ] )

         self.jetM          = array( 'i', [ 0 ] )
         self.jetBtag       = array( 'i', [ 0 ] )
         self.jetHt         = array( 'f', [ 0 ] )
         self.jetSt         = array( 'f', [ 0 ] )

         self.fatjet_size                   = array('i', [0 ])
         self.fatjet_pt                     = array('f', self.maxn*[0. ])
         self.fatjet_eta                    = array('f', self.maxn*[0. ])
         self.fatjet_phi                    = array('f', self.maxn*[0. ])
         self.fatjet_mass                   = array('f', self.maxn*[0. ])
         self.fatjet_tau1                   = array('f', self.maxn*[0. ])
         self.fatjet_tau2                   = array('f', self.maxn*[0. ])
         self.fatjet_tau3                   = array('f', self.maxn*[0. ])
         self.fatjet_tau4                   = array('f', self.maxn*[0. ])
         self.fatjet_msoftdrop              = array('f', self.maxn*[0. ])

         self.fatjetM          = array( 'i', [ 0 ] )
         self.fatjetH2b        = array( 'i', [ 0 ] )
         self.fatjetH1b        = array( 'i', [ 0 ] )
         self.fatjetW          = array( 'i', [ 0 ] )

         self.metpuppi_size         = array( 'i', [ 0 ] )
         self.metpuppi_pt           = array( 'f', self.maxn*[ 0. ] )
         self.metpuppi_phi          = array( 'f', self.maxn*[ 0. ] )

         # declare tree branches
         self.t.Branch( "evt_size",self.evt_size, "evt_size/I")

         self.t.Branch( "genweight",self.genweight, "genweight/F")
         self.t.Branch( "lheweight_size",self.lheweight_size, "lheweight_size/I")
         self.t.Branch( "lheweight_val",self.lheweight_val, "lheweight_val[lheweight_size]/F")

         self.t.Branch( "vtx_size",self.vtx_size, "vtx_size/I")
         self.t.Branch( "vtx_pt2",self.vtx_pt2, "vtx_pt2[vtx_size]/F")
         self.t.Branch( "vtx_z",self.vtx_z, "vtx_x[vtx_size]/F")
         self.t.Branch( "vtx_x",self.vtx_x, "vtx_x[vtx_size]/F")
         self.t.Branch( "vtx_y",self.vtx_y, "vtx_y[vtx_size]/F")

         self.t.Branch( "elec_size",self.elec_size, "elec_size/I")
         self.t.Branch( "elec_pt",self.elec_pt, "elec_pt[elec_size]/F")
         self.t.Branch( "elec_eta",self.elec_eta, "elec_eta[elec_size]/F")
         self.t.Branch( "elec_phi",self.elec_phi, "elec_phi[elec_size]/F")
         self.t.Branch( "elec_mass",self.elec_mass, "elec_mass[elec_size]/F")
         self.t.Branch( "elec_charge",self.elec_charge, "elec_charge[elec_size]/I")
         self.t.Branch( "elec_idvar",self. elec_idvar, "elec_idvar[elec_size]/F")
         self.t.Branch( "elec_reliso",self.elec_reliso, "elec_reliso[elec_size]/F")
         self.t.Branch( "elec_idpass",self.elec_idpass, "elec_idpass[elec_size]/i")
         self.t.Branch( "elec_isopass",self. elec_isopass, "elec_isopass[elec_size]/i")

         self.t.Branch( "tightElec_size",self.tightElec_size, "tightElec_size/I")
         self.t.Branch( "tightElec_pt",self.tightElec_pt, "tightElec_pt[tightElec_size]/F")
         self.t.Branch( "tightElec_eta",self.tightElec_eta, "tightElec_eta[tightElec_size]/F")
         self.t.Branch( "tightElec_phi",self.tightElec_phi, "tightElec_phi[tightElec_size]/F")
         self.t.Branch( "tightElec_mass",self.tightElec_mass, "tightElec_mass[tightElec_size]/F")
         self.t.Branch( "tightElec_charge",self.tightElec_charge, "tightElec_charge[tightElec_size]/I")
         self.t.Branch( "tightElec_idvar",self.tightElec_idvar, "tightElec_idvar[tightElec_size]/F")
         self.t.Branch( "tightElec_reliso",self.tightElec_reliso, "tightElec_reliso[tightElec_size]/F")
         self.t.Branch( "tightElec_idpass",self.tightElec_idpass, "tightElec_idpass[tightElec_size]/i")
         self.t.Branch( "tightElec_isopass",self. tightElec_isopass, "tightElec_isopass[tightElec_size]/i")

         self.t.Branch( "muon_size",self.muon_size, "muon_size/I")
         self.t.Branch( "muon_pt",self.muon_pt, "muon_pt[muon_size]/F")
         self.t.Branch( "muon_eta",self.muon_eta, "muon_eta[muon_size]/F")
         self.t.Branch( "muon_phi",self.muon_phi, "muon_phi[muon_size]/F")
         self.t.Branch( "muon_mass",self.muon_mass, "muon_mass[muon_size]/F")
         self.t.Branch( "muon_charge",self.muon_charge, "muon_charge[muon_size]/I")
         self.t.Branch( "muon_idvar",self. muon_idvar, "muon_idvar[muon_size]/F")
         self.t.Branch( "muon_reliso",self.muon_reliso, "muon_reliso[muon_size]/F")
         self.t.Branch( "muon_idpass",self. muon_idpass, "muon_idpass[muon_size]/i")
         self.t.Branch( "muon_isopass",self. muon_isopass, "muon_isopass[muon_size]/i")

         self.t.Branch( "tightMuon_size",self.tightMuon_size, "tightMuon_size/I")
         self.t.Branch( "tightMuon_pt",self.tightMuon_pt, "tightMuon_pt[tightMuon_size]/F")
         self.t.Branch( "tightMuon_eta",self.tightMuon_eta, "tightMuon_eta[tightMuon_size]/F")
         self.t.Branch( "tightMuon_phi",self.tightMuon_phi, "tightMuon_phi[tightMuon_size]/F")
         self.t.Branch( "tightMuon_mass",self.tightMuon_mass, "tightMuon_mass[tightMuon_size]/F")
         self.t.Branch( "tightMuon_charge",self.tightMuon_charge, "tightMuon_charge[tightMuon_size]/I")
         self.t.Branch( "tightMuon_idvar",self.tightMuon_idvar, "tightMuon_idvar[tightMuon_size]/F")
         self.t.Branch( "tightMuon_reliso",self.tightMuon_reliso, "tightMuon_reliso[tightMuon_size]/F")
         self.t.Branch( "tightMuon_idpass",self.tightMuon_idpass, "tightMuon_idpass[tightMuon_size]/i")
         self.t.Branch( "tightMuon_isopass",self. tightMuon_isopass, "tightMuon_isopass[tightMuon_size]/i")

         self.t.Branch( "jetpuppi_size",self.jetpuppi_size, "jetpuppi_size/I")
         self.t.Branch( "jetpuppi_pt",self.jetpuppi_pt, "jetpuppi_pt[jetpuppi_size]/F")
         self.t.Branch( "jetpuppi_eta",self.jetpuppi_eta, "jetpuppi_eta[jetpuppi_size]/F")
         self.t.Branch( "jetpuppi_phi",self.jetpuppi_phi, "jetpuppi_phi[jetpuppi_size]/F")
         self.t.Branch( "jetpuppi_mass",self.jetpuppi_mass, "jetpuppi_mass[jetpuppi_size]/F")
         self.t.Branch( "jetpuppi_idpass",self. jetpuppi_idpass, "jetpuppi_idpass[jetpuppi_size]/i")
         self.t.Branch( "jetpuppi_DeepJET",self.jetpuppi_DeepJET,"jetpuppi_DeepJET[jetpuppi_size]/F")
         self.t.Branch( "jetpuppi_btag",self.jetpuppi_btag,"jetpuppi_btag[jetpuppi_size]/I")

         self.t.Branch( "jetM",self.jetM, "jetM/I")
         self.t.Branch( "jetBtag",self.jetBtag, "jetBtag/I")
         self.t.Branch( "jetHt",self.jetHt, "jetHt/F")
         self.t.Branch( "jetSt",self.jetSt, "jetSt/F")

         self.t.Branch("fatjet_size", self.fatjet_size, "fatjet_size/I")
         self.t.Branch("fatjet_pt", self.fatjet_pt, "fatjet_pt[fatjet_size]/F")
         self.t.Branch("fatjet_eta", self.fatjet_eta, "fatjet_eta[fatjet_size]/F")
         self.t.Branch("fatjet_phi", self.fatjet_phi, "fatjet_phi[fatjet_size]/F")
         self.t.Branch("fatjet_mass", self.fatjet_mass, "fatjet_mass[fatjet_size]/F")
         self.t.Branch("fatjet_pt", self.fatjet_pt, "fatjet_pt[fatjet_size]/F")
         self.t.Branch("fatjet_tau1", self.fatjet_tau1, "fatjet_tau1[fatjet_size]/F")
         self.t.Branch("fatjet_tau2", self.fatjet_tau2, "fatjet_tau2[fatjet_size]/F")
         self.t.Branch("fatjet_tau3", self.fatjet_tau3, "fatjet_tau3[fatjet_size]/F")
         self.t.Branch("fatjet_tau4", self.fatjet_tau4, "fatjet_tau4[fatjet_size]/F")
         self.t.Branch("fatjet_msoftdrop", self.fatjet_msoftdrop, "fatjet_msoftdrop[fatjet_size]/F")

         self.t.Branch( "fatjetM",self.fatjetM, "fatjetM/I")
         self.t.Branch( "fatjetH2b",self.fatjetH2b, "fatjetH2b/I")
         self.t.Branch( "fatjetH1b",self.fatjetH1b, "fatjetH1b/I")
         self.t.Branch( "fatjetW",self.fatjetW, "fatjetW/I")

         self.t.Branch( "metpuppi_size",self.metpuppi_size, "metpuppi_size/I")
         self.t.Branch( "metpuppi_pt",self. metpuppi_pt, "metpuppi_pt[metpuppi_size]/F")
         self.t.Branch( "metpuppi_phi",self.metpuppi_phi, "metpuppi_phi[metpuppi_size]/F")

    #___________________________________________
    def processEvent(self, entry):
        self.evt_size[0] = entry


    #___________________________________________
    def processWeights(self, genweight, lheweights):
        self.genweight[0] = genweight
        i = 0
        for item in lheweights:
            self.lheweight_val[i] = item.val()
            i += 1
        self.lheweight_size[0] = i

    #___________________________________________
    def processVtxs(self, vtxs):
        i = 0
        for item in vtxs:
            if i == 0:
                self.vtx_pt2   [i] = item.pt2()
                self.vtx_x     [i] = item.x()
                self.vtx_y     [i] = item.y()
                self.vtx_z     [i] = item.z()
            i += 1
        self.vtx_size[0] = i

    #___________________________________________
    def processElectrons(self, electrons):
        i = 0
        for item in electrons:
            self.elec_pt      [i] = item.pt()
            self.elec_eta     [i] = item.eta()
            self.elec_phi     [i] = item.phi()
            self.elec_mass    [i] = item.mass()
            self.elec_charge  [i] = item.charge()
            self.elec_idvar   [i] = item.idvar()  #
            self.elec_reliso  [i] = item.reliso()
            self.elec_idpass  [i] = item.idpass() #
            self.elec_isopass [i] = item.isopass()#
            i += 1
        self.elec_size[0] = i

    #___________________________________________
    def processTightElectrons_(self, value, pt, eta, phi, mass, charge, idvar, reliso, idpass, isopass):
        if value == True:
            self.tightElec_pt      [0] = pt
            self.tightElec_eta     [0] = eta
            self.tightElec_phi     [0] = phi
            self.tightElec_mass    [0] = mass
            self.tightElec_charge  [0] = charge
            self.tightElec_idvar   [0] = idvar
            self.tightElec_reliso  [0] = reliso
            self.tightElec_idpass  [0] = idpass
            self.tightElec_isopass [0] = isopass
            self.tightElec_size    [0] = 1
        else:
            self.tightElec_size    [0] = 0
    #___________________________________________
    def processTightElectrons(self, tightElectrons):
        i = 0
        for item in tightElectrons:
            self.tightElec_pt      [i] = item.pt()
            self.tightElec_eta     [i] = item.eta()
            self.tightElec_phi     [i] = item.phi()
            self.tightElec_mass    [i] = item.mass()
            self.tightElec_charge  [i] = item.charge()
            self.tightElec_idvar   [i] = item.idvar()  #
            self.tightElec_reliso  [i] = item.reliso()
            self.tightElec_idpass  [i] = item.idpass() #
            self.tightElec_isopass [i] = item.isopass()#
            i += 1
        self.tightElec_size[0] = i
    #___________________________________________
    def processMuons(self, muons):
        i = 0
        for item in muons:
            self.muon_pt      [i] = item.pt()
            self.muon_eta     [i] = item.eta()
            self.muon_phi     [i] = item.phi()
            self.muon_mass    [i] = item.mass()
            self.muon_charge  [i] = item.charge()
            self.muon_idvar   [i] = item.idvar()  #
            self.muon_reliso  [i] = item.reliso()
            self.muon_idpass  [i] = item.idpass() #
            self.muon_isopass [i] = item.isopass()#
            i += 1
        self.muon_size[0] = i

    #___________________________________________
    def processTightMuons_(self, value, pt, eta, phi, mass, charge, idvar, reliso, idpass, isopass):
        if value == True:
            self.tightMuon_pt      [0] = pt
            self.tightMuon_eta     [0] = eta
            self.tightMuon_phi     [0] = phi
            self.tightMuon_mass    [0] = mass
            self.tightMuon_charge  [0] = charge
            self.tightMuon_idvar   [0] = idvar
            self.tightMuon_reliso  [0] = reliso
            self.tightMuon_idpass  [0] = idpass
            self.tightMuon_isopass [0] = isopass
            self.tightMuon_size    [0] = 1
        else:
            self.tightMuon_size    [0] = 0
    #___________________________________________
    def processTightMuons(self, tightMuons):
        i = 0
        for item in tightMuons:
            self.tightMuon_pt      [i] = item.pt()
            self.tightMuon_eta     [i] = item.eta()
            self.tightMuon_phi     [i] = item.phi()
            self.tightMuon_mass    [i] = item.mass()
            self.tightMuon_charge  [i] = item.charge()
            self.tightMuon_idvar   [i] = item.idvar()  #
            self.tightMuon_reliso  [i] = item.reliso()
            self.tightMuon_idpass  [i] = item.idpass() #
            self.tightMuon_isopass [i] = item.isopass()#
            i += 1
        self.tightMuon_size[0] = i

    def processPuppiJets(self, jets):
        i = 0
        for item in jets:
            if item.pt() > 30 and abs(item.eta()) < 2.4:
                self.jetpuppi_pt      [i] = item.pt()
                self.jetpuppi_eta     [i] = item.eta()
                self.jetpuppi_phi     [i] = item.phi()
                self.jetpuppi_mass    [i] = item.mass()
                self.jetpuppi_idpass  [i] = item.idpass()        #
                self.jetpuppi_DeepJET [i] = item.DeepJET()        #
                self.jetpuppi_btag    [i] = item.btag()        #
                i += 1
        self.jetpuppi_size[0] = i
    #-------------------------------------------
    #___________________________________________
    def processJetsMul_(self, M, Btag, Ht, St):
        self.jetM[0] = M
        self.jetBtag[0] = Btag
        self.jetHt[0] = Ht
        self.jetSt[0] = St

    def processFatJets(self, jets):
        i = 0
        for item in jets:
            self.fatjet_pt                     [i] = item.pt()
            self.fatjet_eta                    [i] = item.eta()
            self.fatjet_phi                    [i] = item.phi()
            self.fatjet_mass                   [i] = item.mass()
            self.fatjet_tau1                   [i] = item.tau1()
            self.fatjet_tau2                   [i] = item.tau2()
            self.fatjet_tau3                   [i] = item.tau3()
            self.fatjet_tau4                   [i] = item.tau4()
            self.fatjet_msoftdrop              [i] = item.msoftdrop()
            i += 1
        self.fatjet_size[0] = i

    #___________________________________________
    def processFatjetsMul_(self, M, H2b, H1b, W):
        self.fatjetM[0] = M
        self.fatjetH2b[0] = H2b
        self.fatjetH1b[0] = H1b
        self.fatjetW[0] = W
    #___________________________________________
    def processPuppiMissingET(self, met):
        i = 0
        for item in met:
            self.metpuppi_pt    [i] = item.pt()
            self.metpuppi_phi   [i] = item.phi()
            i += 1
        self.metpuppi_size  [0] = i

    #___________________________________________
    def processPuppiMissingET_(self, pt, phi):
        self.metpuppi_pt    [0] = pt
        self.metpuppi_phi   [0] = phi
        self.metpuppi_size  [0] = 1


    def fill(self):
        self.t.Fill()

    def write(self):
        self.t.Write()
#_____________________________________________________________________________________________________________
def main():

#    ROOT.gSystem.Load("libDelphes")
#    try:
#      ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
#      ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
#    except:
#      pass
#
#    parser = argparse.ArgumentParser()
#    parser.add_argument ('-i', '--input', help='input Delphes file',  default='delphes.root')
#    parser.add_argument ('-o', '--output', help='output flat tree',  default='tree.root')
#    parser.add_argument ('-n', '--nev', help='number of events', type=int, default=-1)
#    parser.add_argument ('-d', '--debug', help='debug flag',  action='store_true',  default=False)
#
#    args = parser.parse_args()
#
#    inputFile = args.input
#    outputFile = args.output
#    debug = args.debug
#    print debug
    maxEvents = 10
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    outputFile = 'example_trimmed.root'
    out_root = ROOT.TFile(outputFile,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")

#    chain = ROOT.TChain("Delphes")
#    chain.Add(inputFile)


    # Create object of class ExRootTreeReader
#    treeReader = ROOT.ExRootTreeReader(chain)
#    numberOfEntries = treeReader.GetEntries()

    ## for now only M for electrons, LT for muons and LT for photons are defined !!
    ## should dervie new parameterisations for other working points

#    branchEvent           = treeReader.UseBranch('Event')
#    branchWeight          = treeReader.UseBranch('Weight')
#
#    branchVertex          = treeReader.UseBranch('Vertex')
#    branchParticle        = treeReader.UseBranch('Particle')
#    branchGenJet          = treeReader.UseBranch('GenJet')
#    branchGenMissingET    = treeReader.UseBranch('GenMissingET')
#
#    branchPhoton          = treeReader.UseBranch('Photon')
#    branchPhotonLoose     = treeReader.UseBranch('PhotonLoose')
#    branchPhotonMedium    = treeReader.UseBranch('PhotonMedium')
#    branchPhotonTight     = treeReader.UseBranch('PhotonTight')
#
#    branchElectron        = treeReader.UseBranch('Electron')
#    branchElectronLoose   = treeReader.UseBranch('ElectronLoose')
#    branchElectronMedium  = treeReader.UseBranch('ElectronMedium')
#    branchElectronTight   = treeReader.UseBranch('ElectronTight')
#
#    branchMuon            = treeReader.UseBranch('Muon')
#    branchMuonLoose       = treeReader.UseBranch('MuonLoose')
#    branchMuonMedium      = treeReader.UseBranch('MuonMedium')
#    branchMuonTight       = treeReader.UseBranch('MuonTight')
#
#    branchPuppiJet        = treeReader.UseBranch('JetPUPPI')
#    branchPuppiJetLoose   = treeReader.UseBranch('JetPUPPILoose')
#    branchPuppiJetTight   = treeReader.UseBranch('JetPUPPITight')
#    branchFatJet          = treeReader.UseBranch('JetPUPPIAK8')
#
#    #branchCHSJet          = treeReader.UseBranch('Jet')
#
#    branchPuppiMissingET  = treeReader.UseBranch('PuppiMissingET')
#    #branchPFMissingET     = treeReader.UseBranch('MissingET')
#
#    # NEED these branches to access jet constituents
#    branchPuppiCandidate  = treeReader.UseBranch('ParticleFlowCandidate')
#    #branchPFCandidateCHS  = treeReader.UseBranch('ParticleFlowCandidateCHS')
#
#    branchRho             = treeReader.UseBranch('Rho')

    treeProducer = TreeProducer()
    for event in ntuple:
        if event.entry() >= maxEvents and maxEvents > 0:
            break

        treeProducer.processEvent(event.entry())
        treeProducer.processWeights(event.genweight())
        treeProducer.processElectrons(event.electrons())
        treeProducer.processMuons(event.muons())
        treeProducer.processPuppiJets(event.jetspuppi())
        treeProducer.processFatJets(event.fatjets())
        treeProducer.processPuppiMissingET(event.metspuppi())

        ## fill tree
        treeProducer.fill()
        print " Filled event {}".format(event.entry())

    print out_root
    treeProducer.write()
    out_root.Close()

#_______________________________________________________________________________________
if __name__ == "__main__":
    main()

