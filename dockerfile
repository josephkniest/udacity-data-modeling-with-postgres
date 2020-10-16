# Image

FROM ubuntu

# Package installation

RUN apt-get update

RUN apt-get install -y sudo

RUN apt-get install -y wget

RUN apt-get install -y gnupg2

RUN sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

RUN sudo apt-get -y install postgresql
