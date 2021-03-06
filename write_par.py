import lensing as lensing
import numpy as np
import csv as printer
import ipdb as pdb
from collections import OrderedDict as d
import potentiels as potentiels
import limits as limits

def write_par( par_name, **kwargs ):
    '''
    write the lenstool paramter file to par_name

    par_name : a string

    The default is to have 1 halo, nfw, with 1 limit
    at a reference position of 0.5, 0.5 as this is in line
    with the simulation code.

    kwargs :
        The various modes can be given as kwarfs
        and the code checks, if it doesn exist then
        creat the default


        
    NOTE   1
    -----------
    If i give potentiel, it made be
    made of more than one, so this should be
    a list of potentials. Same goes for limit

    NOTE   2
    -----------
    If I add a source or image keyword to runmode this
    will mess up the image and source sections and create crap
    so ensure only 1 or the other is defined.
    
    '''
    if not 'runmode' in kwargs:
        kwargs['runmode'] = runmode()
    if not 'source' in kwargs:
        kwargs['source'] = source()
    if not 'image' in kwargs:
        kwargs['image'] = image()
    if not 'potentiel' in kwargs:
        kwargs['potentiel'] = [ potentiels.nfw( ) ]
    if not 'limit' in kwargs:
        limits = []
        for i in xrange(len(kwargs['potentiel'])):
            ilimit =  getLimit( kwargs['potentiel'][0]['profil']['int'])
            ilimit['x_centre']['lo'] = kwargs['potentiel'][i]['x_centre']['float']-25.
            ilimit['x_centre']['hi'] = kwargs['potentiel'][i]['x_centre']['float']+25.
            ilimit['y_centre']['lo'] = kwargs['potentiel'][i]['y_centre']['float']-25.
            ilimit['y_centre']['hi'] = kwargs['potentiel'][i]['y_centre']['float']+25.
            
            limits.append( ilimit )
    
            
        kwargs['limit'] = limits
        
    if not 'grille' in kwargs:
        kwargs['grille'] = grille( len(kwargs['potentiel']), \
                                    len(kwargs['limit']) )
    if not 'cosmology' in kwargs:
        kwargs['cosmology'] = cosmology()
    if not 'champ' in kwargs:
        kwargs['champ'] = champ()
    if not 'cline' in kwargs:
        kwargs['cline'] = cline()
    if not 'potfile' in kwargs:
        kwargs['potfile'] = [potfile('galaxies',kwargs['potentiel'][0]['z_lens']['float'])]
    else:
        for iPotFile in kwargs['potfile']:
            iPotFile['potfile']['int'] = 1
        
    file_obj = printer.writer( open(par_name, "wb"), delimiter=' ', \
                               quotechar=' ')                        
    sect_write( file_obj, ['runmode'], kwargs['runmode'] )

    #The image and source keywords cause issues if
    #they exist in the run mode and in the source
    #so if the namesake option ==0 dont print it
    if kwargs['source']['source']['int'] == 1:
        del kwargs['source']['source']
        sect_write( file_obj, ['source'], kwargs['source'] )
    if kwargs['image']['image']['int'] == 1:
        del kwargs['image']['image']
        sect_write( file_obj, ['image'], kwargs['image'] )

    

    sect_write( file_obj, ['grille'], kwargs['grille'] )
    for iPot in xrange(len( kwargs['potentiel'] )):
        try:
             str_iPot = kwargs['potentiel'][iPot]['identity']['str']
        except:
            str_iPot = " "+str(iPot+1)
        sect_write( file_obj, ['potentiel', str_iPot],  kwargs['potentiel'][iPot] )
        
        if iPot < len(kwargs['limit']):
            PotInt = kwargs['potentiel'][iPot]['profil']['int']
            NewLimit = getLimit(PotInt)
            kwargs['limit'].append(NewLimit)

        limit_ints = np.array([ kwargs['limit'][iPot][ k ]['int'] \
                                for k in kwargs['limit'][iPot].keys()])
        if np.sum(limit_ints) > 0:
            sect_write( file_obj, ['limit', str_iPot], kwargs['limit'][iPot] )
        else:
            if kwargs['runmode']['inverse']['int'] != 0:
                print 'WARNING NO PARAMETERS FREE IN POT NUMBER ',iPot
    for iPotFile in kwargs['potfile']:
        if iPotFile['potfile']['int'] == 1:
            potfilename = iPotFile['potfile']['name']
            del iPotFile['potfile']
            sect_write( file_obj, ['potfile', potfilename], \
                            iPotFile )
        
    sect_write( file_obj, ['cline'],  kwargs['cline'] )
    sect_write( file_obj, ['cosmologie'], kwargs['cosmology'] )
    sect_write( file_obj, ['champ'], kwargs['champ'], finish=True )
    
    
def sect_write( file_obj, header, pars, finish=False):
    '''
    Write out the given pars to the file
    '''
    file_obj.writerow(header)
    for var in pars:
        
        pars_str = [ str(pars[var][i]) for i in  pars[var].dtype.names ]
        pars_str.insert(0, "\t")
        file_obj.writerow(pars_str)

    file_obj.writerow([ "\t",'end'])
    if finish:
        file_obj.writerow(['fini'])

                                   
                                       
def runmode( reference= np.array(('reference', 3, 0.50, 0.50), \
                    dtype=[('name', object), ('int', int),('ra', float), ('dec', float) ]), \
             verbose=np.array(('verbose', 1), \
                    dtype=[('name', object), ('int',int)]) , \
             inverse=np.array(('inverse', 3, 0.1, 1000),\
                    dtype=[('name', object), ('int',int),('rate',float), ('samples', int)] ), \
             mass= np.array(('mass', 3, 200, 0.3, 'mass.fits'), \
                    dtype=[('name', object), ('int', int), ('resolution',int), \
                           ('z_lens', float), ('filename', object)]), \
             source=np.array(('source', 0, "source.dat"), \
                    dtype=[('name', object), ('int',int),('filename', object)]), \
             image=np.array(('image', 0, "image.dat"), \
                    dtype=[('name', object), ('int',int),('filename', object)]),\
             dpl= np.array(('dpl', 0, 200, 2.0, 'x_shift.fits', 'y_shift.fits'), \
                    dtype=[('name', object), ('int', int), ('resolution',int), \
                           ('z_source', float), ('x_shift', object), ('y_shift', object)]),
            restart = np.array(('restart', 1, 1), \
                    dtype=[('name', object), ('int',int),('seed', object)]) ):
    '''
    Set up run mode
    '''
    return {'reference':reference, 'verbose':verbose, 'inverse':inverse, \
            'mass': mass, 'source':source, 'image':image, 'dpl':dpl, \
                'restart':restart}

def source( source=np.array(('source', 1), dtype=[('name', object), ('int',int)]), \
            grid=np.array(('grid', 0 ), dtype=[('name', object), ('int', int)]), \
            n_source=np.array(('n_source', 800), dtype=[('name', object), ('int', int)]), \
            z_source=np.array(('z_source', 1.0), dtype=[('name', object), ('float', float)]),\
            elip_max=np.array(('elip_max', 0.3,), dtype=[('name', object), ('float',float)])):

    return {'source':source, 'grid':grid, 'n_source':n_source, \
              'z_source':z_source, 'elip_max':elip_max }

def image( arcletstat=np.array(('arcletstat', 7, 0, 'nfw.lenstool'), \
                dtype=[('name', object), ('option', int), ('int', int), ('filename', object)]), \
            sigell=np.array(('sigell', 0.3), \
                dtype=[('name', object), ('float', float)]), \
            sigpos_arcsec=np.array(( 'sigpos_arcsec', 0.0,), \
                dtype=[('name', object), ('float', float)]), \
            multfile=np.array(('multfile', 0, 'multiple.im'), \
                dtype=[('name', object), ('int', int),('filename', object)]), \
            mult_wcs=np.array(('mult_wcs', 1), \
                dtype=[('name', object), ('float', float)]),\
            forme=np.array(('forme', -1), \
                dtype=[('name', object), ('float', float)]),\
            image=np.array(('image', 1), \
                dtype=[('name', object), ('int', int)]),
            z_arclet=np.array(('z_arclet',1.0),
                dtype=[('name', object), ('redshift', float)])):

    return { 'arcletstat':arcletstat, 'sigell':sigell, 'sigpos_arcsec':sigpos_arcsec, \
             'multfile':multfile, 'mult_wcs':mult_wcs, 'forme':forme, 'image':image,
             'z_arclet':z_arclet }

def grille( nLens, nLens_opt, \
            nombre=np.array(( 'nombre', 30.), \
                dtype=[('name', object), ('int', float)]), \
            polaire=np.array(( 'polaire', 0.), \
                dtype=[('name', object), ('int', float)]) ):

    nlens = np.array(('nlens', nLens), \
            dtype=[('name', object), ('int', int)])
    
    nlens_opt = np.array(('nlens_opt', nLens_opt), \
            dtype=[('name', object), ('int', int)])

    return { 'nlens':nlens, 'nlens_opt':nlens_opt, 'nombre':nombre, 'polaire':polaire }

def getLimit( profil=12 ):
    if profil == 12:
        return limits.nfw()
    if profil == 81:
        return limits.piemd()
    return 

def cosmology(  model = np.array(('model', 1), dtype=[('name', object), ('int', int)]),\
                H0 = np.array(('H0', 70.0), dtype=[('name', object), ('float', float)]), \
                omegaM = np.array(('omegaM', 0.3), dtype=[('name', object), ('float', float)]), \
                omegaX = np.array(('omegaX', 0.7), dtype=[('name', object), ('float', float)]), \
                omegaK = np.array(('omegaK', 0.), dtype=[('name', object), ('float', float)]), \
                wX = np.array(('wX', -1.0), dtype=[('name', object), ('float', float)]), \
                wa = np.array(('wa', 0.), dtype=[('name', object), ('float', float)])):

    return { 'model':model, 'H0':H0, 'omegaM':omegaM, 'omegaX':omegaX,\
            'omegaK':omegaK, 'wX':wX, 'wa':wa}

        
def champ( xmin = np.array(('xmin', -100), dtype=[('name', object), ('float', float)]), \
            xmax = np.array(('xmax', 100), dtype=[('name', object), ('float', float)]), \
            ymin = np.array(('ymin', -100), dtype=[('name', object), ('float', float)]), \
            ymax = np.array(('ymax', 100), dtype=[('name', object), ('float', float)])):
    
    return { 'xmin':xmin, 'xmax':xmax, 'ymin':ymin, 'ymax':ymax}
    

def cline( nplan = np.array(('nplan', 1, 1.), \
                dtype=[('name', object), ('int', int), ('float', float)]), \
            pas = np.array(('pas', 1.), \
                dtype=[('name', object), ('float', float)]) ):


    return { 'nplan' : nplan, 'pas' : pas }
    
    

def potfile( name, z_lens,
            corekpc=False, sigma=True, cutkpc=True, slope=False,
            filein = np.array(('filein', 1, 'galaxy_cat.cat'), \
                dtype=[('name', object), ('int', int), ('filename', object)]), \
            pot_type = np.array(('type', 81), \
                dtype=[('name', object), ('int', int)]), \
            mag0 = np.array(('mag0', 17.), \
                dtype=[('name', object), ('float', float)])):

    potfile = np.array((name, 0), \
                dtype=[('name', object), ('int', int)])
                
    zlens = np.array(('zlens', z_lens ), \
                dtype=[('name', object), ('float', float)])
    #list defaults
    lim_dtype = [('name', object), ('int', int), ('lo', float), ('hi', float), ('res', float)]
    dtype = [('name', object), ('float', float)]
    if corekpc:
        corekpc = np.array(('corekpc', 1, 0., 100., 1.), dtype=lim_dtype)
    else:
        corekpc = np.array(('corekpc', 0.15), dtype=dtype)
    if sigma:
        sigma = np.array(('sigma', 3., 150, 17, 1.),  dtype=lim_dtype)
    else:
        sigma = np.array(('sigma', 100.), dtype=dtype)
    if cutkpc:
        cutkpc = np.array(('cutkpc', 1., 0.0, 100, 0.1), dtype=lim_dtype)
    else:
        cutkpc = np.array(('cutkpc', 50.),dtype=dtype)
    if slope:
        slope = np.array(('slope', 1., 4., 4.2, 0.1), dtype=lim_dtype)
    else:
        slope = np.array(('slope', 0., 4.0, 0.1, 0.1), dtype=lim_dtype)
       

            
    
    return { 'potfile' : potfile, 'filein' : filein,
             'zlens' : zlens, 'type' : pot_type, 'mag0':mag0,
             'corekpc' : corekpc, 'sigma' : sigma, 'cutkpc' : cutkpc, 'slope':slope  }




