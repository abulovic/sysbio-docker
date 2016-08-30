# sysbio-docker

This is a tool I've developed for the purpose of having easily installable tool for simulation and visualization of systems biology ODE models.
Because of complexities during the installation of some of the modules required, I've decided to dockerize the entire thing - so the only thing you need to install now is [Docker](https://www.docker.com/) itself.

The currently supported model input format is [SBML](http://sbml.org/Main_Page), loaded into Python through [libSBML](http://sbml.org/Software/libSBML).
For the purposes of simulation, the tool uses [libroadrunner](http://libroadrunner.org/).
The desired simulation output can be easily configured through a **json-based config file** to output different combinations of species in different timecourses, or to output them all together in one plot. The same configuration file enables you to configure the numerical solver and accepts all the parameters which can be passed onto [RoadRunner.simulate](http://sys-bio.github.io/roadrunner/python_docs/api_reference.html#RoadRunner.RoadRunner.simulate) method (more on configuration below).
The plots are then generated through [IPython](https://ipython.org/) API for creating notebooks, and [Plotly](https://plot.ly/python/) is used for interactive graph generation.

## Installation

To be able to install this tool, you first have to install [Docker](https://www.docker.com/) (detailed installation instructions for all OSs provided on their site). 
After that, you can clone this repository:

    git clone https://github.com/abulovic/sysbio-docker.git

after which you can create [virtual environment](https://virtualenv.pypa.io/en/stable/) by running

    cd sysbio-docker
    virtualenv env
    source env/bin/activate # or env/Scripts/activate on windows

In this environment we will install all that is required to look at our beautiful interactive [jupyter](http://jupyter.readthedocs.io/en/latest/)-based plots.
Let's install this tool:

    python setup.py build install

And now let's setup the docker part of our system

    python setup.py build_docker

Now we're good to go.

## Usage

For ease of usage, there is an example model provided in the repository, and can be found in the `./models` directory. The showcase model is [this one](http://identifiers.org/pubmed/1833774).

The idea of this tool is to give you an interactive IPython notebook though which you can invoke the simulation and visualize the results in the same place, and that interactively. Here is how to to about it:

    cd ./models
    create-notebook BIOMD0000000003.xml sbml
    ipython notebook

First command will position you in the directory where the model is located. If you look in that directory, you will notice that there are two files there. One is an `xml` file - the model in the SBML format, and the other is the `cfg` file, which is the configuration file in JSON format. This file has to be in the same directory as the model, and with the same name to be recognized by the simulator. This file enables you to configure the numeric integrator and plotting details. Configuration details are described in the next chapter.

The second command will create an IPython notebook in the same directory, which will have some basic code to run your simulation and to plot the results. With the third command you run the interactive web tool in which you can open the notebook, and run the commands consecutively. 
Running the code should give you a plot like this one:


![example-plot](https://cloud.githubusercontent.com/assets/1510530/18082444/4747af4e-6e9f-11e6-8589-44d80159ff7f.png)

