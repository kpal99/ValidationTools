#!/usr/bin/env python
import ROOT
# from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from ROOT import TH1D, TFile, TLorentzVector, TProfile, TProfile2D
import sys
import optparse
import itertools
from array import array
import math


def findHadronFlav(genparts, jet, dR):

    isbHad = False
    iscHad = False
    for g in genparts:  # check if there exists one b-hadron
        gVec = ROOT.TLorentzVector()
        gVec.SetPtEtaPhiM(g.pt(), g.eta(), g.phi(), g.mass())
        if jet.DeltaR(gVec) >= dR:
            continue
        if 500 < abs(g.pid()) < 600 or 5000 < abs(g.pid()) < 6000:
            isbHad = True
            break
        if 400 < abs(g.pid()) < 500 or 4000 < abs(g.pid()) < 5000:
            iscHad = True
    if isbHad:
        return 5
    if iscHad:
        return 4
    return 1  # any not 4 or 5 case


def findPartonFlav(genparts, jet, dR):

    isbPar = False
    iscPar = False
    for g in genparts:  # check if there exists one b-hadron
        gVec = ROOT.TLorentzVector()
        gVec.SetPtEtaPhiM(g.pt(), g.eta(), g.phi(), g.mass())
        if jet.DeltaR(gVec) >= dR:
            continue
        if abs(g.pid()) == 5:
            isbPar = True
            break
        if abs(g.pid()) == 4:
            iscPar = True
    if isbPar:
        return 5
    if iscPar:
        return 4
    return 1  # any not 4 or 5 case


def doSum(objs, ptCut, etaCut):
    s = 0
    for j in objs:
        if j.pt() > ptCut and abs(j.eta()) < etaCut:
            s += j.pt()
    return s


def doCount(objs, ptCut, etaCut):
    cnt = 0
    for j in objs:
        if j.pt() > ptCut and abs(j.eta()) < etaCut:
            cnt += 1
    return cnt


def create2dHist(varname, params, title):
    if "to_pt" in varname and "tagRate" in varname:
        h = ROOT.TProfile(varname, title, 50,
                          params["plotPtRange"][0], params["plotPtRange"][1])
        h.GetXaxis().SetTitle("jet p_{T} [GeV]")
        h.GetYaxis().SetTitle("tagging efficiency")
    if "to_eta" in varname and "tagRate" in varname:
        h = ROOT.TProfile(varname, title, 50,
                          params["plotEtaRange"][0], params["plotEtaRange"][1])
        h.GetXaxis().SetTitle("jet #eta")
        h.GetYaxis().SetTitle("tagging efficiency")

    h.Sumw2()
    return h


def create2Dmap(varname, params, title, dumptcl):

    # use the slices to build a list of bin edges
    ptbins = [item[0] for item in params["ptSlices"]]
    etabins = [item[0] for item in params["etaSlices2D"]]
    ptbins.append(params["ptSlices"][-1][1])
    etabins.append(params["etaSlices2D"][-1][1])
    # set more realistic caps
    if not dumptcl:
        if ptbins[-1] > 5e4:
            ptbins[-1] = ptbins[-2]*2.  # probably somewhere in 200 -- 4000?
        if etabins[-1] > 5e4:
            etabins[-1] = 5.

    ptbinsext = []
    for iedge in range(0, len(ptbins)-1):
        # print "ptbins"+str(ptbins)
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
    # print ptbinsext

    etabinsext = []
    for iedge in range(0, len(etabins)-1):
        # print "etabins"+str(etabins)
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
    # print etabinsext

    # arrays for ROOT
    xbins = array('d', ptbinsext)
    ybins = array('d', etabinsext)
    if "efficiency" in varname:
        h = TProfile2D(varname, title, len(xbins) -
                       1, xbins, len(ybins)-1, ybins)
        h.GetXaxis().SetTitle("jet p_{T} [GeV]")
        h.GetYaxis().SetTitle("jet #eta")

    h.Sumw2()
    return h


def main():
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--inFile',
                      dest='inFile',
                      # /eos/cms/store/group/upgrade/RTB/DelphesFlat_343pre01
                      help='input file [%default]',
                      default='/eos/cms/store/group/upgrade/RTB/FullsimFlat_110X/TT_TuneCP5_14TeV_200PU.root',
                      type='string')
    parser.add_option('-o', '--outFile',
                      dest='outFile',
                      help='output file [%default]',
                      default='histo_full/val_btag.root',
                      type='string')
    parser.add_option('-p', '--physObj',
                      dest='physobject',
                      help='object to analyze [%default]',
                      default='jetpuppi',
                      type='string')
    parser.add_option('--maxEvents',
                      dest='maxEvts',
                      help='max number of events [%default]',
                      default=10000,
                      type=int)
    parser.add_option('--dumptcl',
                      dest='dumptcl',
                      help='use more bins for making tcl file?',
                      action="store_true",
                      default=False)
    (opt, args) = parser.parse_args()

    inFile = opt.inFile
    print(inFile)
    ntuple = Ntuple(inFile)
    maxEvents = opt.maxEvts
    dumptcl = opt.dumptcl
    tot_nevents = 0
    outputF = ROOT.TFile(opt.outFile, "RECREATE")
    obj = opt.physobject

    params = {
        "dR": 0.5,
        "ptRatio": 2.0,
        "ptMin": 20,
        "etaSlices": [[0, 1.3], [1.3, 2.5], [2.5, 3], [3, 1e5]],
        # up to eta = 4 for 2D maps
        "etaSlices2D": [[0, 1.3], [1.3, 2.5], [2.5, 3], [3, 4]],
        "ptSlices": [[20, 50], [50, 100], [100, 200], [200, 400], [400, 1e5]],
        "sliceSplit": 1,  # for 2D map, make N divisions of each slice
        "plotPtRange": [0, 500],
        "plotEtaRange": [-5, 5],
        "ids": [
            ["looseID", 1, "#varepsilon(looseID)"],  # btag >= 1
            ["mediumID", 3, "#varepsilon(mediumID)"],
            ["tightID", 7, "#varepsilon(tightID)"]],
        "bitids": [
            ["looseID", (1 << 0), "#varepsilon(looseID)"],  # btag & (1<<0)
            ["mediumID", (1 << 1), "#varepsilon(mediumID)"],
            ["tightID", (1 << 2), "#varepsilon(tightID)"]]
    }

    ## create histo#

    hists = {}

    for cut in ["nocut"]+params["etaSlices"]:
        hnames = ["btagRate_to_pt", "cMistagRate_to_pt",
                  "lightMistagRate_to_pt"]
        for hname in hnames:
            for quality in params["bitids"]:
                newname = hname+"_"+quality[0]+"_" + \
                    str(cut[0]) + "to" + str(cut[1])
                newname = ((newname.replace('.', 'p')).replace(
                    '100000p0', 'Inf')).replace('_ntoo', '')
                hists[obj+"_" +
                      newname] = create2dHist(obj+"_"+newname, params, quality[2])

    for cut in ["nocut"]+params["ptSlices"]:
        hnames = ["btagRate_to_eta", "cMistagRate_to_eta",
                  "lightMistagRate_to_eta"]
        for hname in hnames:
            for quality in params["bitids"]:
                newname = hname+"_"+quality[0]+"_" + \
                    str(cut[0]) + "to" + str(cut[1])
                newname = ((newname.replace('.', 'p')).replace(
                    '100000p0', 'Inf')).replace('_ntoo', '')
                hists[obj+"_" +
                      newname] = create2dHist(obj+"_"+newname, params, quality[2])

    hnames2D = ["btagRate_efficiency2D",
                "cMistagRate_efficiency2D", "lightMistagRate_efficiency2D"]
    for hname in hnames2D:
        for quality in params["ids"]:
            newname = hname+"_"+quality[0]
            hists[obj+"_"+newname] = create2Dmap(
                obj+"_"+newname, params, quality[2], dumptcl)

    # study
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        if (tot_nevents % 100) == 0:  # 1000
            print '... processed {} events ...'.format(event.entry()+1)

        tot_nevents += 1
        genparts = event.genparticles()
        jets = event.jetspuppi()

        for p in jets:
            if p.pt() < params['ptMin']:
                continue
            pVec = ROOT.TLorentzVector()
            pVec.SetPtEtaPhiM(p.pt(), p.eta(), p.phi(), p.mass())
            jetParFlav = findPartonFlav(genparts, pVec, params['dR'])

            if jetParFlav == 5:
                for quality in params["bitids"]:
                    isTagged = int(bool(p.btag() & quality[1]))
                    hists[obj+"_btagRate_to_eta_" +
                          quality[0]].Fill(p.eta(), isTagged)
                    hists[obj+"_btagRate_to_pt_" +
                          quality[0]].Fill(p.pt(), isTagged)
                    hists[obj+"_btagRate_efficiency2D_" +
                          quality[0]].Fill(p.pt(), p.eta(), isTagged)
                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] <= p.pt() < cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(p.btag() & quality[1]))
                            hists[obj+"_btagRate_to_eta_"+quality[0] +
                                  "_" + cutname].Fill(p.eta(), isTagged)
                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] < abs(p.eta()) <= cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(p.btag() & quality[1]))
                            hists[obj+"_btagRate_to_pt_"+quality[0] +
                                  "_" + cutname].Fill(p.pt(), isTagged)

            elif jetParFlav == 4:
                for quality in params["bitids"]:
                    isTagged = int(bool(p.btag() & quality[1]))
                    hists[obj+"_cMistagRate_to_eta_" +
                          quality[0]].Fill(p.eta(), isTagged)
                    hists[obj+"_cMistagRate_to_pt_" +
                          quality[0]].Fill(p.pt(), isTagged)
                    hists[obj+"_cMistagRate_efficiency2D_" +
                          quality[0]].Fill(p.pt(), p.eta(), isTagged)
                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] <= p.pt() < cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(p.btag() & quality[1]))
                            hists[obj+"_cMistagRate_to_eta_"+quality[0] +
                                  "_" + cutname].Fill(p.eta(), isTagged)
                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] < abs(p.eta()) <= cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(p.btag() & quality[1]))
                            hists[obj+"_cMistagRate_to_pt_"+quality[0] +
                                  "_" + cutname].Fill(p.pt(), isTagged)

            else:
                for quality in params["bitids"]:
                    isTagged = int(bool(p.btag() & quality[1]))
                    hists[obj+"_lightMistagRate_to_eta_" +
                          quality[0]].Fill(p.eta(), isTagged)
                    hists[obj+"_lightMistagRate_to_pt_" +
                          quality[0]].Fill(p.pt(), isTagged)
                    hists[obj+"_lightMistagRate_efficiency2D_" +
                          quality[0]].Fill(p.pt(), p.eta(), isTagged)
                for cut in params["ptSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] <= p.pt() < cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(p.btag() & quality[1]))
                            hists[obj+"_lightMistagRate_to_eta_"+quality[0] +
                                  "_" + cutname].Fill(p.eta(), isTagged)
                for cut in params["etaSlices"]:
                    cutname = str(cut[0]) + "to" + str(cut[1])
                    cutname = (cutname.replace('.', 'p')
                               ).replace('100000p0', 'Inf')
                    if cut[0] < abs(p.eta()) <= cut[1]:
                        for quality in params["bitids"]:
                            isTagged = int(bool(p.btag() & quality[1]))
                            hists[obj+"_lightMistagRate_to_pt_"+quality[0] +
                                  "_" + cutname].Fill(p.pt(), isTagged)

    outputF.cd()
    for h in hists.keys():
        hists[h].Write()


if __name__ == "__main__":
    main()
