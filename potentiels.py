import numpy as np

def get_profile( profil ):
    '''
    Given the profil number return that profile
    '''

    if profil == 12:
        return nfw()

    if profil == 81:
        return piemd()
    
    if profil == 813:
        return skewed_piemd()
    

def nfw():
    '''
    The nfw potential for lenstool
    '''
    profil = np.array(('profil', 12), \
                    dtype=[('name', object), ('int', int)])
    identity = np.array(('identity', 'O1'), \
                    dtype=[('name', object), ('str', object)])
    m200 = np.array(('m200', '1e14'), \
                    dtype=[('name', object), ('str', object)])
    z_lens = np.array(('z_lens', 0.3), \
                    dtype=[('name', object), ('float', float)])
    concentration = np.array(('concentration', 4.35), \
                    dtype=[('name', object), ('float', float)])
    x_centre = np.array(('x_centre', 0), \
                    dtype=[('name', object), ('float', float)])
    y_centre = np.array(('y_centre', 0), \
                    dtype=[('name', object), ('float', float)])
    ellipticite=np.array(('ellipticite', 0), \
                    dtype=[('name', object), ('float',float)])
    angle_pos=np.array(('angle_pos', 0), \
                    dtype=[('name', object), ('float', float)])
    alpha=np.array(('alpha', 0), \
                    dtype=[('name', object), ('float', float)])
                    
    return { 'profil':profil, 'x_centre':x_centre, 'y_centre':y_centre, \
            'ellipticite':ellipticite, 'angle_pos':angle_pos, \
            'm200':m200, 'concentration':concentration, 'z_lens':z_lens,\
            'alpha':alpha, 'identity':identity}


def piemd():
    '''
    The piemd profile
    Eliasdottir et al. 2007 (http://arxiv.org/abs/0710.5636).
    
    '''

    profil = np.array(('profil', 81), \
                    dtype=[('name', object), ('int', int)])
    z_lens = np.array(('z_lens', 0.3), \
                    dtype=[('name', object), ('float', float)])
    x_centre = np.array(('x_centre', 0), \
                    dtype=[('name', object), ('float', float)])
    y_centre = np.array(('y_centre', 0), \
                    dtype=[('name', object), ('float', float)])
    ellipticity=np.array(('ellipticite', 0), \
                    dtype=[('name', object), ('float', float)])
    angle_pos=np.array(('angle_pos', 0), \
                    dtype=[('name', object), ('float', float)])
    core_radius=np.array(('core_radius', 1.0), \
                    dtype=[('name', object), ('float', float)])
    cut_radius=np.array(('cut_radius', 450), \
                    dtype=[('name', object), ('float', float)])
    v_disp=np.array(('v_disp', 300), \
                    dtype=[('name', object), ('float', float)])
                    
    identity = np.array(('identity', 'O1'), \
                    dtype=[('name', object), ('str', object)])
                    
    return { 'profil':profil, 'x_centre':x_centre, 'y_centre':y_centre, \
            'ellipticite':ellipticity, 'core_radius':core_radius, \
            'cut_radius':cut_radius, 'v_disp':v_disp, 'z_lens':z_lens,
            'angle_pos':angle_pos, 'identity':identity}

def skewed_piemd():
    '''
    The piemd profile
    Eliasdottir et al. 2007 (http://arxiv.org/abs/0710.5636).
    
    '''

    profil = np.array(('profil', 813), \
                    dtype=[('name', object), ('int', int)])
    z_lens = np.array(('z_lens', 0.3), \
                    dtype=[('name', object), ('float', float)])
    x_centre = np.array(('x_centre', 0), \
                    dtype=[('name', object), ('float', float)])
    y_centre = np.array(('y_centre', 0), \
                    dtype=[('name', object), ('float', float)])
    ellipticity=np.array(('ellipticite', 0), \
                    dtype=[('name', object), ('float', float)])
    angle_pos=np.array(('angle_pos', 0), \
                    dtype=[('name', object), ('float', float)])
    core_radius=np.array(('core_radius', 1.0), \
                    dtype=[('name', object), ('float', float)])
    cut_radius=np.array(('cut_radius', 450), \
                    dtype=[('name', object), ('float', float)])
    v_disp=np.array(('v_disp', 300), \
                    dtype=[('name', object), ('float', float)])
    alpha=np.array(('alpha', 0), \
                    dtype=[('name', object), ('float', float)])
    beta=np.array(('beta', 0), \
                    dtype=[('name', object), ('float', float)])
    identity = np.array(('identity', 'O1'), \
                    dtype=[('name', object), ('str', object)])
    return { 'profil':profil, 'x_centre':x_centre, 'y_centre':y_centre, \
            'ellipticite':ellipticity, 'core_radius':core_radius, \
            'cut_radius':cut_radius, 'v_disp':v_disp, 'z_lens':z_lens,
            'angle_pos':angle_pos, 'alpha':alpha, 'beta':beta, 'identity':identity}
