
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import os
import glob

import numpy
import matplotlib.pyplot as plt

import clawpack.visclaw.colormaps as colormaps
import clawpack.visclaw.geoplot as geoplot
import clawpack.visclaw.gaugetools as gaugetools


import clawpack.clawutil.data as data
import clawpack.geoclaw.data
import clawpack.geoclaw.dtopotools as dtopotools

# Grab dart data
#dart_data_path = os.path.expandvars("../tohoku2011-paper1/dart/")
#dart_data_path = "/h2/pkjain/Desktop/Pushkar/clawpack/geoclaw/examples/tsunami/tohoku2011-paper1/dart"
dart_data_path = "/h2/pkjain/Desktop/Pushkar/clawpack/geoclaw/examples/tsunami/tohoku-pc/dart"

dartdata = {}
for gaugeno in [21401, 21413, 21414, 21415,  21418, 21419, 46411, 51407, 52402]:
    files = glob.glob(os.path.join(dart_data_path, '%s*_notide.txt' % gaugeno))
    if len(files) != 1:
        print "*** Warning: found %s files for gauge number %s" \
                   % (len(files),gaugeno)
        #raise Exception("*** found %s files for gauge number %s" \
        #           % (len(files),gaugeno)   )
    try:
        fname = files[0]
        dartdata[gaugeno] = numpy.loadtxt(fname)
    except:
        pass

tlimits = {}
tlimits[21401] = [0,28800]
tlimits[21413] = [0,28800]
tlimits[21414] = [8000,28800]
tlimits[21415] = [7200,28800]
tlimits[21416] = [0,14400]
tlimits[21418] = [0,28800]
tlimits[21419] = [0,28800]
tlimits[46411] = [5000,28800]
tlimits[51407] = [0,28800]
tlimits[52402] = [0,28800]

#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 

    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'ascii'


    # Import useful run data
    clawdata = data.ClawInputData(2)
    clawdata.read(os.path.join(plotdata.outdir, 'claw.data'))
    dtopo_data = clawpack.geoclaw.data.DTopoData()
    dtopo_data.read(os.path.join(plotdata.outdir, 'dtopo.data'))
    friction_data = clawpack.geoclaw.data.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir, 'friction.data'))

    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos=[21401, 21413, 21414, 21415, 21418, 21419, 46411, 51407, 52402], format_string='ko', add_labels=True)
    

    #-----------------------------------------
    # Figure for pcolor plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='full domain', figno=0)

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True

    def fixup(current_data):
        import pylab
        #addgauges(current_data)
        t = current_data.t
        t = t / 3600.  # hours
        pylab.title('Surface at %4.2f hours' % t, fontsize=20)
        pylab.xticks(fontsize=15)
        pylab.yticks(fontsize=15)
        #pylab.plot([205],[19.7],'wo',markersize=10)
        #pylab.text(200,22,'Hilo',color='k',fontsize=25)
        # pylab.plot([139.7],[35.6],'yo',markersize=5)
        # pylab.text(133.3,36.5,'Sendai',color='y',fontsize=15)
        addgauges(current_data)

    plotaxes.afteraxes = fixup
    plotaxes.xlimits = [clawdata.lower[0], clawdata.upper[0]]
    plotaxes.ylimits = [clawdata.lower[1], clawdata.upper[1]]

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    plotitem.pcolor_cmin = -0.1
    plotitem.pcolor_cmax = 0.1
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 1

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    #plotaxes.xlimits = [138,155]
    #plotaxes.ylimits = [25,42]

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = numpy.linspace(-5000,-100,6)
    plotitem.amr_contour_colors = ['y']  # color on each level
    plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [1,0,0]  
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


    #-----------------------------------------
    # Figure for zoom plot
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Zoom', figno=1)
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.xlimits = [140,146]
    plotaxes.ylimits = [35,41]


    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = colormaps.blue_white_red
    plotitem.pcolor_cmin = -.1
    plotitem.pcolor_cmax = 0.1
    plotitem.add_colorbar = True
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0

    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    #plotitem.show = False
    plotitem.plot_var = geoplot.surface
    plotitem.contour_levels = numpy.linspace(-13,13,14)
    plotitem.amr_contour_colors = ['k']  # color on each level
    #plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,1]  
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0

    # add contour lines of bathy if desired:
    plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.contour_levels = numpy.linspace(-6,6,13)
    plotitem.amr_contour_colors = ['k']  # color on each level
    #plotitem.kwargs = {'linestyles':'solid','linewidths':2}
    plotitem.amr_contour_show = [0,0,0,1]  
    plotitem.celledges_show = 0
    plotitem.patchedges_show = 0


    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'
    plotitem.kwargs = {'linewidth':2}

    if 0:
        # Plot comparison as red curve:
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.show = (dart_data_path is not None)
        # plotitem.outdir = dart_data_path
        plotitem.plot_var = 3
        plotitem.plotstyle = 'r-'
        plotitem.kwargs = {'linewidth':2}

    # Plot topo as green curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = False

    def gaugetopo(current_data):
        q = current_data.q
        h = q[:,0]
        eta = q[:,3]
        topo = eta - h
        return topo
        
    plotitem.plot_var = gaugetopo
    plotitem.plotstyle = 'g-'

    def add_zeroline(current_data):
        t = current_data.t
        plt.plot([0,10800],[0,0],'k')

    def plot_dart(current_data):
        import pylab
        gaugeno = current_data.gaugeno
        try:
            dart = dartdata[gaugeno]
            pylab.plot(dart[:,0],dart[:,1],'r')    
            pylab.legend(['GeoClaw','Obs'])
        except:
            if dart_data_path is None:
                pylab.legend(['GeoClaw'])
            else:
                pylab.legend(['GeoClaw','dart_data_path'])
        if 0:
            add_zeroline(current_data)
        try:
            pylab.xlim(tlimits[gaugeno])
        except:
            pass


    plotaxes.afteraxes = plot_dart


    # =====================
    #  Plot Friction Field
    # =====================
    plotfigure = plotdata.new_plotfigure('Friction')
    plotfigure.show = friction_data.variable_friction and True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = r"Manning's $N$ Coefficient"
    plotaxes.scaled = True
    plotaxes.afteraxes = addgauges

    plotitem = plotaxes.new_plotitem(name='friction',plot_type='2d_pcolor')
    plotitem.plot_var = lambda cd: cd.aux[3,:,:]
    plotitem.pcolor_cmap = plt.get_cmap('YlOrRd')
    plotitem.colorbar_shrink = 0.9
    plotitem.pcolor_cmin = 0.01
    plotitem.pcolor_cmax = 0.1   
    plotitem.add_colorbar = True
    plotitem.colorbar_label = "Manning's-$n$ Coefficient"
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [0,0,0,0,0,0,0]
    plotitem.colorbar_label = r"$n$"

    # ==========================
    #  Plot Fault Configuration
    # ==========================
    def plot_dtopo(plotdata):

        print "Creating html for other figures."
        with open('fault.html', 'w') as out_html:
            out_html.write("<html>\n")
            out_html.write("    <header>\n")
            out_html.write("        <title>Fault Specification</title>\n")
            out_html.write("    </header>\n")
            out_html.write("    <body>\n")
            out_html.write("        <h1>Fault Specification</h1>\n")
            out_html.write("        <img src='fault.png'>\n")
            out_html.write("        <img src='uplift.png'>\n")
            out_html.write("    </body>\n")
            out_html.write("</html>")

        # Need to save this in the run_faults section, cannot do yet
        # fault = dtopotools.Fault(path="./fault_params.txt")
        # fig = plt.figure()
        # axes = fig.add_subplot(1, 1, 1)
        # fault.plot_subfaults(axes, slip_color=True, cmin_slip=0.0, 
                                                    # cmax_slip=120.0)
        # fig.savefig('fault.png')

        if 0:
            dtopo = dtopotools.DTopography(path=dtopo_data.dtopofiles[0][3])
            fig = plt.figure()
            axes = fig.add_subplot(1, 1, 1)
            dtopo.plot_dZ_colors(t=1.0, axes=axes)
            fig.savefig("uplift.png")


    plotfigure = plotdata.new_otherfigure("Fault", "fault.html")
    plotfigure.makefig = plot_dtopo


    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

