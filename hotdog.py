import tkinter as tk 
import requests
from io import BytesIO
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

import os
from dotenv import load_dotenv

# List of widgets can be found here https://www.tutorialspoint.com/python/python_gui_programming.htm with documentation 
# on how to add arguments and control both positioning and control 

# Define general variables 
height = 400
width = 600

load_dotenv()
key = os.getenv("KEY")
endpoint = os.getenv("ENDPOINT")

print(key, endpoint)

# Allows the selected background image to change with the shape of the window
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    backgroundLabel.config(image = photo)
    backgroundLabel.image = photo #avoid garbage collection

def clearFrame():
    for widget in imgFrame.winfo_children():
        widget.destroy()
    for widget in captionFrame.winfo_children():
        widget.destroy()
    
def getCaptionWithURL(imgUrl):
    clearFrame()
    tagColor=""

    headers={'Content-Type':'application/json','Prediction-Key': key}
    response = requests.post(endpoint,json={"Url":imgUrl},headers=headers)
    analysis = response.json()
    print(analysis)
    tag = analysis["predictions"][0]["tagName"]
    print(tag)

    if (tag == "Hotdog"):
        tagColor = "green"
    else:
        tagColor = "red"

    response = requests.get(imgUrl)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    imgBlock = tk.Label(imgFrame, image=img)
    imgBlock.pack(side="bottom", fill="both", expand="yes")
    imgBlock.image = img

    imgCaption=tk.Label(captionFrame, text=tag, bg="white", fg=tagColor, font=("Helvetica", 45))
    imgCaption.pack(side = "bottom", fill="both", expand = YES)
    entry.delete(0, 'end')

root = tk.Tk()
root.title("Hotdog or not Hotdog")
root.geometry('600x400')

image = Image.open('background.jpg')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
backgroundLabel = tk.Label(root, image = photo)
backgroundLabel.bind('<Configure>', resize_image)
backgroundLabel.pack(fill=BOTH, expand = YES)

canvas = tk.Canvas(root, height=height, width=width)
canvas.pack() 

# There are three ways to position things in Tkinter: place, pack, and grid 
upperFrame = tk.Frame(root, bg='#80c1ff')
upperFrame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n') 

entry = tk.Entry(upperFrame, bg='white', font=("Calibri 12"))
entry.place(relx=0.01, rely=0.5, relwidth=0.65, relheight=0.7, anchor='w')

#Lamda functions are known as inline functions which will rerun everytime it is called allowing us to get the updated input 
button = tk.Button(upperFrame, text="Send URL", bg='gray', command=lambda: getCaptionWithURL(entry.get()))
button.place(relx=0.98, rely=0.5, relwidth=0.3, relheight=0.7, anchor='e') 

imgFrame = tk.Frame(root,highlightbackground="grey", highlightthickness=10, bg="white", bd=10)
imgFrame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.5, anchor='n')
captionFrame = tk.Frame(root,highlightbackground="grey", highlightthickness=4, bg="white", bd=10)
captionFrame.place(relx=0.5, rely=0.75, relwidth=0.75, relheight=0.2, anchor='n')

root.mainloop()