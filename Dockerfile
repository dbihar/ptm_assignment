# Our base image
FROM tensorflow/tensorflow

RUN apt-get install python3-pip

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y python3-opencv python3-tk
