
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
    f = rt.TF1('gausfit', 'gaus', wmin, wmax)

    s = 1.0
    theHist.Fit('gausfit', 'Q', '', x0 - s*d, x0 + s*d)

    mu  = f.GetParameter(1)
    #mu  = x0
    sig = f.GetParameter(2)

    #print mu, sig

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

#_________________________________________________________________________________

## THIS FUNCTION REMOVES THE SPUROUS + SIGN AND CONVERTS THE LIST OF STRINGS INTO A STRING
def clean_dump(dump):
    last_line = dump[-1]
    last_char_index = last_line.rfind("+")
    new_string = last_line[:last_char_index] + " " + last_line[last_char_index+1:]
    #print new_string
    dump[-1] = new_string
    dump.append('  }')

    #print dump
    chunk_text='\n'
    chunk_text=chunk_text.join(dump)

    #print chunk_text
    return chunk_text


#_________________________________________________________________________________

## this function replaces content between the two control strings
def replaced(base, content, starting, ending):

    partitioned_string = base.partition(starting)
    before=partitioned_string[0]
    after=partitioned_string[2]
    partitioned_after=after.partition(ending)
    after=partitioned_after[2]

    final=before+content+after
    return final 



#__________________________________________________________________________________

rt.gROOT.SetBatch(True) ## avoid figures pop out to screen

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)

parser.add_option('-i','--useIso',
                  action="store_true",
                  dest='useIso',
                  default=False,
                  help='true/false multiply by iso ratio in tcl file')

parser.add_option('--card-in',
                  dest='card_in',
                  help='path to dummy delphes card [%default]',  
                  default='cards/dummy.tcl',                                                                                                           
                  type='string')

parser.add_option('--card-out',
                  dest='card_out',
                  help='path to output delphes card [%default]',  
                  default='cards/out_card.tcl',                                                                                                           
                  type='string')

object_dict={
              
	      
	      'muon':{
                        'collection':'muon',
                        'qualities':['loose','medium','tight'], ## here store qualities used to produce efficiencies and fake-rate (dummy for now)
                        'fit_range':[0.9,1.1],
                        'scale_quality':'looseIDISO', ## collection used for momentum scale and smearing
                        'control_str':'## DUMMY_MUON',  ## this string is what willbe looked for to insert the new param in the Delphes card
                        'inFileF':'histos/muon_fullsim_LMT012.root',
                        'inFileD':'histos/muon_delphes_V07VAL.root',
                        
              },

              'electron':{
                        'collection':'electron',
                        'qualities':['loose','medium','tight'], ## here store qualities used to produce efficiencies and fake-rate (dummy for now)
                        'fit_range':[0.9,1.1],
                        'scale_quality':'looseIDISO', ## collection used for momentum scale and smearing
                        'control_str':'## DUMMY_ELECTRON',  ## this string is what willbe looked for to insert the new param in the Delphes card
                        'inFileF':'histos/electron_fullsim_LMT012.root',
                        'inFileD':'histos/electron_delphes_V07VAL.root',
                        
              },

              'photon':{
                        'collection':'photon',
                        'qualities':['loose','medium','tight'], ## here store qualities used to produce efficiencies and fake-rate (dummy for now)
                        'fit_range':[0.9,1.1],
                        'scale_quality':'looseIDISO', ## collection used for momentum scale and smearing
                        'control_str':'## DUMMY_PHOTON',  ## this string is what willbe looked for to insert the new param in the Delphes card
                        'inFileF':'histos/photon_fullsim_LMT012.root',
                        'inFileD':'histos/photon_delphes_V07VAL.root',
                        
              },

              'jet':{
                        'collection':'jetpuppi',
                        'qualities':['loose','tight'], ## here store qualities used to produce efficiencies and fake-rate (dummy for now)
                        'fit_range':[0.0,2.0],
                        'scale_quality':'tightID', ## collection used for momentum scale and smearing
                        'control_str':'## DUMMY_JET',  ## this string is what willbe looked for to insert the new param in the Delphes card
                        'inFileF':'histos/jetpuppi_fullsim_LMT012.root',
                        'inFileD':'histos/jetpuppi_delphes_V07VAL.root',
              },


}


(opt, args) = parser.parse_args()

useIso = opt.useIso


### dump dummy card content into string
with open(opt.card_in, 'r') as f:
    base = f.read()

content=base

for obj, params in object_dict.items():

    #obj['']
    collection=params['collection']
    scale_quality=params['scale_quality']

    starting_scale = params['control_str']+'_SCALE'
    ending_scale = starting_scale.replace('DUMMY','ENDDUMMY')
    
    starting_smear = params['control_str']+'_SMEAR'
    ending_smear = starting_smear.replace('DUMMY','ENDDUMMY')

    inFileF=params['inFileF']
    inFileD=params['inFileD']

    fit_range_min=params['fit_range'][0]
    fit_range_max=params['fit_range'][1]

    inputFile_d = rt.TFile.Open(inFileD)
    inputFile_f = rt.TFile.Open(inFileF)

    ## these dicts contain resolutions to be dumped in tcl format
    mean_and_sigmas_d = OrderedDict()
    mean_and_sigmas_f = OrderedDict()


    hist_names = []

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
            #print items

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


            if quality != scale_quality: continue
            
	    print colname, quality, ptmin, ptmax, etamin, etamax

            ## form input ntuple for mean_and_sigmas dictionary
            ntup_in = (colname, quality, ptmin, ptmax, etamin, etamax)

            mean_and_sigmas_d[ntup_in] = get_mean_and_sigma(hd, wmin=fit_range_min, wmax=fit_range_max, step=0.001, epsilon=0.005)
            mean_and_sigmas_f[ntup_in] = get_mean_and_sigma(hf, wmin=fit_range_min, wmax=fit_range_max, step=0.001, epsilon=0.005)


        ### HERE IS WHERE WE COMPUTE EFFICIENCY RATIOS AND FAKE RATE

        '''
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
       '''


    ## HERE IS WHERE WE COMPUTE THE VALUES AND DUMP THE RESOLUTION IN THE INPUT TCL FILE 

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

    scale = 1.
    for ntup_in in sorted_ntup_list:

        coll    = ntup_in[0]
        quality = ntup_in[1]
        ptmin   = ntup_in[2]
        ptmax   = ntup_in[3]
        etamin  = ntup_in[4]
        etamax  = ntup_in[5]

        if quality != scale_quality:
            continue

        if coll != old_coll:
            old_coll = coll

        if quality != old_quality:

            old_quality = quality
            lines_scale[(coll,quality)] = []
            lines_scale[(coll,quality)].append('  ### {} {} momentum scale'.format(coll, quality))
            lines_scale[(coll,quality)].append('  set ScaleFormula {')

            lines_reso[(coll,quality)] = []
            lines_reso[(coll,quality)].append('  ### {} {} momentum resolution'.format(coll, quality))
            lines_reso[(coll,quality)].append('  set ResolutionFormula {')


        ## compute values to write in delphes card

        mu_d = mean_and_sigmas_d[ntup_in][0]
        mu_f = mean_and_sigmas_f[ntup_in][0]

        ## 1 - is gaussian width and 2 - is effective width
        sigma_d = mean_and_sigmas_d[ntup_in][1]
        sigma_f = mean_and_sigmas_f[ntup_in][1]


        if mu_d > 0. and mu_f > 0.:   ## otherwise pick value from previous bin
            scale = mu_f / mu_d

        ## delphes resolution when morphed to full sim scale

        sigmap_d = sigma_d 
        if mu_f > 0.:
            sigmap_d = sigma_d*scale

        sigma_smear = 1.e-06
        if sigma_f**2 > sigmap_d**2: 
            sigma_smear = math.sqrt(sigma_f**2 - sigmap_d**2)

        #print ptmin, ptmax, etamin, etamax
        #print '{}, {}, {}, {}, {}, {}'.format(mu_f, mu_d, sigma_f, sigma_d, sigmap_d, sigma_smear)

        lines_scale[(coll,quality)].append('   (abs(eta) > {:.1f} && abs(eta) <= {:.1f}) * (pt > {:.1f} && pt <= {:.1f}) * ({:.3f}) +'.format(etamin, etamax, ptmin, ptmax, scale))
        lines_reso[(coll,quality)].append('   (abs(eta) > {:.1f} && abs(eta) <= {:.1f}) * (pt > {:.1f} && pt <= {:.1f}) * ({:.6f}) +'.format(etamin, etamax, ptmin, ptmax, sigma_smear))


    dump_scale=lines_scale[(collection,scale_quality)]
    dump_reso=lines_reso[(collection,scale_quality)]

    dump_scale=clean_dump(dump_scale)
    dump_reso=clean_dump(dump_reso)

    ## HERE REPLACE CONTENT OF THE CARD BETWEEN CONTROL STRINGS 

    ## scale parametrisation
    content=replaced(content, dump_scale, starting_scale, ending_scale)
    
    ## smear parametrisation  
    content=replaced(content, dump_reso, starting_smear, ending_smear)



    ## ADD HERE VARIOUS EFFICIENCIES AND FAKE RATES

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


## dump new content into new delphes card

out_card = open(opt.card_out, "w")
n = out_card.write(content)
out_card.close()


