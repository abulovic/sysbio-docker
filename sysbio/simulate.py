#!/usr/bin/env python
import os
import subprocess
from argparse import ArgumentParser
from contextlib import contextmanager

@contextmanager
def create_delete(fname, mname):
    with open(fname, 'w') as f:
        f.write(mname)
    yield
    os.remove(fname)


def get_parser():
    parser = ArgumentParser()
    parser.add_argument("model", help="SBML xml file containing the model")
    return parser

_docker_cp = 'docker cp %(source)s data-store:/data/models/%(mname)s.%(type)s'
_docker_cp_latest = 'docker cp latest data-store:/data/models/latest'


def copy_files(mfile, cfile, mname):
    # copy model file
    _cp_model = _docker_cp % {
        'source': mfile,
        'mname': mname,
        'type': 'xml'
    }
    subprocess.call(_cp_model)

    # copy configuration file
    if os.path.isfile(cfile):
        _cp_cfg = _docker_cp % {
            'source': cfile,
            'mname': mname,
            'type': 'cfg'
        }
        subprocess.call(_cp_cfg)

    # write down the name of the model to simulate
    # in the indicator file - /data/models/latest
    with create_delete('latest', mname):
        subprocess.call(_docker_cp_latest)

def run_simulator():
    _simulate_cmd = 'docker run --rm --volumes-from data-store sysbio-simulate python simulator'
    p = subprocess.Popen(_simulate_cmd.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip()

def run_plot(outdir):
    _plot_cmd = 'docker run --rm --volumes-from data-store sysbio-plot python create-notebook %s' % outdir
    subprocess.call(_plot_cmd)

def main():

    parser = get_parser()
    args = parser.parse_args()

    model_dir = '/'.join(args.model.split('/')[:-1])
    model_name = '.'.join(args.model.split('/')[-1].split('.')[:-1])
    cfg_file = '%s.cfg' % '/'.join([model_dir, model_name])

    copy_files(args.model, cfg_file, model_name)

    outdir = run_simulator()

    run_plot(outdir)

    subprocess.call('docker run --rm -ti --volumes-from data-store ubuntu tar -zcvf %(odir)s/%(mname)s.tar.gz %(odir)s --directory=%(odir)s' % {
            'odir': outdir,
            'mname': model_name
        })

    subprocess.call('docker cp data-store:/%(odir)s/%(mname)s.tar.gz .' % {
            'odir': outdir,
            'mname': model_name
        })


if __name__ == '__main__':
    main()
