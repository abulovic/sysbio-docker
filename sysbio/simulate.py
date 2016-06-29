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

_docker_cp = 'docker cp %(source)s data-store:/data/models/'
_docker_cp_latest = 'docker cp latest data-store:/data/models/latest'


def copy_files(mfile, cfile, mname):
    # copy model file
    _cp_model = _docker_cp % {
        'source': mfile,
        'type': 'xml'
    }
    p = subprocess.Popen(_cp_model.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()

    # copy configuration file
    if os.path.isfile(cfile):
        _cp_cfg = _docker_cp % {
            'source': cfile,
            'type': 'cfg'
        }
        p = subprocess.Popen(_cp_cfg.split(), stdout=subprocess.PIPE)
        out, err = p.communicate()

    # write down the name of the model to simulate
    # in the indicator file - /data/models/latest
    with create_delete('latest', mname):
        subprocess.call(_docker_cp_latest, shell=True)

def run_simulator():
    _simulate_cmd = 'docker run --rm --volumes-from data-store sysbio-simulate python simulator sim'
    p = subprocess.Popen(_simulate_cmd.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip()

def run_plot(outdir):
    _plot_cmd = 'docker run --rm --volumes-from data-store sysbio-plot python create-notebook %s' % outdir
    subprocess.call(_plot_cmd, shell=True)

def main():

    parser = get_parser()
    args = parser.parse_args()

    model_dir = '/'.join(args.model.split('/')[:-1])
    model_name = '.'.join(args.model.split('/')[-1].split('.')[:-1])
    cfg_file = '%s.cfg' % '/'.join([model_dir, model_name])

    copy_files(args.model, cfg_file, model_name)

    outdir = run_simulator()

    ls_cmd = 'docker run --rm -ti --volumes-from data-store ubuntu ls %s' % outdir
    p = subprocess.Popen(ls_cmd.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    files = out.strip().split()

    for _f in filter(lambda f: f.endswith('.txt'), files):
        cp_cmd = 'docker cp data-store:%(odir)s/%(file)s .'
        p = subprocess.Popen(cp_cmd % {
                'odir': outdir,
                'file': _f
            }, shell=True)
        out, err = p.communicate()


def run_simulation(model):

    model_dir = '/'.join(model.split('/')[:-1])
    model_name = '.'.join(model.split('/')[-1].split('.')[:-1])
    if model_dir:
        cfg_file = '%s.cfg' % '/'.join([model_dir, model_name])
    else:
        cfg_file = '%s.cfg' % model_name

    copy_files(model, cfg_file, model_name)

    outdir = run_simulator()

    ls_cmd = 'docker run --rm --volumes-from data-store ubuntu ls %s' % outdir
    p = subprocess.Popen(ls_cmd.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()

    files = filter(lambda f: f.endswith('.txt'), out.strip().split())

    for _f in files:
        cp_cmd = 'docker cp data-store:%(odir)s/%(file)s .'
        p = subprocess.Popen(cp_cmd % {
                'odir': outdir,
                'file': _f
            }, shell=True)
        out, err = p.communicate()
    return list_plots(model)

def list_plots(model):
    model_dir = '/'.join(model.split('/')[:-1])
    model_name = '.'.join(model.split('/')[-1].split('.')[:-1])
    cfg_file = '%s.cfg' % '/'.join([model_dir, model_name])

    copy_files(model, cfg_file, model_name)
    _list_cmd = 'docker run --rm --volumes-from data-store sysbio-simulate python simulator list-plots'
    p = subprocess.Popen(_list_cmd.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip().split()

def create_notebook():
    parser = get_parser()
    args = parser.parse_args()
    model = args.model

    model_dir = '/'.join(model.split('/')[:-1])
    model_name = '.'.join(model.split('/')[-1].split('.')[:-1])
    if model_dir:
        cfg_file = '%s.cfg' % '/'.join([model_dir, model_name])
    else:
        cfg_file = '%s.cfg' % model_name

    copy_files(model, cfg_file, model_name)

    _create_nb = 'docker run --rm --volumes-from data-store sysbio-plot python create-notebook %s' % model.split('/')[-1]
    p = subprocess.Popen(_create_nb.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    nbfile = out.strip()

    _cp_nb = 'docker cp data-store:%(nbfile)s %(mdir)s' % {
        'nbfile': nbfile,
        'mdir': model_dir
    }
    subprocess.call(_cp_nb, shell=True)


if __name__ == '__main__':
    create_notebook()
