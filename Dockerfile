FROM stanleygu/roadrunner

# Install Vim
RUN apt-get install -y vim

# Add antimony binaries to global path
ENV PATH /usr/local/antimony/bin:$PATH

# Download Antimony to get the examples
RUN mkdir /tmp/antimony && \
	cd /tmp/antimony && \
 	wget http://heanet.dl.sourceforge.net/project/antimony/Antimony%20source/2.8/antimony_src_v2.8.tar.gz && \
 	tar xvf antimony_src_v2.8.tar.gz && \
 	cp -r antimony/doc/examples /usr/local/antimony && \
 	rm -r antimony && \
 	rm antimony_src_v2.8.tar.gz

RUN pip install ipdb

USER user

WORKDIR /home/user
