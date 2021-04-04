import os 


samplelist=[

    '/TT_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v2/FEVT',
    '/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/FEVT',
    '/GluGluHToTauTau_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/GluGluToHHTo2B2Tau_node_SM_TuneCP5_14TeV-madgraph-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1_ext1-v3/FEVT',
    '/GluGluToHHTo2B2G_node_SM_TuneCP5_14TeV-madgraph_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT',
    '/GluGluHToGG_M125_14TeV_powheg_pythia8_TuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT',

    # more leptons and taus, hopefully in barrel+endcap
    '/DoublePhoton_FlatPt-1To100/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1_ext1-v2/FEVT',
    '/DoublePhoton_FlatPt-1To100/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1_ext2-v3/FEVT',
    '/DoubleElectron_FlatPt-1To100/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v2/GEN-SIM-DIGI-RAW-MINIAOD',
    '/DoubleMuon_gun_FlatPt-1To100/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT',
    '/MultiTau_PT15to500/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1_ext1-v2/FEVT',
    '/MultiTau_PT15to500/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1_ext2-v3/FEVT',
    
    # more QCD, although not flat in these pT ranges
    '/QCD_Pt_20to30_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1-v2/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt_30to50_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt_30to50_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v2/GEN-SIM-DIGI-RAW-MINIAOD', # do we want "withNewMB" over the other?
    '/QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt_50to80_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v3/GEN-SIM-DIGI-RAW-MINIAOD', # same here
    '/QCD_Pt_80to120_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt_120to170_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt_300to470_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt_470to600_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',
    '/QCD_Pt_600oInf_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD',

]


macro_samples={
    'ELMu':'Electron:Muon:DY',
    'Photon':'2B2G:GluGluHToGG',
    'QCD':'QCD',
    'TauTag':'2B2Tau:HToTauTau:DY',
    'BTag':'TT_TuneCP5:2B2Tau:2B2G',
}


eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/fullsim_Iter6'

histo_dirs = [x[0] for x in os.walk(eospath)]
histo_dirs = histo_dirs[1:]


haddpath=eospath
haddpath='./'

sim='HistosFS'

for key in macro_samples.keys():
    print key, macro_samples[key]

    #if key != 'Photon': continue
    hadd_file='{}{}_{}.root'.format(haddpath, sim, key)
    print '    '
    print 'hadding   ', hadd_file
    print '    '

    hadd_cmd='hadd -f {}'.format(hadd_file)
    
    for proc_str in macro_samples[key].split(':'):
        print '     ', proc_str
        
        for dire in histo_dirs:
            
	    if sim in dire and proc_str in dire:
        	print dire

		for root, dirs, files in os.walk(dire):
                    for filename in files:
                       abs_fname = '{}/{}'.format(dire,filename)
                       #print '                          ', abs_fname

                       hadd_cmd += ' {}'.format(abs_fname)
    
    print hadd_cmd
    os.system(hadd_cmd)
