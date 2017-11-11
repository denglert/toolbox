import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools


c_alignment = "navy"
c_wrongsign = "firebrick"

m_min = 100.0
m_max = 1000.0
m_size = 1.0
alp = 0.6

col_to_label = {
    'mH'                                  : r'$m_{H}$ [GeV]',
    'mHc'                                 : r'$m_{H^{\pm}}$ [GeV]',
    'mA'                                  : r'$m_{A}$ [GeV]',
    'mH_minus_mHc'                        : r'$m_{H} - m_{H^{\pm}}$ [GeV]',
    'mA_minus_mHc'                        : r'$m_{A} - m_{H^{\pm}}$ [GeV]',
    'Z4'                                  : r'$Z_{4}$',
    'Z5'                                  : r'$Z_{5}$',
    'Z7'                                  : r'$Z_{7}$',
    'cba'                                 : r'$\cos(\beta - \alpha)$',
    'tb'                                  : r'$\tan \beta $',
    'xsec_sushi_ggh_A_NNLO'               : r'$\sigma(gg\rightarrow A)$ [pb]',
    'log_xsec_sushi_ggh_A_NNLO'           : r'$\log_{10} \sigma(gg\rightarrow A)$ [pb]',
    'xsec_sushi_ggh_H_NNLO'               : r'$\sigma(gg\rightarrow H)$ [pb]',
    'log_xsec_sushi_ggh_H_NNLO'           : r'$\log_{10} \sigma(gg\rightarrow H)$ [pb]',
    'xsec_sushi_ggh_A_NNLO_x_br_A_Zh'     : r'$\sigma(gg\rightarrow A) \times Br(A \rightarrow Zh)$ [pb]',
    'xsec_sushi_ggh_A_NNLO_x_br_A_ZH'     : r'$\sigma(gg\rightarrow A) \times Br(A \rightarrow ZH)$ [pb]',
    'xsec_sushi_ggh_A_NNLO_x_br_A_tautau' : r'$\sigma(gg\rightarrow A) \times Br(A \rightarrow \tau \tau)$ [pb]',
    'xsec_sushi_ggh_A_NNLO_x_br_A_tt'     : r'$\sigma(gg\rightarrow A) \times Br(A \rightarrow tt)$ [pb]',
    'xsec_sushi_ggh_A_NNLO_x_br_A_bb'     : r'$\sigma(gg\rightarrow A) \times Br(A \rightarrow bb)$ [pb]',
    'xsec_sushi_ggh_H_NNLO_x_br_H_Zh'     : r'$\sigma(gg\rightarrow H) \times Br(H \rightarrow Zh)$ [pb]',
    'xsec_sushi_ggh_H_NNLO_x_br_H_AA'     : r'$\sigma(gg\rightarrow H) \times Br(H \rightarrow AA)$ [pb]',
    'xsec_sushi_ggh_H_NNLO_x_br_H_Zh'     : r'$\sigma(gg\rightarrow H) \times Br(H \rightarrow Zh)$ [pb]',
    'xsec_sushi_ggh_H_NNLO_x_br_H_ZZ'     : r'$\sigma(gg\rightarrow H) \times Br(H \rightarrow ZZ)$ [pb]',
    'xsec_sushi_ggh_H_NNLO_x_br_H_ZA'     : r'$\sigma(gg\rightarrow H) \times Br(H \rightarrow ZA)$ [pb]',
    'xsec_sushi_ggh_H_NNLO_x_br_H_tt'     : r'$\sigma(gg\rightarrow H) \times Br(H \rightarrow tt)$ [pb]',
    'xsec_sushi_ggh_H_NNLO_x_br_H_bb'     : r'$\sigma(gg\rightarrow H) \times Br(H \rightarrow bb)$ [pb]',
    'xsec_sushi_ggh_H_NNLO_x_br_H_tautau' : r'$\sigma(gg\rightarrow H) \times Br(H \rightarrow \tau \tau)$ [pb]',
    'log_xsec_sushi_ggh_H_NNLO_x_br_H_ZA' : r'$\log_{10} \sigma(gg\rightarrow H) \times Br(H \rightarrow ZA)$ [pb]',
    'br_A_Zh'                             : r'$\mathcal{B}r(A \rightarrow Zh)$',
    'br_A_ZH'                             : r'$\mathcal{B}r(A \rightarrow ZH)$',
    'br_A_tautau'                         : r'$\mathcal{B}r(A \rightarrow \tau \tau)$',
    'br_A_ZH'                             : r'$\mathcal{B}r(A \rightarrow ZH)$',
    'br_A_bb'                             : r'$\mathcal{B}r(A \rightarrow bb)$',
    'br_A_tt'                             : r'$\mathcal{B}r(A \rightarrow tt)$',
    'br_A_gaga'                           : r'$\mathcal{B}r(A \rightarrow \gamma \gamma)$',
    'br_H_tautau'                         : r'$\mathcal{B}r(H \rightarrow \tau \tau)$',
    'br_H_Zh'                             : r'$\mathcal{B}r(H \rightarrow Zh)$',
    'br_H_tt'                             : r'$\mathcal{B}r(H \rightarrow tt)$',
    'br_H_bb'                             : r'$\mathcal{B}r(H \rightarrow bb)$',
    'br_H_ZA'                             : r'$\mathcal{B}r(H \rightarrow ZA)$',
    'br_H_AA'                             : r'$\mathcal{B}r(H \rightarrow AA)$',
    'br_H_gaga'                           : r'$\mathcal{B}r(H \rightarrow \gamma \gamma)$',
}

pars = [ 'cba', 'tb', 'mA', 'mH', 'mHc', 'Z7' ]

planes = [ ('cba', 'tb'),
           ('cba', 'mA'), 
           ('mHc', 'mH'),
           ('mHc', 'mA'),
           ('cba', 'Z7'),
           ('tb',  'mHc')
           ]


alpha = 0.1
color_def = 'firebrick'

def plot_on_pars(df):

    pass
#    permutations = itertools.permutations(pars, 2)
#
#    f, a = plt.subplots(ncols=2, nrows=3)
#    a = a.flatten()
#
#    for i, set in enumerate(sets):
#
#        x = set[0]
#        y = set[1]
#
#        df.plot.scatter(x, y, ax=, alpha=alpha, rasterized=True, color=color_def)
        

def plot_par_planes(df, alpha, color):

    f, a = plt.subplots(ncols=2, nrows=3)
    a = a.flatten()

    for i, (x, y) in enumerate(planes):


        df.plot.scatter(x, y, ax=a[i], alpha=alpha, rasterized=True, color=color)
        a[i].set_xlabel( col_to_label[x] )
        a[i].set_ylabel( col_to_label[y] )

    return f, a

def plot_compare_par_planes(df1, df2, alphas, colors, labels):

    f, a = plt.subplots(ncols=2, nrows=3)
    a = a.flatten()

    for i, (x, y) in enumerate(planes):

        if i == 0:
            df1.plot.scatter(x, y, ax=a[i], alpha=alphas[0], rasterized=True, color=colors[0],
                    label=labels[0])
            df2.plot.scatter(x, y, ax=a[i], alpha=alphas[1], rasterized=True, color=colors[1],
                    label=labels[1])
        else:
            df1.plot.scatter(x, y, ax=a[i], alpha=alphas[0], rasterized=True, color=colors[0])
            df2.plot.scatter(x, y, ax=a[i], alpha=alphas[1], rasterized=True, color=colors[1])


        a[i].set_xlabel( col_to_label[x] )
        a[i].set_ylabel( col_to_label[y] )

    return f, a


def scatter_alignment_wrong_sign_xsec_br(df, x, y):
    f, a = plt.subplots(ncols=1, nrows=1)
    al = df.query("k_hdd_type == 'alignment'").plot(x=x, y=y, kind='scatter', c=c_alignment, s=m_size, rasterized=True, alpha=alp, label='Alignment', legend=True, ax=a)
    ws = df.query("k_hdd_type == 'wrongsign'").plot(x=x, y=y, kind='scatter', c=c_wrongsign, s=m_size, rasterized=True, alpha=alp, label='Wrong-sign', legend=True, ax=a)
                
    # - Labels
    a.set_title('2HDM Type II')
    a.set_xlim( 0.0, 1000.0);
    #a.set_ylim( 100, 1000.0);
    a.set_xlabel( col_to_label[x] );
    a.set_ylabel( col_to_label[y] );
    a.set_yscale("log")

    return f, a

def scatter_xsec_br_channels(df):
    f, a = plt.subplots(ncols=2, nrows=3)
    a = a.flatten()

    channels = [('mA', 'xsec_sushi_ggh_A_NNLO_x_br_A_Zh'),
                #('mA', 'xsec_sushi_ggh_A_NNLO_x_br_A_ZH'),
                ('mA', 'xsec_sushi_ggh_A_NNLO_x_br_A_tautau'),
                ('mA', 'xsec_sushi_ggh_A_NNLO_x_br_A_bb'),
                ('mH', 'xsec_sushi_ggh_H_NNLO_x_br_H_ZA'),
                ('mH', 'xsec_sushi_ggh_H_NNLO_x_br_H_tt'),
                ('mH', 'xsec_sushi_ggh_H_NNLO_x_br_H_bb')
                ]
    

    for ich, (xlab, ylab) in enumerate(channels):
        df.plot.scatter(x=xlab, y=ylab, rasterized=True, alpha=1.0, ax=a[ich])

        a[ich].set_yscale("log")
        #a[ich].set_xlim(m_min, m_max)
        a[ich].set_xlabel( col_to_label[xlab] )
        a[ich].set_ylabel( col_to_label[ylab] )

    return f,a
