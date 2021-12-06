from flask import Flask, render_template, Response, request, flash
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from main import calculate

global capture,rec_frame,  switch, rec, out 
capture=0
switch=1
rec=0

#Make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Instatiate flask app  
app = Flask(__name__, template_folder='./templates')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success: 
            if(capture):
                capture=0
                #now = datetime.datetime.now()
                global p
                cv2.imwrite(p, frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            flash('Frame captured')
            capture=1 
        elif  request.form.get('stop') == 'Calculate':
            img = cv2.imread(p)
            try:
                solution, expression = calculate(img)
                flash("Expression: " + expression + " = " + str(solution))
            except KeyboardInterrupt:
                print('Interrupted')
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    import os
    import sys
    os.chdir(sys.path[0])
    p = os.path.sep.join(['shots', "shot_1.jpg"])
    app.run()