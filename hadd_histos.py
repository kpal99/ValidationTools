
# python hadd_histos.py fullsim; python hadd_histos.py delphes

import os, sys 


debug=False

sim = sys.argv[1]

macro_samples={
    'ELMu_113X':'113X_DYToLL',
    'Photon_113X':'113X_GluGluToHHTo2B2G:113X_GluGluHToGG',
    #'QCD_112X':'112X_QCD',
    'QCD_113X':'113X_QCD',
    'TauTag_112X':'112X_GluGluToHHTo2B2Tau:112X_VBFHToTauTau:112X_GluGluHToTauTau:112X_TT_TuneCP5:112X_QCD',
    #'TauTag':'VBFHToTauTau',
    'BTag_112X':'112X_TT_TuneCP5:112X_GluGluToHHTo2B2Tau:112X_QCD',
}


eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/fullsim_Iter6/'
name='HistosFS'

delphes_version='343pre10'
card_version='v11_dummy'


if 'delphes' in sim:
    #eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/delphes343pre07_v09/'
    eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/delphes{}_{}/'.format(delphes_version,card_version)
    name='HistosDELPHES'

haddpath=eospath
#haddpath='./'


histo_dirs = [x[0] for x in os.walk(eospath)]
histo_dirs = histo_dirs[1:]

#print histo_dirs

for key in macro_samples.keys():

    #print '    '
    print 'hadding {} sample'.format(key)

    #if key != 'BTag': continue
    hadd_file='{}{}_{}.root'.format(haddpath, name, key)
    #print '    '
    #print 'hadding   ', hadd_file
    #print '    '

    hadd_cmd='hadd -f {}'.format(hadd_file)
    
    for proc_str in macro_samples[key].split(':'):
        print '  subprocess:   ', proc_str
        
        for dire in histo_dirs:
            #print name, dire            
            if  proc_str in dire:
                print '    ', dire

                for root, dirs, files in os.walk(dire):
                    for filename in files:
                       abs_fname = '{}/{}'.format(dire,filename)
                       #print '                          ', abs_fname

                       hadd_cmd += ' {}'.format(abs_fname)
    
    #print hadd_cmd
    if not debug:
        os.system(hadd_cmd)
