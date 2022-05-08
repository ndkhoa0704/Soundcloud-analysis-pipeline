FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# # Environment
# ENV TZ=Asia/Ho_Chi_Minh
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y curl wget python3.10 python3-distutils python3-pip python3-apt
RUN python3 -m pip install --upgrade pip

# # Install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install ./google-chrome-stable_current_amd64.deb -y

# # Download chromedriver
RUN wget -O ./LATEST_RELEASE http://chromedriver.storage.googleapis.com/LATEST_RELEASE && \
        latest=$(cat ./LATEST_RELEASE) && \
        wget -O ./chromedriver.zip "http://chromedriver.storage.googleapis.com/"$latest"/chromedriver_linux64.zip" && \
        unzip -o chromedriver -d ./

# Copy files
RUN mkdir /code
WORKDIR /code
COPY . /code

# Install dependencies
RUN pip3 install -r requirements.txt