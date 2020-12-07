import ROOT as rt
import os, sys, optparse
from collections import OrderedDict
import math
#____________________________________________________________________________
def get_mean_and_sigma(theHist, wmin=0.2, wmax=1.8, step=0.001, epsilon=0.007):

    ## rms, signal peak position
    x0 = theHist.GetXaxis().GetBinCenter(theHist.GetMaximumBin())
    d  = theHist.GetRMS()

    # now perform gaussian fit in [x_max_sigm, x_max_sigp]
    f = rt.TF1('gausfit', 'gaus',0.0, 2.0)

    s = 1.0
    theHist.Fit('gausfit', 'Q', '', x0 - s*d, x0 + s*d)

    mu  = f.GetParameter(1)
    sig = f.GetParameter(2)

    point = wmin
    weight = 0.
    points = [] #vector<pair<double,double> > 
    thesum = theHist.Integral()
    for i in range(theHist.GetNbinsX()):
      weight += theHist.GetBinContent(i)
      if weight > epsilon:
        points.append( [theHist.GetBinCenter(i),weight/thesum] )
    low = wmin
    high = wmax

    #print points

    width = wmax-wmin
    for i in range(len(points)):
      for j in range(i,len(points)):
        wy = points[j][1] - points[i][1]
        if abs(wy-0.683) < epsilon:

          wx = points[j][0] - points[i][0]
          if wx < width:
            low = points[i][0]
            high = points[j][0]
            width=wx

    sig_eff = 0.5*(high-low)

    #print mu,sig, sig_eff
    return mu,sig, sig_eff


#____________________________________________________________________________

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
parser.add_option('-i','--useIso',
                  action="store_true",
                  dest='useIso',
                  default=False,
                  help='true/false multiply by iso ratio in tcl file')

(opt, args) = parser.parse_args()

inFileD = opt.inFileD
inFileF = opt.inFileF
printoutdir = opt.printoutdir
dumptcl = opt.dumptcl
useIso = opt.useIso

if not os.path.exists(printoutdir):
    os.system('mkdir -p %s'%printoutdir)

inputFile_d = rt.TFile.Open(inFileD)
inputFile_f = rt.TFile.Open(inFileF)

## these dicts contain resolutions to be dumped in tcl format
mean_and_sigmas_d = OrderedDict()
mean_and_sigmas_f = OrderedDict()


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
    try:
        test = hf.Integral()
        if test == 0: continue
    except:
        continue


    if 'resolution' in name:
        items = name.split('_')
        print items
        
        colname = items[0]
        quality = items[1]
        ptmin = items[4]
        ptmax = items[5]
        etamin = items[7].replace('p','.')
        etamax = items[8].replace('p','.')

        if 'Inf' in ptmax:
            ptmax = 14000.
        if 'Inf' in etamax:
            etamax = 5.
            
        etamin = float(etamin)
        etamax = float(etamax)
        ptmin = float(ptmin)
        ptmax = float(ptmax)

        print colname, quality, ptmin, ptmax, etamin, etamax

        ## form input ntuple for mean_and_sigmas dictionary
        ntup_in = (colname, quality, ptmin, ptmax, etamin, etamax)

        mean_and_sigmas_d[ntup_in] = get_mean_and_sigma(hd, wmin=0.2, wmax=1.8, step=0.001, epsilon=0.007)
        mean_and_sigmas_f[ntup_in] = get_mean_and_sigma(hf, wmin=0.2, wmax=1.8, step=0.001, epsilon=0.007)

    if 'efficiency2D' in name or 'fakerate2D' in name or 'fakenonisorate2D' in name:
        rt.gStyle.SetPaintTextFormat("1.2f")
        hd.SetStats(rt.kFALSE)
        if 'efficiency' in name: 
            hd.GetZaxis().SetRangeUser(0,1)
            hf.GetZaxis().SetRangeUser(0,1)
            if hd.GetYaxis().GetBinUpEdge(hd.GetNbinsY()) > 10:
                hd.GetYaxis().SetRange(1,hd.GetNbinsY()-1)
                hf.GetYaxis().SetRange(1,hf.GetNbinsY()-1)
            if hd.GetXaxis().GetBinUpEdge(hd.GetNbinsX()) > 5000:
                hd.GetXaxis().SetRange(1,hd.GetNbinsX()-1)
                hf.GetXaxis().SetRange(1,hf.GetNbinsX()-1)
        else: 
            hd.GetZaxis().SetRangeUser(0,0.2)
            hf.GetZaxis().SetRangeUser(0,0.2)
            if hd.GetYaxis().GetBinUpEdge(hd.GetNbinsY()) > 10:
                hd.GetYaxis().SetRange(1,hd.GetNbinsY()-1)
                hf.GetYaxis().SetRange(1,hf.GetNbinsY()-1)
            if hd.GetXaxis().GetBinUpEdge(hd.GetNbinsX()) > 5000:
                hd.GetXaxis().SetRange(1,hd.GetNbinsX()-1)
                hf.GetXaxis().SetRange(1,hf.GetNbinsX()-1)
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
        if 'efficiency' not in name and 'fake' not in name and 'nonprompt' not in name and 'ptresponse' not in name:
            
            if hf.Integral() > 0:
                hf.Scale(1.0/hf.Integral())
            if hd.Integral() > 0:
                hd.Scale(1.0/hd.Integral())

        if 'efficiency' in name or 'fake' in name or 'nonprompt' in name:
            hf.SetMaximum(1)
        else:
            hf.SetMaximum(max(hd.GetMaximum(),hf.GetMaximum())*1.1)
        hf.SetMinimum(0)

        if '2D' not in name: 
            if 'Profile' in hf.ClassName() or 'Profile' in hd.ClassName():
                try: 
                    hdProject = hd.ProjectionX('projXD_'+name)
                    hdProject.SetLineColor(rt.kRed)
                    hdProject.SetMarkerStyle(20)
                    hdProject.SetMarkerColor(rt.kRed)
                    hdProject.SetStats(rt.kFALSE)        
                except: print('delphes histogram is missing:',name)
                try: 
                    hfProject = hf.ProjectionX('projXF_'+name)
                    hfProject.SetLineColor(rt.kBlue)
                    hfProject.SetMarkerStyle(21)
                    hfProject.SetMarkerColor(rt.kBlue)
                    hfProject.SetStats(rt.kFALSE)
                except: print('fullsim histogram is missing:',name)
                hR = rt.TRatioPlot(hdProject, hfProject)
            else:
                hR = rt.TRatioPlot(hd, hf)
            hR.SetH1DrawOpt("P E0")
            hR.SetGraphDrawOpt("P E0 X0")
            hR.Draw("P E0")
            hR.GetLowerRefYaxis().SetTitle("delphes/fullsim")
            hR.GetLowerRefGraph().SetMaximum(1.5)
            if 'efficiency' in name or 'fake' in name or 'nonprompt' in name:
                hR.GetUpperRefYaxis().SetRangeUser(0,1)
            else: hR.GetUpperRefYaxis().SetRangeUser(0,max(hd.GetMaximum(),hf.GetMaximum())*1.1)
            hR.GetLowerRefGraph().SetMarkerStyle(20)
            canv.Update()
        else:
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

    '''
    dumpme = ['efficiency2D_looseID','efficiency2D_tightID']
    photondump = ['nonpromptfakerate2D_looseID', 'nonpromptfakerate2D_tightID','fakerate2D_looseID','fakerate2D_tightID']

    particle = (hist_names[0].split('_')[0]).replace('gen','')
    if particle == 'photon': dumpme.extend(photondump) 

    for dumpname in dumpme:
        quality = dumpname.split('_')[-1]
        name = particle+'_'+dumpname
        print 'dumping tcl using hist name',name

        form = 'Efficiency'
        if 'non' in dumpname: form = 'NonPrompt';
        elif 'fake' in dumpname: form = 'Fake';

        if particle == 'muon' or particle == 'electron': 
            useIso = True
            print 'Forcing useIso = true for muon/electron tcl files'

        id2D_f = inputFile_f.Get(name).ProjectionXY("id_"+name)
        if useIso: 
            if particle != 'photon':
                #(RecoFS eff * IDFS eff)*(IsoFS eff)/(RecoDelphes eff * IsoDelphes eff)
                iso2D_d = inputFile_d.Get(name.replace('ID','ISO')).ProjectionXY("isoD_"+name) # if removing Reco, add "ifReco" to ID and ISO
                iso2D_f = inputFile_f.Get(name.replace('ID','ISOifReco')).ProjectionXY("isoF_"+name)
            else:
                iso2D_d = inputFile_d.Get(name).ProjectionXY("isoD_"+name)
                iso2D_f = inputFile_f.Get(name).ProjectionXY("isoF_"+name)

        f = open(printoutdir+'/'+particle+quality+form+'.tcl','w')
        f.write('## Fullsim Efficiency for '+name+', multiplying ISO(mu/el) or RECO(photon) Fullsim/Delphes? '+str(useIso)+'\n\n')

        if form == 'Efficiency':
            f.write('set EfficiencyFormula {\n')
        elif form == 'NonPrompt':
            f.write('set NonpromptFormula {\n')
        elif form == 'Fake':
            f.write('set FakeFormula {\n')

        ptlow = id2D_f.GetXaxis().GetBinLowEdge(1)
        f.write('\t(pt <= '+str(ptlow)+')*(1.0) +\n')

        for ybin in range(0,id2D_f.GetNbinsY()): ## eta
            isetaOF = False

            if id2D_f.GetYaxis().GetBinWidth(ybin+1) == 0: continue
            etalow = id2D_f.GetYaxis().GetBinLowEdge(ybin+1)
            etahigh = id2D_f.GetYaxis().GetBinUpEdge(ybin+1)
            if etahigh > 10: isetaOF = True

            for xbin in range (0,id2D_f.GetNbinsX()): ##pt
                isptOF = False
                if id2D_f.GetXaxis().GetBinWidth(xbin+1) == 0: continue
                ptlow = id2D_f.GetXaxis().GetBinLowEdge(xbin+1)
                pthigh = id2D_f.GetXaxis().GetBinUpEdge(xbin+1)
                if pthigh > 9e4: isptOF = True

                ratio = id2D_f.GetBinContent(xbin+1,ybin+1)
                if useIso: 
                    delpheseff = iso2D_d.GetBinContent(xbin+1,ybin+1)
                    if delpheseff > 0: 
                        ratio = ratio * iso2D_f.GetBinContent(xbin+1,ybin+1)/delpheseff
                    else: ratio = ratio * iso2D_f.GetBinContent(xbin+1,ybin+1)

                if isptOF:
                    if isetaOF: string = "(abs(eta) > "+str(etalow)+") * (pt > "+str(ptlow)+") * ("+str(ratio)+") +"
                    else: string = "(abs(eta) > "+str(etalow)+" && abs(eta) <= "+str(etahigh)+") * (pt > "+str(ptlow)+") * ("+str(ratio)+") +"
                else:
                    if isetaOF: string = "(abs(eta) > "+str(etalow)+") * (pt > "+str(ptlow)+" && pt <= "+str(pthigh)+") * ("+str(ratio)+") +"
                    else: string = "(abs(eta) > "+str(etalow)+" && abs(eta) <= "+str(etahigh)+") * (pt > "+str(ptlow)+" && pt <= "+str(pthigh)+") * ("+str(ratio)+") +"
                
                if xbin == id2D_f.GetNbinsX()-1 and ybin == id2D_f.GetNbinsY()-1: string = string[:-2]

                f.write('\t'+string+'\n')
        f.write('}\n')
        f.close()
    '''
    
    ## resolution dumps
    
    ntup_list = mean_and_sigmas_d.keys()
    
    ## order first by collection , then by quality, then by eta min, then by ptmin 
    sorted_ntup_list = sorted(ntup_list, key=lambda v: (v[0], v[1], v[4], v[2]))
    

    old_coll = ''
    old_quality = ''
    old_etamin = -1
    old_etamax = -1
    old_ptmin = -1
    old_ptmax = -1
    
    lines_scale = dict()
    lines_reso = dict()
    
    for ntup_in in sorted_ntup_list:
        #print ntup_in, mean_and_sigmas_d[ntup_in], mean_and_sigmas_f[ntup_in]

        coll    = ntup_in[0]
        quality = ntup_in[1]
        ptmin   = ntup_in[2]
        ptmax   = ntup_in[3]
        etamin  = ntup_in[4]
        etamax  = ntup_in[5]
        
        if coll != old_coll:
            old_coll = coll
            
        if quality != old_quality:

            old_quality = quality
            lines_scale[(coll,quality)] = []
            lines_scale[(coll,quality)].append('### {} {} momentum scale\n'.format(coll, quality))
            lines_scale[(coll,quality)].append('set ScaleFormula {\n')

            lines_reso[(coll,quality)] = []
            lines_reso[(coll,quality)].append('### {} {} momentum resolution\n'.format(coll, quality))
            lines_reso[(coll,quality)].append('set ResolutionFormula {\n')


        ## compute values to write in delphes card
        
        mu_d = mean_and_sigmas_d[ntup_in][0]
        mu_f = mean_and_sigmas_f[ntup_in][0]
        
        ## 1 - is gaussian width and 2 - is effective width
        sigma_d = mean_and_sigmas_f[ntup_in][2]
        sigma_f = mean_and_sigmas_d[ntup_in][2]
        
        
        scale = 1.
        if mu_d > 0.:
            scale = mu_f / mu_d
        
        ## delphes resolution when morphed to full sim scale
        
        sigmap_d = sigma_d 
        if mu_f > 0.:
            sigmap_d = sigma_d*scale
            
        sigma_smear = 1.e-04
        if sigma_f**2 > sigmap_d**2: 
            sigma_smear = math.sqrt(sigma_f**2 - sigmap_d**2)


        #print '{}, {}, {}, {}, {}, {}'.format(mu_f, mu_d, sigma_f, sigma_d, sigmap_d, sigma_smear)

        lines_scale[(coll,quality)].append('   (abs(eta) > {:.1f} && abs(eta) <= {:.1f}) * (pt > {:.1f} && pt <= {:.1f}) * ({:.3f}) +\n'.format(etamin, etamax, ptmin, ptmax, scale))
        lines_reso[(coll,quality)].append('   (abs(eta) > {:.1f} && abs(eta) <= {:.1f}) * (pt > {:.1f} && pt <= {:.1f}) * ({:.4f}) +\n'.format(etamin, etamax, ptmin, ptmax, sigma_smear))


    ## dump scale tcl file    
    for k, v in lines_scale.iteritems():
        
        dump = v
        dump.append('}\n')

        F = open("{}/{}_{}_scale.tcl".format(printoutdir,k[0],k[1]), "w")
        F.writelines(v)
        F.close()


    ## dump scale reso file    
    for k, v in lines_reso.iteritems():
        
        dump = v
        dump.append('}\n')

        F = open("{}/{}_{}_reso.tcl".format(printoutdir,k[0],k[1]), "w")
        F.writelines(v)
        F.close()

