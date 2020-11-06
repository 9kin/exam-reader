FROM python:3.8-slim

WORKDIR /ex

COPY . .

RUN apt-get update
RUN apt-get install -y ffmpeg libsm6 libxext6 ghostscript
RUN pip3 install --upgrade pip
RUN pip3 install .
