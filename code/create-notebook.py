import io
from IPython.nbformat import current

_imports = '''import os, sys
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from plotly.graph_objs import Scatter, Figure, Layout'''

_setup = '''init_notebook_mode(connected=True)'''

_ddir = 'data_dir = "../../../%(ddir)s"'

_data_processing = '''figures = {}
for fname in filter(lambda fname: fname.endswith('.txt'), os.listdir(data_dir)):
    title = fname[:-4]
    timecourses = {}
    full_fname = '%s/%s' % (data_dir, fname)
    with open(full_fname) as fin:
        for line in fin:
            data = line.strip().split(';')
            timecourses[data[0]] = [float(val) for val in data[1:]]
        figures[title] = timecourses
'''

_plot = '''layout = Layout(title='%(title)s')
traces = []
_data = figures['%(title)s']
for name, val in _data.iteritems():
    if name == 'time':
        continue
    else:
        traces.append(Scatter(x=_data['time'], y=_data[name], name=name))
iplot({
    'data': traces,
    'layout': layout
    })
'''

if __name__ == '__main__':
    import os, sys
    ddir = sys.argv[-1]
    figures = {}
    for fname in filter(lambda fname: fname.endswith('.txt'), os.listdir(ddir)):
        title = fname[:-4]
        timecourses = {}
        full_fname = '%s/%s' % (ddir, fname)
        with open(full_fname) as fin:
            for line in fin:
                data = line.strip().split(';')
                timecourses[data[0]] = [float(val) for val in data[1:]]
            figures[title] = timecourses
    
    notebook = current.reads('', format='py')
    notebook['worksheets'][0]['cells'].append(current.new_code_cell(_imports))
    notebook['worksheets'][0]['cells'].append(current.new_code_cell(_setup))
    notebook['worksheets'][0]['cells'].append(current.new_code_cell(_ddir % {'ddir': ddir}))
    notebook['worksheets'][0]['cells'].append(current.new_code_cell(_data_processing))

    for fname in figures:
        notebook['worksheets'][0]['cells'].append(current.new_code_cell(_plot % {'title': fname}))


    with io.open('%s/plotter.ipynb' % ddir, 'w', encoding='utf-8') as f:
        current.write(notebook, f, format='ipynb')

