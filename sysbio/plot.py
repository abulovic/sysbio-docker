from collections import OrderedDict

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout, Bar



def plot_timecourse(tname):
    fname = '%(tname)s.txt' % {'tname': tname}
    title = tname
    timecourses = {}
    with open(fname) as fin:
        for line in fin:
            data = line.strip().split(';')
            timecourses[data[0]] = [float(val) for val in data[1:]]

    layout = Layout(title=title)
    traces = []
    for name, val in timecourses.iteritems():
        if name == 'time':
            continue
        else:
            traces.append(Scatter(x=timecourses['time'], y=timecourses[name], name=name))
    iplot({
        'data': traces,
        'layout': layout
        })
    fig = Figure(data=traces, layout=layout)
    return fig

def plot_steady_state(ss_fname):
    fname = '%s.txt' % ss_fname
    data = OrderedDict()
    with open(fname) as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            name, value = line.split(';')
            data[name] = float(value)

    data = [Bar(
            x = data.values(),
            y = data.keys(),
            orientation = 'h'
        )]
    layout = Layout(
            title=ss_fname,
            xaxis=dict(
                    type='log',
                    autorange=True
                )
        )

    fig = Figure(data=data, layout=layout)
    return fig
