'''
Convert a best.par (or input par file .par) to a fits file
by taking all the potentials and putting them into the fits file
and adding header stuff from the runmode

'''

import numpy as np
import pyfits as py
import ipdb as pdb
import read_best as rb

def best_to_fits( best_file, outfile=None, return_fits=True):
    '''
    read in a best file and then convert it into
    a rec array and save as a fits file in the outfile


    '''

    


    run_mode, potentials = rb.read_best( best_file )

    npots = len(potentials)

    #Set up the array
    pot_dtypes = potential_dtypes( potentials[0] )
    potential_array = np.array([], dtype=pot_dtypes)
    
    for iPot in potentials:
        potential_array = append_potential( potential_array, \
                                            iPot, pot_dtypes)

    run_dtypes = potential_dtypes( run_mode )
    run_rec = np.array([], dtype=run_dtypes)
    run_rec = append_potential( run_rec, run_mode,
                                 run_dtypes)

    header = get_header( run_mode)


    potential_hdu = rec_to_tbhdu( potential_array )

    thdulist = py.HDUList([py.PrimaryHDU(header=header), potential_hdu])
    
    if outfile is not None:
        thdulist.writeto(outfile, clobber=True)

    if return_fits:
        return thdulist
    
def get_header( run_mode):
    '''
    Put the run_mode in the header
    '''
                
    header=py.Header()

    for iKey in run_mode.keys():
        pars = run_mode[iKey].dtype.names
        
        if len(pars) > 2:
            for iPar in xrange(len(pars)-1):
                header[ pars[iPar+1]] =  str(run_mode[iKey][pars[iPar+1]])
        else:
           header[ iKey ] =  str(run_mode[iKey][run_mode[iKey].dtype.names[1]])

    header.add_comment( 'RUN MODE PARAMETERS', before=header.keys()[0])
    header.add_blank(value='',before=header.keys()[0])

    return header
    

def rec_to_tbhdu( rec_array ):
    '''
    Turn a rec array in columns which then in turn
    make in to a hdu item that can go into a
    fits file
    '''

    columns = []
    for iPar in rec_array.dtype.names:
        try:
            columns.append(  py.Column( name = iPar,
                                    format= rec_array[iPar].dtype,
                                    array = rec_array[iPar] ))
        except:
            #The dtype will be 'object' which isnt liked
            #so change to a string

            columns.append(  py.Column( name = iPar,format= 'A20',\
                                        array = rec_array[iPar] ))

    return py.BinTableHDU.from_columns( columns )


def potential_dtypes( potential, return_values=False ):
    '''
    using the first element of a potential list
    setup an empty array with the correct names
    and dtypes

    '''

    dtype = []
    for iKey in potential.keys():
        dtype.append( (iKey, potential[iKey].dtype[1] ) )

    return dtype


def append_potential( array_toappend, potential, dtypes ):
    '''
    using the first element of a potential list
    setup an empty array with the correct names
    and dtypes

    '''
    tmp_array = np.zeros(1, dtype=dtypes)
                         
    for iKey in potential.keys():
        key_type = potential[iKey].dtype.names[1]
        tmp_array[ iKey ] = potential[iKey][potential[iKey].dtype.names[1]]
    
        
    return np.append( array_toappend, tmp_array)
