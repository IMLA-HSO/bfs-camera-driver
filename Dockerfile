ARG BASE_IMAGE=ubuntu:20.04
FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
ENV SHELL /bin/bash

## Essentials
RUN  apt-get update -qq \
   && apt-get install -y \
   software-properties-common build-essential dialog apt-utils curl wget git vim nano ffmpeg cmake tar zip unzip sudo  \
   && rm -rf /var/lib/apt/lists/* 

RUN apt-get update -qq \
  && apt-get install -y python3-pip python-dev\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

## spinnaker-sdk
RUN  apt-get update -qq  \ 
   && apt-get install -y \ 
   libavcodec58 libavformat58 \
   libswscale5 libswresample3 libavutil56 libusb-dev \
   libpcre2-16-0 libdouble-conversion3 libxcb-xinput0 \
   libxcb-xinerama0
RUN wget -P /spinnaker  https://console.box.lenovo.com/v2/delivery/dl_router/a1995795ffba47dbbe45771477319cc3/archive/2.2.0.48/spinnaker_python-2.2.0.48-cp38-cp38-linux_x86_64.tar.gz
RUN wget -P /spinnaker  https://console.box.lenovo.com/v2/delivery/dl_router/a1995795ffba47dbbe45771477319cc3/archive/2.2.0.48/spinnaker-2.2.0.48-Ubuntu20.04-amd64-pkg.tar.gz


#COPY ./docker/spinnaker-2.2.0.48-Ubuntu20.04-amd64-pkg.tar.gz  /spinnaker/spinnaker-2.2.0.48-Ubuntu20.04-amd64-pkg.tar.gz
#COPY ./docker/spinnaker_python-2.2.0.48-cp38-cp38-linux_x86_64.tar.gz /spinnaker/spinnaker_python-2.2.0.48-cp38-cp38-linux_x86_64.tar.gz

WORKDIR /spinnaker
RUN sudo tar -xzf spinnaker-2.2.0.48-Ubuntu20.04-amd64-pkg.tar.gz
RUN sudo tar -xzf spinnaker_python-2.2.0.48-cp38-cp38-linux_x86_64.tar.gz 

##During the installation, some of the dpkg scripts use the `logname` command to get the name of the current user. From my experience, `logname` did not work properly in docker, the command outputs `logname: no login name`. If your `logname` command works correctly, skip this step. The hacky workaround is to replace the `logname` executable with the `whoami` executable with these two commands. 
RUN mv /usr/bin/logname /usr/bin/lognamebak
RUN cp /usr/bin/whoami /usr/bin/logname

COPY ./docker/install_spinnaker_docker.sh /spinnaker/spinnaker-2.2.0.48-amd64/install_spinnaker_docker.sh
WORKDIR /spinnaker/spinnaker-2.2.0.48-amd64
RUN sudo sh install_spinnaker_docker.sh 

WORKDIR /spinnaker
RUN sudo python3.8 -m pip install --upgrade numpy matplotlib
RUN python3.8 -m pip install Pillow==7.0.0
RUN pip3 install spinnaker_python-2.2.0.48-cp38-cp38-linux_x86_64.whl

## publisher
RUN pip3 install pyzmq~=19.0.2
RUN pip3 install opencv-python==4.5.4.58 
RUN pip3 install pyaml

WORKDIR /
COPY ./publisher/calibration.yaml /calibration.yaml
COPY ./publisher/camerapublisher.py /camerapublisher.py


EXPOSE 5557
EXPOSE 5556

CMD [ "python3", "./camerapublisher.py" ]
