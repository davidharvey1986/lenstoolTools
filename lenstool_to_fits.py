'''
Turn a lenstool a catalogue into a fits file with the headers each
of the lines

'''

import astro_tools as at 
import best_to_fits as btf
import numpy as np
import ipdb as pdb

def lenstool_to_fits(lenstool_cat, lenstool_fit, pixel_size = 0.05):
    '''
    The main function

    input :
       lenstool_cat : a string of the name of the lenstool catalogue
       lenstool_fit : a string of the name of the lenstool fits catalogue

       pixel_size = 0.03 : assumed that the image has come from HST image
    '''


    i, ra, dec, a, b, theta, z, mag = \
      np.loadtxt( lenstool_cat, unpack=True )


    dtypes = [('RA', float), ('DEC', float),
              ('A', float), ('B', float), ('THETA', float),
              ('Ell', float), ('fwhm', float)]


    ell = (a**2 - b**2)/(a**2 + b**2)

    fwhm = a / np.sqrt(1 + ell) * pixel_size
  
    rec_array = np.array( (ra[0], dec[0], a[0], b[0], theta[0], ell[0], fwhm[0]), dtype=dtypes)

    for i in range(1,len(ra)):
        iRec = np.array((ra[i], dec[i], a[i], b[i], theta[i], ell[i], fwhm[i]),
                        dtype=rec_array.dtype)
        rec_array = np.append( rec_array, iRec ) 
                           
    
        
    btf.py.writeto(lenstool_fit,rec_array,  clobber=True)


