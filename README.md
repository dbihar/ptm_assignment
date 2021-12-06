# Photomath assignment Daniel Bihar

This project consists of three interfaces to our simple visual expression calculator. 
Interfaces include:
1) A GUI image loader in executable script "image_gui_loader.py"
2) A GUI drawing app input in executable script "draw.py"
3) A Web Flask app in executable script "flask_camera.py"

## Running stand alone GUI apps

## Running modules from command line

### Character classifier module

Character classifier takes images from "./Characters" folderand prints prediction in commandline

	$python3 character_classifier_detect.py

### Character separator module

Character separator take one string argument which is path to image, and saves cropped output in folder "./Characters"

	$python3 character_separator.py ./shots/shot_canvas.png

### Expression module

Expression module takes string as first positional argument and evaluates it. Allowed characters are 0-9, +, *, -, /, (, )

	$python3 expression_calculator.py "2 + 3 - ( 9 * 2 ) / 2 - ( 7 - 20 )"

## Training data download and training model

## Docker
