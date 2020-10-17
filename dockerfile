# Image

FROM postgres

# Package installation

RUN apt-get update

RUN apt-get install -y sudo

RUN sudo apt-get install -y python3.7
