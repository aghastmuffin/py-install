import json, requests, os, sys, time, subprocess, threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


#pretty important. TKINTER IS NOT THREADSAFE
#
class Installer:
    def __init__(self):
        self.root = Tk()
        self.root.title("Installer")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        self.downloaded_indx = 0
        self.root.iconbitmap("icon.ico")
        self.progbar = ttk.Progressbar(self.root, orient=HORIZONTAL, length=100, mode="determinate")
        self.dwnnumb = Label(self.root, text="Downloading file 1 of 1")
        self.download_new = True
        self.progbar.pack()
        self.dwnnumb.pack()
    def download_get(self):
        """Download_GET downloads a file in chunks to a specified output path
        Args:
            url (str): The URL of the file to download
            path (str): The output path of the downloaded file
        """
        #get file size
        #if the download doesn't work we should try to send a user-agent.
        for url, path in self.urls_list.items():
            response = requests.head(url)
            total_size = int(response.headers.get('Content-Length', 0)) #returns in bytes, if avaliable
            
            cur_down = 0
            if os.path.exists(path):
                if messagebox.askyesno("File already exists", "The file already exists, do you want to overwrite it?"):
                    os.remove(path)
                else:
                    return
            
            #start downloading the file
            r = requests.get(url, stream=True)
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        cur_down += len(chunk) 
                        self.update_progbar(round((cur_down/total_size)*100))
                        #cur_down += 1024 #we can assume since a chunk size is 1024 bytes
            self.finish_dwn(path)
    def finish_dwn(self, f_name):
        """
        self.root.destroy() #we don't want this running inside of a thread, so we should have this checking
        exit() #for the final version of this we are gonna have it look for more commands to run, as well as init the next download
        """
        self.downloaded_indx += 1
        self.download_new = True
        if self.downloaded_indx <= len(self.download_urls):
            self.dwnnumb.config(text="Downloading file {} of {} ({})".format(self.downloaded_indx, len(self.download_urls), f_name))
        else:
            self.dwnnumb.config(text="Downloads Complete!".format(self.downloaded_indx, len(self.download_urls), f_name))
        self.update_progbar(0)
    def update_progbar(self, value):
        """Update the progressbar's value"""
        self.progbar["value"] = value
        self.progbar.update()
        self.root.update_idletasks()
    def download_mgr(self):
        download_thread = threading.Thread(target=self.download_get)
        download_thread.start()
                

    def initdwn(self, urls):
        """Initiate the download, provide the urls in dict, as well as this function creates the download button"""
        if type(urls) != dict:
            print(type(urls))
            raise ValueError("Urls must be a dictionary")
        self.download_urls = urls
        self.download_btn = Button(self.root, text="Download", command=self.download_mgr)
        self.download_btn.pack()
        self.urls_list = urls
        
if __name__ == "__main__":
    #one or more donwloads don't work, prob in the for item in dict loop.
    urls = {"https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png": "google.png", "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://github.com&size=128": "github.png"}
    installer = Installer()
    installer.initdwn(urls)
    #installer.download_mgr("https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png", "google.png")
    installer.root.mainloop()
