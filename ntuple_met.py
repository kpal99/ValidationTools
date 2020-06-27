import ROOT as r, math as m #needs 6.14 or greater
r.gROOT.SetBatch()

FindGenBoson=\
"TVector2 v(0,0);for(int i=0;i<genpart_size;i++){\
 if(abs(genpart_pid[i])==23||abs(genpart_pid[i])==22)\
 if(abs(genpart_pid[genpart_d1[i]])==11 || abs(genpart_pid[genpart_d1[i]])==13){\
 v.SetMagPhi(genpart_pt[i],genpart_phi[i]); break;} } return v;"

# FindZ=\
# "TVector2 v1(0,0),v2(0,0);if(muon_size>1)\
# {v1.SetMagPhi(muon_pt[0],muon_phi[0]);v2.SetMagPhi(muon_pt[1],muon_phi[1]);}\
# else if (elec_size>1)\
# {v1.SetMagPhi(elec_pt[0],elec_phi[0]);v2.SetMagPhi(elec_pt[1],elec_phi[1]);}\
# return v1+v2;"


FindLeptons=\
"TVector3 v[2]={(0,0,0),(0,0,0)};if(muon_size>1)\
{v[0].SetPtEtaPhi(muon_pt[0],muon_eta[0],muon_phi[0]);v[1].SetPtEtaPhi(muon_pt[1],muon_eta[1],muon_phi[1]);}\
else if (elec_size>1)\
{v[0].SetPtEtaPhi(elec_pt[0],elec_eta[0],elec_phi[0]);v[1].SetPtEtaPhi(elec_pt[1],elec_eta[0],elec_phi[1]);}\
return v;"

# FindZGamma=\
# "TVector3 v1(0,0,0),v2(0,0,0);if(muon_size>1)\
# {v1.SetPtEtaPhi(muon_pt[0],muon_eta[0],muon_phi[0]);v2.SetPtEtaPhi(muon_pt[1],muon_eta[1],muon_phi[1]);}\
# else if (elec_size>1)\
# {v1.SetPtEtaPhi(elec_pt[0],elec_eta[0],elec_phi[0]);v2.SetPtEtaPhi(elec_pt[1],elec_eta[0],elec_phi[1]);}\
# return v1+v2;"

# FindMedian=\
# "TVector3 v1(0,0,0),v2(0,0,0);if(muon_size>1)\
# {v1.SetPtEtaPhi(muon_pt[0],muon_eta[0],muon_phi[0]);v2.SetPtEtaPhi(muon_pt[1],muon_eta[1],muon_phi[1]);}\
# else if (elec_size>1)\
# {v1.SetPtEtaPhi(elec_pt[0],elec_eta[0],elec_phi[0]);v2.SetPtEtaPhi(elec_pt[1],elec_eta[0],elec_phi[1]);}\
# return (v1.Unit()+v2.Unit()).Unit();"

FindBoson="return leptons[0]+leptons[1];"

FindMedian="TVector3 v(0,0,0); if (leptons[0].Mod()>0.000001) v=leptons[0].Unit()+leptons[1].Unit(); return v;"

Sum=\
"float sum=0.0;\
for(int i=0;i<OBJECT_size;i++){\
if(OBJECT_pt[i]>PTCUT && fabs(OBJECT_eta[i])<ETACUT)\
sum+=OBJECT_pt[i];} return sum;"

# Count=\
# "int count=0;\
# for(int i=0;i<OBJECT_size;i++){\
# if(OBJECT_pt[i]>PTCUT && fabs(OBJECT_eta[i])<ETACUT)\
# count++;} return count;"

intcolor=[r.TColor.GetColor(i) for i in ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]]
def compare(name,file_list,name_list,legend_list,normalize=False,drawoption='hE',xtitle='',ytitle='',minx=0,maxx=0,rebin=1,miny=0,maxy=0,textsizefactor=1,logy=False):
  c=r.TCanvas(name,'',600,600)
  c.SetLeftMargin(0.15)#
  c.SetRightMargin(0.05)#
  c.SetBottomMargin(0.11)
  c.SetTopMargin(0.25)
  legend=r.TLegend(0.0,0.76,0.99,1.04)
  legend.SetHeader('')
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  histo_list=[]
  the_maxy=0
  for i in range(len(name_list)):
    histo_list.append(file_list[i].Get(name_list[i]).Clone(name_list[i]+'_'+str(i)))
    if normalize:
      histo_list[-1].Scale(1.0/(histo_list[-1].Integral()+0.00000001))
    histo_list[-1].SetStats(0)
    histo_list[-1].SetLineWidth(3)
    histo_list[-1].SetLineColor(intcolor[i])
    histo_list[-1].SetTitle('')
    if rebin!=1:
      histo_list[-1].Rebin(rebin)
    the_maxy=max(the_maxy,histo_list[-1].GetBinContent(histo_list[-1].GetMaximumBin())*1.05)
    legend.AddEntry(histo_list[-1],legend_list[i],'l')
  for i in range(len(name_list)):
    if i==0:
      if miny!=0 or maxy!=0:
        histo_list[i].SetMaximum(maxy)
        histo_list[i].SetMinimum(miny)
      else:
        histo_list[i].SetMaximum(the_maxy)
        #histo_list[i].SetMinimum(0.0001)
      histo_list[i].Draw(drawoption)
      charsize=0.05*textsizefactor
      histo_list[i].GetYaxis().SetLabelSize(charsize)
      histo_list[i].GetYaxis().SetTitleSize(charsize)
      histo_list[i].GetYaxis().SetTitleOffset(1.6)
      histo_list[i].GetXaxis().SetLabelSize(charsize)
      histo_list[i].GetXaxis().SetTitleSize(charsize)
      histo_list[i].GetXaxis().SetTitleOffset(0.95)
      if xtitle!='':
        histo_list[i].GetXaxis().SetTitle(xtitle)
      if ytitle!='':  
        histo_list[i].GetYaxis().SetTitle(ytitle)
      if maxx!=0 or minx!=0:
        histo_list[i].GetXaxis().SetRangeUser(minx,maxx)
    else:
      histo_list[i].Draw(drawoption+'SAME')
  if logy:
    c.SetLogy()
  legend.Draw()
  c.SaveAs('pdf/'+name+'.pdf')

def dostudy(path,suffix):
	r.ROOT.EnableImplicitMT()
	d = r.RDataFrame("myana/mytree",path)
	df=\
  #        find gen boson (2D)             find gen boson pT                          find reco boson (3D)             find median
  d.Define('genboson',FindGenBoson).Define('genboson_pt','genboson.Mod()').Define('boson3d',FindBoson).Define('median3d',FindMedian)\
	#        define boson (2D)                                                           define boson pt
  .Define('boson','TVector2 v(0,0);v.SetMagPhi(boson3d.Pt(),boson3d.Phi());return v;').Define('boson_pt','z.Mod()')\
  #        define median (2D)                                                          
  .Define('median','TVector2 v(0,0);v.SetMagPhi(median3d.Pt(),median3d.Phi());return v;')\
  #      select events with a boson
  .Filter('boson_pt>0.00001').Define('z_unit','z.Unit()').Define('zprojz','TVector3(0,0,z3d.Z())')\
  .Filter('median_pt>0.00001').Define('median_unit','median.Unit()').Define('medianprojz','TVector3(0,0,median3d.Z())')\
	.Define('zprojxy','TVector3(z3d.X(),z3d.Y(),0)').Define('z_ortho','zprojz.Cross(zprojxy).XYvector().Unit()')\
  .Define('medianprojxy','TVector3(median3d.X(),median3d.Y(),0)').Define('median_ortho','medianprojz.Cross(medianprojxy).XYvector().Unit()')\
	.Define('ht',Sum.replace("OBJECT","jet").replace("PTCUT","0.0").replace("ETACUT","5000.0"))\
	.Define('ht_pt30_eta4',Sum.replace("OBJECT","jet").replace("PTCUT","30.0").replace("ETACUT","4.0"))\
	.Define('ht_pt30_eta3',Sum.replace("OBJECT","jet").replace("PTCUT","30.0").replace("ETACUT","3.0"))\
	.Define('met_v','TVector2 v(0,0);v.SetMagPhi(met_pt[0],met_phi[0]);return v;').Define('met','met_pt[0]')\
	.Define('met_p','met_v*median_unit').Define('met_t','met_v*median_ortho')\
  .Define('u_v','z+met_v').Define('u_p','u_v*median_unit')\
	# .Define('jet_size_pt30_eta4',Count.replace("OBJECT","jet").replace("PTCUT","30.0").replace("ETACUT","4.0"))\
	# .Define('jet_size_pt30_eta3',Count.replace("OBJECT","jet").replace("PTCUT","30.0").replace("ETACUT","3.0"))\

  #.Define('u_t','u_v*median_ortho')\ ut makes no sense, it's just MET_t. 

	var={}
	var['ht']=(";H_{T} [GeV];Events", 50, 0, 500)
	var['ht_pt30_eta4']=(";H_{T} [GeV];Events", 50, 0, 500)
	var['ht_pt30_eta3']=(";H_{T} [GeV];Events", 50, 0, 500)
	var['vtx_size']=(";N_{PV};Events", 180, 90, 270)
	var['jet_size']=(";N_{jet};Events", 15, 0, 15)
	# var['jet_size_pt30_eta4']=(";N_{jet};Events", 15, 0, 15)
	# var['jet_size_pt30_eta3']=(";N_{jet};Events", 15, 0, 15)
	var['z_pt']=(";p_{T}(Z) [GeV];Events", 150, 0, 150)
	var['met']=(";p_{T,miss} [GeV];Events", 300, 0, 300)
	var['met_p']=(";p_{T,miss,parallel} [GeV];Events", 300, -150, 150)
	var['met_t']=(";p_{T,miss,perpendicular} [GeV];Events", 300, -150, 150)
	var['u_p']=(";u_{parallel} [GeV];Events", 300, -150, 150)
  #var['u_t']=(";u_{perpendicular} [GeV];Events", 300, -150, 150)

	twod_vars=['ht','ht_pt30_eta4','ht_pt30_eta3','vtx_size','z_pt']

	hists=[]
	for v in var:
		hists.append(df.Histo1D((v,)+var[v],v))
		if (v not in twod_vars) or (v=='z_pt'):
			for twod in twod_vars:
				hists.append(df.Profile1D((v+'_VS_'+twod,)+(var[twod][0].replace("Events",'')+var[v][0].split(";")[1],) +var[twod][1:] ,twod,v))

	outfile=r.TFile('outfile_met_'+suffix+'.root','RECREATE')
	for h in hists:
		h.Write()

	for i in twod_vars:
		up_over_qt=outfile.Get("u_p_VS_"+i).Clone()
		up_over_qt.Divide(outfile.Get("z_pt_VS_"+i))
		up_over_qt.Write("up_over_qt_VS_"+i)

		ut=outfile.Get("met_t_VS_"+i).Clone()
		ut_rms=r.TH1F(*(("ut_rms_VS_"+i,var[i][0].replace("Events","RMS u_{perp} = p_{T,miss,perp}"))+var[i][1:]))
		for imtt in range(1,ut.GetNbinsX()+1):
			ut_rms.SetBinContent(imtt,ut.GetBinError(imtt)*m.sqrt(ut.GetBinEntries(imtt)))
		ut_rms.Write()

		up_plus_qt=outfile.Get("met_p_VS_"+i).Clone()
		up_plus_qt_rms=r.TH1F(*(("up_plus_qt_rms_VS_"+i,var[i][0].replace("Events","RMS u_{par}+p_{T}(Z) = p_{T,miss,par}"))+var[i][1:]))
		for imtt in range(1,up_plus_qt.GetNbinsX()+1):
			up_plus_qt_rms.SetBinContent(imtt,up_plus_qt.GetBinError(imtt)*m.sqrt(up_plus_qt.GetBinEntries(imtt)))
		up_plus_qt_rms.Write()
	outfile.Close()

dostudy("/eos/user/w/wenyu/TDRFullsim_ntuple/DYToMuMuorEleEle_M-20_14TeV_pythia8/crab_DYToMuMuorEleEle_M-20_14TeV_pythia8_200PU/190807_164128/0000/*.root","fullsim")
dostudy("/afs/cern.ch/user/e/eusai/DelphesNtuplizer/*.root","delphes")

f={}
for i in ['fullsim','delphes']:	f[i]=r.TFile('outfile_met_'+i+'.root','READ')
hnames=[[key.GetName(),key.GetClassName()] for key in f["fullsim"].GetListOfKeys()]

for i in hnames:
	compare(name=i[0]+'_comp',textsizefactor=0.7,
		normalize= (not (i[1]=='TProfile')) and ('rms' not in i[0]),
		file_list=[f['fullsim'],f['delphes']],legend_list=['Full Sim','Delphes'],name_list=[i[0]]*2,
		drawoption= 'hist' if 'over' in i[0] or 'rms' in i[0] else '')

for i in f:	f[i].Close()