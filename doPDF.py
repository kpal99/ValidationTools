import os, optparse
import re as r
import operator
import collections

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--plotsDir',
                  dest='plotsdir',
                  help='path to input plots [%default]',  
                  default='TTbar/',
                  type='string')

parser.add_option('-o', '--outDir',          
                  dest='printoutdir',       
                  help='output directory for PDFs [%default]',  
                  default='TTbar_PDFs',       
                  type='string')

parser.add_option('-p', '--object',          
                  dest='physObject',       
                  help='object name for plots [%default]',  
                  default='jetpuppi',       
                  type='string')

parser.add_option('-s', '--sample',          
                  dest='smp',       
                  help='sample [%default]',  
                  default='TTbar',       
                  type='string')

(opt, args) = parser.parse_args()

plotsdir = opt.plotsdir
printoutdir = opt.printoutdir
physobj = opt.physObject
smp = opt.smp

if not os.path.exists(printoutdir):
    os.system('mkdir -p %s'%printoutdir)

global plots_list
plots_list = os.listdir(plotsdir)
os.system('touch %s/all_plots.tex'%printoutdir)

def cutName(name, plt_type):
    """Returns the bin of the plots."""
    if plt_type == 'resolution':
        cut_pattern = r"(\w\w\w\d+\w+\d+)"
    else:
        cut_pattern = r"(\d+\w+\d+)"
    cut_name = r.findall(cut_pattern, name)
    cut_name_prop = [name.replace("p", ".").replace(".t", "pt") for name in cut_name]
    return cut_name_prop

def subfigure(figure, caption, plt_type):
    """Defines figures."""
    tex_line = r"\begin{subfigure}{0.32\textwidth}" + "\n" + "\includegraphics[width=\linewidth]{"
    tex_line += figure
    tex_line += r"}"+ "\n" + r"\caption{"
    if caption == '':
        caption = 'no bin'
    if caption == '20to50':
        caption = r"$ 20 < p_{T} < 50 $"
    if caption == '50to100':
        caption = r"$ 50 < p_{T} < 100 $"
    if caption == '100to200':
        caption = r"$ 100 < p_{T} < 200 $"
    if caption == '200to500':
        caption = r"$ 200 < p_{T} < 500 $"
    if caption == "500":
        caption = "$ p_{T} > 500 $"
    
    if caption == "0to1.5":
        caption = r"$ 0 < |\eta| < 1.5 $"
    if caption == "1.5to2.8":
        caption = r"$ 1.5 < |\eta| < 2.8 $"
    if caption == "2.8":
        caption = r"$ |\eta| > 2.8 $"
    if caption == "1.5to3.0" or caption == "1.5to3":
        caption = r"$ 1.5 < |\eta| < 3 $"
    if caption == "3.0to4.0" or caption == "3to4":
        caption = r"$ 3 < |\eta| < 4 $"
    if caption == "4.0to5.0":
        caption = r"$ 4 < |\eta| < 5 $"

    if caption == "eta_0_1.5_pt_20_50":
        caption = r"$ 0 < |\eta| < 1.5  \,\&\,  20 < p_{T} < 50 $"
    if caption == "pt_20_50_eta_1.5_2.8":
        caption = r"$ 1.5 < |\eta| < 2.8 \,\&\, 20 < p_{T} < 50$"
    if caption == "eta_1.5_3.0_pt_20_50" or caption == "pt_20_50_eta_1.5_3":
        caption = r"$ 1.5 < |\eta| < 3 \,\&\, 20 < p_{T} < 50$"
    if caption == "eta_3.0_4.0_pt_20_50":
        caption = r"$  3 < |\eta| < 4 \,\&\, 20 < p_{T} < 50$"
    if caption == "eta_4.0_5.0_pt_20_50":
        caption = r"$  4 < |\eta| < 5 \,\&\, 20 < p_{T} < 50$"

    if caption == "eta_0_1.5_pt_50_100":
        caption = r"$ 0 < |\eta| < 1.5 \,\&\, 50 < p_{T} < 100$"
    if caption == "pt_50_100_eta_1.5_2.8":
        caption = r"$ 1.5 < |\eta| < 2.8 \,\&\, 50 < p_{T} < 100$"
    if caption == "eta_1.5_3.0_pt_50_100" or caption == "pt_50_100_eta_1.5_3":
        caption = r"$ 1.5 < |\eta| < 3 \,\&\, 50 < p_{T} < 100$"
    if caption == "eta_3.0_4.0_pt_50_100" or caption == "pt_50_100_eta_3_4":
        caption = r"$ 3 < |\eta| < 4 \,\&\, 50 < p_{T} < 100$"
    if caption == "eta_4.0_5.0_pt_50_100":
        caption = r"$ 4 < |\eta| < 5 \,\&\, 50 < p_{T} < 100$"

    if caption == "eta_0_1.5_pt_100_200":
        caption = r"$ 0 < |\eta| < 1.5 \,\&\, 100 < p_{T} < 200$"
    if caption == "pt_100_200_eta_1.5_2.8":
        caption = r"$ 1.5 < |\eta| < 2.8 \,\&\, 100 < p_{T} < 200$"
    if caption == "eta_1.5_3.0_pt_100_200" or caption == "pt_100_200_eta_1.5_3":
        caption = r"$ 1.5 < |\eta| < 3 \,\&\, 100 < p_{T} < 200$"
    if caption == "eta_3.0_4.0_pt_100_200":
        caption = r"$ 3 < |\eta| < 4 \,\&\, 100 < p_{T} < 200$"
    if caption == "eta_4.0_5.0_pt_100_200":
        caption = r"$ 4 < |\eta| < 5 \,\&\, 100 < p_{T} < 200$"

    if caption == "eta_0_1.5_pt_200_500":
        caption = r"$ 0 < |\eta| < 1.5 \,\&\, 200 < p_{T} < 500$"
    if caption == "pt_200_500_eta_1.5_2.8":
        caption = r"$ 1.5 < |\eta| < 2.8 \,\&\, 200 < p_{T} < 500$"
    if caption == "eta_1.5_3.0_pt_200_500" or caption == "pt_200_500_eta_1.5_3":
        caption = r"$ 1.5 < |\eta| < 3 \,\&\, 200 < p_{T} < 500$"
    if caption == "eta_3.0_4.0_pt_200_500":
        caption = r"$ 3 < |\eta| < 4 \,\&\, 200 < p_{T} < 500$"
    if caption == "pt_200_500_eta_4.0_5.0":
        caption = r"$ 4 < |\eta| < 5 \,\&\, 200 < p_{T} < 500$"

    if caption == "eta_0_1.5_pt_500_Inf":
        caption = r"$ 0 < |\eta| < 1.5 \,\&\, p_{T} > 500$"
    if caption == "eta_1.5_3.0_pt_500_Inf":
        caption = r"$ 1.5 < |\eta| < 3 \,\&\,p_{T} > 500$"

    tex_line += caption#.replace("_", " ")
    tex_line += "}\n" + r"\end{subfigure}" + "\n" + r"\hfil"
    return tex_line

def beginFrame(plt_type, obj, var, wp, extra):
    """Returns the beginning lines for a new page."""
    tex_line = r"\begin{frame}" + "\n"
    if plt_type == 'resolution':
        tex_line += r"\frametitle{" + obj + " " + plt_type + r" vs pt \& eta" + " " + wp + extra + r"}" + "\n" + r"\begin{figure}"
    else:
        tex_line += r"\frametitle{" + obj + " " + plt_type + " vs " + var + " " + wp + extra + r"}" + "\n" + r"\begin{figure}" 
    return tex_line

def add_figures(figure_list):
    """Adds figure structure to the script."""
    tex_line = "\n"
    for i, figure in enumerate(figure_list):
        if plt == 'resolution' and (i == 5 or i == 10 or i == 14) and i != 0:
            tex_line += "\n" + r"\end{figure}" + "\n" + r"\end{frame}"
            tex_line += "\n" + beginFrame(plt, object_, variable, workingp, " cont'd")
        tex_line += r"\centering" + "\n"
        tex_line += subfigure(figure_list[figure], str(figure).strip("'[]"), plt) + "\n"
    tex_line += r"\end{figure}"
    for i in range(len(figure_list)):
        if i == 6:
            tex_line += "\n" + r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line

def remove_ch(name):
    """Removes excess dirt."""
    new_name = name.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
    return new_name

def reversebins(plot_name):
    """Reverses the bins in the plot name."""
    eta_pattern = r"[e][t][a].+"
    pt_pattern = r".+[e][t][a]"
    eta_bin = r.findall(eta_pattern, plot_name)
    pt_bin = r.findall(pt_pattern, plot_name)
    return remove_ch(str(eta_bin)+"_"+str(pt_bin)).rstrip("_eta")

def texoutput(plt_type, obj, var, wp, plot2D=False):
    """ Generates tex script with the following variables respectively:
        plot type (eff, fakerate etc.), object, variable (eta, pt), working point"""
    global plt
    global object_
    global variable
    global workingp
    plt = plt_type
    object_ = obj
    variable = var
    workingp = wp
    tex_line = beginFrame(plt_type, obj, var, wp, '')
    name_list = {}
    if var == "pt":
        var = "pt_" # to avoid the ptresponse to be taken as pt
    for name in plots_list:
        if plt_type in name and obj in name and var in name and (wp+"." in name or wp+"_" in name):
            if plt_type == 'resolution':
                eta_bin = reversebins((str(cutName(name, plt_type))))
                name_list[str(eta_bin)] = name
                name_list = sorted(name_list.items(), key=operator.itemgetter(0))
            else:
                name_list[str(cutName(name, plt_type))] = name
                name_list = sorted(name_list.items(), key=operator.itemgetter(1))
            print(name_list) # will correct for resoulution plots other than jetpuppi *
            name_list = collections.OrderedDict(name_list)
    if var == "eta" and (plt_type != 'resolution' or plt_type == 'fakerate'):
        name_list.move_to_end("['100to200']")
        name_list.move_to_end("['200to500']")
        if obj != 'muon' and plt_type == 'efficiency':
            name_list.move_to_end("['500']")
        if plt_type == 'fakerate':
            name_list.move_to_end("['500']")
    if plt_type == 'resolution' and obj == 'jetpuppi':
        name_list.move_to_end("eta_0_1.5_pt_100_200")
        name_list.move_to_end("eta_0_1.5_pt_200_500")
        name_list.move_to_end("eta_0_1.5_pt_500_Inf")

        name_list.move_to_end("eta_1.5_3.0_pt_20_50")
        name_list.move_to_end("eta_1.5_3.0_pt_50_100")
        name_list.move_to_end("eta_1.5_3.0_pt_100_200")
        name_list.move_to_end("eta_1.5_3.0_pt_200_500")
        name_list.move_to_end("eta_1.5_3.0_pt_500_Inf")

        name_list.move_to_end("eta_3.0_4.0_pt_20_50")
        name_list.move_to_end("eta_3.0_4.0_pt_50_100")
        name_list.move_to_end("eta_3.0_4.0_pt_100_200")
        name_list.move_to_end("eta_3.0_4.0_pt_200_500")

        name_list.move_to_end("eta_4.0_5.0_pt_20_50")
        name_list.move_to_end("eta_4.0_5.0_pt_50_100")
        name_list.move_to_end("eta_4.0_5.0_pt_100_200")

    # if plt_type == 'resolution' and obj == "muon":
    #     name_list.move_to_end("['pt_50_100_eta_1.5_2.8']", last=False)
    #     name_list.move_to_end("['pt_50_100_eta_0_1.5']", last=False)
    #     name_list.move_to_end("['pt_20_50_eta_1.5_2.8']", last=False)
    #     name_list.move_to_end("['pt_20_50_eta_0_1.5']", last=False)
    if len(name_list) > 6:
        tex_line += add_figures(name_list)
    else:
        tex_line += add_figures(name_list) + "\n" + r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line

tex_lines = "\n".join("{}".format(ln) for ln in
r"""\documentclass[8pt]{beamer}
\setbeamertemplate{footline}[frame number]{}
\setbeamertemplate{navigation symbols}{}
\setbeamersize{text margin left=1mm,text margin right=1mm}
\usepackage{graphicx}
\usepackage{caption,subcaption}
\graphicspath{ {""".split("\n"))
                
tex_lines += plotsdir

tex_lines += r"} }" + "\n" + r"\usepackage[utf8]{inputenc}"

tex_lines += r"\title{" + "{}".format(smp).replace("_", " ") + r"}"


tex_lines += "\n".join("{}".format(ln) for ln in
r"""

\author{RTB}
\institute{CMS}
\date{\today}

\begin{document}

\frame{\titlepage}

""".split("\n"))

if physobj == 'jetpuppi':
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'tightID')
    
    tex_lines += texoutput('resolution', 'jetpuppi', 'pt', 'tightID')

if smp == 'ElMu_Efficiency' and (physobj == 'muon' or physobj == 'electron'):
    #electron
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'electron', 'pt', 'tightID')

    tex_lines += texoutput('resolution', 'electron', 'pt', 'tightID')

    #muon
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'muon', 'pt', 'tightID')

    tex_lines += texoutput('resolution', 'muon', 'pt', 'tightID')

if smp == 'Photon_Efficiency' and physobj == "photon":
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'photon', 'pt', 'tightID')

    tex_lines += texoutput('resolution', 'photon', 'pt', 'tightID')

if (physobj == 'muon' or physobj == 'electron' or physobj == 'photon') and smp == 'QCD':
    #electron
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'looseID')
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'mediumID')
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'looseID')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'mediumID')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'tightID')

    #muon
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'looseID')
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'mediumID')
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'looseID')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'mediumID')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'tightID')

    #photon
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'looseID')
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'mediumID')
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'looseID')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'mediumID')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'tightID')


tex_lines += "\n" + r"\end{document}"

with open('all_plots.tex', 'w') as tex_output:
    tex_output.write(tex_lines)
    
#os.system('pdflatex %s/all_plots.tex'%printoutdir)
