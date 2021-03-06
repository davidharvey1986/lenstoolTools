from lensing.lenstool import potentiels
from write_par import *
import csv as csv
import ipdb as pdb
import read_best as rb
import source_to_wcs as stw
from lensing import ang_distance as ang_dist

def read_par( filename,
               pot_type='AUTO',
               verbose=False,
               return_limits=False,
               return_image=False,
               return_potfile=False,
               return_all=False,
               par_dir='./'):
    '''
    Read the input into lenstool, the .par file and read it
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
       UDPATE : CAN NOW READ INPUT PAR FILES (25/05/2016) DRH

    '''
    nlens = None
    nlens_opt = None
    best_obj = open( par_dir+'/'+filename, "rb")
    run_mode = runmode()
    mode = 'Comment'
    pot = -1
    ind=0
    iLine=0





    comment_flag = 0
    limit_list = []
    limit_flag = 0
    z_m_limit = []
    for iline in best_obj:
        if iline[0] == '#':
            continue
        line = iline.splitlines()[0].split('\t')

        if verbose:
            print line
        if (line[0] != 'runmode') & (comment_flag ==0):
            continue
        
        #if the length of the line is 1 then it is a key word
        if line[0] == 'runmode':
            mode='runmode'
            comment_flag = 1
                
        if line[0] == 'grille':
            mode='grille'

        if line[0] == 'image':
            mode='image'
            ret_image = image()

        if 'potfile' in line[0]:
            mode='potfile'
            if len(line[0].split()) == 1:
                if line[0].split()[0] != 'potfile':
                    name = line[0].split()[0][7:]
                else:
                    #default name
                    name='galaxies'
            else:
                name = line[0].split()[1]
            #Assuming that we have a redshift already
            #and potfile is at the bottom of the pack
            z_lens = run_mode['mass']['z_lens']
            ret_potfile = potfile(name, z_lens)
        if (len(line) == 1):
            if line[0].strip()[0] == '#':
                if verbose:
                    print 'SKIPPING',line
                continue
            if line[0].split()[0] == 'potentiel':
                mode='potentiel'
                pot +=1
                pot_name = line[0].split()[1]

                
            if line[0].split()[0] == 'limit':
                mode='limit'
                limit_list.append(limits.get_limit( potentiel_list[pot]['profil']['int'] ))
                limit_flag = 1
        
        if len(line) > 1:
            if line[1].strip()[0] == '#':
                if verbose:
                    print 'SKIPPING ',line
                continue
            if line[1].strip() != 'end':
                if (mode == 'runmode')  :
                    option=line[1].split()
                    keys = run_mode[option[0]].dtype.names
                    for iKey in xrange(len(keys)):
                        if iKey < len(option):
                            run_mode[option[0]][keys[iKey]] = option[iKey]
                        else:
                            continue
                        
                       
                if (mode == 'grille'):
                    option=line[1].split()
                    #If the filename is the best.par then
                    #the number of lenses is the nlentille
                    #if the input par file then tihs is the nlens_opt
                    if (option[0] == 'nlentille') | (option[0] == 'nlens'):
                        nlens = np.int(option[1])
                    
                    if (option[0] == 'nlentille_opt') | (option[0] == 'nlens_opt'):
                        nlens_opt = np.int(option[1])
                        #If I assume pot is NFW use this
                        #otherwise get the potentiel type automatically
                    if (nlens_opt is not None) & (nlens is not None):
                      
                        if pot_type == 'NFW':
                            potentiel_list = [ potentiels.nfw() for i in xrange( nlens ) ]
                        else:
                            if pot_type == 'AUTO':
                                potentiel_list = rb.get_potential_list( best_file = par_dir+'/'+filename,
                                                                        verbose=verbose )
                                
                
                if (mode == 'image'):
                    
                    option=line[1].split()
                    if (option[0] == 'z_m_limit'):
                        dtype = [('name', object), ('im_label', float),
                                  ('int', np.int), ('lo', float), ('hi', float), ('res', float)]
                        iz_m_limit = np.array(('z_m_limit '+str(option[1]),
                                               option[2],option[3],
                                               option[4], option[5],
                                               option[6]), dtype=dtype)
                        ret_image[ 'z_m_limit '+str(option[1]) ] = \
                          iz_m_limit
                    else:
                        if option[0] == 'sigposArcsec':
                            option[0] = 'sigpos_arcsec'
                        image_keys = ret_image[option[0]].dtype.names
                        
                        for i in xrange( 1, len(image_keys) ):
                            ret_image[ option[0] ][image_keys[i]] = option[i]
                                               
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
                    
                if (mode == 'limit'):
                    option = line[1].split()
                    if option[0] in limit_list[pot]:
                        
                        keys = limit_list[pot][option[0]].dtype.names
                    
                        for iKey in xrange(len(keys)):
                            limit_list[pot][option[0]][keys[iKey]] \
                                = option[iKey]
                        
                if (mode == 'potfile'):
                    option=line[1].split()
                    if not option[0] in ret_potfile.keys():
                        if verbose:
                            print option[0]+' not in '+mode
                        continue
                    keys = ret_potfile[option[0]].dtype.names
                    
                    for iKey in xrange(len(keys)):
                        if iKey < len(option):
                            ret_potfile[option[0]][keys[iKey]] = option[iKey]
                        else:
                            continue
                    
            else:
                mode = 'end'
    
    if nlens != nlens_opt:
        potentiel_list = add_galaxy_lenses( np.array(potentiel_list),
                                            ret_potfile, par_dir, nlens, pot+1 )

    
    if return_limits:
        if limit_flag == 1:
            return run_mode, potentiel_list, limit_list
        else:
            print 'NO LIMIT SECTION > IS THIS A BEST.PAR?'
            return 0
    elif return_image:
        return ret_image
    elif return_potfile:
        return run_mode, potentiel_list, ret_potfile
    elif return_all:
        print 'RETURNING RUNMODE, POTENTIAL LIST, LIMIT LIST, IMAGE, POTFILE'
        return run_mode, potentiel_list, limit_list, ret_image, ret_potfile
    else:
        return run_mode, potentiel_list
                    

                    
def add_galaxy_lenses( potentiel_list, pot_file, par_dir, nlens, nlens_done ):
    '''
    At the moment the potentiel list is full of wrong
    stuff as it has nlens number of lenses, but only nlens_opt,
    that have been put it, as the rest are in the galaxy cataloye
    so i need to add the information lenses from the catalogye
    and potfile

    inputs : an array of the potentiels in question
    potfile : the potfile strucutre from write_par.py
    par_dir : a string of the path to where the parameter file
              is

    CHANGE : nlens_opt is the number optimised but more might exist in the
       part file that wasnt optimised so need to keep
    '''

    
    potfile_catalogue = open( par_dir+'/'+str(pot_file['filein']['filename']), 'rb' )
    header = potfile_catalogue.readline()

    #If the reference is 0 then it is in WCS and not relative coords
    #so convert in to relateive coordaintes and read in again
    dtype = [('id', object), ('x', float), ('y', float), ('a', float), \
             ('b', float), ('angle_pos', float), ('mag', float), ('lum', float)]
             
    if header.split()[1] == 0:
        stw.wcs_to_source( par_dir+'/'+pot_file['filein']['filename'], \
                           par_dir+'/'+pot_file['filein']['filename']+'.rel')
        galaxy_members = np.loadtxt(par_dir+'/'+pot_file['filein']['filename']+'.rel',
                                     dtype=dtype)
    else:
        galaxy_members = np.loadtxt(par_dir+'/'+pot_file['filein']['filename'],
                                dtype=dtype)
   
    galaxy_potentiels = [ potentiel_list[i] for i in xrange(nlens_done) ]
    
    kpc_to_arcsec =  206265. / (ang_dist(pot_file['zlens']['float'])*1e3)

    if len(galaxy_members['id']) != nlens - nlens_done:
        print 'WARNING NLENS != NLENS_OPT + LEN(GALAXY CATALOGUE)'
    
    for i in xrange(len(galaxy_members['id'])):

        iPot = potentiels.get_profile( pot_file['type']['int'])
        ellipticity = (galaxy_members['a'][i]**2 - galaxy_members['b'][i]**2)/\
          (galaxy_members['a'][i]**2 + galaxy_members['b'][i]**2)

          


        iPot['identity']['str'] = galaxy_members['id'][i]
        iPot['x_centre']['float'] = galaxy_members['x'][i]
        iPot['y_centre']['float'] = galaxy_members['y'][i]
        iPot['ellipticite']['float'] = ellipticity
        iPot['angle_pos']['float'] = galaxy_members['angle_pos'][i]
        iPot['z_lens']['float'] = pot_file['zlens']['float']

        mag0 = pot_file['mag0']['float']
        if pot_file['slope']['int'] == 3 | pot_file['slope']['int'] == 0:
            slope = pot_file['slope']['lo']
        else:
            slope = (pot_file['slope']['lo'] + pot_file['slope']['hi'])/2.
        
        if pot_file['sigma']['int'] == 3:
            sigma_star = pot_file['sigma']['lo']
        else:
            sigma_star = (pot_file['sigma']['lo'] + \
                            pot_file['sigma']['hi'])/2.
        if pot_file['cutkpc']['int'] == 3:
            rcut_star = pot_file['cutkpc']['lo']
        else:
            rcut_star = (pot_file['cutkpc']['lo'] + \
                            pot_file['cutkpc']['hi'])/2.
             
        rcore_star = pot_file['corekpc']['float']
        Lum = 10**(-0.4*galaxy_members['mag'][i])
        Lum_star = 10**(-0.4*mag0)
        v_disp = sigma_star*(Lum/Lum_star)**(1./slope)
        r_core = rcore_star*(Lum/Lum_star)**(1./2.)*kpc_to_arcsec
          
        r_cut = rcut_star*( Lum/Lum_star)**(1./slope)*kpc_to_arcsec
        
        iPot['cut_radius']['float'] = r_cut
        iPot['core_radius']['float'] = r_core
        iPot['v_disp']['float'] = v_disp
        iPot['mag'] = np.array(('mag',galaxy_members['a'][i]), \
                               dtype=[('name',object), ('float',float)])
        galaxy_potentiels.append(iPot)

    
    return galaxy_potentiels
        
                            
        
    
    
    
