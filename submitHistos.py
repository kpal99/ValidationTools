import os,time,subprocess
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

# Set some paths
DelphesDir = '/store/group/upgrade/RTB/DelphesFlat_343pre07/' # keep the trailing slash here
FullsimDir = '/store/group/upgrade/RTB/FullsimFlat_111X/'
HistoDir = '/store/group/upgrade/RTB/ValidationHistos_Summer20Val7/'
LogDir = '/afs/cern.ch/work/j/jmhogan/public/UpgradeStudies/ValidationTools/CondorLogs/'

if not os.path.exists(HistoDir):
    os.system('mkdir -p /eos/cms'+HistoDir)
if not os.path.exists(LogDir):
    os.system('mkdir -p '+LogDir)

# Should we run fullsim?
doFullsim = True

# Should we use the dumptcl setting?
dumptcl = False

# Set some particles
particles = ['muon','electron','photon','jet','btag','tau']

# Set some samples. 
# Making them lists to start with guessing we will have multiples
# Making them folders assuming we will stop hadding the flat trees...
DelphesEffs = {'muon':[DelphesDir+'DYToLL_M-50_TuneCP5_14TeV-pythia8_200PU_v07closure'],
               'electron':[DelphesDir+'DYToLL_M-50_TuneCP5_14TeV-pythia8_200PU_v07closure'],
               'photon':[DelphesDir+'GluGluToHHTo2B2G_node_SM_TuneCP5_14TeV-madgraph_pythia8_200PU_v7closure'],
               'jet':[DelphesDir+'QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8_200PU_v7closure'],
               'btag':[DelphesDir+'TT_TuneCP5_14TeV_200PU_v07VAL'],
           }
FullsimEffs = {'muon':[FullsimDir+'DYToLL_M-50_TuneCP5_14TeV-pythia8_HLTTDRSummer20_LMT012'],
               'electron':[FullsimDir+'DYToLL_M-50_TuneCP5_14TeV-pythia8_HLTTDRSummer20_LMT012'],
               'photon':[FullsimDir+'GluGluToHHTo2B2G_node_SM_TuneCP5_14TeV-madgraph_pythia8_HLTTDRSummer20_LMT012'],
               'jet':[FullsimDir+'QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8_HLTTDRSummer20_LMT012'],
               'bjet':[FullsimDir+'TT_TuneCP5_14TeV-powheg-pythia8_HLTTDRSummer20_200PU'],
           }

DelphesFakes = [DelphesDir+'QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8_200PU_v7closure'] # for everything?
FullsimFakes = [FullsimDir+'QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8_HLTTDRSummer20_LMT012'], # for everything?

start_time = time.time()

# Do we need proxies? Maybe not, all local...
# print 'Getting proxy'
# proxyPath=os.popen('voms-proxy-info -path')
# proxyPath=proxyPath.readline().strip()
# print 'ProxyPath:',proxyPath
# if 'tmp' in proxyPath: 
#     print 'Run source environment.(c)sh and make a new proxy!'
#     exit(1)

print 'Starting Submission'
count = 0

# Loop over particles
for particle in particles:
    
    # For each particle we will submit a job for:
    # Delphes efficiency, from all relevant samples
    # Delphes fakes, from all relevant samples
    # Fullsim efficiency, from all relevant samples -- switch to turn off for closures
    # Fullsim fakes, from all relevant samples -- switch to turn off for closures
    # "jet" is the only one that doesn't have "fakes"

    samplelist = DelphesEffs[particle]
    if doFullsim:
        if particle == 'jet': samplelist += FullsimEffs[particle]
        else: samplelist += FullsimEffs[particle] + DelphesFakes + FullsimFakes
    else:
        if particle != 'jet': samplelist += DelphesFakes

    # Loop over the samples
    for sample in samplelist:

        outDir = sample.replace(DelphesDir,HistoDir+particle+'Histos_').replace(FullsimDir,HistoDir+particle+'Histos_')
        logDir = sample.replace(DelphesDir,LogDir+particle+'Histos_').replace(FullsimDir,LogDir+particle+'Histos_')
        
        # For each sample we need a list of input ROOT files
        rootlist = EOSlist_root_files(sample)
        tmpcount = 0

        # Loop over the root files to submit jobs
        for rfile in rootlist:
            
            tmpcount += 1
            #if tmpcount > 1: continue # for a test job

            # Manipulate names -- NEED TO THINK ABOUT EXTENSIONS or avoid them
            # file looks like sample_blah_blah_345.root
            index = (rfile.split('.')[0]).split('_')[-1]
            basename = rfile.split('_')[0] #DYToLL or QCD or GluGluToHHTo2B2G, etc.
            if basename == 'QCD':
                basename = basename+'_'+rfile.split('_')[1] # Pt-20to30, etc.
            
            outname = particle+'_delphes_'+basename+'_'+index

            # Write the condor config
            dict = {'RUNDIR':runDir, 'FILEOUT':outname, 'FILEIN':sample+'/'+rfile, 'TCL':dumptcl, 'PARTICLE':particle, 'OUTDIR':outDir}
            jdfName = logDir+'/'+rfile.replace('.root','.job')
            jdf = open(jdfName,'w')
            jdf.write(
                """universe = vanilla
+JobFlavor = tomorrow
Executable = %(RUNDIR)s/RunHistos.sh
Should_Transfer_files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(RUNDIR)s/ntuple_analyser.py, %(RUNDIR)s/bin/NtupleDataFormat.py, %(RUNDIR)s/bin/__init__.py
Output = %(FILEOUT)s.out
Error = %(FILEOUT)s.err
Log = %(FILEOUT)s.log
Notification = Never
Arguments = %(FILEIN)s %(FILEOUT)s %(TCL)s %(PARTICLE)s %(OUTDIR)s

Queue 1"""%dict)
            jdf.close()
            os.chdir(logDir)
            os.system('condor_submit '+jdfName)
            os.system('sleep 0.5')
            os.chdir(runDir)
            print str(count), "jobs submitted!"

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))
