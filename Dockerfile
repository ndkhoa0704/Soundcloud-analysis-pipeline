ARG UBUNTU_VER=20.04
# ARG CONDA_VER=latest
# ARG OS_TYPE=x86_64

FROM ubuntu:${UBUNTU_VER}

# System packages 
RUN apt-get update && apt-get install -yq curl wget jq vim
RUN apt-get update && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.10 python3-distutils python3-pip python3-apt
RUN python3 -m pip install --upgrade pip

ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Get browser
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y

# Install miniconda to /miniconda
# ARG CONDA_VER
# ARG OS_TYPE
# RUN curl -LO "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh"
# RUN bash Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh -b -p /miniconda
# RUN rm Miniconda3-${CONDA_VER}-Linux-${OS_TYPE}.sh
# ENV PATH=/miniconda/bin:${PATH}
# RUN conda update -y conda

# Copy files
RUN mkdir /project
WORKDIR /project
COPY . /project

# Setup environment
# RUN conda env create -f environment.yml
# RUN conda init bash
# RUN conda activate workenv

RUN pip3 install -r requirements.txt

CMD ["python3", "-m","main"]