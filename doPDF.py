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

def cutName(name):
    """Returns the cut interval of the plots."""
    cut_pattern = "(\d+\w+\d+)"
    cut_name = r.findall(cut_pattern, name)
    return cut_name

def subfigure(figure, caption):
    """Defines figures."""
    tex_line = r"\begin{subfigure}{0.32\textwidth}" + "\n" + "\includegraphics[width=\linewidth]{"
    tex_line += figure
    tex_line += r"}"+ "\n" + r"\caption{"
    if caption == "500":
        tex_line += "500toInf"
    else:
        tex_line += caption.replace("p", ".")
    tex_line += "}\n" + r"\end{subfigure}" + "\n" + r"\hfil"
    return tex_line

def add_figures(figure_list):
    """Adds figure structure to the script."""
    tex_line = r"""
    \begin{figure}[htb]
    \centering""" + "\n"
    for i, figure in enumerate(figure_list):
        print(i)
        while i % 6 != 0:
            tex_line += subfigure(figure, str(figure_list[figure]).strip("'[]")) + "\n"
            if "eta" in figure:
                capt = "pt slices"
            else:
                capt = "eta slices"
        else:
            tex_line += r"\newpage"
            tex_line += subfigure(figure, str(figure_list[figure]).strip("'[]")) + "\n"
            if "eta" in figure:
                capt = "pt slices"
            else:
                capt = "eta slices"
    tex_line += r"\caption{" + capt + r"}" + "\n" + r"\end{figure}"
    return tex_line

def texoutput(plt_type, obj, var, wp, plot2D=False):
    """ Generates tex script with the following variables respectively:
        plot type (eff, fakerate etc.), object, variable (eta, pt), working point"""
    tex_line = r"\begin{frame}" + "\n"
    tex_line += r"\frametitle{" + obj + " " + plt_type + " to " + var + " " + wp + r"}"
    name_list = {}
    for name in plots_list:
        if plt_type in name and obj in name and var in name and (wp+"." in name or wp+"_" in name):
            name_list[name] = cutName(name)
            name_list = sorted(name_list.items(), key=operator.itemgetter(1))
            name_list = collections.OrderedDict(name_list)
    tex_line += add_figures(name_list) + "\n" + r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line


tex_lines = ''

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
    
    #tex_lines += texoutput('resolution', 'jetpuppi', 'pt', 'tightID')

if physobj == 'muon':
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'tightID')
    
    tex_lines += texoutput('ptresponse', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'muon', 'pt', 'tightID')

tex_lines += "\n" + r"\end{document}"


with open('all_plots.tex', 'w') as tex_output:
    tex_output.write(tex_lines)
    
#os.system('pdflatex %s/all_plots.tex'%printoutdir)

    