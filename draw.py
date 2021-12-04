import tkinter as tk
from main import calculate
import sys
import os
import cv2
from PIL import Image

def save_as_png(canvas,fileName):
    # save postscipt image 
    canvas.postscript(file = fileName + '.eps') 
    # use PIL to convert to PNG 
    img = Image.open(fileName + '.eps') 
    img.save(fileName + '.png', 'png') 

class DrawApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.previous_x = self.previous_y = 0
        self.x = self.y = 0
        self.points_recorded = []
        self.canvas = tk.Canvas(self, width=1024, height=420, bg = "white", cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        #self.button_print = tk.Button(self, text = "Display points", command = self.print_points)
        #self.button_print.pack(side="top", fill="both", expand=True)
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        self.button_calculate = tk.Button(self, text = "Calculate", command = self.calculate)
        self.button_clear.pack(side="top", fill="both", expand=True)
        self.button_calculate.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Motion>", self.tell_me_where_you_are)
        self.canvas.bind("<B1-Motion>", self.draw_from_where_you_are)

    def clear_all(self):
        self.canvas.delete("all")

    def calculate(self):
        try:
            save_as_png(self.canvas, "shots/shot_canvas")
            img = cv2.imread("shots/shot_canvas.png")
            calculate(img)
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
                                self.x, self.y,fill="black", width=20)
        self.points_recorded.append(self.previous_x)
        self.points_recorded.append(self.previous_y)
        self.points_recorded.append(self.x)     
        self.points_recorded.append(self.y)    
        self.previous_x = self.x
        self.previous_y = self.y

if __name__ == "__main__":
    app = DrawApp()
    app.mainloop()