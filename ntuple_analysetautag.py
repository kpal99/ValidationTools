#!/usr/bin/env python
import math
import optparse
from array import array

from ROOT import TFile, TLorentzVector, TProfile, TProfile2D

from bin.NtupleDataFormat import Ntuple

def nDaughters(gen):
    """Returns the number of daughters of a genparticle. """
    return gen.d2() - gen.d1()

def finalDaughters(gen, daughters=None):
    """Returns the list of the final daughters of a genparticle."""
    if daughters is None:
        daughters = []
    for i in range(gen.d1(), gen.d2()+1):
        daughter = genparts[i]
        if nDaughters(daughter) == 0:
            daughters.append(daughter)
        else:
            finalDaughters(daughter, daughters)
    return daughters

def hadronic(tau):
    """Returns the given object if it is a hadronic tau."""
    hadronic = True
    for d in finalDaughters(tau):
        if abs(d.pid()) in [11, 13]:
		    hadronic = False
	if hadronic:
		return tau

def fourmomentum(gen):
    """Returns the four-momentum representation of a particle."""
    Px = gen.pt()*math.cos(gen.phi())
    Py = gen.pt()*math.sin(gen.phi())
    Pz = gen.pt()*math.sinh(gen.eta())
    M = gen.mass()
    c = 1
    P = math.sqrt(Px**2 + Py**2 + Pz**2)
    E = math.sqrt(P**2*c**2 + M**2*c**4)
    pVec = TLorentzVector()
    pVec.SetPxPyPzE(Px, Py, Pz, E)
    return pVec

def visibleP4(gen):
    """Returns the four-momentum of the visible parts of tau objects."""
    daughter = finalDaughters(gen)
    taumomentum = TLorentzVector()
    for d in daughter:
        if abs(d.pid()) not in [12, 14, 16]:
            taumomentum += fourmomentum(d)
    return taumomentum

def filterDR(obj, collection):
    """Returns the given object filtered from the given collection."""
    objVec = TLorentzVector()
    objVec.SetPtEtaPhiM(obj.pt(), obj.eta(), obj.phi(), obj.mass())   
    for p in collection:
        pVec = TLorentzVector()
        pVec.SetPtEtaPhiM(p.pt(), p.eta(), p.phi(), p.mass())
        if objVec.DeltaR(pVec) > 0.3:
            return obj

def create2dHist(varname, params, title):
    if "to_pt" in varname and "tagRate" in varname:
        h = TProfile(varname, title, 50,
                          params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("#tau_{vis} p_{T} [GeV]")
        h.GetYaxis().SetTitle("tagging efficiency")
    if "to_eta" in varname and "tagRate" in varname:
        h = TProfile(varname, title, 50,
                          params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("#tau_{vis} #eta")
        h.GetYaxis().SetTitle("tagging efficiency")
    h.Sumw2()
    return h

def create2Dmap(varname, params, title):
    # use the slices to build a list of bin edges
    ptbins = [item[0] for item in params["ptSlices"]]
    etabins = [item[0] for item in params["etaSlices"]]
    ptbins.append(params["ptSlices"][-1][1])
    etabins.append(params["etaSlices"][-1][1])
    ptbinsext = []
    for iedge in range(0, len(ptbins)-1):
        binwidth = ptbins[iedge+1]-ptbins[iedge]
        if ptbins[iedge+1] >= 9e4:
            ptbinsext.append(ptbins[iedge])
            continue  # don't subdivide the overflow bin
        nsplits = params["sliceSplit"]
        if ptbins[iedge+1] >= 150 or ptbins[iedge] == 100:
            nsplits = 2
        for j in range(0, nsplits):  # 0, 1, 2 if sliceSplit = 3
            # low, low+0*width/3, low+width/3, low+2*width/3
            ptbinsext.append(ptbins[iedge] + int(j*binwidth/nsplits))
    ptbinsext.append(ptbins[-1])

    etabinsext = []
    for iedge in range(0, len(etabins)-1):
        binwidth = etabins[iedge+1]-etabins[iedge]
        if etabins[iedge+1] >= 9e4:
            etabinsext.append(etabins[iedge])
            continue  # don't subdivide the overflow bin
        nsplits = params["sliceSplit"]
        if 'electron' in varname and etabins[iedge] == 1.5:
            nsplits = 7
        for j in range(0, nsplits):  # 0, 1, 2 if sliceSplit = 3
            # low, low+0*width/3, low+width/3, low+2*width/3
            etabinsext.append(etabins[iedge] + j*binwidth/nsplits)
    etabinsext.append(etabins[-1])

    # arrays for ROOT
    xbins = array('d', ptbinsext)
    ybins = array('d', etabinsext)
    if "efficiency" in varname:
        h = TProfile2D(varname, title, len(xbins) -
                       1, xbins, len(ybins)-1, ybins)
        h.GetXaxis().SetTitle("tau p_{T} [GeV]")
        h.GetYaxis().SetTitle("tau #eta")
    h.Sumw2()
    return h

def main():
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--inFile',
                      dest='inFile',
                      help='input file [%default]',
                      default='/eos/cms/store/group/upgrade/RTB/FullsimFlat_111X/TT_TuneCP5_14TeV-powheg-pythia8_HLTTDRSummer20_200PU.root',
                      type='string')
    parser.add_option('-o', '--outFile',
                      dest='outFile',
                      help='output file [%default]',
                      default='tautag_analysis_output.root',
                      type='string')
    parser.add_option('-p', '--physObj',
                      dest='physobject',
                      help='object to analyze [%default]',
                      default='tau',
                      type='string')
    parser.add_option('--maxEvents',
                      dest='maxEvts',
                      help='max number of events [%default]',
                      default=10000,
                      type=int)
    (opt, args) = parser.parse_args()

    inFile = opt.inFile
    ntuple = Ntuple(inFile)
    maxEvents = opt.maxEvts
    tot_nevents = 0
    outputF = TFile(opt.outFile, "RECREATE")
    obj = opt.physobject

    params = {
        "dR": 0.5,
        "ptMin": 20,
        "etaSlices": [[0, 1.5], [1.5, 2.5], [2.5, 3.5], [3.5, 5]],
        "ptSlices": [[20, 50], [50, 100], [100, 500]],
        "sliceSplit": 1,
        "plotPtRange": [0, 500],
        "plotEtaRange": [-5, 5],
        "bitids": [
            ["looseID", (1 << 0), "#varepsilon(looseID)"],
            ["mediumID", (1 << 1), "#varepsilon(mediumID)"],
            ["tightID", (1 << 2), "#varepsilon(tightID)"],
        ]

    }

    ## create histos
    hists = {}
    for cut in ["nocut"]+params["etaSlices"]:
        hnames = ["tautagRate_to_pt",
                  "elecMistagRate_to_pt", "muonMistagRate_to_pt", "lightMistagRate_to_pt"]
        for hname in hnames:
            for quality in params["bitids"]:
                newname = hname+"_"+quality[0]+"_" + \
                    str(cut[0]) + "to" + str(cut[1])
                newname = ((newname.replace('.', 'p')).replace(
                    '100000p0', 'Inf')).replace('_ntoo', '')
                hists[obj+"_" +
                      newname] = create2dHist(obj+"_"+newname, params, quality[2])

    for cut in ["nocut"]+params["ptSlices"]:
        hnames = ["tautagRate_to_eta",
                  "elecMistagRate_to_eta", "muonMistagRate_to_eta", "lightMistagRate_to_eta"]
        for hname in hnames:
            for quality in params["bitids"]:
                newname = hname+"_"+quality[0]+"_" + \
                    str(cut[0]) + "to" + str(cut[1])
                newname = ((newname.replace('.', 'p')).replace(
                    '100000p0', 'Inf')).replace('_ntoo', '')
                hists[obj+"_" +
                      newname] = create2dHist(obj+"_"+newname, params, quality[2])

    hnames2D = ["tautagRate_efficiency2D",
                "elecMistagRate_efficiency2D", "muonMistagRate_efficiency2D", "lightMistagRate_efficiency2D"]
    for hname in hnames2D:
        for quality in params["bitids"]:
            newname = hname+"_"+quality[0]
            hists[obj+"_"+newname] = create2Dmap(
                obj+"_"+newname, params, quality[2])

    #study
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents % 1000) == 0:
            print '... processed {} events ...'.format(event.entry()+1)

        tot_nevents += 1

        taus = [p for p in event.taus() if p.pt() > params["ptMin"]]

        electrons = event.electrons()
        muons = event.muons()

        isolated_electrons = [p for p in electrons if p.pt() > 20 and (p.isopass() & 1) == 0 and (p.idpass() & 1) == 1]
        isolated_muons= [p for p in muons if p.pt() > 20 and (p.isopass() & 1) == 1 and (p.idpass() & 1) == 1]

        elec_filtered_taus = [filterDR(tau, isolated_electrons) for tau in taus if filterDR(tau, isolated_electrons) is not None]
        all_filtered_taus = [filterDR(tau, isolated_muons) for tau in elec_filtered_taus if filterDR(tau, isolated_muons) is not None]
        
        global genparts
        genparts = event.genparticles()

        genelectrons = [p for p in genparts if abs(p.pid()) == 11 and p.pt() > params["ptMin"]]
        genmuons = [p for p in genparts if abs(p.pid()) == 13 and p.pt() > params["ptMin"]]

        gentaus = [p for p in genparts if abs(p.pid()) == 15 and p.pt() > params["ptMin"]]
        hadronictaus = [visibleP4(hadronic(tau)) for tau in gentaus if hadronic(tau) != None]

        genlight = [p for p in genparts if abs(p.pid()) == 4 or abs(p.pid()) == 3 or abs(p.pid()) == 2 or abs(p.pid()) == 1] # creating a list here for the pids makes code run slower

        for tau in all_filtered_taus:
            tVec = TLorentzVector()
            tVec.SetPtEtaPhiM(tau.pt(), tau.eta(), tau.phi(), tau.mass())

            for gentau in hadronictaus:
                gentauVec = TLorentzVector()
                gentauVec.SetPtEtaPhiM(gentau.Pt(), gentau.Eta(), gentau.Phi(), gentau.M())
                if tVec.DeltaR(gentauVec) >= params["dR"]: continue
                for quality in params["bitids"]:
                    isTagged = int(bool(tau.isopass() & quality[1]))
                    hists[obj+"_tautagRate_to_eta_" +
                          quality[0]].Fill(tau.eta(), isTagged)
                    hists[obj+"_tautagRate_to_pt_" +
                          quality[0]].Fill(tau.pt(), isTagged)
                    hists[obj+"_tautagRate_efficiency2D_" +
                          quality[0]].Fill(tau.pt(), tau.eta(), isTagged)

                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] <= tau.pt() < cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(tau.isopass() & quality[1]))
                            hists[obj+"_tautagRate_to_eta_"+quality[0] +
                                  "_" + cutname].Fill(tau.eta(), isTagged)

                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] < abs(tau.eta()) <= cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(tau.isopass() & quality[1]))
                            hists[obj+"_tautagRate_to_pt_"+quality[0] +
                                  "_" + cutname].Fill(tau.pt(), isTagged)

            for e in genelectrons:
                eVec = TLorentzVector()
                eVec.SetPtEtaPhiM(e.pt(), e.eta(), e.phi(), e.mass())
                if tVec.DeltaR(eVec) >= params["dR"]: continue
                for quality in params["bitids"]:
                    isTagged = int(bool(tau.isopass() & quality[1]))
                    hists[obj+"_elecMistagRate_to_eta_" +
                          quality[0]].Fill(tau.eta(), isTagged)
                    hists[obj+"_elecMistagRate_to_pt_" +
                          quality[0]].Fill(tau.pt(), isTagged)
                    hists[obj+"_elecMistagRate_efficiency2D_" +
                          quality[0]].Fill(tau.pt(), tau.eta(), isTagged)

                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] <= tau.pt() < cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(tau.isopass() & quality[1]))
                            hists[obj+"_elecMistagRate_to_eta_"+quality[0] +
                                  "_" + cutname].Fill(tau.eta(), isTagged)

                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] < abs(p.eta()) <= cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(tau.isopass() & quality[1]))
                            hists[obj+"_elecMistagRate_to_pt_"+quality[0] +
                                  "_" + cutname].Fill(tau.pt(), isTagged)

            for m in genmuons:
                mVec = TLorentzVector()
                mVec.SetPtEtaPhiM(m.pt(), m.eta(), m.phi(), m.mass())
                if tVec.DeltaR(mVec) >= params["dR"]: continue
                for quality in params["bitids"]:
                    isTagged = int(bool(tau.isopass() & quality[1]))
                    hists[obj+"_muonMistagRate_to_eta_" +
                          quality[0]].Fill(tau.eta(), isTagged)
                    hists[obj+"_muonMistagRate_to_pt_" +
                          quality[0]].Fill(tau.pt(), isTagged)
                    hists[obj+"_muonMistagRate_efficiency2D_" +
                          quality[0]].Fill(tau.pt(), tau.eta(), isTagged)

                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] <= tau.pt() < cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(tau.isopass() & quality[1]))
                            hists[obj+"_muonMistagRate_to_eta_"+quality[0] +
                                  "_" + cutname].Fill(tau.eta(), isTagged)

                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] < abs(p.eta()) <= cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(tau.isopass() & quality[1]))
                            hists[obj+"_muonMistagRate_to_pt_"+quality[0] +
                                  "_" + cutname].Fill(tau.pt(), isTagged)

            for l in genlight:
                if l.pt() < params["ptMin"]: continue
                lVec = TLorentzVector()
                lVec.SetPtEtaPhiM(l.pt(), l.eta(), l.phi(), l.mass())
                if tVec.DeltaR(lVec) >= params["dR"]: continue
                for quality in params["bitids"]:
                    isTagged = int(bool(tau.isopass() & quality[1]))
                    hists[obj+"_lightMistagRate_to_eta_" +
                          quality[0]].Fill(tau.eta(), isTagged)
                    hists[obj+"_lightMistagRate_to_pt_" +
                          quality[0]].Fill(tau.pt(), isTagged)
                    hists[obj+"_lightMistagRate_efficiency2D_" +
                          quality[0]].Fill(tau.pt(), tau.eta(), isTagged)

                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] <= tau.pt() < cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(tau.isopass() & quality[1]))
                            hists[obj+"_lightMistagRate_to_eta_"+quality[0] +
                                  "_" + cutname].Fill(tau.eta(), isTagged)

                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] < abs(tau.eta()) <= cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(tau.isopass() & quality[1]))
                            hists[obj+"_lightMistagRate_to_pt_"+quality[0] +
                                  "_" + cutname].Fill(tau.pt(), isTagged)

    outputF.cd()
    for h in hists.keys():
        hists[h].Write()

if __name__ == "__main__":
    main()
