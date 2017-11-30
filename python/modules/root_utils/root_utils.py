import sys
sys.path.append('/home/de3u14/lib/build/hep/ROOT/build/root_v5.34.36/lib/root')
from ROOT import TFile, TCanvas, TH1D, gROOT, TStyle, gPad, TText, TLegend, TLatex
from collections import defaultdict

########################################################

# - Plotting style
myStyle = TStyle("myStyle","My own Root Style");
myStyle.SetTitleSize(0.3);
myStyle.SetTitleX(0.3);
myStyle.SetTitleXOffset(1.5);
myStyle.SetTitleYOffset(1.3);
myStyle.SetTitleSize(0.04,"xy");
myStyle.SetOptStat(0);

gROOT.SetStyle("myStyle")

color_black   = 1
color_red     = 2
color_green   = 3
color_blue    = 4
color_yellow  = 5
color_magenta = 6

line_width = 2
text_size = 0.025

style_color = { 'all' : color_black, 'SM_only' : color_blue, 'A_only' : color_red, 'qq' : color_magenta }

############################

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

##############################

def get_weight_to_nevents(lumi, xsec, ngen):
    w = lumi*xsec/ngen
#    print('Luminosity:    ', lumi)
#    print('Cross section: ', xsec)
#    print('N_gen:         ', ngen)
#    print('weight:        ', w)
    return w

def get_weight_to_xsec( xsec, ngen):
    w = xsec/ngen
#    print('Cross section: ', xsec)
#    print('N_gen:         ', ngen)
#    print('weight:        ', w)
    return w

#def normalise_components( root_file, info_file, lumi ):
#
#    import pandas as pd
#
#    info = pd.read_csv( root_file, delim_whitespace=True )
#    tf = TFile( root_file, "w" )
#
#    hcopy = (TH1D*)h->Clone("");



def plot_all_components( workdir, root_file_path, info_file, lumi ):

    import pandas as pd
    import os


    histo_names = { 'all'     : 'gg_zh1_all_{}_generator-level',   
                    'SM_only' : 'gg_zh1_SM_only_{}_generator-level',
                    'A_only'  : 'gg_zh1_A_only_{}_generator-level',
                    'qq'      : 'qq_zh1_{}_generator-level'   
                    }

    labels = {     'all'     : 'gg - all',
                   'SM_only' : 'gg - SM only.',
                   'A_only'  : 'gg - A only',
                   'qq'      : 'qq'
                   }

    types = { 'mZh'  : {'xlabel' : 'm_{inv}(Zh) [GeV]', 'name' : 'mZh'}  ,
              'h_pt' : {'xlabel' : 'p_{T}(h) [GeV]'   , 'name' : 'h_Pt'} ,
              'Z_pt' : {'xlabel' : 'p_{T}(Z) [GeV]'   , 'name' : 'Z_Pt'}  }

    info = pd.read_csv( info_file , delim_whitespace=True )

    info['xsec_gg_Zh_qq'] = 0.74829 * info['sinba'] * info['sinba']

    info['xsec_gg_Zh_all']     =  info['xsec_gg_Zh_all']  * 2.0
    info['xsec_gg_Zh_SM_only'] =  info['xsec_gg_Zh_SM_only'] * 2.0
    info['xsec_gg_Zh_A_only']  =  info['xsec_gg_Zh_A_only']  * 2.0

    w  = {'all' : None, 'SM_only' : None, 'A_only' : None, 'qq' : None }
    th = {'all' : None, 'SM_only' : None, 'A_only' : None, 'qq' : None }
    
    tf = TFile( root_file )
    
    for type in types.keys():


        for component in histo_names.keys():
    
            th[component]  = tf.Get( histo_names[component].format(type) )
            xsec           = info[ 'xsec_gg_Zh_{}'.format(component) ]
            w              = get_weight_to_xsec( xsec*1000, 10000 ) # xsec * 1000 to convert from pb to fb
            th[component].Scale( w, "width" )
            th[component].SetLineColor(   style_color[component] )
            th[component].SetMarkerColor( style_color[component] )
            th[component].SetLineWidth(   line_width )
            print('\nw[key]:', w)
        
        # - Plotting
        c = TCanvas( 'canvas', 'canvas', 800, 600 )
        
        th['qq'].GetXaxis().SetTitle( types[type]['xlabel'] )
        th['qq'].GetYaxis().SetTitle('d#sigma/dm_{Zh^{0}}  [fb/bin]')
    
        #th['all'].GetXaxis().SetRangeUser(200,1000)
        #th['all'].GetYaxis().SetRangeUser(0.0006,20)
        #h_all.GetYaxis().SetRangeUser(200,1000)
        
        gPad.SetLeftMargin(   0.14 );
        gPad.SetBottomMargin( 0.15 );
        
        label_posx, label_posy = 0.63, 0.6
        text1 = "2HDM Type-II"
        text2 = "m_{{A}}={:.0f} GeV #Gamma_{{A}}={:.3f} GeV".format( info.mA[0], info.Gamma_A[0]  )
        text3 = "cos(#beta-#alpha)={:.2f}  tan(#beta)={:.2f}".format( info.cba[0], info.tb[0] )
        text_vshift = 0.06
        label1 = TLatex(label_posx, label_posy, text1 )
        label1.SetNDC( True )
        label1.SetTextSize( text_size )
        label2 = TLatex(label_posx, label_posy-text_vshift, text2 )
        label2.SetNDC( True )
        label2.SetTextSize( text_size )
        label3 = TLatex(label_posx, label_posy-2.0*text_vshift, text3 )
        label3.SetNDC( True )
        label3.SetTextSize( text_size )
    
        legend = TLegend(0.65, 0.70, 0.85, 0.82,)
        legend.SetTextSize( 0.035 )
    
        for key in histo_names.keys():
            legend.AddEntry( th[key], labels[key] )
    
        ############################
        ## --- Linear plot
    
        
        c.SetLogy(0)
        #th['all'].GetYaxis().SetRangeUser(0.0006,3.5)
        
        th['qq'].Draw("SAME hist")
        th['all'].Draw("SAME hist")
        th['SM_only'].Draw("SAME hist")
        th['A_only'].Draw("SAME hist")
        
        #h_A_only.Draw("SAME")
        
        label1.Draw("SAME")
        label2.Draw("SAME")
        label3.Draw("SAME")
        legend.Draw("SAME")
        
        c.SaveAs( os.path.join( workdir, '{}_lin.pdf'.format( types[type]['name'] ) ))

        ############################
        ## --- Log plot
        
        c.Clear()
        c.SetLogy()
        
        th['qq'].Draw("hist")
        th['all'].Draw("SAME hist")
        th['SM_only'].Draw("SAME hist")
        th['A_only'].Draw("SAME hist")
        
        label1.Draw("SAME")
        label2.Draw("SAME")
        label3.Draw("SAME")
        legend.Draw("SAME")
        
        c.SaveAs( os.path.join( workdir, '{}_log.pdf'.format( types[type]['name'] ) ))

def plot_multiple_components( work_dir, root_file_path, plot_config, info_file_path, info_file_index=0 ):

    import os
    import pandas as pd

    # - Plotting style
    myStyle = TStyle("myStyle","My own Root Style");
    myStyle.SetTitleSize(0.3);
    myStyle.SetTitleX(0.3);
    myStyle.SetTitleXOffset(1.5);
    myStyle.SetTitleYOffset(1.5);
    myStyle.SetTitleSize(0.04,"xy");
    myStyle.SetOptStat(0);
    myStyle.SetCanvasColor(0);
    myStyle.SetFrameBorderMode(0)
    
    gROOT.SetStyle("myStyle")
    
    line_width = 2
    text_size = 0.025

    df = pd.read_table(info_file_path, delim_whitespace=True)
    
    print("plot_config['components']", plot_config['components'])
    nComponents = len( plot_config['components'] )
    
    th = nested_dict(3, dict)
    tf = TFile( root_file_path )

    print(plot_config)
    
    for level, level_opts in plot_config['levels'].iteritems():
        for type, type_opts in plot_config['types'].iteritems():
            for component, comp_opts in plot_config['components'].iteritems():
    
                print( "xsec_{}".format( comp_opts['name'] ))
                xsec = df.loc[ info_file_index, "xsec_{}".format( comp_opts['name'] )  ] * comp_opts['K_factor'] * 1000

                th[component][type][level] = tf.Get( plot_config['histo_name_template_format'].format( comp_opts['name'], type, level) )
                print('histo name: {}'.format( plot_config['histo_name_template_format'].format(
                    comp_opts['name'], type, level) ))
                print('level: {}'.format( level ))
                w                          = get_weight_to_xsec( xsec, comp_opts['nEvents'] ) # xsec * 1000 to convert from pb to fb
                th[component][type][level].Scale( w, 'width' )
                th[component][type][level].SetLineColor(   comp_opts['color'] )
                th[component][type][level].SetMarkerColor( comp_opts['color'] )
                th[component][type][level].SetLineWidth(   comp_opts['line_width'] )
                th[component][type][level].SetLineStyle(   comp_opts['line_style'] )
                print('\nw[key]:', w)
            
            # - Plotting
            c = TCanvas( 'canvas', 'canvas', 800, 600 )
            
            th[ plot_config['first_plot'] ][type][level].GetXaxis().SetTitle( type_opts['xlabel'] )
            th[ plot_config['first_plot'] ][type][level].GetYaxis().SetTitle( type_opts['ylabel'] )
    

#           int = {}
#           int['gg'] = th['gg'][type][level].Integral(bin1, bin2, 'width' )
#           int['qq'] = th['qq'][type][level].Integral(bin1, bin2, 'width' )
#   
#           print("integral1: {:.2f}".format(int['gg']) )
#           print("integral2: {:.2f}".format(int['qq']) )
    
            #th[ plot_config['first_plot'] ][type][level].GetYaxis().SetRangeUser(-1.5,8)

            if 'ranges' in plot_config:
                th[ plot_config['first_plot'] ][type][level].GetYaxis().SetRangeUser(plot_config['ranges']['y_min'], plot_config['ranges']['y_max'])
            #th['all'].GetXaxis().SetRangeUser(200,1000)
            #th['all'].GetYaxis().SetRangeUser(0.0006,20)
            #h_all.GetYaxis().SetRangeUser(200,1000)
            
            gPad.SetLeftMargin(   0.14 );
            gPad.SetBottomMargin( 0.13 );
            gPad.SetRightMargin(  0.03 );
            gPad.SetTopMargin(  0.03 );
            
            label_posx, label_posy = plot_config['label']['pos_x'], plot_config['label']['pos_y']
            label_int_posx, label_int_posy = plot_config['label_int']['pos_x'], plot_config['label_int']['pos_y']
            text_vshift = plot_config['label']['shift_y']

            labels     = []
            labels_int = []
            labels_param = []

            labels.append ( TLatex( plot_config['label']['pos_x'], plot_config['label']['pos_y'],
                plot_config['label']['text'] ) )
            labels[0].SetNDC( True )
            labels[0].SetTextSize( plot_config['label']['text_size'] )

            for i, (comp, comp_opts) in enumerate(plot_config['components'].iteritems(), 1):
                xsec = df.loc[ info_file_index, "xsec_{}".format( comp_opts['name'] )  ] * comp_opts['K_factor'] * 1000
                text = "#sigma_{{tot}}({}) = {:.2f} fb".format( comp_opts['label'],xsec )
                labels.append( TLatex(label_posx, label_posy-i*text_vshift, text ) )
                labels[i].SetNDC( True )
                labels[i].SetTextSize( plot_config['label']['text_size'] )

            labels_int.append ( TLatex( plot_config['label_int']['pos_x'], plot_config['label_int']['pos_y'],
                level_opts['name'] ) )
            labels_int[0].SetNDC( True )
            labels_int[0].SetTextSize( plot_config['label_int']['text_size'] )

            for i, (comp, comp_opts) in enumerate(plot_config['components'].iteritems(), 1):
                bin1 = th[comp_opts['name']][type][level].FindBin(000.0)
                bin2 = th[comp_opts['name']][type][level].FindBin(1500.0)
                xsec = th[comp_opts['name']][type][level].Integral(bin1, bin2, 'width' )
                text = "#sigma_{{int}}({}) = {:.2f} fb".format( comp_opts['label'],xsec )
                labels_int.append( TLatex(label_int_posx, label_int_posy-i*text_vshift, text ) )
                labels_int[i].SetNDC( True )
                labels_int[i].SetTextSize( plot_config['label_int']['text_size'] )

#            for i, (row, row_opts) in enumerate(plot_config['label_param']['rows'].iteritems(), 0):
#                text = row_opts['text'].format( df.loc[info_file_index, row_opts['input'][0]],
#                        df.loc[info_file_index, row_opts['input'][1]])
#                labels_param.append( TLatex(plot_config['label_param']['pos_x'], plot_config['label_param']['pos_y']-i*plot_config['label_param']['shift_y'], text ) )
#                labels_param[i].SetNDC( True )
#                labels_param[i].SetTextSize( plot_config['label_param']['text_size'] )

#            text2 = "#sigma_{{tot}}(gg #rightarrow Zh)={:.2f} fb".format( xsec['gg'] )
#            text2 = "#sigma_{{tot}}(gg #rightarrow Zh)={:.2f} fb".format( xsec['gg'] )
#            text3 = "#sigma_{{tot}}(qq #rightarrow Zh)={:.2f} fb".format( xsec['qq'] )
#            text4 = "#sigma_{{integral}}(gg #rightarrow Zh)={:.2f} fb".format( int['gg'] )
#            text5 = "#sigma_{{integral}}(qq #rightarrow Zh)={:.2f} fb".format( int['qq'] )
#           label1 = TLatex(label_posx, label_posy, text1 )
#           label1.SetNDC( True )
#           label1.SetTextSize( text_size )
#           label2 = TLatex(label_posx, label_posy-text_vshift, text2 )
#           label2.SetNDC( True )
#           label2.SetTextSize( text_size )
#           label3 = TLatex(label_posx, label_posy-2.0*text_vshift, text3 )
#           label3.SetNDC( True )
#           label3.SetTextSize( text_size )
#           label4 = TLatex(label_posx, label_posy-3.0*text_vshift, text4 )
#           label4.SetNDC( True )
#           label4.SetTextSize( text_size )
#           label5 = TLatex(label_posx, label_posy-4.0*text_vshift, text5 )
#           label5.SetNDC( True )
#           label5.SetTextSize( text_size )
    
            legend = TLegend(plot_config['legend']['bl_corner_x'],
                    plot_config['legend']['bl_corner_y'], plot_config['legend']['tr_corner_x'], plot_config['legend']['tr_corner_y'])
            legend.SetTextSize( plot_config['legend']['textsize'] )
    
            for comp, comp_opts in plot_config['components'].iteritems():
                legend.AddEntry( th[comp][type][level], comp_opts['label'] )
    
            # - Label
            #label = TLatex( plot_config['label']['pos_x'], plot_config['label']['pos_y'],
            #        plot_config['label']['text'] )
            #label.SetNDC( True )
            #label.SetTextSize( plot_config['label']['text_size'] )


            ############################
            ## --- Linear plot
    
            c.SetLogy(0)
            #th['all'].GetYaxis().SetRangeUser(0.0006,3.5)
            
            th[ plot_config['first_plot'] ][type][level].Draw("hist")

            for comp in plot_config['remaining_plots']:
                th[comp][type][level].Draw("SAME hist")

            for label in labels:
                label.Draw("SAME")

            for label in labels_int:
                label.Draw("SAME")
            
#            for label in labels_param:
#                label.Draw("SAME")


            
#           label1.Draw("SAME")
#           label2.Draw("SAME")
#           label3.Draw("SAME")
#           label4.Draw("SAME")
#           label5.Draw("SAME")
            legend.Draw("SAME")
#            label.Draw("SAME")
            
            c.SaveAs( os.path.join( work_dir, '{}_{}_lin.pdf'.format( type_opts['name'], level ) ))
    
            ############################
            ## --- Log plot
            
            c.Clear()
            c.SetLogy()
            
            th[ plot_config['first_plot'] ][type][level].Draw("hist")

            for comp in plot_config['remaining_plots']:
                th[comp][type][level].Draw("SAME hist")

            
#           label1.Draw("SAME")
#           label2.Draw("SAME")
#           label3.Draw("SAME")
#           label4.Draw("SAME")
#           label5.Draw("SAME")
            legend.Draw("SAME")
            
            c.SaveAs( os.path.join( work_dir, '{}_{}_log.pdf'.format( type_opts['name'], level ) ))
