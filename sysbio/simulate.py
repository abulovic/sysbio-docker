#!/usr/bin/env python
import os
import subprocess
from argparse import ArgumentParser
from contextlib import contextmanager

from sysbio.utils import get_imported_models


@contextmanager
def create_delete(fname, mname, _format):
    with open(fname, 'w') as f:
        f.write(mname)
        f.write('\n')
        f.write(_format)
        f.write('\n')
    yield
    os.remove(fname)


def get_parser():
    parser = ArgumentParser()
    parser.add_argument("model", help="Path to model file")
    parser.add_argument("format", help="Model format", choices=['sbml', 'antimony'])
    return parser

_docker_cp = 'docker cp %(source)s data-store:/data/models/'
_docker_cp_latest = 'docker cp latest data-store:/data/models/latest'


def copy_files(mfile, cfile, mname, _format):

    mdir = '/'.join(mfile.split('/')[:-1])

    old_import_len = 0
    if mdir:
        imports = ['%s/%s' % (mdir, _mfile) for _mfile in get_imported_models(mfile)]
    else:
        imports = get_imported_models(mfile)
    imports = set(imports)
    while len(imports) != old_import_len:
        old_import_len = len(imports)
        new_imports = set()
        for f in imports:
            new_imports.update(get_imported_models(f))
        imports.update(new_imports)

    for imp in imports:
        _cp_import = _docker_cp % {
            'source': imp
        }
        p = subprocess.Popen(_cp_import.split(), stdout=subprocess.PIPE)
        out, err = p.communicate()

    # copy model file
    _cp_model = _docker_cp % {
        'source': mfile,
    }
    p = subprocess.Popen(_cp_model.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()

    # copy configuration file
    if os.path.isfile(cfile):
        _cp_cfg = _docker_cp % {
            'source': cfile,
        }
        p = subprocess.Popen(_cp_cfg.split(), stdout=subprocess.PIPE)
        out, err = p.communicate()


def run_simulator(model, _format):
    _simulate_cmd = 'docker run --rm --volumes-from data-store sysbio-simulate python simulator.py %(m)s %(f)s sim' % {
        'm': model,
        'f': _format
    }
    p = subprocess.Popen(_simulate_cmd.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip()

def run_simulation(model, _format):
    model_dir = '/'.join(model.split('/')[:-1])
    model_name = '.'.join(model.split('/')[-1].split('.')[:-1])
    if model_dir:
        cfg_file = '%s.cfg' % '/'.join([model_dir, model_name])
    else:
        cfg_file = '%s.cfg' % model_name

    copy_files(model, cfg_file, model_name, _format)

    d_model_file = '/data/models/%s' % model.split('/')[-1]
    outdir = run_simulator(d_model_file, _format)


    plot_names = list_plots(d_model_file, _format)
    plot_files = ['%s.txt' % name for name in plot_names]

    for _f in plot_files:
        cp_cmd = 'docker cp data-store:%(odir)s/%(file)s .'
        p = subprocess.Popen(cp_cmd % {
                'odir': outdir,
                'file': _f
            }, shell=True)
        out, err = p.communicate()
    return list_plots(d_model_file, _format)

def list_plots(model, _format):
    model_dir = '/'.join(model.split('/')[:-1])
    model_name = '.'.join(model.split('/')[-1].split('.')[:-1])
    cfg_file = '%s.cfg' % '/'.join([model_dir, model_name])

    _list_cmd = 'docker run --rm --volumes-from data-store sysbio-simulate python simulator.py %(m)s %(f)s list-plots' % {
        'm': model,
        'f': _format
    }
    p = subprocess.Popen(_list_cmd.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip().split('\n')

def create_notebook():
    parser = get_parser()
    args = parser.parse_args()
    model = args.model
    _format = args.format

    model_dir = '/'.join(model.split('/')[:-1])
    model_name = '.'.join(model.split('/')[-1].split('.')[:-1])
    if model_dir:
        cfg_file = '%s.cfg' % '/'.join([model_dir, model_name])
    else:
        cfg_file = '%s.cfg' % model_name

    copy_files(model, cfg_file, model_name, _format)

    _create_nb = 'docker run --rm --volumes-from data-store sysbio-plot python create-notebook %(model)s %(format)s' %  {
        'model': model.split('/')[-1],
        'format': _format,
    }

    p = subprocess.Popen(_create_nb.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    nbfile = out.strip()

    if not model_dir:
        model_dir = '.'

    _cp_nb = 'docker cp data-store:%(nbfile)s %(mdir)s' % {
        'nbfile': nbfile,
        'mdir': model_dir
    }
    subprocess.call(_cp_nb, shell=True)


if __name__ == '__main__':
    create_notebook()
