
# python hadd_histos.py fullsim; python hadd_histos.py delphes

import os, sys 


debug=False

sim = sys.argv[1]

macro_samples_fullsim={
    'DYToLL_113X':'113X_DYToLL',
#    'Photon_113X':'113X_GluGluToHHTo2B2G:113X_GluGluHToGG',
#    'QCD_112X':'112X_QCD',
#    'QCD_113X':'113X_QCD',
#    'TauTag_112X':'112X_GluGluToHHTo2B2Tau:112X_VBFHToTauTau:112X_GluGluHToTauTau:112X_TT_TuneCP5:112X_QCD',
#    #'TauTag':'VBFHToTauTau',
#    'BTag_112X':'112X_TT_TuneCP5:112X_GluGluToHHTo2B2Tau:112X_QCD',
    #'BTag_112X':'112X_TT_TuneCP5',
}

macro_samples_delphes={
    'DYToLL':'DYToLL',
#    'Photon':'GluGluToHHTo2B2G:GluGluHToGG',
#    'QCD':'QCD',
#    #'TauTag':'GluGluToHHTo2B2Tau:VBFHToTauTau:GluGluHToTauTau:TT_TuneCP5:112X_QCD',
#    'TauTag':'VBFHToTauTau:GluGluToHHTo2B2Tau:VBFHToTauTau:GluGluHToTauTau:TT_TuneCP5:QCD:Zprime',
#    'BTag':'TT_TuneCP5:GluGluToHHTo2B2Tau:QCD',
#    #'BTag':'TT_TuneCP5',
}


macro_samples=macro_samples_fullsim


#eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/fullsim_Iter6/'
#eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/fullsim_Iter6_JEC/'
eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/fullsim_Iter6_wenyu/'
name='HistosFS'

delphes_version='343pre11'
delphes_version='343pre12'
card_version='v13b'
card_version='v13c'
card_version='v14a'
card_version='v14b'
card_version='v14c'
card_version='v14d'
card_version='v14e'
card_version='v14f'



if 'delphes' in sim:
    #eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/delphes343pre07_v09/'
    eospath='/eos/cms/store/group/upgrade/RTB/ValidationHistos/delphes{}_{}_wenyu/'.format(delphes_version,card_version)
    name='HistosDELPHES'
    macro_samples=macro_samples_delphes

haddpath=eospath
#haddpath='./'


histo_dirs = [x[0] for x in os.walk(eospath)]
histo_dirs = histo_dirs[1:]

#print histo_dirs

working_dir=os.getcwd()


with open("hadd_cmds.sh", "w") as text_file:

    for key in macro_samples.keys():

        #print '    '
        print 'hadding {} sample'.format(key)

        #if key != 'BTag_112X': continue
        #if key != 'QCD_113X': continue
        #if key != 'QCD': continue
        #if key != 'Photon_113X': continue
        hadd_file='{}{}_{}.root'.format(haddpath, name, key)
        #print '    '
        #print 'hadding   ', hadd_file
        #print '    '

        hadd_cmd='hadd -k -f {}'.format(hadd_file)

        for proc_str in macro_samples[key].split(':'):
            print '  subprocess:   ', proc_str

            for dire in histo_dirs:
                #print name, dire            
                if  proc_str in dire:
                    print '    ', dire

                    for root, dirs, files in os.walk(dire):
                        for filename in files:
                           abs_fname = '{}/{}'.format(dire,filename)
                           #print '                          ', abs_fname, '   ', os.stat(abs_fname).st_size == 0

                           ## quickly check whether file is not empty
                           if os.stat(abs_fname).st_size > 0:
                               hadd_cmd += ' {}'.format(abs_fname)

        hadd_cmd += '\n' 
        hadd_cmd += '\n' 

        if not debug:
            text_file.write(hadd_cmd)

if not debug:
    os.chdir(working_dir)  
    os.system('pwd')  
    os.system('source {}/hadd_cmds.sh'.format(working_dir))
