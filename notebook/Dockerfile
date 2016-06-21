FROM ipython/ipython:3.x

MAINTAINER IPython Project <ipython-dev@scipy.org>

ARG UID

RUN useradd --shell=/bin/bash --create-home --home-dir=/home/sysbio --uid $UID sysbio

EXPOSE 8888

RUN pip install --upgrade pip && \
    pip install plotly

ADD notebook.sh /
