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

	_docker_cp_to = 'docker cp %(mfile)s data-store:/data/models/to-convert' % {
		'mfile': mfile
	}
	subprocess.call(_docker_cp_to, shell=True)
	_docker_convert = 'docker run --rm --volumes-from data-store sysbio-simulate python converter %(src)s %(dest)s' % {
		'src': src_fromat,
		'dest': dest_format
	}
	subprocess.call(_docker_convert, shell=True)
	_docker_cp_from = 'docker cp data-store:/data/models/converted %(mname)s.%(fend)s' % {
		'mname': mname,
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
