from lensing.lenstool import potentiels
from write_par import *
import csv as csv
import ipdb as pdb

def read_best( filename='best.par', pot_type='AUTO', verbose=False ):
    '''
    Read the output from lenstool, the best.par and read it
    into a python class

    It assumes that the input file is best.par however this
    can be changed with the keyword

    RETURNS :
       2 Rec arrays 
       - run_mode : contains the reference position of the halo
       - potentiel_list : a n halo list of the potentiels found in the recon

       For more information on these rec arrays see write_par.py and potentiels.py


       BUGS:
          It does require the output best.par to be in a paticular order
          (the one output from lenstool)
          And for now can only read NFWs, because I never use anything else

    '''

    best_obj = open( filename, "rb")
    run_mode = runmode()
    mode = 'Comment'
    pot = -1
    ind=0
    iLine=0
    comment_flag = 0
    for iline in best_obj:
                
        line = iline.split('\t')
        line[-1] = line[-1][:-1]
        
        line[-1] = line[-1]
        
        if (line[0] != 'runmode') & (comment_flag ==0):
            continue
        
        #if the length of the line is 1 then it is a key word
        if line[0] == 'runmode':
            mode='runmode'
            comment_flag = 1
                
        if line[0] == 'grille':
            mode='grille'
            
        if (len(line) == 1):
            if line[0].split()[0] == 'potentiel':
                mode='potentiel'
                pot +=1
                pot_name = line[0].split()[1]
                
        if len(line) > 1:
            if line[1] != 'end':
                if (mode == 'runmode')  :
                    option=line[1].split()
                    if option[0] == 'reference':
                        run_mode['reference']['ra'] = option[2]
                        run_mode['reference']['dec'] = option[3]
                       
                if (mode == 'grille'):
                    option=line[1].split()
                    if option[0] == 'nlentille':
                        nlens = np.int(option[1])

                        #If I assume pot is NFW use this
                        #otherwise get the potentiel type automatically
                        if pot_type == 'NFW':
                            potentiel_list = [ potentiels.nfw() for i in xrange( nlens ) ]
                        else:
                            if pot_type == 'AUTO':
                                potentiel_list = get_potential_list( best_file = filename )

                if (mode == 'potentiel'):
                    if pot >= nlens:
                        continue
                    option = line[1].split()
                    try:
                        data_type = potentiel_list[pot][option[0]].dtype.names[1]
                        potentiel_list[pot][option[0]][data_type] = \
                        np.array(option[1]).astype(data_type)
                       
                                   
                    except:
                        if verbose == True:
                            print option[0],' does not exist in potentiel'
                        else:
                            pass
                        
                    ra_halo = run_mode['reference']['ra'] - \
                          potentiel_list[pot]['x_centre']['float']/3600./\
                          np.cos(run_mode['reference']['dec']*np.pi/180.)
                    dec_halo = run_mode['reference']['dec'] + \
                          potentiel_list[pot]['y_centre']['float']/3600.
                        
                    potentiel_list[pot]['ra'] = \
                          np.array(('ra', ra_halo), dtype=[('name', object), ('float', float)])
                    potentiel_list[pot]['dec'] = \
                          np.array(('dec', dec_halo), dtype=[('name', object), ('float', float)])
                    potentiel_list[pot]['identity'] =\
                        np.array(('identity', pot_name), dtype=[('name', object), ('str', object)])

            else:
                mode = 'end'


    return run_mode, potentiel_list
                    

                    
                
def get_potential_list( best_file='best.par' ):
    '''
    Run this script to get the list of potentials
    which may not be necessarily NFW


    Currently only valid for NFW or PIEMD since these
    are the only ones in limit.py and potentiels.py

    '''

    run_mode, pots = read_best( best_file, pot_type='NFW' )

    return [ potentiels.get_profile(iPot['profil']['int']) for iPot in pots ]

    
