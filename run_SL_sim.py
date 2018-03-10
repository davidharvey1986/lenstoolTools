import lensing as l
import ipdb as pdb
import os as os
import numpy as np
from matplotlib import pyplot as plt

def run_sim( output_dir='.', **kwargs ):

    '''
    Run a simualtion that creates strong lensing simulatio
    '''
    nImages = 0

    os.chdir(output_dir)

    alpha = np.linspace(0., 0.5, 10)
    mass = 10**(np.linspace( 13.5, 15.5, 20))
    concentration = np.linspace( 1, 10, 10)
    nClusters = 10
    
    mult_images = np.zeros( (len(mass), len(concentration), len(alpha)), np.double)
    for iMass in xrange(len(mass)):            
        for iConc in xrange(len(concentration)):
            for iCore in xrange(len(alpha)):
                nImages = 0.
                for iCluster in xrange(nClusters):
      
                    #First create sources
                    create_sources( n_source=1200, z_source=2.0 )
                
                    #Next determine image positions
                    create_multiple_images( alpha=alpha[iCore], \
                                            concentration=concentration[iConc], \
                                            m200=str( mass[iMass] ).format( 'E10.5'), \
                                            z_lens=0.5 )
    
                    #Next extract multiple_images
                    nImages += l.lenstool.extract_multiple( output='multiple.im')


                mult_images[ iMass, iConc, iCore ] = float(nImages)/(float(nClusters)*1.5)
                
            #Re-run properly
            #test_lenstool( **kwargs )

   
    #[ plt.plot( alpha, mult_images[ i, :], color=plt.cm.RdYlBu(i*10)) for i in xrange(len(mass)) ]

    #plt.show()
    pdb.set_trace()
    
def create_sources( **kwargs ):

    '''
    The only free par here is n_sources
    at the moment
    '''

    x_box = 205./3600.
    y_box = 205./3600.

    if not 'n_source' in kwargs:
        kwargs['n_source'] = 800
    if not 'z_source' in kwargs:
        kwargs['z_source'] = 1.0
        
    x = np.random.random( kwargs['n_source'] )*x_box - x_box/2.
    y = np.random.random( kwargs['n_source'] )*y_box - y_box/2.

    a = np.zeros( kwargs['n_source'] ) + 1.0
    b = np.zeros( kwargs['n_source'] ) + 1.0
    theta = np.zeros( kwargs['n_source'] )
    z = np.zeros( kwargs['n_source'] ) + kwargs['z_source']
    mag = np.zeros( kwargs['n_source'] ) + 25.5
    
    cat = open( "source_wcs.dat", "wb" )

    for i in xrange(kwargs['n_source']):
        cat.write( "%i %0.5f %0.5f %0.3f %0.3f %0.3f %0.3f %0.3f \n" \
                   %( i+1, x[i], y[i], a[i], b[i], theta[i], z[i], mag[i]) )

    cat.close()
    
    
def create_multiple_images( **kwargs ):
    '''
    Free parametes here could be:
    - Mass
    - Concentration
    - Alpha
    - Ellipticituy
    - Angle Position
    - Z_lens
    '''
    if not 'm200' in kwargs:
        kwargs['m200'] = '5e14'
    if not 'concentration' in kwargs:
        kwargs['concentration'] = 10.
    if not 'alpha' in kwargs:
        kwargs['alpha'] = 0.1
    if not 'ellipticity' in kwargs:
        kwargs['ellipticity'] = 0.
    if not 'angle_pos' in kwargs:
        kwargs['angle_pos'] = 0.
    if not 'z_lens' in kwargs:
        kwargs['z_lens'] = 0.3
        
    runmode = l.lenstool.runmode()
    runmode['inverse']['int'] = 0
    runmode['source']['int'] = 1
    runmode['source']['filename'] = 'source_wcs.dat'
    runmode['verbose']['int'] = 0
    runmode['mass']['z_lens'] = kwargs['z_lens']

    source = l.lenstool.source()
    source['source']['int'] = 0
    
    image = l.lenstool.image()
    image['arclestat']['option'] = 0
    image['sigell']['float'] = 0.3
    par_name = 'testB.par'

    grille= l.lenstool.grille( 1, 1 )
    grille['nombre']['int'] = 128
    grille['polaire']['int'] = 1

    
    potentiel = l.lenstool.potentiels.nfw()
    potentiel['m200']['str'] =  kwargs['m200']
    potentiel['concentration']['float'] =  kwargs['concentration']
    potentiel['alpha']['float'] =  kwargs['alpha']
    potentiel['ellipticity']['float'] =  kwargs['ellipticity']
    potentiel['angle_pos']['float'] =  kwargs['angle_pos']
    potentiel['z_lens']['float'] = kwargs['z_lens']

    limit = l.lenstool.limits.nfw()
    
    potentiel1 = l.lenstool.potentiels.piemd()
    limit1 = l.lenstool.limits.piemd()
    

    champ = l.lenstool.champ()
    champ['xmin']['float'] = -100.0
    champ['xmax']['float'] = 100.0
    champ['ymin']['float'] = -100.0
    champ['ymax']['float'] = 100.0

    cline = l.lenstool.cline()
    cline['nplan']['float'] = 2.0
    
    
    l.lenstool.write_par( par_name, runmode=runmode, \
                          image=image, \
                          potentiel=[potentiel, potentiel1], \
                          limit = [limit, limit1], \
                          grille=grille, cline=cline)
    
    l.lenstool.run( par_name, logfile='logfile' )

def test_lenstool( **kwargs ):

    grille= l.lenstool.grille( 1, 1 )
    grille['nombre']['int'] = 128
    grille['polaire']['int'] = 0
    
    runmode = l.lenstool.runmode()
    runmode['inverse']['int'] = 4
    runmode['inverse']['samples'] = 500

    source = l.lenstool.source()
    source['source']['int'] = 0
    image = l.lenstool.image()
    image['arclestat']['option'] = 0
    image['sigell']['float'] = 0.
    image['multfile']['int'] = 1
    image['multfile']['filename'] = 'multiple.im'

    champ = l.lenstool.champ()
    champ['xmin']['float'] = -100.0
    champ['xmax']['float'] = 100.0
    champ['ymin']['float'] = -100.0
    champ['ymax']['float'] = 100.0

    potentiel = l.lenstool.potentiel()
    potentiel['alpha']['float'] = 0.1
    
    limit = l.lenstool.limit()
    limit['alpha']['int'] = 1
    
    par_name = 'testC.par'
    
    l.lenstool.write_par( par_name, limit=[limit], runmode=runmode, image=image,\
                          grille=grille, potentiel=[potentiel])
