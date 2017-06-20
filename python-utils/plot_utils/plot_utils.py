import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from matplotlib      import ticker, colors
import os
#from __future__ import division

#plt.switch_backend('PDF')

def pandas_pixel( ps, df, x_col, y_col, z_col ):

    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    sorted = df.sort_values( by=[y_col, x_col], ascending=[False,True] )
    array  = np.array( sorted[z_col] )

    # - Get the number of bins in along each dimension
    nrows = df[y_col].nunique()
    ncols = df[x_col].nunique()

    # - Reshape the array to match the image layout
    grid = array.reshape((nrows, ncols))

    # - Create figures
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True )
    im = ax.imshow(grid, interpolation='nearest', cmap=ps['cb_colormap'])

    if 'cb_range' in ps:
        im.set_clim(vmin=ps['cb_range'][0], vmax=ps['cb_range'][1])

    # - Position and rescale colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.15)

    cb = plt.colorbar(im, ax=ax, cax=cax)

    # - Ticks
    ax.set_xticks( np.linspace(0, ncols, ps['n_xticks']))
    ax.set_xticklabels( np.linspace(ps['xrange'][0], ps['xrange'][1], ps['n_xticks'] ) )
    ax.set_yticks( np.linspace(nrows, 0, ps['n_yticks']) )
    ax.set_yticklabels( np.linspace(ps['yrange'][0], ps['yrange'][1], ps['n_yticks'] ) )

    # - Labels
    cb.set_label( ps['cb_label'] )
    ax.set_title( ps['title'] )
    ax.set_xlabel( ps['xlabel'] )
    ax.set_ylabel( ps['ylabel'] )

    return fig, ax

def pandas_contour( plotSettings, df, x_col, y_col, z_col ):

    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)

    x = df[x_col]
    y = df[y_col]
    z = df[z_col]
    
    xi = np.linspace( plotSettings['xrange'][0],  plotSettings['xrange'][1], 100, endpoint=True )
    yi = np.linspace( plotSettings['yrange'][0],  plotSettings['yrange'][1], 100, endpoint=True )
    zi = griddata(x, y, z, xi, yi, interp='linear')

    if 'contour_levels' in plotSettings:
        ### --- Contours --- ###
        if 'contour_colormap' in plotSettings:
            cs = plt.contour(xi, yi, zi, plotSettings['contour_levels'],
                    cmap=plotSettings['contour_colormap'], extend='both' )
        else:
            cs = plt.contour(xi, yi, zi, plotSettings['contour_levels'] )


    plt.clabel(cs, inline=1)
	
    if 'cb_logscale' in plotSettings:
        cs = plt.contourf(xi, yi, zi, plotSettings['cb_levels'], norm=colors.LogNorm(),
                cmap=plotSettings['cb_colormap'])
    else:
        if plotSettings['cb_levels'] == 'auto':
            cs = plt.contourf(xi, yi, zi, cmap=plotSettings['cb_colormap'], extend='both' )
        else:
            cs = plt.contourf(xi, yi, zi, plotSettings['cb_levels'],
                    cmap=plotSettings['cb_colormap'], extend='both' )

    if 'under' in plotSettings:
        cs.cmap.set_over('red')
        cs.cmap.set_under('navy')

    CB = plt.colorbar(cs, ax=ax, extend='max')
	
    if 'cb_ticks' in plotSettings:
    	CB.set_ticks     ( plotSettings['cb_ticks'] )
    	CB.set_ticklabels( plotSettings['cb_ticklabels'] )
    
    plt.locator_params(axis='y', nbins=11)
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.12)
    
    # - Labels
    CB.set_label( plotSettings['cb_label'] )
    fig.suptitle( plotSettings['title'], fontsize=14)
    plt.xlabel(   plotSettings['xlabel'], labelpad=10, fontsize=18)
    plt.ylabel(   plotSettings['ylabel'], labelpad=10, fontsize=18)

    return fig, ax


def plot_map( plotSettings, x, y, z ):

    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
#    fig = plt.figure()
    
    xi = np.linspace( plotSettings['xrange'][0],  plotSettings['xrange'][1], 100, endpoint=True )
    yi = np.linspace( plotSettings['yrange'][0],  plotSettings['yrange'][1], 100, endpoint=True )
    zi = griddata(x, y, z, xi, yi, interp='linear')
    
    ### --- Contours --- ###
    if 'contour_colormap' in plotSettings:
        cs = plt.contour(xi, yi, zi, plotSettings['contour_levels'], cmap=plotSettings['contour_colormap'] )
    else:
        cs = plt.contour(xi, yi, zi, plotSettings['contour_levels'] )


    plt.clabel(cs, inline=1, fontsize=10)
	
    if 'cb_logscale' in plotSettings:
        cs = plt.contourf(xi, yi, zi, plotSettings['cb_levels'], norm=colors.LogNorm(), cmap=plotSettings['cb_colormap'])
    else:
        if plotSettings['cb_levels'] == 'auto':
            cs = plt.contourf(xi, yi, zi, cmap=plotSettings['cb_colormap'] )
        else:
            cs = plt.contourf(xi, yi, zi, plotSettings['cb_levels'], cmap=plotSettings['cb_colormap'] )

#    CB = plt.colorbar()
    CB = plt.colorbar(cs, ax=ax, extend='max')
	
    if 'cb_ticks' in plotSettings:
    	CB.set_ticks     ( plotSettings['cb_ticks'] )
    	CB.set_ticklabels( plotSettings['cb_ticklabels'] )
    
    plt.locator_params(axis='y', nbins=11)
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.12)
    
    # - Labels
    CB.set_label( plotSettings['cb_label'] )
    fig.suptitle( plotSettings['title'], fontsize=14)
    plt.xlabel(   plotSettings['xlabel'], labelpad=10, fontsize=18)
    plt.ylabel(   plotSettings['ylabel'], labelpad=10, fontsize=18)
    
    plt.show(  )
  #  plt.savefig( plotSettings['figname'] )
  #  plt.clf()


#####

def make_plots(data, folder, tag):


    os.makedirs( './results/{}'.format(folder), exist_ok=True )

    x = data['mA']
    y = data['gt'] 
    S = data['PS'][0]
    s = data['rs'][0]
    
    #################################################################
    
    z = data['xsec']
    
    #log_zmin  = np.log10( z.min() )
    log_zmin  = np.log10( 0.01 )
    cb_levels = np.logspace( log_zmin, 1, 20)

    plotSettings = {
    'figname'          : './results/{}/{}_xsec.pdf'.format( folder, tag),
    'title'            : r'MWTC - $\sigma( p p \rightarrow Z h)$' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'cb_label'         : r'$\sigma $ [pb]',
    'cb_levels'        : cb_levels,
    'cb_logscale'      : True,
    'contour_levels'   : [0.5, 1.0, 2.0],
    'cb_ticks'         : [ 0.01  , 0.1,   0.5,  1.0, 5.0,  10],
    'cb_ticklabels'    : ['0.01' ,'0.1', '0.5', '1','5','10'],
    'contour_colormap' : plt.cm.Greens,
    'cb_colormap'      : plt.cm.gnuplot
                   }
    
    plot_map( plotSettings, x, y, z )
    
    #################################################################
    
    z = data['M1N']
    
    cb_levels = np.linspace( 300, 2700, 25)
    
    plotSettings = {
    'figname'          : './results/{}/{}_M1N.pdf'.format( folder, tag) ,
    'title'            : r'MWTC,  $R^{0}_{1}$ mass' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$m_{R^{0}_1}$ [GeV]',
    'cb_levels'        : cb_levels,
    'contour_levels'   : [1000.0, 1500.0, 2000.0],
    'contour_colormap' : plt.cm.Greens_r,
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )
    
    #################################################################
    
    z = data['M2N']
    
    cb_levels = np.linspace( 300, 2700, 25)
    
    plotSettings = {
    'figname'          : './results/{}/{}_M2N.pdf'.format( folder, tag) ,
    'title'            : r'MWTC,  $R^{0}_{2}$ mass' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$m_{R^{0}_1}$ [GeV]',
    'cb_levels'        : cb_levels,
    'contour_levels'   : [1000.0, 1500.0, 2000.0],
    'contour_colormap' : plt.cm.Greens_r,
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )
    
    
    #################################################################
    
    z = data['M2N']-data['M1N']
    
    plotSettings = {
    'figname'          : './results/{}/{}_dMN.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $R^{0}_{2} - R^{0}_1$ mass difference' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$m_{R^{0}_{2}} - m_{R^{0}_1}$ [GeV]',
    'cb_levels'        : 'auto',
    'contour_levels'   : [50.0, 100.0, 500.0],
    'contour_colormap' : plt.cm.Greens_r,
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )
    
    #################################################################
    
    z = data['M2C']-data['M1C']
    
    plotSettings = {
    'figname'        : './results/{}/{}_dMC.pdf'.format( folder, tag) ,
    'title'          : r'MWTC, $R^{\pm}_{2} - R^{\pm}_1$ mass difference' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'         : [ 250.0, 2050.0],
    'yrange'         : [ 0.5, 9.5 ],
    'xlabel'         : r'$m_{A}$ [GeV]',
    'ylabel'         : r'$\widetilde{g}$',
    'cb_label'       : r'$m_{R^{\pm}_{2}} - m_{R^{\pm}_1}$ [GeV]',
    'cb_levels'      : 'auto',
    'contour_levels' : [0.5, 1.0, 2.0],
    'cb_colormap'    : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )
    
    #################################################################
#    
#    z = data['w1N']
#    
#    plotSettings = {
#    'figname'          : './results/{}/{}_Gamma_R1N.pdf'.format( folder, tag) ,
#    'title'            : r'MWTC, $\Gamma_{R^{0}_{1}}$' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
#    'xrange'           : [ 250.0, 2050.0],
#    'yrange'           : [ 0.5, 9.5 ],
#    'xlabel'           : r'$m_{A}$ [GeV]',
#    'ylabel'           : r'$\widetilde{g}$',
#    'cb_label'         : r'$\Gamma_{R^{0}_{1}}$ [GeV]',
#    'cb_levels'        : 'auto',
#    'contour_levels'   : [0.5, 1.0, 2.0],
#    'contour_colormap' : plt.cm.Greens,
#    'cb_colormap'      : plt.cm.Blues
#                   }
#    
#    plot_map( plotSettings, x, y, z )
#    
#    #################################################################
#    
#    z = data['w2N']
#    
#    log_zmin  = np.log10( z.min() )
#    log_zmax  = np.log10( z.max() )
#    cb_levels = np.logspace( log_zmin, log_zmax, 20 )
#    
#    plotSettings = {
#    'figname'          : './results/{}/{}_Gamma_R2N.pdf'.format( folder, tag) ,
#    'title'            : r'MWTC, $\Gamma_{R^{0}_{2}}$' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
#    'xrange'           : [ 250.0, 2050.0],
#    'yrange'           : [ 0.5, 9.5 ],
#    'xlabel'           : r'$m_{A}$ [GeV]',
#    'ylabel'           : r'$\widetilde{g}$',
#    'cb_label'         : r'$\Gamma_{R^{0}_{2}}$ [GeV]',
#    'cb_levels'        : cb_levels,
#    'cb_logscale'      : True,
#    'contour_levels'   : [10.0, 50.0, 100.0],
#    'contour_colormap' : plt.cm.Greens,
#    'cb_colormap'      : plt.cm.Blues,
#    'cb_ticks'         : [  1.0   ,  10.0,    100.0,    1000.0  ],
#    'cb_ticklabels'    : [ '1.0'  , '10.0',  '100.0',  '1000.0' ]
#                   }
#    
#    plot_map( plotSettings, x, y, z )
#    
#    
    #################################################################
    
    z = (data['M2N']-data['M1N']) / ( data['w1N'] + data['w2N'] )
    
    plotSettings = {
    'figname'          : './results/{}/{}_dMN_div_Gamma.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $R^{0}_{2} - R^{0}_1$ mass degeneracy' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$(m_{R^{0}_{2}} - m_{R^{0}_1})/(\Gamma_{R^{0}_{1}} +  \Gamma_{R^{0}_2} )$',
    'cb_levels'        : 'auto',
    'contour_levels'   : [0.5, 1.0, 2.0],
    'contour_colormap' : plt.cm.Greens,
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )
    
    #################################################################
    
    z = (data['M2C']-data['M1C']) / ( data['w1C'] + data['w2C'] )
    
    plotSettings = {
    'figname'          : './results/{}/{}_dMC_div_Gamma.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $R^{\pm}_{2} - R^{\pm}_1$ mass degeneracy' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$(m_{R^{\pm}_{2}} - m_{R^{\pm}_1})/(\Gamma_{R^{\pm}_{1}} +  \Gamma_{R^{\pm}_2} )$',
    'cb_levels'        : 'auto',
    'contour_levels'   : [0.5, 1.0, 2.0],
    'contour_colormap' : plt.cm.Greens,
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )
    
    #################################################################
    
    z = (data['M1C']-data['M1N'])
    
    plotSettings = {
    'figname'          : './results/{}/{}_dM1CN.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $R^{\pm}_{1} - R^{0}_1$ mass difference' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$m_{R^{\pm}_{1}} - m_{R^{0}_1}$',
    'cb_levels'        : 'auto',
    'contour_levels'   : [-10.0, -5.0, -2.0],
    'contour_colormap' : plt.cm.Greens_r,
    'cb_colormap'      : plt.cm.Blues_r
                   }
    
    plot_map( plotSettings, x, y, z )
    
    #################################################################
    
    z = (data['M2C']-data['M2N'])
    
    plotSettings = {
    'figname'          : './results/{}/{}_dM2CN.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $R^{\pm}_{2} - R^{0}_2$ mass difference' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$m_{R^{\pm}_{2}} - m_{R^{0}_2}$',
    'cb_levels'        : 'auto',
    'contour_colormap' : plt.cm.Greens_r,
    'contour_levels'   : [-2.0,  -1.0],
    'cb_colormap'      : plt.cm.Blues_r
                   }
    
    plot_map( plotSettings, x, y, z )

    #################################################################
    
    z = (data['w1N'])

    cb_levels = np.logspace( 0, 4, 20)
    
    plotSettings = {
    'figname'          : './results/{}/{}_Gamma_R1N.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $\Gamma_{R^{0}_{1}}$' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$\Gamma_{R^{0}_{1}}$ [GeV]',
    'cb_levels'        : cb_levels,
    'cb_ticks'         : [ 10.0,  100.0 ,  1000.0,    10000.0],
    'cb_ticklabels'    : ['10.0', '100.0', '1000.0', '10000.0'],
    'cb_logscale'      : True,
    'contour_colormap' : plt.cm.Greens_r,
    'contour_levels'   : [ 100.0, 1000.0],
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )

    #################################################################
    
    z = (data['w2N'])

    cb_levels = np.logspace( 0, 4, 20)
    
    plotSettings = {
    'figname'          : './results/{}/{}_Gamma_R2N.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $\Gamma_{R^{0}_{2}}$' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$\Gamma_{R^{0}_{2}}$ [GeV]',
    'cb_levels'        : cb_levels,
    'cb_ticks'         : [ 10.0,  100.0 ,  1000.0,    10000.0],
    'cb_ticklabels'    : ['10.0', '100.0', '1000.0', '10000.0'],
    'cb_logscale'      : True,
    'contour_colormap' : plt.cm.Greens_r,
    'contour_levels'   : [ 1.0, 10.0, 100.0, 1000.0],
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )


    #################################################################
    
    z = (data['M1N']/data['w1N'])

    cb_levels = np.logspace( 0, 4, 20)

    
    plotSettings = {
    'figname'          : './results/{}/{}_M1N_div_Gamma.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $m_{R^{0}_{1}} / \Gamma_{R^{0}_{1}}$' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$m_{R^{0}_{1}} / \Gamma_{R^{0}_{1}}$',
    'cb_levels'        : cb_levels,
    'cb_ticks'         : [  1.0,  10.0,  100.0 ,  1000.0,    10000.0],
    'cb_ticklabels'    : [ '1.0', '10.0', '100.0', '1000.0', '10000.0'],
    'cb_logscale'      : True,
    'contour_colormap' : plt.cm.Greens_r,
    'contour_levels'   : [ 1.0, 10.0, 100.0, 1000.0],
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )

    #################################################################
    
    z = (data['M2N']/data['w2N'])

    cb_levels = np.logspace( 0, 4, 20)

#    print('z.min():', z.min())
#    print('z.max():', z.max())
#    print('log_zmin():', log_zmin)
#    print('log_zmax():', log_zmax)
#    print('cb_levels', cb_levels)

    
    plotSettings = {
    'figname'          : './results/{}/{}_M2N_div_Gamma.pdf'.format( folder, tag) ,
    'title'            : r'MWTC, $m_{R^{0}_{2}} / \Gamma_{R^{0}_{2}}$' + '\n' + r'S = {:.3f}, s = {:.1f}'.format(S, s),
    'xrange'           : [ 250.0, 2050.0],
    'yrange'           : [ 0.5, 9.5 ],
    'xlabel'           : r'$m_{A}$ [GeV]',
    'ylabel'           : r'$\widetilde{g}$',
    'cb_label'         : r'$m_{R^{0}_{2}} / \Gamma_{R^{0}_{2}}$',
    'cb_levels'        : cb_levels,
    'cb_ticks'         : [  1.0,  10.0,  100.0 ,  1000.0,    10000.0],
    'cb_ticklabels'    : [ '1.0', '10.0', '100.0', '1000.0', '10000.0'],
    'cb_logscale'      : True,
    'contour_colormap' : plt.cm.Greens_r,
    'contour_levels'   : [ 1.0, 10.0, 100.0, 1000.0],
    'cb_colormap'      : plt.cm.Blues
                   }
    
    plot_map( plotSettings, x, y, z )



def trapezoid(x, b1, b2, t1, t2):
    if x < b1 or x > b2:
        y = 0.0

    if x >= b1 and x < t1:
        y = (x-b1)/(t1-b1)

    if x >= t1 and x <= t2:
        y = 1.0

    if x > t2 and x <= b2:
        y = -(x-t2)/(b2-t2) + 1.0

    return y



def grayify_cmap(cmap):
	# - Original source:
	# - https://jakevdp.github.io/blog/2014/10/16/how-bad-is-your-colormap/
    """Return a grayscale version of the colormap"""
    cmap = plt.cm.get_cmap(cmap)
    colors = cmap(np.arange(cmap.N))
    
    # convert RGBA to perceived greyscale luminance
    # cf. http://alienryderflex.com/hsp.html
    RGB_weight = [0.299, 0.587, 0.114]
    luminance = np.sqrt(np.dot(colors[:, :3] ** 2, RGB_weight))
    colors[:, :3] = luminance[:, np.newaxis]
    
    return cmap.from_list(cmap.name + "_grayscale", colors, cmap.N)

def show_colormap(cmap):
    im = np.outer(np.ones(10), np.arange(100))
    fig, ax = plt.subplots(2, figsize=(6, 1.5),
                           subplot_kw=dict(xticks=[], yticks=[]))
    fig.subplots_adjust(hspace=0.1)
    ax[0].imshow(im, cmap=cmap)
    ax[1].imshow(im, cmap=grayify_cmap(cmap))
