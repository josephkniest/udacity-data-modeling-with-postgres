# Image

FROM postgres

# CPython and udacity dependencies installation

RUN apt-get update

RUN apt-get install -y sudo

RUN sudo apt-get install -y python3.7

RUN sudo apt-get install -y python3-pip

RUN sudo apt-get install libpq-dev

RUN pip3 install psycopg2

# Drop udacity project files into image

COPY udacity/ /root

# Install some GNU essentials into image

RUN sudo apt-get install nano
