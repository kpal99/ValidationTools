import ROOT as r 

FindZ=\
"for(int i=0;i<genpart_size;i++){\
 if(abs(genpart_pid[i])==23)\
 if(abs(genpart_pid[genpart_d1[i]])==11 || abs(genpart_pid[genpart_d1[i]])==13){\
 TVector2 v;\
 v.SetMagPhi(genpart_pt[i],genpart_phi[i]);\
 return v;} } return TVector2(0,0);"

Sum=\
"float sum=0.0;\
for(int i=0;i<OBJECT_size;i++){\
sum+=OBJECT_pt[i];} return sum;"

def compare(name,file_list,name_list,legend_list,normalize=False,drawoption='hE',xtitle='',ytitle='',minx=0,maxx=0,rebin=1,miny=0,maxy=0,textsizefactor=1,logy=False):
  c=TCanvas(name,'',600,600)
  c.SetLeftMargin(0.15)#
  c.SetRightMargin(0.05)#
  c.SetBottomMargin(0.11)
  c.SetTopMargin(0.25)
  legend=TLegend(0.0,0.76,0.99,1.04)
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
  colors=[1179, 1180, 1181, 1182, 1183, 1184, 1185, 14, 1186, 1187]
  for i in range(len(name_list)):
    histo_list.append(file_list[i].Get(name_list[i]).Clone(name_list[i]+'_'+str(i)))
    print(legend_list[i],histo_list[-1].Integral())
    if normalize:
      histo_list[-1].Scale(1.0/(histo_list[-1].Integral()+0.00000001))
    histo_list[-1].SetStats(0)
    histo_list[-1].SetLineWidth(3)
    histo_list[-1].SetLineColor(colors[i])
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
        histo_list[i].SetMinimum(0.0001)
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
	df=d\
	.Define('z',FindZ).Define('z_pt','z.Mod()')\
	.Define('ht',Sum.replace("OBJECT","jet"))\
	.Define('met_v','TVector2 v(0,0);v.SetMagPhi(met_pt[0],met_phi[0]);return v;')\
	.Define('met','met_pt[0]')\
	.Define('met_p','met_v.Proj(z).Mod()')\
	.Define('met_t','met_v.Norm(z).Mod()')\
	.Define('u_p','(z+met_v).Proj(z).Mod()')\

	var={}
	var['ht']=(";H_{T} [GeV];Events", 50, 0, 500)
	var['vtx_size']=(";N_{PV};Events", 180, 90, 270)
	var['jet_size']=(";N_{jet};Events", 15, 0, 15)
	var['z_pt']=(";p_{T}(Z) [GeV];Events", 150, 0, 150)
	var['met']=(";p_{T,miss} [GeV];Events", 300, 0, 300)
	var['met_p']=(";parallel p_{T,miss} [GeV];Events", 150, 0, 150)
	var['met_t']=(";transverse p_{T,miss} [GeV];Events", 150, 0, 150)
	var['u_p']=(";u_{p} [GeV];Events", 150, 0, 150)

	twod_vars=['ht','vtx_size','jet_size','z_pt']

	hists=[]
	for v in var:
		hists.append(df.Histo1D((v,)+var[v],v))
		if v not in twod_vars:
			for twod in twod_vars:
				hists.append(df.Profile1D((v+'_VS_'+twod,)+(var[twod][0].replace("Events",'')+var[v][0].split(";")[1],) +var[twod][1:] ,twod,v))

	outfile=r.TFile('outfile_met_'+suffix+'.root','RECREATE')
	for h in hists:
		h.Write()
	outfile.Close()

dostudy("/eos/user/w/wenyu/TDRFullsim_ntuple/DYToMuMuorEleEle_M-20_14TeV_pythia8/crab_DYToMuMuorEleEle_M-20_14TeV_pythia8_200PU/190807_164128/0000/*.root","fullsim")
dostudy("/afs/cern.ch/user/e/eusai/DelphesNtuplizer/*.root","delphes")

f={}
for i in ['delphes','fullsim']:
	f[i]=r.TFile('outfile_met_'+i+'.root','READ')

hnames=[key.GetName() for key in f["fullsim"].GetListOfKeys()]

for i in hnames:


