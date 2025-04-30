import tkinter as tk
import tkinter.font
from tkinter import filedialog,messagebox
import yt_dlp
import threading 


# Downloading 

def download():
    #print("pressed")
    url = url_entry.get()
    if not url:
        messagebox.showerror("URL Error","Type appropriate URL.")
        return
    
    download_button.config(state="disabled")
    status_label.config(text="downloading...")
    

    def run_download():
        try:
            save_path = filedialog.askdirectory()
            if not save_path:
                raise Exception("Save Path not selected.")
            
            ydl_opts = {
                'outtmpl': f'{save_path}/%(title)s.%(ext)s',  # 저장 경로
                'extractaudio':True,
                'format': 'bestaudio/best',
                'audioformat':'wav',
                'quiet':True, # Do not print messages to stdout. 
                'writeinfojson':True,
                'getcomments':True,

            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])


            status_label.config(text="Download Finished")

        except Exception as e:
            messagebox.showerror("Download Error",f"Download failed:{e}")
            status_label.config(text="")
        
        finally:
            download_button.config(state="normal")

    threading.Thread(target=run_download).start()


# GUI Setup
root = tk.Tk()
screen_w,screen_h = root.winfo_screenwidth(),root.winfo_screenheight()
prog_w,prog_h = 600,600
pos_w,pos_h = int((screen_w - prog_w) / 2) , int((screen_h - prog_h) / 2)

root.title("Youtube Downloader")
root.geometry(f"{prog_w}x{prog_h}+{pos_w}+{pos_h}") 

title_font = tkinter.font.Font(size=20,weight="bold",slant="italic")
title = tk.Label(root,text="Welcome",font= title_font) 
title.pack()

introduction_text = """
Hi, Welcome to Youtube Downloader. 
This application is based on yt-dlp, which is a beautiful library for handling youtube video/audio.
Start your first download by clicking the button below. 
"""

label = tk.Label(root,text=introduction_text)
label.pack()

url_label = tk.Label(root,text="Youtube URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root,width=50)
url_entry.pack(pady=5)


# CheckBoxes

audio_checkbox = tk.Checkbutton(text="Audio Only")
audio_checkbox.pack()



# Download Button
download_button = tk.Button(root,text="Start Download",command=download)
download_button.pack(pady=20)


# Status 
status_label = tk.Label(root,text="")
status_label.pack(pady=5)


root.mainloop()