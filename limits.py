import numpy as np


def get_limit( profil ):
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
    m200 = np.array(('m200', 0, '1e13', '1e16', '1e12'), \
            dtype=[('name', object), ('int', int),('lo', object), ('hi', object), ('res', object)])
    concentration = np.array(('concentration', 0, 0, 20, 0.1), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi', float), ('res', float)])
    x_centre = np.array(('x_centre', 0, -25, 25, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    y_centre = np.array(('y_centre', 0, -25, 25, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    ellipticite = np.array(('ellipticite', 0, 0, 1, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    angle_pos = np.array(('angle_pos', 0, 0, 180, 0.1), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    alpha = np.array(('alpha', 0, 0, 1, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    e1 = np.array(('e1', 0, -1, 1, 0.01), \
                dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    e2 = np.array(('e2', 0, -1, 1, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    return { 'x_centre':x_centre, 'y_centre':y_centre, \
            'ellipticite':ellipticite, 'angle_pos':angle_pos, \
            'm200':m200, 'concentration':concentration, 'alpha':alpha,\
                 'e1':e1, 'e2':e2}

def piemd():
    core_radius = np.array(('core_radius', 0, 0., 1000., 0.1), \
            dtype=[('name', object), ('int', int),('lo', object), ('hi', object), ('res', object)])
    cut_radius = np.array(('cut_radius', 0, 0, 1000, 0.1), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi', float), ('res', float)])
    x_centre = np.array(('x_centre', 0, -25, 25, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    y_centre = np.array(('y_centre', 0, -25, 25, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    ellipticite = np.array(('ellipticite', 0, 0, 1, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    angle_pos = np.array(('angle_pos', 0, 0, 180, 0.1), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    v_disp = np.array(('v_disp', 0, 0., 1000., 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    e1 = np.array(('e1', 0, -1, 1, 0.01), \
                dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    e2 = np.array(('e2', 0, -1, 1, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])

    return { 'x_centre':x_centre, 'y_centre':y_centre, \
            'ellipticite':ellipticite, 'angle_pos':angle_pos, \
            'core_radius':core_radius, 'cut_radius':cut_radius, \
            'v_disp':v_disp, 'e1':e1, 'e2':e2 }

def skewed_piemd():
    core_radius = np.array(('core_radius', 1, 0., 1000., 0.1), \
            dtype=[('name', object), ('int', int),('lo', object), ('hi', object), ('res', object)])
    cut_radius = np.array(('cut_radius', 1, 0, 1000, 0.1), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi', float), ('res', float)])
    x_centre = np.array(('x_centre', 1, -25, 25, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    y_centre = np.array(('y_centre', 1, -25, 25, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    ellipticite = np.array(('ellipticite', 1, 0, 1, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    angle_pos = np.array(('angle_pos', 1, 0, 180, 0.1), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    v_disp = np.array(('v_disp', 1, 0., 1000., 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    alpha = np.array(('alpha', 1, -0.3, 0.3, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
    beta = np.array(('beta', 1, 0., np.pi, 0.01), \
            dtype=[('name', object), ('int', int),('lo', float), ('hi',object), ('res', float)])
            
    return { 'x_centre':x_centre, 'y_centre':y_centre, \
            'ellipticite':ellipticite, 'angle_pos':angle_pos, \
            'core_radius':core_radius, 'cut_radius':cut_radius, \
            'v_disp':v_disp, 'alpha':alpha, 'beta':beta }
