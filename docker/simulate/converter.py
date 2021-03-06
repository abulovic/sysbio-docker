import sys, os
from contextlib import nested

import tellurium as te

converters = {
	'sbml:antimony': te.sbmlToAntimony,
	'antimony:sbml': te.antimonyTosbml,
	'cellml:antimony': te.cellmlFileToAntimony,
	'cellml:sbml': te.cellmlFileToSBML,
}



model = 'to-convert'
src_dest = {
	'src': sys.argv[1],
	'dest': sys.argv[2],
}

os.chdir('/data/models/')

conversion = '%(src)s:%(dest)s' % src_dest

if conversion not in converters:
	raise Exception("Coversion from %(src)s to %(dest)s not available." % src_dest)
else:
	conv = converters[conversion]
	converted_file = 'converted'
	with nested(open(model), open(converted_file, 'w')) as (fin, fout):
		fout.write(conv(fin.read()))
