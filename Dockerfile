FROM python:3
RUN mkdir photomath
ADD draw.py /photomath
ADD flask_camera.py /photomath
ADD requirements.txt /photomath
ADD expression_calculator.py /photomath
ADD character_classifier_train.py /photomath
ADD character_classifier_detect.py /photomath
ADD character_separator.py /photomath
ADD image_gui_loader.py /photomath
ADD main.py /photomath
ADD Model /photomath
ADD Characters /photomath
ADD img /photomath
ADD shots /photomath
ADD templates /photomath

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y python3-opencv
RUN pip3 install opencv-python

RUN pip3 uninstall protobuf
RUN pip3 install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.12.0-py3-none-any.whl
RUN pip3 install -U protobuf==3.0.0b2
