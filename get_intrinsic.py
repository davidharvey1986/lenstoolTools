from model_cluster import *
import glob as glob

'''
A function that returns the intrinsic a, b and theta
in the source plane using either the source.dat from
lenstool, or from cluster_model, that uses the best.par
and converts back myself
    
This function has two different functions
1 lenstool : which uses lenstool to simulate the clsuter
             and produce a source.dat file of intrinsic and
             return those
             
2. uses model_cluster.py which models it myself and then outputs
   the intrinsic as determined byt his.

    This function takes a cluster and returns what we expect
    the intrinsic ellipticity to be (source plane image) given
    some input files from lenstool
'''


def lenstool( best_file, cat_name=None, outDir='.',
              source_file=None, use_potentials=None, **kwargs):
    '''
    Use lenstool which requires :
    Reuires the best.par to create the source.dat

    best_file : a path to the best.par from lenstool
    cat_name : the catalogue name used to create the best.par
    datadir : where I want to creat the outputs.

    '''
    
    if not 'mass_res' in kwargs:
        kwargs['mass_res'] = 800
        
    if not os.path.isfile( best_file):
        return 'BEST FILE ILL DEFINED'

    if use_potentials is None:
        run_mode, pot = l.lenstool.read_best( best_file )
    else:
        run_mode, not_use_pots = l.lenstool.read_best( best_file )
        pot = use_potentials
    
    if source_file is None:
        if cat_name is None:
            print 'CATALOGUE NAME UNDEFINED'
            cats_aval = glob.glob(outDir+'/*.lenstool')
            if (len(cats_aval) != 1) :
                print 'TRIED FINDING CAT BUT TO NO AVAIL',outDir       
                return 0
            else:
                cat_name = cats_aval[0].split('/')[-1]
                print 'USING CAT NAME ', cat_name
                
        #Create the lenstool source file using the best.par
        image_par_run = l.lenstool.runmode()
        image_par_run['source']['int'] = 0
        image_par_run['image']['int'] = 1
        image_par_run['image']['filename'] = cat_name
        image_par_run['inverse']['int'] = 0
        image_par_run['mass']['resolution'] =  kwargs['mass_res']
        image_par_run['mass']['int'] = 1.
        image_par_source = l.lenstool.source()
        image_par_source['source']['int'] = 0
        image_par_image = l.lenstool.image()
        image_par_image['image']['int'] = 0
        image_par_limit = [ l.lenstool.limit() for i in xrange(len(pot)) ]
        l.lenstool.write_par(outDir+"/image.par", runmode=image_par_run, \
                source=image_par_source, image=image_par_image,\
                potentiel=pot, limit=image_par_limit )
        l.lenstool.run( "image.par", outdir=outDir)


        #Source.dat should be the intrinsic ell as defined by lenstool
        source_file = outDir+'/source.dat'
    
    
    #Use the lenstool source file    
    ind, ra_source, dec_source, a_source, b_source, theta_source, z_source, mag_source =\
            np.loadtxt( source_file, unpack=True)

    #Source.dat is in the format ra relative to ra_ref, in arcseconds
    ra_source = ra_source*-1./np.cos(run_mode['reference']['dec']*np.pi/180.)/3600.+\
            run_mode['reference']['ra']
    dec_source = dec_source/3600.+run_mode['reference']['dec']

    


    return ra_source, dec_source, a_source, b_source, theta_source 


def model( image_file, best_file, intrinsic_cat=None):
    
    '''
    My way which uses cluster_model() which requires:
    image_file : string of path+name of catalogue of the galaxies
                 used in the reconstruction

    optional : intrinsic_cat  which is the string name of the output
                catalogue in which I will put the catalgoue name of
                source shapes
    '''
    if not os.path.isfile( image_file ):
        return 'IMAGE FILE ILL DEFINED'

    #Load the image_file (catalogue used for the reconstruciton)
    ind, ra_image, dec_image, a_image, b_image, theta_image, z_image, mag_image =\
        np.loadtxt( image_file, unpack=True)
            
    #Pass a dummy ar to model cluster as this needs to be made better            
    dummy_var = 'dummy'

    #Get the model of the cluster
    cluster_mod = model_cluster( ra_image, dec_image, 'dummy', best_file=best_file)

    #And deduct of the image shapes
    ell = (a_image**2-b_image**2)/(a_image**2+b_image**2)
        
    chi_image = ell*np.cos(2.*theta_image) + \
        1j*ell*np.sin(2.*theta_image)
    chi_source = l.image_to_source( chi_image, \
                                    cluster_mod.source[0].shear)
    
    ra_source = ra_image
    dec_source = dec_image
    a_source = np.sqrt( 1. +  np.abs(chi_source))
    b_source = np.sqrt( 1. -  np.abs(chi_source))
    theta_source = np.arctan2( np.imag(chi_source), \
                                np.real(chi_source))/2.*180./np.pi

                                            
    cluster_mod.source[0].a = a_source
    cluster_mod.source[0].b = b_source
    cluster_mod.source[0].angle_lenstool = theta_source

    if intrinsic_cat:    
        cluster_mod.write_cat(intrinsic_cat)


    return ra_source, dec_source, a_source, b_source, theta_source 
