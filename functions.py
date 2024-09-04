#Libraries
import customtkinter
from CTkMessagebox import CTkMessagebox
import tkinter as tk
from tkinter import filedialog
import os
import math
import lzma
import shutil
import moviepy.editor as mp
from PIL import Image

text_file = [".txt"]
doc_file = [".pdf", ".pptx", ".docx"]
video_file = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm']
audio_file = ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a']
image_file = ['.jpg', '.jpeg', '.png', '.png','.gif']

'''
These are the functions required for the project
'''
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.log10(size_bytes) // 3)
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def upload_file():
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)


    file_size = convert_size(file_size)

    if file_path:
       selected_file.set(file_path)
       file_label.configure(text="File Path: " + file_path)
       file_name_label.configure(text="File Name: " + file_name)
       file_size_label.configure(text="File Size: " + str(file_size))


def get_file_extension(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        return "File does not exist."
    
    # Guess the file type
    try:
        kind = os.path.splitext(file_path)[1].lower() #filetype.guess(file_path)
        if kind is None:
            return "Could not determine the file extension."
        else:
            print(kind)
            return kind
    except Exception as e:
        return f"Error determining file extension: {e}"
    
def compress_image(input_path, output_path, quality=85):
    try:
        with Image.open(input_path) as img:
            img.save(output_path, quality=quality, optimize=True)
        print(f"Image compressed and saved to {output_path}")
    except Exception as e:
        print(f"Error compressing image: {e}")




def compress_media(input_path, output_path, target_resolution=(1280, 720), video_bitrate="500k", audio_bitrate="128k"):

    file_extension = get_file_extension(input_path)
    
    if file_extension in video_file:
#         # Compress video
        video = mp.VideoFileClip(input_path)
        
#         # Resize the video
        video_resized = video.resize(newsize=target_resolution)
        
#         # Write the compressed video to the output path with the specified bitrate
        video_resized.write_videofile(output_path, bitrate=video_bitrate, codec="libx264", audio_bitrate=audio_bitrate)
        CTkMessagebox(title="Successs", message=f"Video compressed and saved to {output_path}", icon="info")
        
    elif file_extension in audio_file:
#         # Compress audio
        audio = mp.AudioFileClip(input_path)
        
#         # Write the compressed audio to the output path with the specified bitrate
        audio.write_audiofile(output_path, bitrate=audio_bitrate)
        CTkMessagebox(title="Success", message=f"Audio compressed and saved to {output_path}", icon="info")
        #print(f"Audio compressed and saved to {output_path}")
    elif file_extension in image_file:
#             # Compress image
        compress_image(input_path, output_path)
        
#     # else:
#     #     print("Unsupported file type. Please provide a valid video or audio file.")


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)

def compress():
    file_path = selected_file.get()
    if not file_path:
        CTkMessagebox(title="Warning", message="Please select a file first.", icon="info")
        return
    
    file_extension = get_file_extension(file_path)
    if file_extension in text_file or file_extension in doc_file:
        print(file_extension)
        output_path = file_path + '.xz'
        try:
            with open(file_path, 'rb') as input_file:
                with lzma.open(output_path, 'wb') as output_file:
                    output_file.write(input_file.read())
            CTkMessagebox(title="Success", message=f"File compressed successfully: {output_path}", icon="info")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="info")
    elif file_extension in video_file or file_extension in audio_file or file_extension in image_file:
        output_path = file_path # + '.compressed'
        try:
            compress_media(file_path, output_path)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="info")
    else:
        CTkMessagebox(title="Warning", message=file_extension + "Sorry! File Type Not Supported.", icon="info")



#Decompression function
def decompress():
    file_path = selected_file.get()
    if not file_path:
        CTkMessagebox(title="warning", message="Please select a file first.", icon="info")
        return

    if not file_path.endswith('.xz'):
        CTkMessagebox(title="warning", message="The file is not an .xz file.", icon="info")
        return

    output_file_path = file_path[:-3]

    try:
        with lzma.open(file_path, 'rb') as f_in:
            with open(output_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        CTkMessagebox(title="Success", message=f"File decompressed successfully: {file_path} to {output_file_path}", icon="info")
    except Exception as e:
        CTkMessagebox(title="Erro", message= f"An error occurred: {e}", icon="info")



def change_scaling_event(new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)

'''
Creating the GUI
'''
root = customtkinter.CTk()
root.geometry("800x450")
root.title("Data Compression Software")


selected_file = tk.StringVar()
type_of_file = tk.StringVar()


# configure grid layout (4x4)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

 # create sidebar frame with widgets
root.sidebar_frame = customtkinter.CTkFrame(root, width=400, corner_radius=0)
root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
root.sidebar_frame.grid_rowconfigure(4, weight=1)


customtkinter.appearance_mode_label = customtkinter.CTkLabel(root.sidebar_frame, text="Appearance Mode:", anchor="w")
customtkinter.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
customtkinter.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(root.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=change_appearance_mode_event)
customtkinter.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
customtkinter.scaling_label = customtkinter.CTkLabel(root.sidebar_frame, text="UI Scaling:", anchor="w")
customtkinter.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
customtkinter.scaling_optionemenu = customtkinter.CTkOptionMenu(root.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=change_scaling_event)
customtkinter.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

#Creating the header
root.header = customtkinter.CTkLabel(root, text="Data Compressor", font=("Arial", 24))
root.header.grid(row=0, column=1, pady=12, padx=10)

#Creating a tab view
root.tabview = customtkinter.CTkTabview(root, width=550)
root.tabview.grid(row=1, column=1, padx=(20, 30), pady=(20, 40), sticky="nsew")
root.tabview.add("Compress")
root.tabview.add("Decompress")
root.tabview.add("Students")

#Confiugurating the tabs
root.tabview.tab("Compress").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
root.tabview.tab("Decompress").grid_columnconfigure(0, weight=1)
root.tabview.tab("Students").grid_columnconfigure((1,3), weight=1)


#Inputing items in the tabs


#Input button
select_file_btn = customtkinter.CTkButton(root.tabview.tab("Compress"), text="Select File", command=upload_file)
select_file_btn.grid(row=0, column=0, padx=20, pady=(20, 10))

file_label = customtkinter.CTkLabel(root.tabview.tab("Compress"), text="No file selected", wraplength=300)
file_label.grid(row=1, column=0, padx=20, pady=(20, 10))

detail_label = customtkinter.CTkLabel(root.tabview.tab("Compress"), text="File details", font=("impact", 20), wraplength=300, width=100)
detail_label.grid(row=0, column=1, padx=20, pady=(20, 10))

file_name_label = customtkinter.CTkLabel(root.tabview.tab("Compress"), text="File Name: ", wraplength=300)
file_name_label.grid(row=1, column=1, padx=20, pady=(20, 10))
file_size_label = customtkinter.CTkLabel(root.tabview.tab("Compress"), text="File size: ", wraplength=300)
file_size_label.grid(row=2, column=1, padx=20, pady=(20, 10))

compress_btn = customtkinter.CTkButton(root.tabview.tab("Compress"), text="Compress", command=compress)
compress_btn.grid(row=4, column=0, padx=20, pady=(20, 10))

#Decompression tab view
#Input button
select_file_btn = customtkinter.CTkButton(root.tabview.tab("Decompress"), text="Select File", command=upload_file)
select_file_btn.grid(row=0, column=0, padx=20, pady=(20, 10))

file_label_1 = customtkinter.CTkLabel(root.tabview.tab("Decompress"), text="No file selected", wraplength=300)
file_label_1.grid(row=1, column=0, padx=20, pady=(20, 10))

detail_label_1 = customtkinter.CTkLabel(root.tabview.tab("Decompress"), text="File details", font=("impact", 20), wraplength=300, width=100)
detail_label_1.grid(row=0, column=1, padx=20, pady=(20, 10))

file_name_label_1 = customtkinter.CTkLabel(root.tabview.tab("Decompress"), text="File Name: ", wraplength=300)
file_name_label_1.grid(row=1, column=1, padx=20, pady=(20, 10))
file_size_label_1 = customtkinter.CTkLabel(root.tabview.tab("Decompress"), text="File size: ", wraplength=300)
file_size_label_1.grid(row=2, column=1, padx=20, pady=(20, 10))

decompress_btn = customtkinter.CTkButton(root.tabview.tab("Decompress"), text="Decompress", command=decompress)
decompress_btn.grid(row=4, column=0, padx=20, pady=(20, 10))

#About tab view
#Input button
detail_label_1 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="NAMES OF STUDENTS", font=("impact", 20), wraplength=300, width=100)
detail_label_1.grid(row=0, column=1, padx=20, pady=(20, 10))

file_name_label_1 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="ABUBAKAR UMAR", wraplength=300)
file_name_label_1.grid(row=1, column=1, padx=20, pady=(20, 10))
file_size_label_2 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="ABBA IBRAHIM MUSA", wraplength=300)
file_size_label_2.grid(row=2, column=1, padx=20, pady=(20, 10))
file_size_label_3 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="ANARUWE OMOLOWO ELIJAH", wraplength=300)
file_size_label_3.grid(row=3, column=1, padx=20, pady=(20, 10))
file_size_label_4 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="FAVOUR MICHEAL", wraplength=300)
file_size_label_4.grid(row=4, column=1, padx=20, pady=(20, 10))
file_size_label_5 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="JOB ENEMONA SHAIBU", wraplength=300)
file_size_label_5.grid(row=1, column=2, padx=20, pady=(20, 10))
file_size_label_6 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="KENNETH BULUS", wraplength=300)
file_size_label_6.grid(row=2, column=2, padx=20, pady=(20, 10))
file_size_label_7 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="LEPNAN ERIC MATEP", wraplength=300)
file_size_label_7.grid(row=3, column=2, padx=20, pady=(20, 10))
file_size_label_8 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="PATRICK DUBA JOSHUA", wraplength=300)
file_size_label_8.grid(row=4, column=2, padx=20, pady=(20, 10))
file_size_label_9 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="RUTH SIMON", wraplength=300)
file_size_label_9.grid(row=1, column=3, padx=20, pady=(20, 10))
file_size_label_10 = customtkinter.CTkLabel(root.tabview.tab("Students"), text="STELLA OBASI", wraplength=300)
file_size_label_10.grid(row=2, column=3, padx=20, pady=(20, 10))


root.mainloop()
