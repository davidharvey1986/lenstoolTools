import os as os
import potentiels as pots
import subprocess as sp
import numpy as np
import ipdb as pdb
import read_best as rb
def read_bayesresults( lenstool_dir='./', value_type='median' ):
    '''
    Run the bayesResults.pl script from lenstool on
    the bayes.dat.

    Then read the results into a potential file

    results file should be the full path length

    lenstool_dir : the path to the directory where bayes.dat is

    At the moment only works for NFWs

    the terms it returns are
    stat   : index (using : as delimter)
    median : 0
    best   :1
    mean   :2
    
    '''

    #Record where i am first so i can return at the end
    cwd = os.getcwd()  

    #Move to the director with the bayes.dat and run bayesResuts.pl
    os.chdir( lenstool_dir )
    command=['/Users/DavidHarvey/Library/lenstool_cored/perl/bayesResults.pl']

    process = sp.Popen(command,stdout=sp.PIPE)

    
    result = process.stdout.read().split('\n')
   

    #ids = get_halo_ids( result )

    #poten_list = np.array([ pots.nfw() for i in xrange(len(ids))])

    #Now get the references so i can add ra's, dec's and z_lens
    run_mode, poten_list = rb.read_best()

    ra_ref = run_mode['reference']['ra']
    dec_ref = run_mode['reference']['dec']
    
    ids = np.array([ iPot['identity']['str'] for iPot in poten_list])    
    #for iPot in xrange(len(ids)):
        #poten_list[iPot]['identity']['str'] = ids[iPot]

    if value_type == 'median':
        index = 0
    if value_type == 'best':
        index = 1
    if value_type == 'mean':
        index = 2

    i_list = np.arange(len(poten_list))
    for iRow in result:
        #SOme have no length
        if len(iRow) == 0:
            continue
        #split up the row the id will be the first ite,
        #remove the first char as it is a #
        split_row = iRow.split()
        iID = split_row[0][1:]
        
        
        if np.any(iID == ids):
            par_vals = np.float(iRow.split(':')[2].split()[index])
            if split_row[2] == 'x':
                poten_list[ i_list[iID == ids] ]['x_centre']['float'] = par_vals
                poten_list[ i_list[iID == ids] ]['ra']['float'] = \
                  get_ra( ra_ref, dec_ref, par_vals)
            if split_row[2] == 'y':
                poten_list[ i_list[iID == ids] ]['y_centre']['float'] = par_vals
                poten_list[ i_list[iID == ids] ]['dec']['float'] = \
                  (dec_ref + par_vals/3600.)
            if split_row[2] == 'emass':
                poten_list[ i_list[iID == ids] ]['ellipticite']['float'] = par_vals
            if split_row[2] == 'theta':
                poten_list[ i_list[iID == ids] ]['angle_pos']['float'] = par_vals
            if split_row[2] == 'c':
                poten_list[ i_list[iID == ids] ]['concentration']['float'] = par_vals
            if split_row[2] == 'M200':
                poten_list[ i_list[iID == ids] ]['m200']['str'] = str(par_vals)


    os.chdir( cwd )
    return poten_list

def get_ra( ra_ref, dec_ref, x_centre):
    '''
    Get the ra of an object given its ra reference
    and the offset from this reference according
    to lenstool

    dec_ref and ra in degress x_centre in arcseconds
    '''

    return ra_ref - 1./np.cos(dec_ref*np.pi/180.)*x_centre/3600.




    
def get_halo_ids( results):

    halos_id = np.array([])
    for iRow in results:
        if len(iRow) == 0:
            continue
        iID = iRow.split()[0]
        
        if ('#' in iID) & ('Lhood' not in iID) \
          & ('Chi' not in iID):
            halos_id = np.append( halos_id, iRow.split()[0] )


    return np.unique(halos_id)
            
            
        
