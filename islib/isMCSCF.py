####################################################
###                Loading modules               ###
####################################################
##            isGAMESS internal modules           ##
from islib.gamessJob import jobSetup, jobSetupMRCI
##        Operating System Interfaces Module      ##
import os
##          High-level operations on files        ##
import shutil
####################################################

class InnerShellMCSCF():
    def __init__(self, gamess_env, options):
        self.fullpath = os.getcwd()
        self.loops = ['IS', 'FR']

        step_count = 1
        self.converged = False

        while not self.converged:
            for step_loop in self.loops:
                self.step = self.Step(step_count, step_loop)
                self.job = jobSetup(self.step, options)

                self.prepare_job_directory(options)
                self.job.run_gamess_job(gamess_env, options)
                self.last = self.job

            self.write_energy_convergence(step_count)
            self.converged = self.check_energy_convergence(options, step_count)
            self.step_last = self.job
            step_count += 1

    def prepare_job_directory(self, options):
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

    def write_energy_convergence(self, _step_count):
        self.log = os.path.join(self.fullpath, 'convergence.log')

        if _step_count == 1:
            with open(self.log, 'w') as file:
                file.write('{:<13s}\t{:<10s}\n'.format('Energy (Hartree)', 'Difference (Hartree)'))
                self.diff = 0.0
                file.write('{:<13.8f}\t{:>10.8f}\n'.format(self.job.output.energy, self.diff))
        else:
            self.diff = self.job.output.energy - self.step_last.output.energy

            with open(self.log, 'a') as file:
                file.write('{:<13.8f}\t{:10.8f}\n'.format(self.job.output.energy, self.diff))

    def check_energy_convergence(self, options, _step_count):
        if ((_step_count >= options.max_steps) or
                ((abs(self.diff) <= options.cutoff) and (_step_count > 1))):
            return True

    class Step():
        def __init__(self, _step_number, _step_type):
            self.number = _step_number
            self.type = _step_type

class InnerShellMRCI():
    def __init__(self, gamess_env, _is_mcscf, options):
        self.fullpath = os.getcwd()

        self.job = jobSetupMRCI(options)

        self.prepare_job_directory(options)
        self.job.run_gamess_job(gamess_env, options)

        self.write_final_energy()

    def prepare_job_directory(self, options):
        os.mkdir(self.job.fullpath)

        _is_mcscf.last.dat.get_dat_geometry()
        _is_mcscf.last.dat.get_dat_orbitals()

        with open(self.job.header.fullpath, 'r') as file:
            header = file.readlines()

        with open(self.job.input.fullpath, 'w') as file:
            for line in header:
                file.write(line)
            for line in _is_mcscf.last.dat.geometry:
                file.write(line)
            for line in _is_mcscf.last.dat.orbitals:
                file.write(line)

    def write_final_energy(self):
        self.log = os.path.join(self.fullpath, 'mrci.log')

        with open(self.log, 'w') as file:
            file.write('{:<13s}\n'.format('Energy (Hartree)'))
            file.write('{:<13.8f}\n'.format(self.job.output.energy))
