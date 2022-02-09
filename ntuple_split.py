#!/usr/bin/env python
import ROOT
#from __future__ import print_function
from bin.NtupleDataFormat import Ntuple
from mytree import TreeProducer
import sys
import os

maxEvents = 0

def tagging(event):
# multiplicity of fatjet
    btag_multiplicity = 0
    for item in event.jetspuppi():
        if item.btag() > 0:
            btag_multiplicity += 1

    fatjet_count = 0
    h2b_count = 0
    h1b_count = 0
    w_count = 0
    for item in event.fatjets():
        if abs(item.eta()) < 2.4:
            fatjet_count += 1
            if item.pt() > 300 and 60 <= item.msoftdrop() <= 160:
                b_count = 0
                for jtem in event.jetspuppi():
                    if jtem.btag() > 0:
                        deltaR =  ((item.eta() - jtem.eta())**2 + (item.phi() - jtem.phi())**2)**0.5
                        if deltaR < 0.8:
                            b_count += 1
                if b_count >= 2:
                    h2b_count += 1
                elif b_count == 1:
                    h1b_count += 1
            if item.tau1() != 0:
                if item.pt() > 200 and abs(item.eta()) < 2.4 and 60 <= item.msoftdrop() <= 110 and item.tau2() / item.tau1() < 0.55 and h2b_count == 0 and h1b_count == 0:
                    w_count += 1

    if h2b_count > 0:
        h1b_count = 0
        w_count = 0
    if h1b_count > 0:
        w_count = 0
    return [h2b_count, h1b_count, w_count, btag_multiplicity]

def h2bTuple(ntuple, dir_str, filename):
    h2bTuple_size = 0

    total_count = 0
# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "h2b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break
        total_count += 1

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if h2b > 0:
            h2bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"nTuple_size  : {:<20}".format(total_count)
    print"h2bTuple_size: {:<20}".format(h2bTuple_size)

def h1bTuple(ntuple, dir_str, filename):
    h1bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "h1b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if h1b > 0 and h2b == 0:
            h1bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"h1bTuple_size: {:<20}".format(h1bTuple_size)

def w3bTuple(ntuple, dir_str, filename):
    w3bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "w3b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if w > 0 and btag >= 3:
            w3bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"w3bTuple_size: {:<20}".format(w3bTuple_size)

def w2bTuple(ntuple, dir_str, filename):
    w2bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "w2b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if w > 0 and btag == 2:
            w2bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"w2bTuple_size: {:<20}".format(w2bTuple_size)

def w1bTuple(ntuple, dir_str, filename):
    w1bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "w1b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if w > 0 and btag == 1:
            w1bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"w1bTuple_size: {:<20}".format(w1bTuple_size)

def w0bTuple(ntuple, dir_str, filename):
    w0bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "w0b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if w > 0 and btag == 0:
            w0bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"w0bTuple_size: {:<20}".format(w0bTuple_size)

def _3bTuple(ntuple, dir_str, filename):
    _3bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "_3b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if h2b == 0 and h1b == 0 and w == 0 and btag >= 3:
            _3bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"_3bTuple_size: {:<20}".format(_3bTuple_size)

def _2bTuple(ntuple, dir_str, filename):
    _2bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "_2b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if h2b == 0 and h1b == 0 and w == 0 and btag == 2:
            _2bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"_2bTuple_size: {:<20}".format(_2bTuple_size)

def _1bTuple(ntuple, dir_str, filename):
    _1bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "_1b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if h2b == 0 and h1b == 0 and w == 0 and btag == 1:
            _1bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"_1bTuple_size: {:<20}".format(_1bTuple_size)

def _0bTuple(ntuple, dir_str, filename):
    _0bTuple_size = 0

# using last part of out_str to creating a root file
    out_root = ROOT.TFile(dir_str + "_0b/" + filename,"RECREATE")
    out_root.mkdir("myana")
    out_root.cd("myana")
    treeProducer = TreeProducer()
# iterating through the all events; if value of maxEvents is zero.
    for event in ntuple:
        if maxEvents > 0 and event.entry() >= maxEvents:
            break

        [h2b, h1b, w, btag] = tagging(event)
#tight lepton selection. Only single lepton is required.
        if h2b == 0 and h1b == 0 and w == 0 and btag == 0:
            _0bTuple_size += 1
            treeProducer.processEvent(event.entry())
            treeProducer.processElectrons(event.electrons())
            treeProducer.processMuons(event.muons())
            treeProducer.processPuppiJets(event.jetspuppi())
            treeProducer.processFatJets(event.fatjets())
            treeProducer.processPuppiMissingET(event.metspuppi())
            treeProducer.fill()

    treeProducer.write()
    out_root.Close()
    print"_0bTuple_size: {:<20}".format(_0bTuple_size)

def main():
    if len(sys.argv) != 2:
        print "USAGE: {} <ntuple(s)>".format(sys.argv[0])
        sys.exit(1)
    inFile = sys.argv[1]
    ntuple = Ntuple(inFile)
    dir_str = os.path.dirname(inFile) + '/'
    filename = os.path.basename(inFile)
    h2bTuple(ntuple, dir_str, filename)
    h1bTuple(ntuple, dir_str, filename)
    w3bTuple(ntuple, dir_str, filename)
    w2bTuple(ntuple, dir_str, filename)
    w1bTuple(ntuple, dir_str, filename)
    w0bTuple(ntuple, dir_str, filename)
    _3bTuple(ntuple, dir_str, filename)
    _2bTuple(ntuple, dir_str, filename)
    _1bTuple(ntuple, dir_str, filename)
    _0bTuple(ntuple, dir_str, filename)


if __name__ == "__main__":
    main()
