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
    curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.9.tar.gz
    tar xvfz virtualenv-1.9.tar.gz
    cd virtualenv-1.9
    python virtualenv.py ../env
    cd ..
    source env/bin/activate # or env/Scripts/activate on windows
    pip install --upgrade pip
    pip install --upgrade setuptools

If you want to be able to activate this virtual environment from every location in your shell, run

    echo -ne "\nalias run-sb-docker=\"source [PATH-TO-sysbio-docker]/env/bin/activate\"" >> ~/.bashrc

where you replace the `PATH-TO-sysbio-docker` with an absolute path to the directory where you downloaded sysbio-docker. Next time you start your console, you should be able to start your environment by running

    run-sb-docker

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

## Configuration

The configuration file supports configuring the numerical integration and plotting. 

The numerical integration setup is easy - it supports whatever is supported by the RoadRunner.simulate](http://sys-bio.github.io/roadrunner/python_docs/api_reference.html#RoadRunner.RoadRunner.simulate) method, except for the `plot` option, which could provide you with an automatically generated plot. Example would be:

    "integration": {
        "start": 0,
        "end": 100,
        "stiff": true,
        "steps": 5000
    }

The other part of the configuration is the `plotting` configuration. Example would be:
    
    "plotting": {
        "timecourse": {
            "plot-all": false,
            "plot-groups": true,
            "groups": {
                "CM-plot": {
                    "species": ["C", "M"]
                }
            }
        }
    }

The currently best-tested feature is the `timecourse` plot, which is also the only one I would suggest using for now. Here you can specify if you want to plot all the species with setting the `plot-all` to `true`. You can also specify if you want to provide your own custom groupings of the species, which you can then list in the `groups` section of the config.

For a new model, you can invoke a command `create-config`, which will provide you with a new configuration file in the described format.
