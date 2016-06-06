# sysbio-docker

Serves the purpose of having some systems biology simulation and coversion tools in one place. \
Features:

1. [libSBML](http://sbml.org/Software/libSBML)
2. [libroadrunner](http://libroadrunner.org/) for Python
3. [antimony](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2735663/)
4. Local scripts for simulation and plotting.

## Installation

This repository is linked to [Docker hub](https://hub.docker.com/r/abulovic/sysbio-docker/) via an [automated build](https://docs.docker.com/docker-hub/builds/) process. 
Having all of these tools in Docker format enables easier management of the tools necessary across different Linux machines.

### From Github
You can clone this repo and build the Docker locally:

    git clone https://github.com/abulovic/sysbio-docker.git
    cd sysbio-docker
    docker build -t abulovic/sysbio-docker .

This will create a Docker image named `sysbio` which you can find if you invoke

    docker images

### From Docker Hub

You can clone the docker image directly from Docker hub:

    docker run -ti abulovic/sysbio-docker

After this, you will have a `abulovic/sysbio-docker` image listed under `docker images`.

## Running the image
The way this docker image is being used now is to:

* Run interactive shell through Docker with all tools installed
* Share certain local folders with the Docker image 
* Simulate models and export the data to the shared folders

You can run the Docker image by running the provided `run-docker.sh` script.

## How it works
So, the idea is that you put the models you want to simulate in the local `./models` directory in the SBML (XML) format. You need to put the models there prior to running the docker:

    ./run-docker

Let us presume the name of your model is called `model.xml`. The simulator needs the model file, but it can also accept configuration in json format and the output directory to which the simulation results will be stored:

    ./code/simulator [PATH TO MODEL FILE] --cfg [PATH TO JSON CONFIG] --odir [OUTPUT DIRECTORY]

In your case:

    ./code/simulator ./models/model.xml --odir ./output

The configuration is not necessary, but useful, as I'll explain in a second. If successful, it will give you the output of a format:

    Results stored to:  ./output//ModelName/2016-06-06T20:37:32.778831

You can browse the folder and see that the results of the simulation are stored in the `;` delimited format in a textual file.
You can use this file to generate plots in an interactive IPython notebook using [Plotly](https://plot.ly/)-offline.
Run the following command with the output folder from the previous script:

    ./code/create-notebook ./output//ModelName/2016-06-06T20:37:32.778831

You can now check the content of that folder - you should have a `plotter.ipynb`