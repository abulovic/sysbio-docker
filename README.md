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

To test whether we've successfuly installed all that's necessary, let's try and simulate a model provided in the repository:

    sb-simulate models/BIOMD0000000003.xml

If the command was successful, you should get a BIOMD0000000003.tar.gz file in your current directory. When you unpack it, you can see the following files listed:

    .
    ..
    BIOMD0000000003.xml
    BIOMD0000000003.cfg
    CM-plot.txt
    X.txt
    plots.ipynb

The first file is the original model we've supplied to the simulator. The second is the configuration file which the program has automatically recognized because it has the same name and is in the same directory as the model file. If you open this file, you will see that using it we've configured both the numerical solver:

    {
        "integration": {
            "start": 0,
            "end": 100,
            "stiff": true
        },
        ...

and how the simulation data will be grouped into output textual files and plots:

    "plotting": {
            "timecourse": {
                "plot-all": false,
                "plot-groups": true,
                "groups": {
                    "CM-plot": {
                        "species": ["C", "M"],
                        "vlines": [],
                        "hlines": []
                    },
                    "X": {
                        "species": ["X"]
                    }
                }
            }
        }

The 'plot-all' option will create an output file with all the species from the model, and the corresponding plot.
The 'groups' option enables you to specify how you want to group species into separate plots and output files. Here we see two plots named 'CM-plot' and 'X'.

This is an example of what the final plot looks like. Notice that this one is not interactive, while the real plots you will get as a result of simulation are.

![example-plot](https://cloud.githubusercontent.com/assets/1510530/16435301/3c40d5a2-3d95-11e6-8854-f381924eea94.png)
