# python hadd_histos.py fullsim; python hadd_histos.py delphes

import os, sys 

sim = sys.argv[1]

macro_samples={
    'ELMu':'DY',
    'Photon':'2B2G:GluGluHToGG',
    'QCD':'QCD',
    'TauTag':'2B2Tau:HToTauTau:DY',
    #'BTag':'TT_TuneCP5:2B2Tau:2B2G',
    #'BTag':'TT_TuneCP5:2B2Tau:2B2G',
    'BTag':'TT_TuneCP5',
}


eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/fullsim_Iter6/'
name='HistosFS'


if 'delphes' in sim:
    eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/delphes343pre07_v09/'
    name='HistosDELPHES'

haddpath=eospath
haddpath='./'


histo_dirs = [x[0] for x in os.walk(eospath)]
histo_dirs = histo_dirs[1:]

#print histo_dirs

for key in macro_samples.keys():
    print key, macro_samples[key]

    if key != 'BTag': continue
    hadd_file='{}{}_{}.root'.format(haddpath, name, key)
    print '    '
    print 'hadding   ', hadd_file
    print '    '

    hadd_cmd='hadd -f {}'.format(hadd_file)
    
    for proc_str in macro_samples[key].split(':'):
        print '     ', proc_str
        
        for dire in histo_dirs:
            #print name, dire            
            if  proc_str in dire:
                print dire

                for root, dirs, files in os.walk(dire):
                    for filename in files:
                       abs_fname = '{}/{}'.format(dire,filename)
                       #print '                          ', abs_fname

                       hadd_cmd += ' {}'.format(abs_fname)
    
    #print hadd_cmd
    os.system(hadd_cmd)
