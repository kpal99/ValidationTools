import os
import optparse
import re as r
import operator
from collections import OrderedDict
from commands import getstatusoutput


def remove_ch(name):
    """Remove excess dirt."""
    new_name = name.replace("[", "").replace(
        "]", "").replace("'", "").replace('"', "")
    return new_name


def cutName(name, plt_type):
    """Return the bin of the plots."""
    if plt_type == 'resolution':
        cut_pattern = r"(\w\w\w\d+\w+\d+\w+)"
    else:
        cut_pattern = r"(\d+\w*\d*)"
    cut_name = r.findall(cut_pattern, name)
    new_cut_name = [name.replace("p", ".").replace(
        ".t", "pt") for name in cut_name]
    return new_cut_name


def pt_bin(caption):
    """Return edited pt bins for subfigure captions."""
    pt_low_pattern = r"\d+[t][o]"
    pt_high_pattern = r"[t][o]\d+"
    pt_highest_pattern = r"\d+[t][o][I][n][f]"

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
    """Return edited eta bins for subfigure captions."""
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
    sorted_dict = OrderedDict()
    if plt == "resolution":
        pt_low_pattern = r"[p][t][_]\d+"
        batch_list = []
        unique_pt_values = []
        for caption in dictt:
            pt_low = remove_ch(
                str(r.findall(pt_low_pattern, caption))).lstrip("pt_")
            if pt_low not in unique_pt_values:
                unique_pt_values.append(pt_low)
                batch_list.append(OrderedDict())
        global batch_size
        batch_size = len(batch_list)
        for i, caption in enumerate(dictt):
            pt_low = remove_ch(
                str(r.findall(pt_low_pattern, caption))).lstrip("pt_")
            if i == 0 or i % batch_size != 0:
                batch[int(remove_ch(str(pt_low)))] = [caption, dictt[caption]]
                batch = sorted(batch.items())
                batch = OrderedDict(batch)
                div = i // batch_size
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
                batch = OrderedDict(batch)
        for key in batch:
            sorted_dict[batch[key][0]] = batch[key][1]
    else:
        sorted_dict = dictt
    return sorted_dict


def res_bin_edit(caption):
    """Return nicely edited version of the resolution plot captions."""
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
        str(r.findall(pt_high_pattern, caption))).lstrip('pt_').replace(pt_low+'_', '')
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


def reversebins(plot_name):  # easily sort the plot list according to eta bins
    """Reverse the bins in the plot name."""
    eta_pattern = r"[e][t][a].+"
    pt_pattern = r".+[e][t][a]"
    eta_bin = r.findall(eta_pattern, plot_name)
    pt_bin = r.findall(pt_pattern, plot_name)
    return remove_ch(str(eta_bin)+"_"+str(pt_bin)).rstrip("_eta")


def beginFrame(extra=''):
    """Return the beginning lines for a new page."""
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
    """Return tex lines for subfigures."""
    tex_line = r"\begin{subfigure}{0.32\textwidth}" + \
        "\n" + r"\includegraphics[width=\linewidth]{"
    tex_line += path + figure
    tex_line += r"}" + "\n" + r"\vspace*{-0.15cm}" + "\n" + r"\caption{"

    if 'eta' in figure and 'pt_' not in figure:  # 'pt_': underscore is used to exclude 'ptresponse'
        caption = pt_bin(caption)
    if 'pt_' in figure and 'eta' not in figure:
        caption = eta_bin(caption)
    if 'eta' in figure and 'pt_' in figure:  # resolution bins
        caption = res_bin_edit(caption)
    if caption == '':
        caption = 'no bin'

    tex_line += r"\text{{\tiny " + caption + r"}}}"
    tex_line += "\n" + r"\end{subfigure}" + "\n" + r"\hfil"
    return tex_line


def add_figures(figure_dict):
    """Add figure structure to the script."""
    tex_line = "\n"
    plots_per_page = False
    for i, figure in enumerate(figure_dict):
        if plt == 'resolution':
            new_batch_size = batch_size
            if batch_size > 9:  # at max. 9 figures can be displayed per page
                new_batch_size = round(batch_size / 2)
            if i != 0 and i % new_batch_size == 0:
                tex_line += "\n" + r"\end{figure}" + "\n" + r"\end{frame}"
                tex_line += "\n" + \
                    beginFrame(" cont'd")
        elif len(figure_dict) > 9:
            plots_per_page = round(float(len(figure_dict)) / 2)
            if i != 0 and plots_per_page and i % plots_per_page == 0:
                tex_line += "\n" + r"\end{figure}" + "\n" + r"\end{frame}"
                tex_line += "\n" + beginFrame(" cont'd")
        tex_line += subfigure(figure_dict[figure],
                              str(figure).strip("'[]")) + "\n"
    tex_line += r"\end{figure}" + "\n" + \
        r"\end{frame}" + "\n" + r"\newpage" + 2*"\n"
    return tex_line


def texoutput(plt_type, obj, var, wp):
    """ Generate tex script with the following variables respectively:
        plot type (eff, fakerate etc.), object, variable (eta, pt), working point"""
    global plt, object_, variable, workingp
    plt, object_, variable, workingp = plt_type, obj, var, wp
    tex_line = beginFrame()
    name_dict = {}
    if var == "pt":
        var = "pt_"  # avoid the ptresponse to be taken as pt
    for name in plots_list:
        if plt_type in name and obj in name and var in name and (wp+"." in name or wp+"_" in name):
            if plt_type == 'resolution':
                new_bin = reversebins((str(cutName(name, plt_type))))
                name_dict[str(new_bin)] = name
                name_dict = sorted(name_dict.items(),
                                   key=operator.itemgetter(0))
            else:
                name_dict[str(cutName(name, plt_type))] = name
                name_dict = sorted(name_dict.items(),
                                   key=operator.itemgetter(1))
            name_dict = OrderedDict(name_dict)
    name_dict = sorter(name_dict)
    tex_line += add_figures(name_dict)
    return tex_line


def change_path(plots_path):
    """Change the directory."""
    global plots_list
    global path
    plots_list = os.listdir(plots_path)
    path = plots_path
    os.system('cd {}'.format(plots_path))
    return plots_list, path


def add_met_plots(title):
    """Add MET plots to the tex output."""
    tex_lines = r"""
        \begin{frame}
        \frametitle{"""
    tex_lines += title
    tex_lines += r"""}
        \begin{figure}
        \captionsetup[subfigure]{labelformat=empty}
        """
    for plot in met_plots:
        tex_lines += r"\begin{subfigure}{0.32\textwidth}" + "\n"
        tex_lines += r"\includegraphics[width=\linewidth]{"
        tex_lines += path + plot[0] + r"}" + "\n"
        tex_lines += r"\caption{{\tiny " + plot[1] + r"}}" + "\n"
        tex_lines += r"\end{subfigure}" + "\n"
        tex_lines += r"\hfil"
    tex_lines += r"""
        \begin{subfigure}{0.32\textwidth}
        \includegraphics[width=\linewidth]{met_figure.png}
        \end{subfigure}
        \hfil
        \end{figure}
        \end{frame}
        """
    return tex_lines


def main():

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('-o', '--outDir',
                      dest='printoutdir',
                      help='output directory for PDF file [%default]',
                      default='texOutput/',
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

    tex_lines = "\n".join("{}".format(ln) for ln in
                          r"""\documentclass[8pt]{beamer}
    \setbeamertemplate{frametitle}{
    \insertframetitle}
    \setbeamertemplate{footline}{%
      \raisebox{5pt}{\makebox[\paperwidth]{\hfill\makebox[10pt]{\scriptsize\insertframenumber}}}}
    \setbeamertemplate{navigation symbols}{}
    \setbeamersize{text margin left=0mm,text margin right=0mm}
    \usepackage{graphicx}
    \usepackage{bookmark}
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

    # Jetpuppi

    change_path(qcdpath)

    tex_lines += "\n" + r"\section{Jetpuppi}" + "\n" + r"\subsection{Response}"
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'jetpuppi', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Resolution}"
    tex_lines += texoutput('resolution', 'jetpuppi', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'tightID')
    # tex_lines += texoutput('efficiency', 'jetpuppi', 'eta', 'reco')
    # tex_lines += texoutput('efficiency', 'jetpuppi', 'pt', 'reco')

    # MET
    change_path(elmupath)
    os.system("wget https://cds.cern.ch/record/2205284/files/Figure_007-a.png")
    os.system('mv Figure_007-a.png met_figure.png'.format(printoutdir))
    tex_lines += "\n" + r"\section{MET}" + "\n" + r"\subsection{MET}"

    global met_plots
    met_plots = [['met.pdf', 'MET'],
                 ['met_VS_npuVtx.pdf', 'MET vs nPU Vertices'],
                 ['met_VS_genz_pt.pdf', 'MET vs p$_{T}$(gen Z)'],
                 ['met_VS_genht_pt30_eta5.pdf', 'MET vs H$_{T}$ gen'],
                 ]
    tex_lines += add_met_plots('MET')

    # MET Transverse
    met_plots = [['met_t.pdf', 'MET$_{T}$'],
                 ['met_t_VS_npuVtx.pdf', 'MET$_{T}$ vs nPU Vertices'],
                 ['met_t_VS_genz_pt.pdf', 'MET$_{T}$ vs p$_{T}$(gen Z)'],
                 ['met_t_VS_genht_pt30_eta5.pdf', 'MET$_{T}$ vs H$_{T}$ gen'],
                 ]
    tex_lines += add_met_plots(r'MET$_{T}$')

    # MET Parallel
    met_plots = [['met_p.pdf', 'MET$_{P}$'],
                 ['met_p_VS_npuVtx.pdf', 'MET$_{P}$ vs nPU Vertices'],
                 ['met_p_VS_genz_pt.pdf', 'MET$_{P}$ vs p$_{T}$(gen Z)'],
                 ['met_p_VS_genht_pt30_eta5.pdf', 'MET$_{P}$ vs H$_{T}$ gen'],
                 ]
    tex_lines += add_met_plots(r'MET$_{P}$')

    # U_{T}
    tex_lines += "\n" + r"\subsection{U}"
    met_plots = [['u_t.pdf', 'u$_{T}$'],
                 ['u_t_VS_npuVtx.pdf', 'u$_{T}$ vs nPU Vertices'],
                 ['u_t_VS_genz_pt.pdf', 'u$_{T}$ vs p$_{T}$(gen Z)'],
                 ['u_t_VS_genht_pt30_eta5.pdf', 'u$_{T}$ vs H$_{T}$ gen'],
                 ]
    tex_lines += add_met_plots(r'U$_{T}$')

    # U_{P}
    met_plots = [['u_p.pdf', 'u$_{P}$'],
                 ['u_p_VS_npuVtx.pdf', 'u$_{P}$ vs nPU Vertices'],
                 ['u_p_VS_genz_pt.pdf', 'u$_{P}$ vs p$_{T}$(gen Z)'],
                 ['u_p_VS_genht_pt30_eta5.pdf', 'u$_{P}$ vs H$_{T}$ gen'],
                 ]
    tex_lines += add_met_plots(r'U$_{P}$')

    # U_{T} (RMS)
    met_plots = [['u_t.pdf', 'u$_{T}$'],
                 ['ut_rms_VS_npuVtx.pdf', 'u$_{T}$(RMS) vs nPU Vertices'],
                 ['ut_rms_VS_genz_pt.pdf', 'u$_{T}$(RMS) vs p$_{T}$(gen Z)'],
                 ['ut_rms_VS_genht_pt30_eta5.pdf', 'u$_{T}$(RMS) vs H$_{T}$ gen']]
    tex_lines += add_met_plots(r'U$_{T}$(RMS)')

    # U_{P} (RMS)
    met_plots = [['u_p.pdf', 'u$_{P}$'],
                 ['up_plus_qt_rms_VS_npuVtx.pdf',
                     'u$_{P}+$q$_{T}$(RMS) vs nPU Vertices'],
                 ['up_plus_qt_rms_VS_genz_pt.pdf',
                     'u$_{P}+$q$_{T}$(RMS) vs p$_{T}$(gen Z)'],
                 ['up_plus_qt_rms_VS_genht_pt30_eta5.pdf',
                     'u$_{P}+$q$_{T}$(RMS) vs H$_{T}$ gen']
                 ]
    tex_lines += add_met_plots(r'U$_{P}$(RMS)')

    # Z
    tex_lines += "\n" + r"\subsection{Z}"
    met_plots = [['z_pt.pdf', 'p$_{T}$(Z)'],
                 ['z_pt_VS_npuVtx.pdf', 'p$_{T}$(Z) vs nPU Vertices'],
                 ['z_pt_VS_genz_pt.pdf', 'p$_{T}$(Z) vs p$_{T}$(gen Z)'],
                 ['z_pt_VS_genht_pt30_eta5.pdf', 'p$_{T}$(Z) vs H$_{T}$ gen'],
                 ]
    tex_lines += add_met_plots('Z')

    # Photon

    change_path(gammapath)
    tex_lines += r"\section{Photon}" + "\n" + r"\subsection{Response}"
    tex_lines += texoutput('ptresponse', 'photon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'photon', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Resolution}"
    tex_lines += texoutput('resolution', 'photon', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'looseIDISO')
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'mediumIDISO')
    tex_lines += texoutput('efficiency', 'photon', 'eta', 'tightIDISO')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'looseIDISO')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'mediumIDISO')
    tex_lines += texoutput('efficiency', 'photon', 'pt', 'tightIDISO')

    change_path(qcdpath)
    tex_lines += "\n" + r"\subsection{Fakerate}"
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'eta', 'tightIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'photon', 'pt', 'tightIDISO')

    # Electron

    change_path(elmupath)

    tex_lines += r"\section{Electron}" + "\n" + r"\subsection{Response}"
    tex_lines += texoutput('ptresponse', 'electron', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'electron', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Resolution}"
    tex_lines += texoutput('resolution', 'electron', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'looseIDISO')
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'mediumIDISO')
    tex_lines += texoutput('efficiency', 'electron', 'eta', 'tightIDISO')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'looseIDISO')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'mediumIDISO')
    tex_lines += texoutput('efficiency', 'electron', 'pt', 'tightIDISO')

    change_path(qcdpath)
    tex_lines += "\n" + r"\subsection{Fakerate}"
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'eta', 'tightIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'electron', 'pt', 'tightIDISO')

    # Muon
    change_path(elmupath)
    tex_lines += r"\section{Muon}" + "\n" + r"\subsection{Response}"
    tex_lines += texoutput('ptresponse', 'muon', 'eta', 'tightID')
    tex_lines += texoutput('ptresponse', 'muon', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Resolution}"
    tex_lines += texoutput('resolution', 'muon', 'pt', 'tightID')

    tex_lines += "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'looseIDISO')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'mediumIDISO')
    tex_lines += texoutput('efficiency', 'muon', 'eta', 'tightIDISO')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'looseIDISO')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'mediumIDISO')
    tex_lines += texoutput('efficiency', 'muon', 'pt', 'tightIDISO')

    change_path(qcdpath)
    tex_lines += "\n" + r"\subsection{Fakerate}"
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'eta', 'tightIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'looseIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'mediumIDISO')
    tex_lines += texoutput('fakerate', 'muon', 'pt', 'tightIDISO')

    # Btag
    change_path(btagpath)
    tex_lines += "\n" + r"\section{Btag}" + "\n" + r"\subsection{Efficiency}"
    tex_lines += texoutput('btagRate', 'jetpuppi', 'eta', 'looseID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'eta', 'mediumID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'eta', 'tightID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'pt', 'looseID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'pt', 'mediumID')
    tex_lines += texoutput('btagRate', 'jetpuppi', 'pt', 'tightID')

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
    change_path(taupath)
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

    change_path(elmupath)
    tex_lines += "\n" + r"\subsection{Tau Electron MisTag Rate}"
    tex_lines += texoutput('elecMistagRate', 'tau', 'eta', 'looseID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'eta', 'mediumID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'eta', 'tightID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'pt', 'looseID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'pt', 'mediumID')
    tex_lines += texoutput('elecMistagRate', 'tau', 'pt', 'tightID')

    change_path(taupath)
    tex_lines += "\n" + r"\subsection{Tau Muon MisTag Rate}"
    tex_lines += texoutput('muonMistagRate', 'tau', 'eta', 'looseID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'eta', 'mediumID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'eta', 'tightID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'pt', 'looseID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'pt', 'mediumID')
    tex_lines += texoutput('muonMistagRate', 'tau', 'pt', 'tightID')

    tex_lines += "\n" + r"\end{document}"
    
    status, basename = getstatusoutput("basename {}".format(parentpath))
    file_name = basename

    with open(printoutdir+'{}.tex'.format(file_name), 'w') as tex_output:
        tex_output.write(tex_lines)

    print("\n {}{}.tex file is created!\n".format(printoutdir, file_name))
    
    print("Creating pdf file... {}{}.pdf".format(printoutdir, file_name))
    
    os.system("pdflatex {}{}.tex".format(printoutdir, file_name))
    os.system("cp {}.pdf {}".format(file_name ,printoutdir))
    os.system("rm {}.aux".format(file_name))
    os.system("rm {}.log".format(file_name))
    os.system("rm {}.nav".format(file_name))
    os.system("rm {}.pdf".format(file_name))
    os.system("rm {}.snm".format(file_name))
    os.system("rm {}.toc".format(file_name))
    os.system("rm met_figure.png")
    
if __name__ == "__main__":
    main()
