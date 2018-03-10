import os as os

def run(par_file, outdir='.',
        logfile=None,
        lenstool_path=''):
    '''
    run the lenstool program
    using the given par_file
    '''
    CWD =  os.environ['PWD']

    #Change to the desired directory
    os.chdir(outdir)
    
    if logfile is not None:
        command_str = lenstool_path+'lenstool '+par_file+' -n > '+logfile
    else:
        command_str = lenstool_path+'lenstool '+par_file+' -n '
    os.system( command_str)

    #Change back to the original dir
    os.chdir(CWD)
