import os
from pytube import YouTube
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import threading
import time

# Create a window
root = Tk()
root.geometry('540x150') # Set window size
root.configure(bg='lightblue') # Set background color

# Global variable to control download thread
stop_thread = False

# Function to show progress
def show_progress(stream, chunk, bytes_remaining):
    if stop_thread:
        raise Exception("Download cancelled")
    current = ((stream.filesize - bytes_remaining)/stream.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    progress_bar['value'] = percent
    progress_label.config(text=f'{percent}% downloaded')
    root.update_idletasks()

# Function to download video
def download():
    global stop_thread
    stop_thread = False
    download_button.config(state=DISABLED)
    start_time = time.time()
    try:
        urls = url_input.get().split(',')
        for url in urls:
            yt = YouTube(url.strip(), on_progress_callback=show_progress)
            stream = yt.streams.get_by_itag(get_quality())
            output_path = path_input.get()
            output_file = os.path.join(output_path, f"{yt.title}.mp4")
            stream.download(output_path=output_path)
        end_time = time.time()
        time_taken = end_time - start_time
        messagebox.showinfo("Information",f"Download completed! Time taken: {time_taken} seconds")
    except Exception as e:
        if str(e) == "Download cancelled":
            if os.path.exists(output_file):
                os.remove(output_file)
            messagebox.showinfo("Information", "Download cancelled")
        else:
            messagebox.showerror("Error", str(e))
    finally:
        progress_bar['value'] = 0
        progress_label.config(text='')
        download_button.config(state=NORMAL)

# Function to start download in a new thread
def start_download():
    download_thread = threading.Thread(target=download)
    download_thread.start()

# Function to stop download
def stop_download():
    global stop_thread
    stop_thread = True

# Function to get quality
def get_quality():
    quality = quality_var.get()
    if quality == 'sd':
        return 18
    elif quality == 'hd':
        return 22
    elif quality == '4k':
        return 313

# Function to select path
def select_path():
    path = filedialog.askdirectory()
    path_input.delete(0, END)  # Remove current text in entry
    path_input.insert(0, path)  # Insert the 'path'

# Create labels
url_label = Label(root, text="URLs here (comma separated):")
url_label.grid(row=0, column=0)
path_label = Label(root, text="Path here:")
path_label.grid(row=1, column=0)
download_label = Label(root, text="Download here:")
download_label.grid(row=2, column=0)

# Create input fields
url_input = Entry(root, width=50)
url_input.grid(row=0, column=1)

# Create path selection button
path_button = Button(root, text='Select Path', command=select_path)
path_button.grid(row=1, column=2)

path_input = Entry(root, width=50)
path_input.grid(row=1, column=1)

# Create dropdown for quality
quality_var = StringVar(root)
quality_var.set('sd') # default value
quality_options = OptionMenu(root, quality_var, 'sd', 'hd', '4k')
quality_options.grid(row=2, column=1)

# Create download button
download_button = Button(root, text='Download', command=start_download)
download_button.grid(row=3, column=1)

# Create cancel button
cancel_button = Button(root, text='Cancel', command=stop_download)
cancel_button.grid(row=3, column=2)

# Create progress bar
progress_bar = ttk.Progressbar(root, length=200, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=3, sticky='we')

# Create progress label
progress_label = Label(root, text='', bg='lightblue')
progress_label.grid(row=5, column=0, columnspan=3)

# Run the window
root.mainloop()