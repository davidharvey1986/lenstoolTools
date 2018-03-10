'''
Run the bayesChires in the c function on best setting only

'''
import os as os
import numpy as np

def bayesChires( par_file, lenstool_dir='./'):
    '''
    Run the bayesChires function and return the
    results

    '''

    #Record where i am first so i can return at the end
    cwd = os.getcwd()

    #Move to the lenstool dir
    os.chdir( lenstool_dir )

    
    command = os.environ['LENSTOOL_DIR']+'/utils/bayesChires '+par_file+' best'
    os.system(command)

    if os.path.isfile( "chires/chires_best.dat"):
        chires_file = open( "chires/chires_best.dat", "rb")
    else:
        raise ValueError("Chires for %s not found" % (par_file))

    N = -1
    image_family_list = []
    for iRow in chires_file:
        image = iRow.split()
        
        if (len(image) > 10):
            if (image[0] != 'N'):

                if N != image[0]:
                    if N != -1:
                        image_family_list.append(iImage_family)
                    N = image[0] 
                    iImage_family = image_family( np.floor(np.float(image[1])), np.float(image[2]) )

            
                iImage_family.append_image( image )
    
            
    os.chdir(cwd)
    return image_family_list

class image_family(dict):
    
    def __init__( self, family, redshift ):
        self.__dict__['family'] = family
        self.__dict__['redshift'] = redshift
        self.__dict__['label'] = np.array([])
        self.__dict__['rmss'] = np.array([])
        self.__dict__['rmsi'] = np.array([])
        self.__dict__['dx'] = np.array([])
        self.__dict__['dy'] = np.array([])

    def append_image( self, chires_row ):
        
        if (chires_row[10] != 'N/A' ) & (chires_row[11] != 'N/A'):
            self.label = np.append(self.label, np.float(chires_row[1]))
            self.rmss = np.append(self.rmss, np.float(chires_row[8]))
            self.rmsi = np.append(self.rmsi, np.float(chires_row[9]))
            self.dx = np.append(self.dx, np.float(chires_row[10]))
            self.dy = np.append(self.dy, np.float(chires_row[11]))
   

    def keys(self):
        return self.__dict__.keys()
    
    def __getitem__(self, key): 
        return self.__dict__[key]
