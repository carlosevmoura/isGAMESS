####################################################
###                Loading modules               ###
####################################################
##        Operating System Interfaces Module      ##
import os
##     System-specific parameters and functions   ##
import sys
####################################################

class EnvironmentSetup():
    def __init__(self):
        self.path, self.rungms = self.check_environment()
        self.current = os.getcwd()

    def check_environment(self):
        try:
            path = os.environ['GMSPATH']
            rungms = os.path.join(path, 'rungms')
        except KeyError:
            print('> Environment variable $GMSPATH does not exist.')
            print('Please, set the variable using: export GMSPATH=<GAMESS-DIR-PATH>')
            sys.exit()

        # Check if 'rungms' script is found inside $GMSPATH
        if not os.path.isdir(path):
            print('> Directory $GMSPATH {} does not exist.'.format(path))
            print(
                'Please, set correctly the $GMSPATH variable: export GMSPATH=<GAMESS-DIR-PATH>')
            sys.exit()

        if not os.path.isfile(rungms):
            print('rungms script not found.')
            print('Please, set correctly the $GMSPATH variable: export GMSPATH=\< GAMESS-DIR-PATH\>')
            sys.exit()

        return path, rungms
