#Image gui loader

import glob
import PySimpleGUI as sg
from PIL import Image, ImageTk
import shutil

from google.protobuf.descriptor import EnumDescriptor

# absolute path
#src_path = r"E:\pynative\reports\sales.txt"
#dst_path = r"E:\pynative\account\sales.txt"
#shutil.move(src_path, dst_path)

glob_path = ""

def parse_folder(path):
    images = glob.glob(f'{path}/*.jpg') + glob.glob(f'{path}/*.png')
    return images
def load_image(path, window):
    try:
        image = Image.open(path)
        global glob_path
        glob_path = path
        image = image.resize((320,320), resample=Image.BICUBIC)
        image.thumbnail((320, 320))
        photo_img = ImageTk.PhotoImage(image)
        window["image"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")
        
def main():
    elements = [
        [sg.Image(size=(320,320), key="image")],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), enable_events=True, key="file"),
            sg.FolderBrowse(),
        ],
        [
            sg.Button("Prev"),
            sg.Button("Next --> move to 1"),
            sg.Button("Next --> move to SLASH")
        ]
    ]
    window = sg.Window("Image Viewer", elements, size=(475, 475))
    images = []
    location = 0
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "file":
            images = parse_folder(values["file"])
            if images:
                load_image(images[0], window)
        if event == "Next --> move to 1" and images:
            if location == len(images) - 1:
                print("EOF")
            else:
                location += 1
            load_image(images[location], window)
        if(event == "Next --> move to SLASH") and images:
            if location == len(images) - 1:
                print("EOF")
            else:    
                src_path = images[location]
                name_im = images[location][str(images[location]).rfind('/'):]
                dst_path = images[location][0:str(images[location]).rfind('/')]
                dst_path = dst_path[0:str(dst_path).rfind('/')]
                dst_path = dst_path + "/15" + name_im
                print("Moved ", images[location], " dst = ", dst_path)
                shutil.move(src_path, dst_path)
                location += 1
            load_image(images[location], window)
        if event == "Prev" and images:
            if location == 0:
                location = len(images) - 1
            else:
                location -= 1
            load_image(images[location], window)
    window.close()
if __name__ == "__main__":
    main()