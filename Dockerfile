# Our base image
FROM tensorflow/tensorflow

RUN apt-get install python3-pip
RUN mkdir photomath
ADD draw.py /photomath
ADD flask_camera.py /photomath
ADD requirements.txt /
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

RUN apt-get update && apt-get install -y python3-opencv python3-tk
