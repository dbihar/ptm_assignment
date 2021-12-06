import tkinter as tk
from warnings import catch_warnings
from main import calculate
import sys
import os
import cv2
from PIL import Image, ImageGrab
import numpy as np
from tkinter import messagebox
from numpy import isnan

class DrawApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas_counter = 0
        self.previous_x = self.previous_y = 0
        self.x = self.y = 0
        self.points_recorded = []
        self.canvas = tk.Canvas(self, width=1300, height=620, bg = "white", cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        import tkinter.font as font
        buttonFont = font.Font(family='Helvetica', size=16, weight='bold')
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all, font = buttonFont)
        self.button_calculate = tk.Button(self, text = "Calculate", command = self.calculate, font = buttonFont)
        self.button_clear.pack(side="top", fill="both", expand=True)
        self.button_calculate.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Motion>", self.tell_me_where_you_are)
        self.canvas.bind("<B1-Motion>", self.draw_from_where_you_are)

    def clear_all(self):
        self.canvas.delete("all")

    def calculate(self):
        try:          
            x, y = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            # take a snapshot on the canvas and save the image to file
            img = ImageGrab.grab((x+10, y+10, x+w-10, y+h-10)).convert('RGB') 
            opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            img.save('shots/shot_canvas.png', 'png')
            solution, expression = calculate(opencvImage)
            messagebox.showinfo("Information", "Expression: " + expression + " = " + str(solution))

        except KeyboardInterrupt:
            print('Expression not correct')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    def print_points(self):
        if self.points_recorded:
            self.points_recorded.pop()
            self.points_recorded.pop()
        self.canvas.create_line(self.points_recorded, fill = "black", width=20)
        self.points_recorded[:] = []

    def tell_me_where_you_are(self, event):
        self.previous_x = event.x
        self.previous_y = event.y

    def draw_from_where_you_are(self, event):

        if self.points_recorded:
            self.points_recorded.pop()
            self.points_recorded.pop()

        self.x = event.x
        self.y = event.y
        self.canvas.create_line(self.previous_x, self.previous_y, 
                                self.x, self.y,fill="black", width=17)
        self.points_recorded.append(self.previous_x)
        self.points_recorded.append(self.previous_y)
        self.points_recorded.append(self.x)     
        self.points_recorded.append(self.y)    
        self.previous_x = self.x
        self.previous_y = self.y

if __name__ == "__main__":
    app = DrawApp()
    app.mainloop()