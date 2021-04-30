import os 
import multiprocessing as mp

def run_cmd(plot_cmd):
    os.system(plot_cmd)

delphes_version='343pre10'
card_version='v11_dummy'

#delphes_version='343pre07'
#card_version='v09'

fullsim_version='Iter6'

debug=False

eospath='/eos/cms/store/group/upgrade/RTB/'


histo_dir = '{}/ValidationHistos/'.format(eospath)
plot_dir = '{}/ValidationPlots/'.format(eospath)

delphes_prefix='HistosDELPHES'
fullsim_prefix='HistosFS'



# format delphes:fullsim
samples=[
    'ELMu:ELMu_113X',
    'Photon:Photon_113X',
    'QCD:QCD_113X',
    'TauTag:TauTag_112X',
    'BTag:BTag_112X'
]


threads = []

for sample in samples:
    
    sample_d=sample.split(':')[0]
    sample_f=sample.split(':')[1]
    
    delphes_file='{}/delphes{}_{}/{}_{}.root'.format(histo_dir,delphes_version,card_version,delphes_prefix,sample_d)
    fullsim_file='{}/fullsim_{}/{}_{}.root'.format(histo_dir,fullsim_version,fullsim_prefix,sample_f)

    #print delphes_file
    #print fullsim_file

    output_dir='{}/fullsim_{}_delphes_{}_{}/{}'.format(plot_dir,fullsim_version, delphes_version, card_version, sample_d)
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
