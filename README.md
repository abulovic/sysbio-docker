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