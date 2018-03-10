import numpy as np
import write_par as wp
import read_best as rb
import run as run

def cluster_rms( multiple_image_file='multiple.im'):
#                 runmode, 
 #                cluster_model ):
    
    '''
    Determine the RMS of a cluster model, i.e. how well
    the model is predicting the data.

    1. Take the cluster model project the multiple iamges
       back to the source plane

    2. Aggregate the sources into one bary-center
    3. Reproject the source back to the image plane
    4. Compare to the original image positions

    cluster model is a list of potentials
    that i want to use to project cluster back
    '''
    runmode, cluster_model = rb.read_best()

    #Need to append the image source redshifts to the multiple
    #image file and save in a new one
    multiple_image_file_with_redshift = 'multiple_w_redshifts.im'
    multiple_to_image( multiple_image_file,
                       multiple_image_file_with_redshift,
                       z_limits)

    runmode['image']['int'] = 1
    runmode['image']['filename'] = multiple_image_file_with_redshift
    runmode['source']['int'] = 0
    runmode['inverse']['int'] = 0
    src_image = wp.image()
    src_image['image']['int'] = 0
    src_source = wp.source()
    src_source['source']['int'] = 0
    
    src_par_file = 'cluster_rms_src.par'


    
    wp.write_par( src_par_file,
               potentiel=cluster_model,
               runmode=runmode,
               source=src_source,
               image=src_image )

    run.run( src_par_file )

    aggregate_sources( source_file='source.dat',
                       outfile='source_agg.dat')
def aggregate_sources( source_file='source.dat',
                       outfile='source_agg.dat'):
    '''
    Aggregate the sources in the given source file
    to the barycenter of each image

    Then write out the source file
    '''
    header = open( source_file, 'rb').readline()
    
    dtype = [('im_labels', float), ('ra', float), \
             ('dec', float), ('a', float), ('b', float),
             ('angle_pos', float), ('redshift', float),
             ('magnitude', float) ]
        
    sources = np.loadtxt( source_file, dtype=dtype )

    family_labels = np.floor( sources['im_labels'])
    unique_family_labels = np.unique(family_labels)

    family_data = open( outfile, 'wb')
    family_data.write( header )
    
    for iFamily in xrange(len(unique_family_labels)):

        
        family_id = unique_family_labels[iFamily]
        family_ra = np.mean( sources['ra'][ family_id == family_labels])
        family_dec = np.mean( sources['dec'][ family_id == family_labels])
        family_z = np.mean( sources['redshift'][ family_id == family_labels])
        
        family_data.write( "%0.1f %0.5f %0.5f %0.1f %0.1f %0.1f %0.5f %0.1f\n"%
          (family_id, family_ra, family_dec, 0.5, 0.5, 50., family_z, 25.0))

    family_data.close()
                
    
def multiple_to_image( infile, outfile, z_limits):
    '''
    Take a multiple image file, read it, and output
    another file that has the z_limits put in it

    i.e. in the mulitple image file the redhsift
    of the image will be 0 if not spectroscopic and
    used to constrain. So therefore use the limits
    and just take centre of the prior as the truth

    '''
    header = open(infile, 'rb').readline()

    dtype = [('im_label', float), ('ra', float),
             ('dec', float), ('a', float),
             ('b', float), ('theta', float),
             ('redshift', float), ('mag', float)]


    orig_images = np.loadtxt( infile, dtype=dtype)

    image_families = np.floor( orig_images['im_label'] )

    for iImage in xrange(len(z_limits)):
        iMult_images = orig_images
        iRedshift = z_limits[iImage]['redshift']
            
        orig_images['redshift'][ image_families == z_limits[iImage]['im_label'] ] =  iRedshift

    fileobj = open( outfile, 'wb')
    fileobj.write( header )
    for iLine in xrange(len(orig_images['im_label'])):
        fileobj.write('%0.1f    %0.5f   %0.5f   %0.2f   %0.2f   %0.2f   %0.4f   %0.1f\n' %
                      (orig_images['im_label'][iLine],
                       orig_images['ra'][iLine], orig_images['dec'][iLine],
                       0.5, 0.5, 50.0, orig_images['redshift'][iLine], 25.0 ))

    fileobj.close()
