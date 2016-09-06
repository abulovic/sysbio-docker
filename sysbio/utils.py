import os
import subprocess
from argparse import ArgumentParser

_file_endings = {
	'sbml': 'xml',
	'antimony': 'txt',
	'cellml': 'txt',
}

_default_cfg = '''{
	"integration": {
		"start": 0,
		"end": 100,
		"steps": 1000,
		"stiff": false
	},
	"plotting": {
		"timecourse": {
			"plot-all": true,
			"plot-groups": false
		}
	}
}
'''


def get_covert_parser():
	p = ArgumentParser()
	p.add_argument('model', help='Path to model file')
	p.add_argument('src_fromat', help='Format of the provided model')
	p.add_argument('dest_format', help='Format after coversion')
	return p

def get_config_parser():
	p = ArgumentParser()
	p.add_argument('model', help='Path to the model for which default config is to be generated')
	return p

def convert(mfile, src_fromat, dest_format):

	mname = mfile.split('/')[-1].split('.')[0]
	mdir = '/'.join(mfile.split('/')[:-1])

	if mdir:
		imports = ['%s/%s' % (mdir, _mfile) for _mfile in get_imported_models(mfile)]
	else:
		imports = get_imported_models(mfile)

	for imp in imports:	
		_docker_cp_to = 'docker cp %(mfile)s data-store:/data/models/to-convert' % {
			'mfile': imp
		}
		subprocess.call(_docker_cp_to, shell=True)


	_docker_cp_to = 'docker cp %(mfile)s data-store:/data/models/to-convert' % {
		'mfile': mfile
	}
	subprocess.call(_docker_cp_to, shell=True)
	_docker_convert = 'docker run --rm --volumes-from data-store sysbio-simulate python converter.py %(src)s %(dest)s' % {
		'src': src_fromat,
		'dest': dest_format
	}
	subprocess.call(_docker_convert, shell=True)
	_docker_cp_from = 'docker cp data-store:/data/models/converted %(mname)s.%(fend)s' % {
		'mname': os.path.sep.join([mdir, mname]),
		'fend': _file_endings[dest_format]
	}
	subprocess.call(_docker_cp_from, shell=True)



def run_conversion():
	parser = get_covert_parser()
	args = parser.parse_args()

	convert(args.model, args.src_fromat, args.dest_format)


def create_default_config(model):
	mname = model.split('/')[-1].split('.')[0]
	mpath = '/'.join(model.split('/')[:-1])

	cfile = '%(odir)s/%(mname)s.cfg' % {
		'odir': mpath,
		'mname': mname
	}

	with open(cfile, 'w') as fout:
		fout.write(_default_cfg)

def run_create_default_config():
	parser = get_config_parser()
	args = parser.parse_args()
	model = args.model

	create_default_config(model)

def get_imported_models(mfile):
	import re

	imports = []
	with open(mfile) as fin:
		for line in fin:
			if line.startswith('import'):
				res = re.match('import +"(.+)"', line.strip())
				if len(res.groups()) == 1:
					imports.append(res.groups()[0])
			else:
				continue
	return imports


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
