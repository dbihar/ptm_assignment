#!/usr/bin/env python3
#
#   Loading images GUI
#

import cv2
import io
import os, sys
import PySimpleGUI as sg

from PIL import Image
from main import calculate
from tkinter import messagebox
from numpy import isnan, float

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
def image_load():
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
            sg.Button("Calculate"),
        ],
    ]
    window = sg.Window("Image Viewer", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Load Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())
        if event == "Calculate":
            img = cv2.imread(values["-FILE-"])
            try:
                solution, expression = calculate(img)
                messagebox.showinfo("Information", "Expression: " + expression + " = " + str(solution))
            except KeyboardInterrupt:
                print('Expression not correct')
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)

    window.close()
if __name__ == "__main__":
    os.chdir(sys.path[0])
    image_load()