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

    alpha = np.linspace(0., 0.5, 5)
    mass = 10**(np.linspace( 13, 16, 20))
    nClusters = 100
    
    mult_images = np.zeros( (len(mass),len(alpha)), np.double)
    for iMass in xrange(len(mass)):
        for iCore in xrange(len(alpha)):
            nImages = 0.
            for icluster in xrange(nClusters):
        
                #First create sources
                create_sources( **kwargs )
    
                #Convert the source.dat into wcs and output into source_wcs.dat
                l.lenstool.arc_wcs('source.dat', output='source_wcs.dat')
    
                #Next determine image positions
                create_multiple_images( alpha=alpha[iCore], \
                                        m200=str( mass[iMass] ).format( 'E10.5'), **kwargs )
    
                #Next extract multiple_images
                nImages += l.lenstool.extract_multiple( output='multiple.im')

                
            mult_images[ iMass, iCore ] = float(nImages)/float(nClusters)
            #Re-run properly
            #test_lenstool( **kwargs )

   
    [ plt.plot( alpha, mult_images[ i, :], color=plt.cm.RdYlBu(i*10)) for i in xrange(len(mass)) ]

    plt.show()
    pdb.set_trace()
def create_sources( **kwargs ):

    '''
    The only free par here is n_sources
    at the moment
    '''
    if not 'n_source' in kwargs:
        kwargs['n_source'] = 1000
    
    runmode = l.lenstool.runmode()
    runmode['inverse']['int'] = 0
    runmode['source']['int'] = 0
    
    image = l.lenstool.image()
    image['arclestat']['option'] = 0
    image['sigell']['float'] = 0.3
    par_name = 'testA.par'

    source = l.lenstool.source()
    source['elip_max']['float'] = 0
    source['n_source']['int'] = kwargs['n_source']
    source['source']['int'] = 1
    
    
    
    champ = l.lenstool.champ()
    champ['xmin']['float'] = -100.0
    champ['xmax']['float'] = 100.0
    champ['ymin']['float'] = -100.0
    champ['ymax']['float'] = 100.0

    
    l.lenstool.write_par( par_name, runmode=runmode, \
                          image=image, source=source, \
                          champ=champ)

    
    l.lenstool.run( par_name )

    
def create_multiple_images( **kwargs ):
    '''
    Free parametes here could be:
    - Mass
    - Concentration
    - Alpha
    - Ellipticituy
    - Angle Position
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

        
    runmode = l.lenstool.runmode()
    runmode['inverse']['int'] = 0
    runmode['source']['int'] = 1
    runmode['source']['filename'] = 'source_wcs.dat'
    runmode['verbose']['int'] = 0

    source = l.lenstool.source()
    source['source']['int'] = 0
    
    image = l.lenstool.image()
    image['arclestat']['option'] = 0
    image['sigell']['float'] = 0.3
    par_name = 'testB.par'

    grille= l.lenstool.grille( 1, 1 )
    grille['nombre']['int'] = 128
    grille['polaire']['int'] = 1

    
    potentiel = l.lenstool.potentiel()
    potentiel['m200']['str'] =  kwargs['m200']
    potentiel['concentration']['float'] =  kwargs['concentration']
    potentiel['alpha']['float'] =  kwargs['alpha']
    potentiel['ellipticity']['float'] =  kwargs['ellipticity']
    potentiel['angle_pos']['float'] =  kwargs['angle_pos']
    

    champ = l.lenstool.champ()
    champ['xmin']['float'] = -100.0
    champ['xmax']['float'] = 100.0
    champ['ymin']['float'] = -100.0
    champ['ymax']['float'] = 100.0
    
    l.lenstool.write_par( par_name, runmode=runmode, \
                          image=image, \
                          potentiel=[potentiel], \
                          grille=grille)
    
    l.lenstool.run( par_name, logfile='logfile' )


def test_lenstool( **kwargs ):

    
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
    champ['xmin']['float'] = -25.0
    champ['xmax']['float'] = 25.0
    champ['ymin']['float'] = -25.0
    champ['ymax']['float'] = 25.0


    limit = l.lenstool.limit()
    limit['alpha']['int'] = 1
    
    par_name = 'testC.par'
    
    l.lenstool.write_par( par_name, limit=[limit], runmode=runmode, image=image)
