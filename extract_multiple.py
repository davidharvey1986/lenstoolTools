import numpy as np
import ipdb as pdb
import csv as csv

def extract_multiple( image_file='image.all', output=False ):

    dtypes = [('i', int), ('ra', float), ('dec', float), \
              ('a', float), ('b', float), ('theta', float), \
              ('z', float), ('mag', float)]
              
    i, ra, dec, a, b, theta, z, mag = \
      np.loadtxt(image_file, unpack=True, \
                dtype=dtypes, skiprows=1)
    #i = np.insert( i, 0, 0)
    
    strings = np.loadtxt(image_file, dtype='S0', skiprows=0, \
                         comments='|', delimiter='\n')
    
    mult_i, mult_ind, nImages = np.unique( i, return_counts=True, return_index=True )
    print 'There are ',np.sum( nImages[ nImages > 1 ] ),' multiple images'
    multnames = mult_i[ nImages > 1 ]

    if len( multnames ) > 0 :
        if output is not False:
            print 'Writing to ',output
            file_obj = open( output, "wb" )
            file_obj.write( strings[0]+'\n' )
            
            for iFam in multnames:
                images = np.arange( len(i))[ i == iFam ]
                for iImage in images:
                    file_obj.write( ' %i  %f5  %f5  %f5  %f5  %f5  %f5  %f5 \n' \
                                    %(i[iImage], ra[iImage], dec[iImage], \
                                    a[iImage], b[iImage], theta[iImage], \
                                    z[iImage], mag[iImage] ) )
        
            file_obj.close()
    
            arc_wcs( output, header=True, output='multiple.im' )
    else:
        print 'NO MULTIPLE IMAGES FOUND'
        
    return np.sum( nImages[ nImages > 1 ] )

def arc_wcs( filename, header=True, output=False, inverse=False):
    '''
    Take a standard lenstool output file int he form
    i x y a b theta z mag
    and convert the x and y to ra and dec ( or the other way
    round if inverse is set)

    output : the filename of the otuputted catalogue

    NOTE AT THE MOMENT ASSUMES RA AND DEC REFERENCE = 0.00

    axis = Rescale the a and b as well
    '''
    dtypes = [('i', int), ('ra', float), ('dec', float), \
              ('a', float), ('b', float), ('theta', float), \
              ('z', float), ('mag', float)]

              
    i, ra, dec, a, b, theta, z, mag = \
      np.loadtxt(filename, unpack=True, \
                dtype=dtypes, skiprows=1)
    
    strings = np.loadtxt(filename, dtype='S0', skiprows=0, \
                         comments='|', delimiter='\n')

    if inverse:
        ra *= -1*3600.
        dec *= 3600.
    else:
        ra /= -1*3600.
        dec /= 3600.

        
    if not output:
        file_obj = open( filename, "wb")
        print 'OVERWRITING ', filename
    else:
        file_obj = open( output, "wb" )

    if header:
        file_obj.write( '# REFERENCE 0\n' )
    else:
        file_obj.write( strings[0]+'\n' )
    for iImage in xrange(len(ra)):
        file_obj.write( ' %i  %f5  %f5  %f5  %f5  %f5  %f5  %f5 \n' \
                                %(i[iImage], ra[iImage], dec[iImage], \
                                a[iImage], b[iImage], theta[iImage], \
                                z[iImage], mag[iImage] ) )
