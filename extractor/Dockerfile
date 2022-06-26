ARG UBUNTU_VER=20.04

FROM ubuntu:${UBUNTU_VER}

# System packages 
RUN apt-get update && apt-get install -yq curl wget jq vim
RUN apt-get update && apt-get install -y software-properties-common gcc

RUN apt-get update && apt-get install -y python3.10 python3-distutils python3-pip python3-apt
RUN python3 -m pip install --upgrade pip

ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Get browser
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y

# Copy files
RUN mkdir /project
WORKDIR /project
COPY . /project

# Install dependencies
RUN pip3 install -r requirements.txt

# ENTRYPOINT [ "python", "main.py"]