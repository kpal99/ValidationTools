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

r.ROOT.EnableImplicitMT()
d = r.RDataFrame("myana/mytree","/eos/user/w/wenyu/TDRFullsim_ntuple/DYToMuMuorEleEle_M-20_14TeV_pythia8/crab_DYToMuMuorEleEle_M-20_14TeV_pythia8_200PU/190807_164128/0000/*.root")
df=d\
.Define('z',FindZ)\
.Define('z_pt','z.Mod()')\
.Define('ht',Sum.replace("OBJECT","jet"))\
.Define('met_v','TVector2 v(0,0);v.SetMagPhi(met_pt[0],met_phi[0]);return v;')\
.Define('met','met_pt[0]')\
.Define('met_p','met_v.Proj(z).Mod()')\
.Define('met_t','met_v.Norm(z).Mod()')\

var={}
var['ht']=(";H_{T} [GeV];Events", 200, 0, 2000)
var['vtx_size']=(";N_{PV};Events", 300, 1, 300)
var['jet_size']=(";N_{jet};Events", 100, 0, 100)
var['z_pt']=(";p_{T}(Z) [GeV];Events", 1000, 0, 100)
var['met']=(";p_{T,miss} [GeV];Events", 1000, 0, 100)
var['met_p']=(";parallel p_{T,miss} [GeV];Events", 1000, 0, 100)
var['met_t']=(";transverse p_{T,miss} [GeV];Events", 1000, 0, 100)

hists=[]
for v in var:
	print v
	hists.append(df.Histo1D((v,)+var[v],v))

outfile=r.TFile('outfile_met.root','RECREATE')
for h in hists:
	h.Write()
outfile.Close()

