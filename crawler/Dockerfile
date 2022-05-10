FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# # Environment
RUN apt-get update && apt-get install -y wget unzip
    
RUN apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get install -y python3.10 python3-distutils python3-pip python3-apt

# # Install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y

# Copy files
RUN mkdir /code
WORKDIR /code
COPY . /code

# Download chromedriver
RUN wget -O ./LATEST_RELEASE http://chromedriver.storage.googleapis.com/LATEST_RELEASE && \
        latest=$(cat ./LATEST_RELEASE) && \
        wget -O ./chromedriver.zip "http://chromedriver.storage.googleapis.com/"$latest"/chromedriver_linux64.zip" && \
        unzip -o chromedriver -d ./

# Install dependencies
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "getdata.py"]