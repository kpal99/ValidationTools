import os
import optparse
import re as r
import operator
import collections


def remove_ch(name):
    """Removes excess dirt."""
    new_name = name.replace("[", "").replace(
        "]", "").replace("'", "").replace('"', "")
    return new_name


def cutName(name, plt_type):
    """Returns the bin of the plots."""
    if plt_type == 'resolution':
        cut_pattern = r"(\w\w\w\d+\w+\d+)"
    else:
        cut_pattern = r"(\d+\w+\d+)"
    cut_name = r.findall(cut_pattern, name)
    cut_name_prop = [name.replace("p", ".").replace(
        ".t", "pt") for name in cut_name]
    return cut_name_prop


def bin_edit(caption):
    """Returns nicely edited version of the bins for the resolution plot captions."""
    eta_low_pattern = r"[e][t][a][_]\d\.*\d*"
    eta_high_pattern = r"[e][t][a][_]\d\.*\d*[_]\d\.*\d*"
    pt_low_pattern = r"[p][t][_]\d+"
    pt_high_pattern = r"[p][t][_]\d+[_]\d+"

    eta_low = remove_ch(
        str(r.findall(eta_low_pattern, caption))).lstrip("eta_")
    eta_high = remove_ch(
        str(r.findall(eta_high_pattern, caption))).lstrip("eta_" + eta_low)
    pt_low = remove_ch(str(r.findall(pt_low_pattern, caption))).lstrip("pt_")
    pt_high = remove_ch(
        str(r.findall(pt_high_pattern, caption))).lstrip("pt_" + pt_low)

    new_caption = "$ " + eta_low + r" < |\eta| < " + eta_high + r" \,and\, "
    if pt_low == "500":
        new_caption += " p_{T} > " + pt_low + " $"
    else:
        new_caption += pt_low + " < p_{T} < " + pt_high + " $"
    return new_caption


def subfigure(figure, caption, plt_type):
    """Defines figures."""
    tex_line = r"\begin{subfigure}{0.32\textwidth}" + \
        "\n" + r"\includegraphics[width=\linewidth]{"
    tex_line += path + r"/" + figure
    tex_line += r"}" + "\n" + r"\caption{"
    if caption == '':  # will compose a function for the following lines or include in bin_edit function
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

    resolution_bins = [
        "eta_0_1.5_pt_20_50", "eta_1.5_2.8_pt_20_50",
        "eta_1.5_3.0_pt_20_50", "eta_1.5_3_pt_20_50",
        "eta_3.0_4.0_pt_20_50", "eta_4.0_5.0_pt_20_50",
        "eta_0_1.5_pt_50_100", "eta_1.5_2.8_pt_50_100",
        "eta_1.5_3.0_pt_50_100", "eta_1.5_3_pt_50_100",
        "eta_3.0_4.0_pt_50_100", "eta_3_4_pt_50_100",
        "eta_4.0_5.0_pt_50_100", "eta_0_1.5_pt_100_200",
        "eta_1.5_2.8_pt_100_200", "eta_1.5_3.0_pt_100_200",
        "eta_1.5_3_pt_100_200", "eta_3.0_4.0_pt_100_200",
        "eta_4.0_5.0_pt_100_200", "eta_0_1.5_pt_200_500",
        "eta_1.5_2.8_pt_200_500", "eta_1.5_3.0_pt_200_500",
        "eta_1.5_3_pt_200_500", "eta_3.0_4.0_pt_200_500",
        "eta_4.0_5.0_pt_200_500", "eta_0_1.5_pt_500_Inf",
        "eta_1.5_3.0_pt_500_Inf"
    ]

    if caption in resolution_bins:
        caption = bin_edit(caption)

    tex_line += caption
    tex_line += "}\n" + r"\end{subfigure}" + "\n" + r"\hfil"
    return tex_line


def beginFrame(plt_type, obj, var, wp, extra):
    """Returns the beginning lines for a new page."""
    tex_line = r"\begin{frame}" + "\n" + r"\frametitle{" + obj + " " + plt_type
    if plt_type == 'resolution':
        tex_line += r" vs pt and eta"
    else:
        tex_line += " vs " + var
    tex_line += " " + wp + extra + r"}" + "\n" + r"\begin{figure}"
    return tex_line


def add_figures(figure_list):
    """Adds figure structure to the script."""
    tex_line = "\n"
    for i, figure in enumerate(figure_list):
        if plt == 'resolution':
            if i != 0 and (i == 5 or i == 10 or i == 14) and object_ != 'muon':
                tex_line += "\n" + r"\end{figure}" + "\n" + r"\end{frame}"
                tex_line += "\n" + \
                    beginFrame(plt, object_, variable, workingp, " cont'd")
            if object_ == 'muon' and i == 4:
                tex_line += "\n" + r"\end{figure}" + "\n" + r"\end{frame}"
                tex_line += "\n" + \
                    beginFrame(plt, object_, variable, workingp, " cont'd")

        #tex_line += r"\centering" + "\n"
        tex_line += subfigure(figure_list[figure],
                              str(figure).strip("'[]"), plt) + "\n"
    tex_line += r"\end{figure}"
    for i in range(len(figure_list)):
        if i == 6:
            tex_line += "\n" + r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line


def reversebins(plot_name):  # will omit this function since it is now unnecessary
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
        var = "pt_"  # to avoid the ptresponse to be taken as pt
    for name in plots_list:
        if plt_type in name and obj in name and var in name and (wp+"." in name or wp+"_" in name):
            if plt_type == 'resolution':
                eta_bin = reversebins((str(cutName(name, plt_type))))
                name_list[str(eta_bin)] = name
                name_list = sorted(name_list.items(),
                                   key=operator.itemgetter(0))
            else:
                name_list[str(cutName(name, plt_type))] = name
                name_list = sorted(name_list.items(),
                                   key=operator.itemgetter(1))
            name_list = collections.OrderedDict(name_list)
    if var == "eta" and plt_type != 'resolution':  # or plt_type == 'fakerate'):
        name_list.move_to_end("['100to200']")
        name_list.move_to_end("['200to500']")
        if obj != 'muon' and plt_type == 'efficiency':
            name_list.move_to_end("['500']")
        if plt_type == 'fakerate' or plt_type == "ptresponse" and obj != "muon":
            name_list.move_to_end("['500']")
    if plt_type == 'resolution':
        name_list.move_to_end("eta_0_1.5_pt_50_100", last=False)
        name_list.move_to_end("eta_0_1.5_pt_20_50", last=False)
        if obj == 'jetpuppi':
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

        if obj == "electron":
            name_list.move_to_end("eta_1.5_3_pt_100_200")
            name_list.move_to_end("eta_1.5_3_pt_200_500")
            name_list.move_to_end("eta_3_4_pt_50_100")

        if obj == "muon":
            name_list.move_to_end("eta_1.5_2.8_pt_100_200")
            name_list.move_to_end("eta_1.5_2.8_pt_200_500")

        if obj == "photon":
            name_list.move_to_end("eta_1.5_3_pt_20_50")
            name_list.move_to_end("eta_1.5_3_pt_50_100")
            name_list.move_to_end("eta_1.5_3_pt_100_200")
            name_list.move_to_end("eta_1.5_3_pt_200_500")

    if len(name_list) > 6:
        tex_line += add_figures(name_list)
    else:
        tex_line += add_figures(name_list) + "\n" + \
            r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line


def main():

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('-o', '--outDir',
                      dest='printoutdir',
                      help='output directory for PDF file [%default]',
                      default='Plots/',
                      type='string')
    parser.add_option('-t', '--ttbarpath',
                      dest='ttbarpath',
                      help='path for TTbar histo file [%default]',
                      default='TTbar/',
                      type='string')
    parser.add_option('-e', '--elmupath',
                      dest='elmupath',
                      help='path for ElMu_Efficiency histo file [%default]',
                      default='ElMu_Efficiency/',
                      type='string')
    parser.add_option('-g', '--gammapath',
                      dest='gammapath',
                      help='path for Photon_Efficiency histo file [%default]',
                      default='Photon_Efficiency/',
                      type='string')
    parser.add_option('-q', '--qcdpath',
                      dest='qcdpath',
                      help='path for QCD histo file [%default]',
                      default='QCD/',
                      type='string')

    (opt, args) = parser.parse_args()

    printoutdir = opt.printoutdir
    qcdpath = opt.qcdpath
    ttbarpath = opt.ttbarpath
    elmupath = opt.elmupath
    gammapath = opt.gammapath

    if not os.path.exists(printoutdir):
        os.system('mkdir -p %s' % printoutdir)

    os.system('touch %s/validation_plots.tex' % printoutdir)

    tex_lines = "\n".join("{}".format(ln) for ln in
                          r"""\documentclass[8pt]{beamer}
    \setbeamertemplate{footline}[frame number]{}
    \setbeamertemplate{navigation symbols}{}
    \setbeamersize{text margin left=0mm,text margin right=0mm}
    \usepackage{graphicx}
    \usepackage{caption,subcaption}
    \graphicspath{ {.} }
    \usepackage[utf8]{inputenc}

    \title{Validation Plots}

    \author{RTB}
    \institute{CMS}
    \date{\today}

    \begin{document}

    \frame{\titlepage}
    \setbeamertemplate{section in toc}{\inserttocsection}
    \begin{frame}
        \frametitle{Table of Contents}
        \tableofcontents
        \clearpage
    \end{frame}

    """.split("\n"))

    global plots_list
    plots_list = os.listdir(ttbarpath)

    global path

    # TTbar
    path = ttbarpath
    os.system('cd TTbar')
    plot_title = "Jetpuppi Efficiency"
    #obj = 'jetpuppi'
    #object_ = obj

    tex_lines += "\n" + r"\section{Jetpuppi}"
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'tightID')

    tex_lines += texoutput('resolution', 'jetpuppi', 'pt', 'tightID')

    # ElMu_Efficiency
    plots_list = os.listdir(elmupath)
    path = elmupath
    os.system("cd ..")
    os.system('cd ElMu_Efficiency')
    plot_title = "Electron and Muon Efficiency"

    tex_lines += r"\section{Electron Efficiency}"
    # electron
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'electron', 'pt', 'tightID')

    tex_lines += texoutput('resolution', 'electron', 'pt', 'tightID')

    # muon
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'muon', 'pt', 'tightID')

    tex_lines += texoutput('resolution', 'muon', 'pt', 'tightID')

    # Photon_Efficiency
    plots_list = os.listdir(gammapath)
    path = gammapath
    os.system("cd ..")
    os.system('cd Photon_Efficiency')
    plot_title = "Photon Efficiency"

    tex_lines += "\n" + r"\section{Photon Efficiency}"
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'tightID')

    tex_lines += texoutput('ptresponse', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'photon', 'pt', 'tightID')

    tex_lines += texoutput('resolution', 'photon', 'pt', 'tightID')

    # QCD
    plots_list = os.listdir(qcdpath)
    path = qcdpath
    os.system("cd ..")
    os.system('cd QCD')
    plot_title = "Electron-Muon-Photon Fakerate"
    tex_lines += "\n" + r"\section{Electron Fakerate}"
    # electron
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'looseID')
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'mediumID')
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'looseID')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'mediumID')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'tightID')

    # muon
    tex_lines += "\n" + r"\section{Muon Fakerate}"
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'looseID')
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'mediumID')
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'looseID')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'mediumID')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'tightID')

    # photon
    tex_lines += "\n" + r"\section{Photon Fakerate}"
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'looseID')
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'mediumID')
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'looseID')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'mediumID')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'tightID')

    tex_lines += "\n" + r"\end{document}"

    with open(printoutdir+'validation_plots.tex', 'w') as tex_output:
        tex_output.write(tex_lines)
    os.system("cd {}".format(printoutdir))
    os.system('pdflatex %svalidation_plots.tex' % printoutdir)


if __name__ == "__main__":
    main()
