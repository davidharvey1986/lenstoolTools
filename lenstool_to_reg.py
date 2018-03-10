import numpy as np

def lenstool_to_reg( filename, output ):
    '''
    Convert a lenstool catalogue into a reg file that can be used in
    ds9
    '''

    i, x, y, a, b, theta, z, mag = \
      np.loadtxt( filename, unpack=True)


    file_obj = open( output, "wb")
    
    file_obj.write("# Region file format: DS9 version 4.1\n")
    file_obj.write("# Filename: "+filename+"\n")
    file_obj.write('global color=green dashlist=8 3 width=1 ')
    file_obj.write('font="helvetica 10 normal roman" select=1')
    file_obj.write(' highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1')
    file_obj.write(' include=1 source=1 \n')
    file_obj.write("fk5\n")

    for i in xrange(len(x)):
        file_obj.write('ellipse( %f,%f,%f",%f",%f)\n' % (x[i],y[i],a[i]*5.,b[i]*5.,theta[i]))


    
