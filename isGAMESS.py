#!/usr/bin/env python3

####################################################################################################
#                                                                                                  #
#                                           isGAMESS.py                                            #
#           Python script to obtain geometries from a Gaussian09 Optimization Log File             #
#                                                                                                  #
####################################################################################################
### Author: Carlos E. V. de Moura, Ph.D. (https://github.com/carlosevmoura)                      ###
### From isGAMESS repository (https://github.com/carlosevmoura/isGAMESS)                         ###
####################################################################################################
#                                                                                                  #
# Usage: isGAMESS.py <INPUT> --header-is <HEADER_INNER_SHELL> --header-fr <HEADER_FROZEN_SHELL>    #
#                            --cutoff CUTOFF --max-steps MAX_STEPS --version VERSION --cpus CPUS   #
####################################################################################################

#################################################
###              Loading modules              ###
#################################################
##      Operating System Interfaces Module     ##
import os
##   System-specific parameters and functions  ##
import sys
##        High-level operations on files       ##
import shutil
##        Allows to spawn new processes        ##
import subprocess
##       Parser for command-line options       ##
import argparse
#################################################

class GamessJob():
    def __init__(self, _step):
        self.step = _step
        self.jobtitle = 'STEP-{:02d}-{:s}'.format(self.step.number, self.step.type)
        self.fullpath = os.path.abspath(self.jobtitle)

        self.input = self.GamessInput(self.fullpath, self.jobtitle)
        self.output = self.GamessOutput(self.fullpath, self.jobtitle)
        self.dat = self.GamessDat(self.fullpath, self.jobtitle)
        self.header = self.GamessHeader(self.step)

    def run_gamess_job(self):
        os.chdir(self.fullpath)
        with open(self.output.fullpath, 'w') as file:
            subprocess.run([gamess.rungms, self.input.filename,
                            options.version, options.cpus],
                            stdout=file, stderr=subprocess.DEVNULL)

        os.chdir(gamess.current)
        self.output.check_job()
        self.output.get_final_energy()

    class GamessInput():
        def __init__(self, _fullpath, _job_title):
            self.filename = '{}.inp'.format(_job_title)
            self.fullpath = os.path.join(_fullpath, self.filename)

    class GamessHeader():
        def __init__(self, _step):
            header_dictionary = {
                'IS': options.header_inner_shell,
                'FR': options.header_frozen
            }

            self.filename = header_dictionary[_step.type]
            self.fullpath = os.path.abspath(self.filename)

    class GamessOutput():
        def __init__(self, _fullpath, _job_title):
            self.filename = '{}.out'.format(_job_title)
            self.fullpath = os.path.join(_fullpath, self.filename)

        def check_job(self):
            with open(self.fullpath, 'r') as file:
                output_data = file.readlines()

            for line_number, line_data in enumerate(output_data):
                if 'EXECUTION OF GAMESS TERMINATED -ABNORMALLY-' in line_data:
                    print('> ERROR: GAMESS job {} terminated abnormally.'
                            .format(self.filename))
                    sys.exit()

        def get_final_energy(self):
            with open(self.fullpath, 'r') as file:
                output_data = file.readlines()

            for line_number, line_data in reversed(list(enumerate(output_data))):
                if 'FINAL MCSCF ENERGY IS' in line_data:
                    self.energy = float(line_data.strip().split()[4])

    class GamessDat():
        def __init__(self, _fullpath, _job_title):
            self.filename = '{}.dat'.format(_job_title)
            self.fullpath = os.path.join(_fullpath, self.filename)

        def get_dat_geometry(self):
            with open(self.fullpath, 'r') as file:
                raw_geometry = file.readlines()

            for line_number, line_data in enumerate(raw_geometry):
                if '$DATA' in line_data:
                    start_line_number = line_number
                    break

            for line_number, line_data in enumerate(raw_geometry, start=start_line_number):
                if '$END' in line_data:
                    end_line_number = line_number
                    break

            self.geometry = raw_geometry[start_line_number:end_line_number + 1]

        def get_dat_orbitals(self):
            with open(self.fullpath, 'r') as file:
                raw_orbitals = file.readlines()

            for line_number, line_data in enumerate(raw_orbitals):
                if '--- OPTIMIZED MCSCF MO-S ---' in line_data:
                    start_line_number = line_number
                    break

            self.orbitals = raw_orbitals[start_line_number:]

class InnerShellMCSCF():
    def __init__(self):
        self.range = list(range(1, options.max_steps + 1))
        self.loops = ['IS', 'FR']

        for step_number in self.range:
            for step_type in self.loops:
                    self.step = self.Step(step_number, step_type)
                    self.job = GamessJob(self.step)
                    self.prepare_job_directory()
                    self.job.run_gamess_job()
                    self.check_energy_convergence()
                    self.last = self.job

    def prepare_job_directory(self):
        os.mkdir(self.job.fullpath)

        if not hasattr(self, 'last'):
            shutil.copy(options.input, self.job.input.fullpath)
        else:
            self.last.dat.get_dat_geometry()
            self.last.dat.get_dat_orbitals()

            with open(self.job.header.fullpath, 'r') as file:
                header = file.readlines()

            with open(self.job.input.fullpath, 'w') as file:
                for line in header:
                    file.write(line)
                for line in self.last.dat.geometry:
                    file.write(line)
                for line in self.last.dat.orbitals:
                    file.write(line)

    def check_energy_convergence(self):
        if self.step.number == 1:
            with open(self.job.input.fullpath, 'w') as file:
                file.write('{:<13s}\t{:<10s}'.format('Energy (Hartree)', 'Difference (Hartree'))
                file.write('{:13.8f}\t{:10.8f}'.format(self.job.output.energy, 0.0))
        else:
            self.diff = self.job.output.energy - self.last.output.energy

            with open(self.job.input.fullpath, 'w') as file:
                file.write('{:13.8f}\t{:10.8f}'.format(self.job.output.energy, self.diff))

    class Step():
        def __init__(self, step_number, step_type):
            self.number = step_number
            self.type = step_type

class GamessEnvironment():
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

def get_options():
    """Function to obtaing the arguments from Terminal

    Returns:
        obj:options -- options given by user
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('input',
                        type=str,
                        help='GAMESS input filename (usually .inp extension)')

    parser.add_argument('--header-is', dest='header_inner_shell',
                        type=str,
                        default='HEADER-IS',
                        help='???')

    parser.add_argument('--header-fr', dest='header_frozen',
                        type=str,
                        default='HEADER-FR',
                        help='???')

    parser.add_argument('--cutoff', dest='cutoff',
                        type=float,
                        default=0.0001,
                        help='energy cutoff criteria to finish the inner-shell calculation')

    parser.add_argument('--max-steps', dest='max_steps',
                        type=int,
                        default=5,
                        help='max number of double-loop steps to be done')

    parser.add_argument('--version', dest='version',
                        type=str,
                        default='00',
                        help='number of GAMESS executable to be used')

    parser.add_argument('--cpus', dest='cpus',
                        type=str,
                        default='1',
                        help='number of CPUs to be used by GAMESS job')

    return parser.parse_args()

# Main program
if __name__ == '__main__':

    # Checking it GAMESS path is defined
    gamess = GamessEnvironment()

    # Obtaining arguments from terminal
    options = get_options()

    ## IS-MCSCF
    running = InnerShellMCSCF()