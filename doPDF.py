import os, optparse
import re as r

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

(opt, args) = parser.parse_args()

plotsdir = opt.plotsdir
printoutdir = opt.printoutdir

if not os.path.exists(printoutdir):
    os.system('mkdir -p %s'%printoutdir)

plots_list = os.listdir(plotsdir)
os.system('touch all_plots.tex')

def sliceName(name):
    """Returns the cut interval of the plots."""
    slice_pattern = r"(\d+\w+\d+)"
    sliced_name = r.findall(slice_pattern, name)
    return sliced_name

def subfigure(figure, caption='default'):
    """Defines figures."""
    if figure == None:
        return ''
    else:
        tex_line = r"\begin{subfigure}{0.3\textwidth}" + "\n" + "\includegraphics[width=\linewidth]{"
        tex_line += figure
        tex_line += r"}"+ "\n" + r"\caption{"
        tex_line += caption
        tex_line += "}\n" + r"\end{subfigure}\hfil"
        return tex_line

def add_figures(figure_list):
    """Adds figure structure to the script."""
    tex_line = r"""
    \begin{figure}[htb]
    \centering""" + "\n"
    for figure in figure_list:
        tex_line += subfigure(figure, str(figure_list[figure])) + "\n"
    tex_line += r"\caption{caption}" + "\n" + r"\end{figure}"
    return tex_line

def texoutput(plt_type, obj, var, wp, plot_list, tex_line, plot2D=False):
    """ Generates tex script with the following variables respectively:
        plot type, object, variable (eta, pt), working point, list of all plot files, tex output."""
    tex_line = r"\begin{frame}"
    tex_line += r"\frametitle{" + obj + " " + plt_type + " vs " + var + " " + wp + r"}"
    name_list = {}
    for name in plot_list:
        if plt_type in name and obj in name and var in name and (wp+"." in name or wp+"_" in name):
            name_list[name] = sliceName(name)
    tex_line += add_figures(name_list) + "\n" + r"\end{frame}" + "\n" + r"\newpage"
    return tex_line


tex_lines = ''

tex_lines = "\n".join("{}".format(ln) for ln in
r"""\documentclass{beamer}
\setbeamersize{text margin left=1mm,text margin right=1mm} 
\usepackage{graphicx}
\usepackage{caption,subcaption}
\graphicspath{ {""".split("\n"))
                
tex_lines += plotsdir

tex_lines += "\n".join("{}".format(ln) for ln in
r"""} }
\usepackage[utf8]{inputenc}

\title{All plots}

\author{RTB}
\institute{CMS}
\date{\today}

\begin{document}

\frame{\titlepage}

""".split("\n"))
    
tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'looseID', plots_list, tex_lines)
tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'tightID', plots_list, tex_lines)
tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'looseID', plots_list, tex_lines)
tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'tightID', plots_list, tex_lines)

tex_lines += texoutput('fakerate', 'jetpuppi', 'eta', 'looseID', plots_list, tex_lines)
tex_lines += texoutput('fakerate', 'jetpuppi', 'eta', 'tightID', plots_list, tex_lines)
tex_lines += texoutput('fakerate', 'jetpuppi', 'pt', 'looseID', plots_list, tex_lines)
tex_lines += texoutput('fakerate', 'jetpuppi', 'pt', 'tightID', plots_list, tex_lines)

tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'looseID', plots_list, tex_lines)
tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'tightID', plots_list, tex_lines)
tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'looseID', plots_list, tex_lines)
tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'tightID', plots_list, tex_lines)

tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'looseID', plots_list, tex_lines)
tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'tightID', plots_list, tex_lines)
tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'looseID', plots_list, tex_lines)
tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'tightID', plots_list, tex_lines)

tex_lines += "\n" + r"\end{document}"


with open('all_plots.tex', 'w') as tex_output:
    tex_output.write(tex_lines)
    