#!/usr/bin/env python3

####################################################################################################
#                                                                                                  #
#                                           isGAMESS.py                                            #
#          Python script to obtain Inner-Shell Excited States at MCSCF level using GAMESS          #
#                                                                                                  #
####################################################################################################
### Author: Carlos E. V. de Moura, Ph.D. (https://github.com/carlosevmoura)                      ###
### From isGAMESS repository (https://github.com/carlosevmoura/isGAMESS)                         ###
####################################################################################################
#                                                                                                  #
# Usage: isGAMESS.py <INPUT> --header-is <HEADER_INNER_SHELL> --header-fr <HEADER_FROZEN_SHELL>    #
#                            --cutoff CUTOFF --max-steps MAX_STEPS --version VERSION --cpus CPUS   #
####################################################################################################

####################################################
###                Loading modules               ###
####################################################
##            isGAMESS internal modules           ##
from islib import gamessEnv, isOptions, isMCSCF
##        Operating System Interfaces Module      ##
import os
##     System-specific parameters and functions   ##
import sys
##          High-level operations on files        ##
import shutil
##          Allows to spawn new processes         ##
import subprocess
##         Parser for command-line options        ##
import argparse
####################################################

# Main program
if __name__ == '__main__':

    # Checking it GAMESS path is defined
    gamess = gamessEnv.EnvironmentSetup()

    # Obtaining arguments from terminal
    options = isOptions.get_options()

    # IS-MCSCF
    if not options.skip_mcscf:
        is_mcscf = isMCSCF.InnerShellMCSCF(gamess, options)
    else:
        is_mcscf = None

    # IS-MRCI
    if options.mrci:
        is_mrci = isMCSCF.InnerShellMRCI(gamess, is_mcscf, options)