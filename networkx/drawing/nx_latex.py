
import networkx as nx
from networkx.drawing.layout import shell_layout,\
    circular_layout,spectral_layout,spring_layout,random_layout


def draw_latex(G, pos=None, with_labels=True, **kwds):
    if pos is None:
        pos=nx.drawing.spring_layout(G) # default to spring layout

    text = ""
    text += figure_prelude()
    text += draw_nodes(G, pos)
    text += draw_edges(G, pos)
    text += epilogue()
    return text

def figure_prelude():
    return r"""
\tikzstyle{node}=[draw, circle,bottom color=black!25, top color =
gray!25,      minimum size=20pt,inner sep=0pt]
\tikzstyle{edge} = [draw,thick,-]
\tikzstyle{weight} = [font=\small]


\begin{figure}
\begin{tikzpicture}[scale=5, auto, swap]
"""
def epilogue():
    return r"""
\end{tikzpicture}
\end{figure}"""

def draw_nodes(G, pos,
                        nodelist=None,
                        node_size=300,
                        node_color='r',
                        node_shape='o',
                        alpha=1.0,
                        cmap=None,
                        vmin=None,
                        vmax=None,
                        ax=None,
                        linewidths=None,
                        **kwds):
    s = ""
    s+=     r"    \foreach \pos/\name in {"+"\n"
    for node, (x,y) in pos.items():
        s+= r"                            {(%f, %f)/%s},"%(x,y,node)+"\n"
    s = s[:-2]+"}\n"

    s +=    r"        \node[node] (\name) at \pos {$\name$};"+"\n"

    return s

def draw_edges(G, pos,
                        edgelist=None,
                        width=1.0,
                        edge_color='k',
                        style='solid',
                        alpha=None,
                        edge_cmap=None,
                        edge_vmin=None,
                        edge_vmax=None,
                        ax=None,
                        arrows=True,
                        **kwds):

    s = ""
    s +=     r"    \foreach \source/ \dest /\weight in{"+"\n"
    for source, dest in G.edges():
        s += "                            %s/%s/1,\n"%(source, dest)
    s = s[:-2]+"}\n"

    s +=     r"         \path[edge] (\source) -- node[weight] {} (\dest);"+"\n"
    return s

def tikz_prelude():
    return r"""
\usepackage{tikz}
\usepackage{verbatim}
\usetikzlibrary{arrows,shapes}

"""

def full_tex_document(G, filename = None, show = True):
    s = r"""
\documentclass{beamer}""" + tikz_prelude() + r"""

\begin{document}
\begin{frame}
""" + draw_latex(G) + r"""
\end{frame}
\end{document}"""
    if not filename:
        return s
    else:
        file = open(filename, 'w')
        file.write(s)
        file.close()
    if show:
        import os
        os.system('pdflatex %s'%filename)
        os.system('evince %s'%(filename.replace('.tex', '.pdf')))


