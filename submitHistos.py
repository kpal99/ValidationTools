import os,time,subprocess,string,sys
runDir = os.getcwd()

def striplist(alist): 
	ret = []
	for item in alist:
		ret.append(item.strip())
	return ret

def EOSlist_root_files(Dir):
    xrd = 'eos root://eoscms.cern.ch/'
    items = os.popen(xrd+' ls '+Dir).readlines() #they have a \n at the end 
    items2 = striplist(items)
    rootlist = []
    for item in items2:
        if string.rfind(item,'root',-4) != -1:
            rootlist.append(item)
    return rootlist

# Should we run fullsim?
doFullsim = True
FS = sys.argv[1]
if 'elphes' in FS: doFullsim = False

# Set some paths
url = 'root://eoscms.cern.ch/'
DelphesDir = '/store/group/upgrade/RTB/DelphesFlat_343pre07/v07VALclosure_v2/' # keep the trailing slash here
FullsimDir = '/store/group/upgrade/RTB/Iter5/'
FullsimDir2 = '/store/group/upgrade/RTB/Iter4/'
HistoDir = '/store/group/upgrade/RTB/ValidationHistos/v07VALclosure_v2/'
LogDir = '/afs/cern.ch/work/j/jmhogan/public/UpgradeStudies/ValidationTools/CondorLogs/ValidationHistos/'

if not os.path.exists(HistoDir):
    os.system('mkdir -p /eos/cms'+HistoDir)
if not os.path.exists(LogDir):
    os.system('mkdir -p '+LogDir)

# Should we use the dumptcl setting?
dumptcl = False

# Set some samples. 
# Making them lists to start with guessing we will have multiples
# Making them folders assuming we will stop hadding the flat trees...
DelphesPaths = [
        DelphesDir+'DoubleElectron_FlatPt-1To100_200PU_flat',
        DelphesDir+'DoubleMuon_gun_FlatPt-1To100_200PU_flat',
        DelphesDir+'DoublePhoton_FlatPt-1To100_200PU_flat',
        # DelphesDir+'DYToLL_M-50_TuneCP5_14TeV-pythia8_200PU_flat',
        DelphesDir+'GluGluHToTauTau_M125_14TeV_powheg_pythia8_TuneCP5_200PU_flat',
        DelphesDir+'GluGluToHHTo2B2G_node_SM_TuneCP5_14TeV-madgraph_pythia8_200PU_flat',
        DelphesDir+'GluGluToHHTo2B2Tau_node_SM_TuneCP5_14TeV-madgraph-pythia8_200PU_flat',
        DelphesDir+'MultiTau_PT15to500_200PU_flat',
        DelphesDir+'QCD_Pt_120to170_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8_200PU_flat',
        DelphesDir+'QCD_Pt_170to300_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'QCD_Pt_20to30_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'QCD_Pt_300to470_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'QCD_Pt_30to50_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'QCD_Pt_470to600_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'QCD_Pt_50to80_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'QCD_Pt_600oInf_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'QCD_Pt_80to120_TuneCP5_14TeV_pythia8_200PU_flat',
        DelphesDir+'TT_TuneCP5_14TeV-powheg-pythia8_200PU_flat',
]

FullsimPaths = [
        FullsimDir+'TT_TuneCP5_14TeV-powheg-pythia8/crab_TT_TuneCP5_14TeV-powheg-pythia8/201211_161715/0000',
        FullsimDir2+'DYToLL_M-50_TuneCP5_14TeV-pythia8/crab_DYToLL_M-50_TuneCP5_14TeV-pythia8_HLTTDRSummer20_200PU/201110_160006/0000',
        FullsimDir2+'QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/crab_QCD_Pt-15to3000_14TeV_HLTTDRSummer20_200PU/201104_162940/0000',
        FullsimDir2+'GluGluHToGG_M125_14TeV_powheg_pythia8_TuneCP5/crab_GluGluHToGG_M125_14TeV_HLTTDRSummer20_200PU/201106_214038/0000',
        FullsimDir2+'GluGluHToTauTau_M125_14TeV_powheg_pythia8_TuneCP5/crab_GluGluHToTauTau_M125_14TeV_HLTTDRSummer20_200PU/201106_214058/0000',
        FullsimDir2+'GluGluToHHTo2B2G_node_SM_TuneCP5_14TeV-madgraph_pythia8/crab_GluGluToHHTo2B2G_node_SM_14TeV_HLTTDRSummer20_200PU/201105_172451/0000',
        FullsimDir2+'GluGluToHHTo2B2Tau_node_SM_TuneCP5_14TeV-madgraph-pythia8/crab_GluGluToHHTo2B2Tau_node_SM_TuneCP5_14TeV_HLTTDRSummer20_200PU/201106_214118/0000',
]

start_time = time.time()

# Do we need proxies? Maybe not, all local...
# print 'Getting proxy'
# proxyPath=os.popen('voms-proxy-info -path')
# proxyPath=proxyPath.readline().strip()
# print 'ProxyPath:',proxyPath
# if 'tmp' in proxyPath: 
#     print 'Run source environment.(c)sh and make a new proxy!'
#     exit(1)

    
# For each sample we submit 1 job per ROOT file
# particle "all" runs muon, electron, photon, jet, met
# hadds all outputs and writes that mega-file to eos

samplelist = DelphesPaths
pfix = 'delphes_'
filesperjob = 20
if doFullsim: 
        samplelist = FullsimPaths
        pfix = 'fullsim_'
        #filesperjob = 10  # just Wenyu's 'Automatic' splitting in TT gives few/big files

# Particle: muon, electron, photon, jet, met
# 'all' will process all of them
particle = 'all'

print 'Starting Submission'
count = 0

# Loop over the samples
for sample in samplelist:

        if doFullsim and 'TT_TuneCP5' in sample: filesperjob = 5 # Wenyu's sample
        
        outDir = sample.replace(DelphesDir,HistoDir+'Histos_').replace(FullsimDir,HistoDir+'HistosFS_').replace(FullsimDir2,HistoDir+'HistosFS_').replace('flat','histos')
        logDir = sample.replace(DelphesDir,LogDir+'Histos_').replace(FullsimDir,LogDir+'HistosFS_').replace(FullsimDir2,LogDir+'HistosFS_')
        if doFullsim:
                outDir = outDir.split('/')[:-3]  # remove crab_stuff/datastamp/0000
                outDir = '/'.join(outDir)
                logDir = logDir.split('/')[:-3]
                logDir = '/'.join(logDir)
        if not os.path.exists(outDir):
                os.system('mkdir -p /eos/cms'+outDir)
        if not os.path.exists(logDir):
                os.system('mkdir -p '+logDir)
        print 'Files to:',outDir
        print 'Logs to:',logDir
        
        
        
        # For each sample we need a list of input ROOT files
        rootlist = EOSlist_root_files(sample)
        tmpcount = 0

        basefilename = (rootlist[0].split('.')[0]).split('_')[:-1]
        basefilename = '_'.join(basefilename)
        print "Running basefilenames:",basefilename
        print 'Input file like:',sample+'/'+basefilename+'_N.root'

        # Loop over the root files to submit jobs
        for i in range(0,len(rootlist),filesperjob):
        #for rfile in rootlist:
            
                count += 1
                tmpcount += 1
                #if tmpcount > 1: continue # for a test job
                
                index = (rootlist[i].split('.')[0]).split('_')[-1] ## 1-1                

                idlist = index+' '
                for j in range(i+1,i+filesperjob):
                        if j >= len(rootlist): continue
                        idlist += (rootlist[j].split('.')[0]).split('_')[-1]+' '
                        
                idlist = idlist.strip()
                print "Running IDs",idlist


                outname = pfix+basefilename.replace('_flat','_'+particle+'histos').replace('file',particle+'histos').replace('output',particle+'histos')+'_'+str(tmpcount)
                print 'Output name:',outname

                # Write the condor config
                dict = {'RUNDIR':runDir, 'FILEOUT':outname, 'FILEIN':sample+'/'+basefilename, 'TCL':dumptcl, 'PARTICLE':particle, 'OUTDIR':outDir, 'IDLIST':idlist}
                jdfName = logDir+'/'+basefilename+'_'+str(tmpcount)+'.job'
                jdf = open(jdfName,'w')
                jdf.write(
                        """universe = vanilla
+JobFlavour = "workday"
Executable = %(RUNDIR)s/RunHistos.sh
Should_Transfer_files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/ntuple_analyser.py, %(RUNDIR)s/bin/NtupleDataFormat.py, %(RUNDIR)s/bin/__init__.py
Output = %(FILEOUT)s.out
Error = %(FILEOUT)s.err
Log = %(FILEOUT)s.log
Notification = Never
Arguments = "%(FILEIN)s %(FILEOUT)s %(TCL)s %(PARTICLE)s '%(IDLIST)s' %(OUTDIR)s"

Queue 1"""%dict)
                jdf.close()
                os.chdir(logDir)
                os.system('condor_submit '+jdfName)
                os.system('sleep 0.5')
                os.chdir(runDir)
                print str(count), "jobs submitted!"

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


