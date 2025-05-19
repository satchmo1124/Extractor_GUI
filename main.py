import tkinter as tk
import tkinter.font
from tkinter import filedialog,messagebox
import yt_dlp
import threading 
import eyed3

class YoutubeDownloader:
    def __init__(self,root):

        self.root = root
        self.root.title("Youtube Downloader")


        # Screen Setup 

        screen_w,screen_h = root.winfo_screenwidth(),root.winfo_screenheight()
        prog_w,prog_h = 600,600
        pos_w,pos_h = int((screen_w - prog_w) / 2) , int((screen_h - prog_h) / 2)
        self.root.geometry(f"{prog_w}x{prog_h}+{pos_w}+{pos_h}") 


        # GUI Setup 

        title_font = tkinter.font.Font(size=20,weight="bold",slant="italic")
        self.title = tk.Label(root,text="Welcome",font= title_font) 
        self.title.pack()

        introduction_text = """

        Hi, Welcome to Youtube Downloader. 
        This application is based on yt-dlp, which is a beautiful library for handling youtube video/audio.
        Start your first download by clicking the button below. 
        """

        self.label = tk.Label(root,text=introduction_text)
        self.label.pack()

        self.url_label = tk.Label(root,text="Youtube URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(root,width=50)
        self.url_entry.pack(pady=5)

        # User Option Frame


        self.user_options = tk.Frame(root)
        self.user_options.pack()

        self.artist_label = tk.Label(self.user_options,text= "Artist Name:")
        self.artist_label.pack()

        self.artist_entry = tk.Entry(self.user_options,width = 50)
        self.artist_entry.pack()

        self.album_artist_label = tk.Label(self.user_options,text="Album Artist Name:")
        self.album_artist_label.pack()

        self.album_artist_entry =tk.Entry(self.user_options,width = 50)
        self.album_artist_entry.pack()

        self.artist_to_album_artist = tk.Checkbutton(self.user_options,text="use artist name as album artist",command=self.artist_as_album_artist)
        self.artist_to_album_artist.pack()

        # self.user_thumbnail = tk.Checkbutton(self.user_options,text="use user thumbnail")
        # self.user_thumbnail.pack()



        # Download Button Frame

        self.download_button_mp4 = tk.Button(root, text="Download Video (MP4)", command=lambda: self.download_media('mp4'))
        self.download_button_mp4.pack(pady=10)



        self.download_button_mp3 = tk.Button(root, text="Download Audio (MP3)", command=lambda: self.download_media('mp3'))
        self.download_button_mp3.pack(pady=5)

        # Status 
        self.status_label = tk.Label(root,text="")
        self.status_label.pack(pady=10)

    def artist_as_album_artist(self):
        self.album_artist_entry.delete(0,tk.END)
        self.album_artist_entry(0,self.artist_entry.get())



    def download_media(self,format):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("URL Error","Type appropriate URL.")
            return
        
        self.download_button_mp4.config(state="disabled")
        self.download_button_mp3.config(state="disabled")
        self.status_label.config(text="downloading...")

        

        ydl_opts = {}

        if format == "mp4" :
            ydl_opts['format'] = 'bestvideo*+bestaudio/best'
            ydl_opts['writethumbnail'] = True
            ydl_opts['quiet'] = True
            
        

        if format == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            #ydl_opts['writethumbnail'] = True
            #ydl_opts['verbose'] = True  # Print additional info to stdout. 
            #ydl_opts['list_thumbnails'] = True
            ydl_opts['convert_thumbnails'] = 'jpg'
            ydl_opts['writethumbnail'] = True
            ydl_opts['embedthumbnail'] = True
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192', # bitrate of the audio file that ffmpeg will produce
            },
            {
                'key' : 'EmbedThumbnail'
            },
            {
                'key' : 'FFmpegMetadata'
            }
            ]


        def run_download(ydl_opts):
            try:
                save_path = filedialog.askdirectory()
                if not save_path:
                    raise Exception("Save Path not selected.")
                
                ydl_opts['outtmpl'] = f'{save_path}/%(title)s.%(ext)s'
             
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                self.status_label.config(text="Download Finished")

            except Exception as e:
                messagebox.showerror("Download Error",f"Download failed:{e}")
                self.status_label.config(text="")
            
            finally:
                file = ydl_opts['outtmpl']
                audiofile = eyed3.load(file)

                if audiofile.tag is None:
                    audiofile.initTag()

                artist_name = self.artist_entry.get()
                if artist_name is not None:
                    audiofile.tag.artist = artist_name

                    if self.album_artist_entry.get() is None:
                        audiofile.tag.album_artist = audiofile.tag.artist

                
                self.download_button_mp4.config(state="normal")
                self.download_button_mp3.config(state='normal')

        threading.Thread(target=lambda: run_download(ydl_opts)).start()


if __name__ == "__main__":
    root = tk.Tk()
    #help(yt_dlp.YoutubeDL)

    app = YoutubeDownloader(root)
    root.mainloop()
        

'''


# if format == "mp4":
            ydl_opts = {
            'format' : 'bestvideo+bestaudio/best',
            'quiet':True, # Do not print messages to stdout. 
                #'writeinfojson':True, 
                #'getcomments':True, # get comment from the video
            
            }


'''