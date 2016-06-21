FROM ipython/ipython:latest
#FROM jupyter/notebook

MAINTAINER IPython Project <ipython-dev@scipy.org>

ARG UID

RUN useradd --shell=/bin/bash --create-home --home-dir=/home/sysbio --uid $UID sysbio

EXPOSE 8888

RUN pip install --upgrade pip && \
	pip install jupyter && \
    pip install plotly && \
    pip install nbformat

ADD create-notebook /home/sysbio

WORKDIR /home/sysbio/
