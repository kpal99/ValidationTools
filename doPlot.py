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
parser.add_option('-t','--tcl',
                  action="store_true",
                  dest='dumptcl',
                  default=False,
                  help='true/false dump a tcl parameterization file')
(opt, args) = parser.parse_args()

inFileD = opt.inFileD
inFileF = opt.inFileF
printoutdir = opt.printoutdir
dumptcl = opt.dumptcl

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
        if 'efficiency' in name: 
            hd.GetZaxis().SetRangeUser(0,1)
            hf.GetZaxis().SetRangeUser(0,1)
        else: 
            hd.GetZaxis().SetRangeUser(0,0.2)
            hf.GetZaxis().SetRangeUser(0,0.2)
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
        hd.SetLineColor(rt.kRed)
        hd.SetMarkerStyle(20)
        hd.SetMarkerColor(rt.kRed)
        hd.SetStats(rt.kFALSE)        
        if 'efficiency' not in name and 'fakerate' not in name and 'ptresponse' not in name:
	    try:
              hf.Scale(1.0/hf.Integral())
              hd.Scale(1.0/hd.Integral())
	    except:
              print hf, hd
              pass

        if 'efficiency' in name or 'fakerake' in name:
            hf.SetMaximum(1)
        else:
            hf.SetMaximum(max(hd.GetMaximum(),hf.GetMaximum())*1.1)

        hf.SetMinimum(0)
        hf.Draw()
        hd.Draw("same")
        legend = rt.TLegend(.9,.9,.99,.99)
        legend.SetTextSize(0.03)
        legend.SetBorderSize(0) 
        legend.AddEntry(hd,"Delphes","l")
        legend.AddEntry(hf,"FullSim","l")
        legend.Draw()
        canv.Print(printoutdir+ "/" + canv_name +".png")


if dumptcl:
    dumpme = ['efficiency2D_looseID','efficiency2D_tightID']
    for dumpname in dumpme:
        quality = dumpname.split('_')[-1]
        particle = (hist_names[0].split('_')[0]).replace('gen','')
        name = particle+'_'+dumpname
        print 'useing hist name',name

        useIso = True
        if particle == 'gamma' or particle == 'jet_': useIso = False;

        id2D_f = inputFile_f.Get(name).ProjectionXY("id_"+name)
        if useIso:
            iso2D_d = inputFile_d.Get(name.replace('ID','ISOifReco')).ProjectionXY("isoD_"+name)
            iso2D_f = inputFile_f.Get(name.replace('ID','ISOifReco')).ProjectionXY("isoF_"+name)

        f = open(printoutdir+'/'+particle+quality+'Efficiency.tcl','w')
        f.write('## Fullsim Efficiency for '+name+', multiplying ISO Fullsim/Delphes?'+str(useIso)+'\n\n')
        f.write('set EfficiencyFormula{\n')
        for ybin in range(0,id2D_f.GetNbinsY()): ## eta
            if id2D_f.GetYaxis().GetBinWidth(ybin+1) == 0: continue
            etalow = id2D_f.GetYaxis().GetBinLowEdge(ybin+1)
            etahigh = id2D_f.GetYaxis().GetBinUpEdge(ybin+1)
            for xbin in range (0,id2D_f.GetNbinsX()): ##pt
                if id2D_f.GetXaxis().GetBinWidth(xbin+1) == 0: continue
                ptlow = id2D_f.GetXaxis().GetBinLowEdge(xbin+1)
                pthigh = id2D_f.GetXaxis().GetBinUpEdge(xbin+1)

                ratio = id2D_f.GetBinContent(xbin+1,ybin+1)
                if useIso: 
                    delpheseff = iso2D_d.GetBinContent(xbin+1,ybin+1)
                    if delpheseff > 0: 
                        ratio = ratio * iso2D_f.GetBinContent(xbin+1,ybin+1)/delpheseff
                    else: ratio = ratio * iso2D_f.GetBinContent(xbin+1,ybin+1)

                string = "(abs(eta) > "+str(etalow)+" && abs(eta) <= "+str(etahigh)+") * (pt > "+str(ptlow)+" && pt <= "+str(pthigh)+") * ("+str(ratio)+") + \\"
                if xbin == id2D_f.GetNbinsX()-1 and ybin == id2D_f.GetNbinsY()-1: string = string[:-3]

                f.write('\t'+string+'\n')
        f.write('}\n')
        f.close()
    
