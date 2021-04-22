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
        cut_pattern = r"(\w\w\w\d+\w+\d+\w+)"
    else:
        cut_pattern = r"(\d+\w*\d*)"
    cut_name = r.findall(cut_pattern, name)
    cut_name_prop = [name.replace("p", ".").replace(
        ".t", "pt") for name in cut_name]
    return cut_name_prop


def pt_bin(caption):
    """Returns edited pt bins for subfigure captions."""
    pt_low_pattern = r"\d\d+[t][o]"
    pt_high_pattern = r"[t][o]\d\d+"
    pt_highest_pattern = r"\d\d\d[t][o][I][n][f]"

    pt_low = remove_ch(str(r.findall(pt_low_pattern, caption))).rstrip("to")
    pt_high = remove_ch(str(r.findall(pt_high_pattern, caption))).lstrip("to")
    pt_highest = remove_ch(
        str(r.findall(pt_highest_pattern, caption))).rstrip("toInf")

    if caption == '':
        new_name = 'no bin'
    elif pt_highest:
        new_name = "$ p_{T} > " + pt_highest + " $"
    else:
        new_name = "$ " + pt_low + " < p_{T} < " + pt_high + " $"
    return new_name


def eta_bin(caption):
    """Returns edited eta bins for subfigure captions."""
    eta_low_pattern = r"\A\d\.*\d*"
    eta_high_pattern = r"[t][o]\d\.*\d*"
    eta_highest_pattern = r"\d\.*\d*[t][o][I][n][f]"

    eta_low = remove_ch(str(r.findall(eta_low_pattern, caption))).rstrip("to")
    eta_high = remove_ch(
        str(r.findall(eta_high_pattern, caption))).lstrip("to")
    eta_highest = remove_ch(
        str(r.findall(eta_highest_pattern, caption))).strip("_toInf")

    if caption == '':
        new_name = 'no bin'
    elif eta_highest:
        new_name = r"$ |\eta| > " + eta_highest + " $"
    else:
        new_name = "$ " + eta_low + r" < |\eta| < " + eta_high + " $"
    return new_name


def sorter(dictt):
    """Sort resolution plots."""
    batch = {}
    sorted_dict = collections.OrderedDict()
    if plt == "resolution":
        pt_low_pattern = r"[p][t][_]\d+"
        batch_list = []
        for i in range(len(dictt) // 5):
            batch_list.append(collections.OrderedDict())
        for i, caption in enumerate(dictt):
            pt_low = remove_ch(
                str(r.findall(pt_low_pattern, caption))).lstrip("pt_")
            if i == 0 or i % 5 != 0:
                batch[int(remove_ch(str(pt_low)))] = [caption, dictt[caption]]
                batch = sorted(batch.items())
                batch = collections.OrderedDict(batch)
                div = i // 5
                if i + 1 == len(dictt):
                    batch_list[div].update(batch)
            else:
                batch_list[div].update(batch)
                batch = {}
                batch[int(remove_ch(str(pt_low)))] = [caption, dictt[caption]]
        for entry in batch_list:
            for key in entry:
                sorted_dict[entry[key][0]] = entry[key][1]

    elif variable == "eta":
        pt_low_pattern = r"\d\d+[t][o]"
        for caption in dictt:
            pt_low = remove_ch(
                str(r.findall(pt_low_pattern, dictt[caption]))).rstrip("to")
            if pt_low == '':
                batch[0] = [caption, dictt[caption]]
            else:
                batch[int(pt_low)] = [caption, dictt[caption]]
                batch = sorted(batch.items())
                batch = collections.OrderedDict(batch)
        for key in batch:
            sorted_dict[batch[key][0]] = batch[key][1]
    else:
        sorted_dict = dictt
    return sorted_dict


def res_bin_edit(caption):
    """Returns nicely edited version of the resolution plot captions."""
    eta_low_pattern = r"[e][t][a][_]\d\.*\d*"
    eta_high_pattern = r"[e][t][a][_]\d\.*\d*[_]\d\.*\d*"
    eta_highest_pattern = r"[e][t][a][_]\d\.*\d*[_][I][n][f]"

    pt_low_pattern = r"[p][t][_]\d+"
    pt_high_pattern = r"[p][t][_]\d+[_]\d+"
    pt_highest_pattern = r"[p][t][_]\d+[_]\D+"

    eta_low = remove_ch(
        str(r.findall(eta_low_pattern, caption))).lstrip("eta_")
    eta_high = remove_ch(
        str(r.findall(eta_high_pattern, caption))).lstrip("eta_" + eta_low)
    eta_highest = remove_ch(
        str(r.findall(eta_highest_pattern, caption))).lstrip("eta_").strip("_Inf")

    pt_low = remove_ch(str(r.findall(pt_low_pattern, caption))).lstrip("pt_")
    pt_high = remove_ch(
        str(r.findall(pt_high_pattern, caption))).lstrip("pt_" + pt_low)
    pt_highest = remove_ch(
        str(r.findall(pt_highest_pattern, caption)))

    if eta_highest:
        new_caption = "$ " + r" |\eta| > " + eta_highest + r" \,\text{and}\, "
    else:
        new_caption = "$ " + eta_low + r" < |\eta| < " + \
            eta_high + r" \,\text{and}\, "

    if pt_highest:
        new_caption += " p_{T} > " + pt_low + " $"
    else:
        new_caption += pt_low + " < p_{T} < " + pt_high + " $"

    return new_caption


def reversebins(plot_name):  # to easily sort the plot list according to eta bins
    """Reverses the bins in the plot name."""
    eta_pattern = r"[e][t][a].+"
    pt_pattern = r".+[e][t][a]"
    eta_bin = r.findall(eta_pattern, plot_name)
    pt_bin = r.findall(pt_pattern, plot_name)
    return remove_ch(str(eta_bin)+"_"+str(pt_bin)).rstrip("_eta")


def beginFrame(extra=''):
    """Returns the beginning lines for a new page."""
    tex_line = "\n" r"\begin{frame}" + "\n" + \
        r"\frametitle{" + object_ + " " + plt
    if plt == 'resolution':
        tex_line += r" vs pt and eta"
    else:
        tex_line += " vs " + variable
    tex_line += " " + workingp + extra + r"}" + "\n" + r"\begin{figure}"
    # remove the numbering under the subfigures
    tex_line += "\n" + r"\captionsetup[subfigure]{labelformat=empty}"
    return tex_line


def subfigure(figure, caption):
    """Returns subfigure lines for tex."""
    tex_line = r"\begin{subfigure}{0.32\textwidth}" + \
        "\n" + r"\includegraphics[width=\linewidth]{"
    tex_line += path + figure
    tex_line += r"}" + "\n" + r"\caption{"

    if 'eta' in figure and 'pt_' not in figure:  # 'pt_': underscore is used to exclude 'ptresponse'
        caption = pt_bin(caption)

    if 'pt_' in figure and 'eta' not in figure:
        caption = eta_bin(caption)

    if 'eta' in figure and 'pt_' in figure:  # resolution bins
        caption = res_bin_edit(caption)

    if caption == '':
        caption = 'no bin'

    tex_line += r"\text{" + caption + r"}"
    tex_line += "}\n" + r"\end{subfigure}" + "\n" + r"\hfil"
    return tex_line


def add_figures(figure_dict):
    """Adds figure structure to the script."""
    tex_line = "\n"
    for i, figure in enumerate(figure_dict):
        if plt == 'resolution':
            if i != 0 and i % 5 == 0:
                tex_line += "\n" + r"\end{figure}" + "\n" + r"\end{frame}"
                tex_line += "\n" + \
                    beginFrame(" cont'd")
        tex_line += subfigure(figure_dict[figure],
                              str(figure).strip("'[]")) + "\n"
    tex_line += r"\end{figure}"
    for i in range(len(figure_dict)):
        if i == 6:
            tex_line += "\n" + r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line


def texoutput(plt_type, obj, var, wp):
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
    tex_line = beginFrame()
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
    name_list = sorter(name_list)
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
                      default='pdfOutput/',
                      type='string')
    parser.add_option('-b', '--btagpath',
                      dest='btagpath',
                      help='path for TTbar histo file [%default]',
                      default='BTag/',
                      type='string')
    parser.add_option('-e', '--elmupath',
                      dest='elmupath',
                      help='path for ElMu_Efficiency histo file [%default]',
                      default='ELMu/',
                      type='string')
    parser.add_option('-g', '--gammapath',
                      dest='gammapath',
                      help='path for Photon_Efficiency histo file [%default]',
                      default='Photon/',
                      type='string')
    parser.add_option('-q', '--qcdpath',
                      dest='qcdpath',
                      help='path for QCD histo file [%default]',
                      default='QCD/',
                      type='string')
    parser.add_option('-t', '--taupath',
                      dest='taupath',
                      help='path for QCD histo file [%default]',
                      default='TauTag/',
                      type='string')
    parser.add_option('--parentpath',
                      dest='parentpath',
                      help='parent path for all the plot directories [%default]',
                      default=None,
                      type='string')

    (opt, args) = parser.parse_args()

    printoutdir = opt.printoutdir
    parentpath = opt.parentpath
    qcdpath = opt.qcdpath
    btagpath = opt.btagpath
    elmupath = opt.elmupath
    gammapath = opt.gammapath
    taupath = opt.taupath
    if parentpath:
        qcdpath = parentpath+opt.qcdpath
        btagpath = parentpath+opt.btagpath
        elmupath = parentpath+opt.elmupath
        gammapath = parentpath+opt.gammapath
        taupath = parentpath+opt.taupath

    if not os.path.exists(printoutdir):
        os.system('mkdir -p {}'.format(printoutdir))

    os.system('touch {}/validation_plots.tex'.format(printoutdir))

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
    
    \section{Cover}
    
    \frame{\titlepage}

    """.split("\n"))

    global plots_list
    global path

    # Electron
    plots_list = os.listdir(elmupath)
    path = elmupath
    os.system('cd {}'.format(path))
    tex_lines += r"\section{Electron}" + "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'tightID')

    plots_list = os.listdir(qcdpath)
    path = qcdpath
    os.system('cd {}'.format(path))

    tex_lines += "\n" + r"\subsection{Fakerate reco*ID*ISO}"
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'tightIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'tightIDISO')

    plots_list = os.listdir(elmupath)
    path = elmupath
    os.system('cd {}'.format(path))
    tex_lines += "\n" + r"\subsection{$ p_{T} $ response}"
    tex_lines += texoutput('ptresponse', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'electron', 'pt', 'tightID')
    tex_lines += "\n" + r"\subsection{Resolution}"
    tex_lines += texoutput('resolution', 'electron', 'pt', 'tightID')

    # Muon
    plots_list = os.listdir(elmupath)
    path = elmupath
    os.system('cd {}'.format(path))
    tex_lines += r"\section{Muon}" + "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'tightID')

    plots_list = os.listdir(qcdpath)
    path = qcdpath
    os.system('cd {}'.format(path))
    tex_lines += "\n" + r"\subsection{Fakerate reco*ID*ISO}"
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'tightIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'tightIDISO')

    plots_list = os.listdir(elmupath)
    path = elmupath
    os.system('cd {}'.format(path))
    tex_lines += "\n" + r"\subsection{$ p_{T} $ response}"
    tex_lines += texoutput('ptresponse', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'muon', 'pt', 'tightID')
    tex_lines += "\n" + r"\subsection{Resolution}"
    tex_lines += texoutput('resolution', 'muon', 'pt', 'tightID')

    # Photon
    plots_list = os.listdir(gammapath)
    path = gammapath
    os.system('cd {}'.format(path))
    tex_lines += r"\section{Photon}" + "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'mediumID')
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'mediumID')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'tightID')
    plots_list = os.listdir(qcdpath)
    path = qcdpath
    os.system('cd {}'.format(path))
    tex_lines += "\n" + r"\subsection{Fakerate reco*ID*ISO}"
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'tightIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'tightIDISO')
    plots_list = os.listdir(gammapath)
    path = gammapath
    os.system('cd {}'.format(path))
    tex_lines += "\n" + r"\subsection{$ p_{T} $ response}"
    tex_lines += texoutput('ptresponse', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'photon', 'pt', 'tightID')
    tex_lines += "\n" + r"\subsection{Resolution}"
    tex_lines += texoutput('resolution', 'photon', 'pt', 'tightID')

    # Jetpuppi
    plots_list = os.listdir(qcdpath)
    path = qcdpath
    os.system('cd {}'.format(qcdpath))
    tex_lines += "\n" + r"\section{Jetpuppi}" + \
        "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'tightID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'reco')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'reco')
    tex_lines += "\n" + r"\subsection{$ p_{T} $ response}"
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'tightID')
    tex_lines += "\n" + r"\subsection{Resolution}"
    tex_lines += texoutput('resolution', 'jetpuppi', 'pt', 'tightID')

    # MET
    plots_list = os.listdir(elmupath)
    path = elmupath
    os.system('cd {}'.format(elmupath))
    tex_lines += "\n" + r"\section{MET}" + "\n" + r"\subsection{MET}"

    met_plots = {'met.pdf': 'Missing E_{T}', 'met_p.pdf': 'Parr. Miss. E_{T}',
                 'met_t.pdf': 'Perp. Miss. E_{T}', 'u_t.pdf': 'u_{T}', 'z_pt.pdf': 'p_{T}(Z)'}
    tex_lines += r"""
    \begin{frame}
    \frametitle{MET}
    \begin{figure}
    \captionsetup[subfigure]{labelformat=empty}
    """
    for plot in met_plots:
        tex_lines += r"\begin{subfigure}{0.32\textwidth}" + "\n"
        tex_lines += r"\includegraphics[width=\linewidth]{"
        tex_lines += elmupath + plot + r"}" + "\n"
        tex_lines += r"\caption{" + met_plots[plot] + r"}" + "\n"
        tex_lines += r"\end{subfigure}" + "\n"
        tex_lines += r"\hfil"
    tex_lines += r"""
    \begin{subfigure}{0.32\textwidth}
    \includegraphics[width=\linewidth]{met_figure.pdf}
    \end{subfigure}
    \hfil
    \end{figure}
    \end{frame}
    """

    # Btag
    plots_list = os.listdir(btagpath)
    path = btagpath
    os.system('cd {}'.format(path))
    tex_lines += "\n" + r"\section{Btag}" + "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('btagRate', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'eta', 'mediumID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'pt', 'mediumID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'pt', 'tightID')

    plots_list = os.listdir(btagpath)
    path = btagpath
    os.system('cd {}'.format(path))
    tex_lines += "\n" + r"\subsection{Btag Light MisTag Rate}"
    tex_lines += texoutput('lightMistagRate', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('lightMistagRate', 'jetpuppi', 'eta', 'mediumID')
    tex_lines += texoutput('lightMistagRate', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('lightMistagRate', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('lightMistagRate', 'jetpuppi', 'pt', 'mediumID')
    tex_lines += texoutput('lightMistagRate', 'jetpuppi', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Btag c MisTag Rate}"
    tex_lines += texoutput('cMistagRate', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('cMistagRate', 'jetpuppi', 'eta', 'mediumID')
    tex_lines += texoutput('cMistagRate', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('cMistagRate', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('cMistagRate', 'jetpuppi', 'pt', 'mediumID')
    tex_lines += texoutput('cMistagRate', 'jetpuppi', 'pt', 'tightID')

    # Tau
    plots_list = os.listdir(taupath)
    path = taupath
    os.system('cd {}'.format(path))
    tex_lines += r"\section{Tau}" + "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('tautagRate', 'tau', 'eta', 'looseID')
    tex_lines += texoutput('tautagRate', 'tau', 'eta', 'mediumID')
    tex_lines += texoutput('tautagRate', 'tau', 'eta', 'tightID')
    tex_lines += texoutput('tautagRate', 'tau', 'pt', 'looseID')
    tex_lines += texoutput('tautagRate', 'tau', 'pt', 'mediumID')
    tex_lines += texoutput('tautagRate', 'tau', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Tau Light MisTag Rate}"
    tex_lines += texoutput('lightMistagRate', 'tau', 'eta', 'looseID')
    tex_lines += texoutput('lightMistagRate', 'tau', 'eta', 'mediumID')
    tex_lines += texoutput('lightMistagRate', 'tau', 'eta', 'tightID')
    tex_lines += texoutput('lightMistagRate', 'tau', 'pt', 'looseID')
    tex_lines += texoutput('lightMistagRate', 'tau', 'pt', 'mediumID')
    tex_lines += texoutput('lightMistagRate', 'tau', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Tau Muon MisTag Rate}"
    tex_lines += texoutput('muonMistagRate', 'tau', 'eta', 'looseID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'eta', 'mediumID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'eta', 'tightID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'pt', 'looseID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'pt', 'mediumID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'pt', 'tightID')

    plots_list = os.listdir(elmupath)
    path = elmupath
    os.system('cd {}'.format(path))
    tex_lines += "\n" + r"\subsection{Tau Electron MisTag Rate}"
    tex_lines += texoutput('elecMistagRate', 'tau', 'eta', 'looseID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'eta', 'mediumID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'eta', 'tightID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'pt', 'looseID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'pt', 'mediumID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'pt', 'tightID')

    tex_lines += "\n" + r"\end{document}"

    with open(printoutdir+'validation_plots.tex', 'w') as tex_output:
        tex_output.write(tex_lines)
    print("\n {}validation_plots.tex file is created!\n".format(printoutdir))

    print("Creating pdf output...")

    os.system(
        'pdflatex --interaction=batchmode {}/validation_plots.tex 2>&1 > /dev/null'.format(printoutdir))

    os.system('open validation_plots.pdf')


if __name__ == "__main__":
    main()
