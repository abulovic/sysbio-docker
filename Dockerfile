FROM stanleygu/roadrunner

# Install Vim
RUN apt-get install -y vim

# Add antimony binaries to global path
ENV PATH /usr/local/antimony/bin:$PATH