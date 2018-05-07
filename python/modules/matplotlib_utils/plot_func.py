#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import itertools
from matplotlib      import ticker, colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage.filters import gaussian_filter
from scipy.interpolate import griddata as griddata_scipy
from matplotlib.mlab import griddata as griddata_mlab


def pandas_pixel( df,
                  x_col,
                  y_col,
                  z_col,
                  **kwargs
                  ):

    from mpl_toolkits.axes_grid1 import make_axes_locatable

    # - Create new figure and axis if not passed as keyword.
    if 'ax' not in kwargs:
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
    else:
        ax = kwargs['ax']
    
    sorted = df.sort_values( by=[y_col, x_col], ascending=[False,True] )
    array  = np.array(sorted[z_col])

    # - Get the number of bins in along each dimension
    nrows = df[y_col].nunique()
    ncols = df[x_col].nunique()

    # - Reshape the array to match the image layout
    grid = np.resize(array, (nrows, ncols))

    if 'cb_colormap' in kwargs:
        im = ax.imshow(grid, interpolation='nearest', cmap=kwargs['cb_colormap'])
    else:
        im = ax.imshow(grid, interpolation='nearest')

    if 'cb_range_min' in kwargs and 'cb_range_max' in kwargs:
        im.set_clim(vmin=kwargs['cb_range_min'], vmax=kwargs['cb_range_max'])

    # - Position and rescale colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.15)

    cb = plt.colorbar(im, ax=ax, cax=cax)

    # - Ticks
    if 'n_xticks' in kwargs:
        ax.set_xticks( np.linspace(0, ncols, kwargs['n_xticks']))

    if 'xtick_min' in kwargs and 'xtick_max' in kwargs and 'n_xticks' in kwargs:
        ax.set_xticklabels( np.linspace(kwargs['xtick_min'][0], kwargs['xtick_max'][1], kwargs['n_xticks'] ) )

    if 'ytick_min' in kwargs and 'ytick_max' in kwargs and 'n_yticks' in kwargs:
        ax.set_yticks( np.linspace(nrows, 0, kwargs['n_yticks']) )
        ax.set_yticklabels( np.linspace(kwargs['ytick_min'][0], kwargs['ytick_max'][1], kwargs['n_yticks'] ) )

    # - Labels
    if 'cb_label' in kwargs:
        cb.set_label( kwargs['cb_label'] )

    if 'title' in kwargs:
        ax.set_title( kwargs['title'] )

    if 'xlabel' in kwargs:
        ax.set_xlabel( kwargs['xlabel'] )

    if 'ylabel' in kwargs:
        ax.set_ylabel( kwargs['ylabel'] )

    if 'ax' not in kwargs:
        return fig, ax


def create_griddata(x, y, z, x_num=100, y_num=100,  interp='cubic', backend='scipy',
        gaussian_filter_sigma=None, reshape=None):

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    xi = np.linspace( xmin,  xmax, x_num, endpoint=True )
    yi = np.linspace( ymin,  ymax, y_num, endpoint=True )

    if (gaussian_filter_sigma is not None) and (reshape is not None):
        z = z.reshape(reshape)
        z = gaussian_filter(z, gaussian_filter_sigma)
        z = z.flatten()
    
    if backend == 'scipy':
        
        # - Original points
        xy_points = np.array(list(zip(x,y)))

        # - Interpolating at points
        Xi,Yi = np.meshgrid(xi,yi)

        zi = griddata_scipy(xy_points, z, (Xi, Yi), method=interp)
    elif backend == 'mlab':
        zi = griddata_mlab(x, y, z, xi, yi, interp=interp)
    else:
        print("Unknown backend. Available backends are`scipy` and `mlab`.")
        exit()
    

    return xi, yi, zi


def pandas_contour(df, x_col, y_col, z_col,
                   interp='cubic', x_num=100, y_num=100,
                   contour_kwargs={},
                   colorbar_kwargs=False,
                   griddata_kwargs={},
                   clabel_kwargs={},
                   *args,
                   **kwargs):

    isColorbar = False

    # - Create new figure and axis if not passed as keyword.
    if 'ax' not in kwargs:
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
    else:
        ax = kwargs['ax']

    x, y, z = df[x_col], df[y_col], df[z_col]

    if bool(griddata_kwargs):
        xi, yi, zi = create_griddata(x, y, z, **griddata_kwargs)
    else:
        dfmesh = df.pivot(x_col, y_col, z_col)
        xi, yi, zi = dfmesh.index.values, dfmesh.columns.values, dfmesh.values.T

#   xi, yi, zi = create_griddata(x, y, z, **griddata_kwargs)
#   xi, yi, zi = create_griddata(x, y, z, interp=interp, x_num=x_num, y_num=y_num,
#               gaussian_filter_sigma=gaussian_filter_sigma)

    if kwargs.get('resize'):
        xi, yi, zi = np.resize(x, kwargs['resize']), np.resize(y, kwargs['resize']), np.resize(z, kwargs['resize'])

    cs = plt.contour(xi, yi, zi, **contour_kwargs)


    if clabel_kwargs: 
        plt.clabel(cs, **clabel_kwargs)
    
    #if 'cb_logscale' in kwargs:
    #    cs = plt.contourf(xi, yi, zi, kwargs['cb_levels'], norm=colors.LogNorm(),
    #            cmap=kwargs['cb_colormap'])
    #else:
    #    if 'cb_levels' in kwargs and kwargs['cb_levels'] == 'auto':
    #        cs = plt.contourf(xi, yi, zi, cmap=kwargs['cb_colormap'], extend='both' )
    #    else:
    #       cs = plt.contourf(xi, yi, zi)

    if 'under' in kwargs:
        cs.cmap.set_over(kwargs['under'])
    if 'over' in kwargs:
        cs.cmap.set_under(kwargs['over'])

    if not colorbar_kwargs == False:
        cb = plt.colorbar(cs, ax=ax, **colorbar_kwargs)
        isColorbar = True

    if 'cb_ticks' in kwargs:
    	cb.set_ticks     ( kwargs['cb_ticks'] )
    	cb.set_ticklabels( kwargs['cb_ticklabels'] )
    
    plt.locator_params(axis='y', nbins=11)
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.12)
    
    # - Labels
    if 'cb_label' in kwargs:
        cb.set_label( kwargs['cb_label'] )
    if 'title' in kwargs:
        fig.suptitle( kwargs['title'], fontsize=14)
    if 'xlabel' in kwargs:
        plt.xlabel(   kwargs['xlabel'], labelpad=10, fontsize=18)
    if 'ylabel' in kwargs:
        plt.ylabel(   kwargs['ylabel'], labelpad=10, fontsize=18)


    return_list = []

    if 'ax' not in kwargs:
        return_list.append(fig)
        return_list.append(ax)

    if isColorbar:
        return_list.append(cb)

    return_tuple = tuple(return_list)

    if len(return_tuple) == 1:
        return return_tuple[0]
    else:
        return return_tuple

def pandas_contourf(df, x_col, y_col, z_col,
                   griddata_kwargs={},
                   contourf_kwargs={},
                   colorbar_kwargs=False,
                   **kwargs):

    isColorbar = False

    if 'ax' not in kwargs:
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
    else:
        ax = kwargs['ax']

    x, y, z = df[x_col], df[y_col], df[z_col]

    if bool(griddata_kwargs):
        xi, yi, zi = create_griddata(x, y, z, **griddata_kwargs)
    else:
        dfmesh = df.pivot(x_col, y_col, z_col)
        xi, yi, zi = dfmesh.index.values, dfmesh.columns.values, dfmesh.values.T
    
    cs = plt.contourf(xi, yi, zi, **contourf_kwargs)

    # - https://stackoverflow.com/questions/43150687/colorbar-limits-are-not-respecting-set-vmin-vmax-in-plt-contourf-how-can-i-more
    if 'clim_min' in kwargs:
        m = plt.cm.ScalarMappable(cmap=kwargs['clim_cmap'])
        m.set_array(zi)
        m.set_clim(kwargs['clim_min'], kwargs['clim_max'])
        cb = plt.colorbar(m, boundaries=np.arange(kwargs['clim_min'], kwargs['clim_max'],
            kwargs['clim_space']))
        isColorbar = True

    if not colorbar_kwargs == False:
        cb = plt.colorbar(cs, ax=ax, **colorbar_kwargs)
        isColorbar = True

    return_list = []

    if 'ax' not in kwargs:
        return_list.append(fig)
        return_list.append(ax)

    if isColorbar:
        return_list.append(cb)

    return_tuple = tuple(return_list)

    if len(return_tuple) == 1:
        return return_tuple[0]
    else:
        return return_tuple

def plot_map( plotSettings, x, y, z ):

    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)
    
    xi = np.linspace( plotSettings['xrange'][0],  plotSettings['xrange'][1], 100, endpoint=True )
    yi = np.linspace( plotSettings['yrange'][0],  plotSettings['yrange'][1], 100, endpoint=True )
    zi = griddata_mlab(x, y, z, xi, yi, interp='linear')
    
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
