####################################################
###                Loading modules               ###
####################################################
##        Operating System Interfaces Module      ##
import os
##     System-specific parameters and functions   ##
import sys
##          Allows to spawn new processes         ##
import subprocess
####################################################

class jobSetup():
    def __init__(self, step, options):
        self.step = step
        self.jobtitle = 'STEP-{:02d}-{:s}'.format(self.step.number, self.step.type)
        self.fullpath = os.path.abspath(self.jobtitle)

        self.input = self.jobInput(self.fullpath, self.jobtitle)
        self.output = self.jobOutput(self.fullpath, self.jobtitle)
        self.dat = self.jobDat(self.fullpath, self.jobtitle)
        self.header = self.jobHeader(self.step, options)

    def run_gamess_job(self, gamess_env, options):
        os.chdir(self.fullpath)
        with open(self.output.fullpath, 'w') as file:
            subprocess.run([gamess_env.rungms, self.input.filename,
                            options.version, options.cpus],
                           stdout=file, stderr=subprocess.DEVNULL)

        os.chdir(gamess_env.current)
        self.output.check_job()
        self.output.get_final_energy()

    class jobInput():
        def __init__(self, _fullpath, _job_title):
            self.filename = '{}.inp'.format(_job_title)
            self.fullpath = os.path.join(_fullpath, self.filename)

    class jobHeader():
        def __init__(self, step, options):
            header_dictionary = {
                'IS': options.header_inner_shell,
                'FR': options.header_frozen
            }

            self.filename = header_dictionary[step.type]
            self.fullpath = os.path.abspath(self.filename)

    class jobOutput():
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
                if '                       TOTAL ENERGY =' in line_data:
                    self.energy = float(line_data.strip().split()[3])

    class jobDat():
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

class jobSetupMRCI():
    def __init__(self, options):
        self.jobtitle = 'MRCI'
        self.fullpath = os.path.abspath(self.jobtitle)

        self.input = self.jobInput(self.fullpath, self.jobtitle)
        self.output = self.jobOutput(self.fullpath, self.jobtitle)
        self.header = self.jobHeader(options)

    def run_gamess_job(self, gamess_env, options):
        os.chdir(self.fullpath)
        with open(self.output.fullpath, 'w') as file:
            subprocess.run([gamess_env.rungms, self.input.filename,
                            options.version, options.cpus],
                           stdout=file, stderr=subprocess.DEVNULL)

        os.chdir(gamess_env.current)
        self.output.check_job()
        self.output.get_final_energy()

    class jobInput():
        def __init__(self, _fullpath, _job_title):
            self.filename = '{}.inp'.format(_job_title)
            self.fullpath = os.path.join(_fullpath, self.filename)

    class jobHeader():
        def __init__(self, options):
            self.filename = options.header_mrci
            self.fullpath = os.path.abspath(self.filename)

    class jobOutput():
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

            for line_number, line_data in list(enumerate(output_data)):
                if '                       TOTAL ENERGY =' in line_data:
                    self.energy = float(line_data.strip().split()[3])

class jobSetupMRMP():
    def __init__(self, options):
        self.jobtitle = 'MRMP'
        self.fullpath = os.path.abspath(self.jobtitle)

        self.input = self.jobInput(self.fullpath, self.jobtitle)
        self.output = self.jobOutput(self.fullpath, self.jobtitle)
        self.header = self.jobHeader(options)

    def run_gamess_job(self, gamess_env, options):
        os.chdir(self.fullpath)
        with open(self.output.fullpath, 'w') as file:
            subprocess.run([gamess_env.rungms, self.input.filename,
                            options.version, options.cpus],
                           stdout=file, stderr=subprocess.DEVNULL)

        os.chdir(gamess_env.current)
        self.output.check_job()
        self.output.get_final_energy()

    class jobInput():
        def __init__(self, _fullpath, _job_title):
            self.filename = '{}.inp'.format(_job_title)
            self.fullpath = os.path.join(_fullpath, self.filename)

    class jobHeader():
        def __init__(self, options):
            self.filename = options.header_mrmp
            self.fullpath = os.path.abspath(self.filename)

    class jobOutput():
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

            for line_number, line_data in list(enumerate(output_data)):
                if '1     E(REF-CI)=' in line_data:
                    self.energy = float(line_data.strip().split()[4])
