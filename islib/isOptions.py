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

