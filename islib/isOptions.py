####################################################
###                Loading modules               ###
####################################################
##         Parser for command-line options        ##
import argparse
####################################################

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
                        help='GAMESS input filename containing keywords for inner-shell optimization')

    parser.add_argument('--header-fr', dest='header_frozen',
                        type=str,
                        default='HEADER-FR',
                        help='GAMESS input filename containing keywords for valence optimization')

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

    parser.add_argument('--mrci', dest='mrci',
                        type=bool,
                        default=False,
                        help='enable IS-MRCI calculation after IS-MCSCF')

    parser.add_argument('--skip-mrci', dest='skip_mrci',
                        type=bool,
                        default=False,
                        help='create IS-MRCI calculation input files and skip its calculation')

    parser.add_argument('--mrmp', dest='mrmp',
                        type=bool,
                        default=False,
                        help='enable IS-MRMP calculation after IS-MCSCF')

    parser.add_argument('--skip-mrmp', dest='skip_mrmp',
                        type=bool,
                        default=False,
                        help='create IS-MRMP calculation input files and skip its calculation')

    parser.add_argument('--header-mrci', dest='header_mrci',
                        type=str,
                        default='IS-MRCI',
                        help='GAMESS input filename containing keywords for IS-MRCI calculation')

    parser.add_argument('--header-mrmp', dest='header_mrmp',
                        type=str,
                        default='IS-MRMP',
                        help='GAMESS input filename containing keywords for IS-MRMP calculation')

    parser.add_argument('--skip-mcscf', dest='skip_mcscf',
                        type=bool,
                        default=False,
                        help='skip IS-MCSCF calculation and run previously prepared post-IS-MCSCF calculation')

    return parser.parse_args()

