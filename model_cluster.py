'''
This script has 2 functions:

1. model_cluster( ra, dec, cluster, \
                   halos=None, \
                   best_file=None)

  This models the input cluster and returns a structure
  from simulate_project with shear, chi, etc.

  


'''

import numpy as np
import ipdb as pdb
import astro_tools as at
import idlsave as idlsave
import lensing as l
import copy as copy
import glob as glob
import os 

def model_cluster( ra, dec, cluster, \
                   halos=None, \
                   best_file=None):
    '''
    Model the NFW signal of the cluster using the
    input from halos
    
    '''
    if best_file is None:
        dataDir = '/Users/DavidHarvey/Documents/Work/Trails/data/rerun/'+cluster
        best_file = dataDir+'/best.par'
        
    runmode, potentials = l.lenstool.read_best( filename=best_file)
    
    space = l.simulations.templates.space()
    space.lens[0].del_profile('isothermal')
    
    space.source[0].ell_disp = 0.
    space.source[0].ra = ra
    space.source[0].dec = dec
    space.telescope.nGalaxies = len(dec)
    space.lens[0].redshift = potentials[0]['z_lens']['float']
    space.source[0].redshift = 1.0
    
    
    space.lens[0].ra = potentials[0]['ra']['float']
    space.lens[0].dec = potentials[0]['dec']['float']
    if halos is not None:
        space.lens[0].ra = halos['halos'][0]['gal']['ra'][0]
        space.lens[0].dec = halos['halos'][0]['gal']['dec'][0]
   
    space.lens[0].profiles['nfw'].args['mass'] = \
      potentials[0]['m200']['str'].astype(np.double)
    space.lens[0].profiles['nfw'].args['conc'] = \
      potentials[0]['concentration']['float']
    space.lens[0].profiles['nfw'].args['ellipticity'] = \
      potentials[0]['ellipticite']['float']
    space.lens[0].profiles['nfw'].args['potential_angle'] = \
        potentials[0]['angle_pos']['float']

      

    
      
    scale_radius = l.profiles.nfw.scale_radius(space.lens[0].profiles['nfw'].args['mass'], \
                                               space.lens[0].profiles['nfw'].args['conc'],\
                                               potentials[0]['z_lens']['float'])

    space.lens[0].profiles['nfw'].args['scale_radius'] = scale_radius
    
    for iHalo in range(1,len(potentials)):
        space.add_lens()
        space.lens[iHalo].redshift = potentials[0]['z_lens']['float']
        space.source[iHalo].redshift = 1.0
        space.lens[iHalo].ra = potentials[iHalo]['ra']['float']
        space.lens[iHalo].dec = potentials[iHalo]['dec']['float']

        if halos is not None:
            space.lens[iHalo].ra = halos['halos'][iHalo]['gal']['ra'][0]
            space.lens[iHalo].dec = halos['halos'][iHalo]['gal']['dec'][0]
        
        space.lens[iHalo].profiles['nfw'].args['mass'] = \
          potentials[iHalo]['m200']['str'].astype(np.double)
        space.lens[iHalo].profiles['nfw'].args['conc'] = \
          potentials[iHalo]['concentration']['float']
        space.lens[iHalo].profiles['nfw'].args['ellipticity'] = \
            potentials[iHalo]['ellipticite']['float']
        space.lens[iHalo].profiles['nfw'].args['potential_angle'] = \
            potentials[iHalo]['angle_pos']['float']
                
        scale_radius = l.profiles.nfw.scale_radius(space.lens[iHalo].profiles['nfw'].args['mass'], \
                                               space.lens[iHalo].profiles['nfw'].args['conc'],\
                                               potentials[iHalo]['z_lens']['float'])

                                               

        space.lens[iHalo].profiles['nfw'].args['scale_radius'] = scale_radius
    


    
    space.reload(positions=False)

    space.weak_lensing()
    
    
    

    return space
