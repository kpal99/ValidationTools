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

(opt, args) = parser.parse_args()

plotsdir = opt.plotsdir
printoutdir = opt.printoutdir
physobj = opt.physObject

if not os.path.exists(printoutdir):
    os.system('mkdir -p %s'%printoutdir)

global plots_list
plots_list = os.listdir(plotsdir)
os.system('touch %s/all_plots.tex'%printoutdir)

def cutName(name, plt_type):
    """Returns the cut interval of the plots."""
    if plt_type == 'resolution':
        cut_pattern = r"(\w\w\w\d+\w+\d+)"
    else:
        cut_pattern = r"(\d+\w+\d+)"
    cut_name = r.findall(cut_pattern, name)
    return cut_name

def subfigure(figure, caption, plt_type):
    """Defines figures."""
    tex_line = r"\begin{subfigure}{0.32\textwidth}" + "\n" + "\includegraphics[width=\linewidth]{"
    tex_line += figure
    tex_line += r"}"+ "\n" + r"\caption{"
    if caption == '':
        caption = 'no slice'
    if caption == "500":
        caption = "500toInf"
    if plt_type == 'resolution':
        tex_line += caption.replace("_", " ").replace("p", ".").replace(".t", "pt")
    else:
        tex_line += caption.replace("p", ".").replace("_", "\_")
    tex_line += "}\n" + r"\end{subfigure}" + "\n" + r"\hfil"
    return tex_line

def beginFrame(plt_type, obj, var, wp, extra):
    """Returns the beginning lines for a new page."""
    tex_line = r"\begin{frame}" + "\n"
    if plt_type == 'resolution':
        tex_line += r"\frametitle{" + obj + " " + plt_type + " to pt vs eta" + " " + wp + extra + r"}" + "\n" + r"\begin{figure}"
    else:
        tex_line += r"\frametitle{" + obj + " " + plt_type + " to " + var + " " + wp + extra + r"}" + "\n" + r"\begin{figure}" 
    return tex_line

def add_figures(figure_list):
    """Adds figure structure to the script."""
    tex_line = "\n" #+ r"\begin{figure}[htb]"
    for i, figure in enumerate(figure_list):
        if i % 6 == 0 and i != 0:
            tex_line += "\n" + r"\end{figure}" + "\n" + r"\end{frame}"
            tex_line += "\n" + beginFrame(plt, object_, variable, workingp, " cont'd")
        tex_line += r"\centering" + "\n"
        tex_line += subfigure(figure_list[figure], str(figure).strip("'[]"), plt) + "\n"
        if "eta" in figure_list[figure]:
            capt = "pt slices"
        else:
            capt = "eta slices"
    tex_line += r"\caption{" + capt + r"}" + "\n" + r"\end{figure}"
    for i in range(len(figure_list)):
        if i == 6:
            tex_line += "\n" + r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line

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
            name_list[str(cutName(name, plt_type))] = name
            name_list = sorted(name_list.items(), key=operator.itemgetter(1))
            name_list = collections.OrderedDict(name_list)
    if var == "eta" and plt_type != 'resolution':
        name_list.move_to_end("['100to200']")
        name_list.move_to_end("['200to500']")
        name_list.move_to_end("['500']")
    if plt_type == 'resolution':
        name_list.move_to_end("['pt_50_100_eta_4p0_5p0']", last=False)
        name_list.move_to_end("['pt_50_100_eta_3p0_4p0']", last=False)
        name_list.move_to_end("['pt_50_100_eta_1p5_3p0']", last=False)
        name_list.move_to_end("['pt_50_100_eta_0_1p5']", last=False)
        name_list.move_to_end("['pt_20_50_eta_4p0_5p0']", last=False)
        name_list.move_to_end("['pt_20_50_eta_3p0_4p0']", last=False)
        name_list.move_to_end("['pt_20_50_eta_1p5_3p0']", last=False)
        name_list.move_to_end("['pt_20_50_eta_0_1p5']", last=False)
    if len(name_list) > 6:
        tex_line += add_figures(name_list)
    else:
        tex_line += add_figures(name_list) + "\n" + r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line

tex_lines = "\n".join("{}".format(ln) for ln in
r"""\documentclass[10pt]{beamer}
\setbeamertemplate{footline}[frame number]{}
\setbeamertemplate{navigation symbols}{}
\setbeamersize{text margin left=1mm,text margin right=1mm}
\usepackage{graphicx}
\usepackage{caption,subcaption}
\graphicspath{ {""".split("\n"))
                
tex_lines += plotsdir

tex_lines += "\n".join("{}".format(ln) for ln in
r"""} }
\usepackage[utf8]{inputenc}

\title{TTbar}

\author{RTB}
\institute{CMS}
\date{\today}

\begin{document}

\frame{\titlepage}

""".split("\n"))

params = {
    "plot_types" : ["efficiency", "fakerate", "ptresponse", "resolution", "multiplicity"],
    "objects" : ["electron", "jetpuppi", "muon", "photon"],
    "variables" : ["pt", "eta"]
}

if physobj == 'jetpuppi':
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'tightID')
    
    tex_lines += texoutput('fakerate', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('fakerate', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('fakerate', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('fakerate', 'jetpuppi', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'tightID')
    
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'tightID')
    
    tex_lines += texoutput('resolution', 'jetpuppi', 'pt', 'tightID')

#if physobj == 'muon':
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'tightID')
    
    tex_lines += texoutput('ptresponse', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'muon', 'pt', 'tightID')

#if physobj == 'electron':
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'looseID')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'looseIDISO')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'looseISO')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'mediumID')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'mediumIDISO')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'mediumISO')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'reco')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'tightID')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'tightIDISO')
    tex_lines += texoutput('multiplicity', 'electron', 'electron', 'tightISO')


tex_lines += "\n" + r"\end{document}"

with open('all_plots.tex', 'w') as tex_output:
    tex_output.write(tex_lines)
    
#os.system('pdflatex %s/all_plots.tex'%printoutdir)
