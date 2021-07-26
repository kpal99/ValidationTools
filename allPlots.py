import os 
import multiprocessing as mp

def run_cmd(plot_cmd):
    os.system(plot_cmd)

delphes_version='343pre11'
delphes_version='343pre12'
card_version='v12a'
card_version='v13b'
card_version='v13c'
card_version='v14a'
card_version='v14b'
card_version='v14c'
card_version='v14d'
card_version='v14e'
card_version='v14f'

#delphes_version='343pre07'
#card_version='v09'

fullsim_version='Iter6'

debug=False
debug=True

eospath='/eos/cms/store/group/upgrade/RTB/'


histo_dir = '{}/ValidationHistos/'.format(eospath)
plot_dir = '{}/ValidationPlots/'.format(eospath)

delphes_prefix='HistosDELPHES'
fullsim_prefix='HistosFS'



# format delphes:fullsim
samples=[
    'DYToLL:DYToLL_113X',
#    'Photon:Photon_113X',
#    'QCD:QCD_113X',
#    'TauTag:TauTag_112X',
#    'BTag:BTag_112X'
]


threads = []

for sample in samples:
    
    sample_d=sample.split(':')[0]
    sample_f=sample.split(':')[1]
   
    #if sample_d != 'BTag': continue
 
    delphes_file='{}/delphes{}_{}_wenyu/{}_{}.root'.format(histo_dir,delphes_version,card_version,delphes_prefix,sample_d)
    fullsim_file='{}/fullsim_{}_wenyu/{}_{}.root'.format(histo_dir,fullsim_version,fullsim_prefix,sample_f)

    #print delphes_file
    #print fullsim_file

    output_dir='{}/fullsim_{}_delphes_{}_{}_wenyu/{}'.format(plot_dir,fullsim_version, delphes_version, card_version, sample_d)
    #print output_dir

    os.system('mkdir -p {}'.format(output_dir))
    plot_cmd = 'python doPlot.py -d {} -f {} -o {}/  --outFormat pdf'.format(delphes_file, fullsim_file, output_dir)

    thread = mp.Process(target=run_cmd,args=(plot_cmd,))
    thread.start()
    threads.append(thread)
    
    print(plot_cmd)

    #if not debug: run_cmd(plot_cmd)

if not debug: 
    for proc in threads:
	proc.join()   
