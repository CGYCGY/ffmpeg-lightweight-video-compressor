import os
import tkinter as tk
from tkinter import filedialog
from converter import main


options = ['', '-y', False, '-n']


def load_folder():
    file_path_label['text'] = filedialog.askdirectory()
    if not file_path_label['text']:
        file_path_label['text'] = os.getcwd()


def start(mode='compress'):
    global options
    if file_path_label['text'] and file_path_label['text'] != 'Select A Folder':
        # os.system('python video_converter.py ' + file_path_label['text'])
        main(mode, file_path_label['text'], options[option.get()])
    else:
        main(mode, overwrite=options[option.get()])


def start_compress():
    start()


def start_convert():
    start('convert_to_mp4')


root = tk.Tk()
root.title('Video Compressor')
root.geometry("300x350")

option = tk.IntVar(value=0)

load_button = tk.Button(root, command=load_folder, text='Load', bg='grey', fg='white')
file_path_label = tk.Label(root, text=os.getcwd(), fg='green', font=('helvetica', 12, 'bold'), wraplength=190)
option_button_1 = tk.Radiobutton(root, text='Ask everytime', variable=option, value=0)
option_button_2 = tk.Radiobutton(root, text='Overwrite files if exist', variable=option, value=1)
option_button_3 = tk.Radiobutton(root, text='Skip files if exist', variable=option, value=2)
option_button_4 = tk.Radiobutton(root, text='Delete files if exist', variable=option, value=3)
compress_button = tk.Button(root, command=start_compress, text='Compress!', bg='brown', fg='white')
convert_button = tk.Button(root, command=start_convert, text='Convert!', bg='blue', fg='white')

load_button.pack(pady=10)
file_path_label.pack()
option_button_1.pack()
option_button_2.pack()
option_button_3.pack()
option_button_4.pack()
compress_button.pack(pady=10)
convert_button.pack(pady=10)

root.mainloop()
