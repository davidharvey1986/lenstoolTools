import numpy as np
import astro_tools as at
import ipdb as pdb

def source_to_wcs( filename='source.dat', outfile='source_wcs.dat'):
    '''

    Lenstool always outputs the source file in relative coordinates
    so to convert this into a normal file in world coord sys
    run this script.
    '''
    header = open(filename, "rb").readline()
    if  header[0] == '#':
        print 'REFERENCE ',header
    else:
        print 'NEED A HEADER TO BE ABLE TO SOURCE TO WCS'
        return 0
        
        
    reference = header.split()

    reference[1] = '0'
    outobj = open(outfile,'wb')
    outobj.write( ' '.join( reference )+'\n' )
    
    source_array = np.loadtxt( filename )
    
    source_array[:, 1] = -1.*source_array[:,1]/np.cos( np.float(reference[-1])*np.pi/180.)/3600.+ \
      np.float(reference[-2])
    source_array[:, 2] = np.float(reference[-1])+source_array[:, 2]/3600.

    for iGal in xrange(len(source_array[:,0])):
        write_line = [ i for i in source_array[iGal, :] ]

        outobj.write( '%.1f\t%.7f\t%.7f\t%.7f\t%.7f\t%.7f\t%.7f\t%.7f\n' % \
                      tuple(write_line))

        
    outobj.close()

def wcs_to_source( filename, outfile):
    '''
    Convert a wcs file into relative postiions
    '''
    header = open(filename, "rb").readline()

    reference = header.split()

    

    source_array = np.loadtxt( filename )

    source_array[:, 1] = at.ra_separation( source_array[:, 1],
                                        np.float(reference[3]),
                                        np.float(reference[2]),
                                        np.float(reference[3]))
    source_array[:, 2] = (source_array[:, 2] - np.float(reference[3]))*3600.

    
    reference = header.split()
    
    reference[1] = '3'
    outobj = open(outfile,'wb')
    outobj.write( ' '.join( reference )+'\n' )
    

    for iGal in xrange(len(source_array[:, 0])):
        write_line = [ i for i in source_array[iGal, :] ]
        outobj.write( '%0.1f %f %f %f %f %f %f %f \n' % \
                       tuple(write_line) )
    outobj.close()
    
