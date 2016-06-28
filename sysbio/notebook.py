#!/usr/bin/env python

import os
import io
import subprocess
from argparse import ArgumentParser

def get_parser():
    parser = ArgumentParser()
    parser.add_argument("RESULT_DIR", help="Directory with comma-separated values of simulation in .txt files")
    parser.add_argument("PLOT_DIR", help="Directory where to store IPython notebook with plots")
    parser.add_argument("NAME", help="Name of the IPython notebook with plots")
    parser.add_argument("--ts", help='Timestamp the Ipython notebook name', action='store_true')
    return parser


if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()
    res_dir = os.path.abspath(args.RESULT_DIR)
    res_dir = res_dir.replace(' ', '\\ ')
    plot_dir = os.path.abspath(args.PLOT_DIR)
    plot_dir = plot_dir.replace(' ', '\\ ')
    notebook_name = args.NAME
    timestamp = args.ts

    docker_cmd = 'docker run -ti -v %(host_odir)s:/home/sysbio/sim-output -v %(host_plot_dir)s:/home/sysbio/plots sysbio-ipython' % {
        'host_odir': res_dir,
        'host_plot_dir': plot_dir
    }

    exec_cmd = '%(docker)s ./create-notebook %(name)s' % {
        'docker': docker_cmd,
        'name': notebook_name
    }

    print
    print exec_cmd
    print

    subprocess.call(exec_cmd, shell=True)
