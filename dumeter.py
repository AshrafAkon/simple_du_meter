import tkinter as tk
import psutil
import threading
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W, NW, SE, SW
import requests
import time

class UploadDownloadMeter():
    def __init__(self, root): 
        self.frame = root 
        self.root = root 
        self.download_speed_var = tk.StringVar()
        self.upload_speed_var = tk.StringVar()

        self.download_speed_var.set('Download speed: 0.00 Mbps')
        self.upload_speed_var.set('Upload speed: 0.00 Mbps')

        self.download_label = tk.Label(self.frame,textvariable = self.download_speed_var,
                                            width = 25)
        self.download_label.grid(column = 0, row=0, columnspan=3,sticky = N)
        self.download_label.configure(borderwidth = 0)

        self.upload_label = tk.Label(self.root, textvariable = self.upload_speed_var,
                                            width = 25)
        self.upload_label.configure(borderwidth = 0)
        self.upload_label.grid(column = 0, row = 1, columnspan = 3,sticky=N)
        #tk.Label(self.frame,text="pani" ,height =5, width =10).grid(row = 4, column =1)

        visit_ex = threading.Thread(target = self.visit_example)
        visit_ex.daemon = True
        visit_ex.start()

    def visit_example(self):
        self.list1 = []
        self.network_card = False
        self.card_list = []
        for card in psutil.net_io_counters(pernic=True):
            self.list1.append(psutil.net_io_counters(pernic=True)[card].bytes_sent)
            self.card_list.append(card)
        
        for card in psutil.net_io_counters(pernic=True):
            self.list1.append(psutil.net_io_counters(pernic=True)[card].bytes_sent )
        
        try:
            #generating some trafic so that psutil returns value greater than 10
            requests.post("https://example.com")
            requests.post("https://example.com")
            requests.post("https://example.com")
        except Exception as e:
            print(e)
        
        list2 = []
        for card in psutil.net_io_counters(pernic=True):
            list2.append(psutil.net_io_counters(pernic=True)[card].bytes_sent )

        for i in range(len(list2)):
            if (list2[i] - self.list1[i]) > 10:
                self.network_card = self.card_list[i]

        print(self.network_card)
        self.root.after(100, self.check_speed)


    def check_speed(self):
        download_thread = threading.Thread(target = self.download_speed_checker)
        upload_thread = threading.Thread(target = self.upload_speed_checker)
        upload_thread.daemon = True
        download_thread.daemon = True
        download_thread.start()
        upload_thread.start()


    def download_speed_checker(self):
        last_time = time.time()
        last_bytes = psutil.net_io_counters(pernic=True)[self.network_card].bytes_recv
        while True:
            now_bytes = psutil.net_io_counters(pernic=True)[self.network_card].bytes_recv
            now_time = time.time()
            down_speed = (((now_bytes - last_bytes) / (now_time - last_time)) / 1000000.00)*8.00
            self.download_speed_var.set("Download speed: {:.3f} Mbps".format(down_speed))
            last_time = now_time
            last_bytes = now_bytes
            time.sleep(1)


    def upload_speed_checker(self):
        last_time = time.time()
        last_bytes = psutil.net_io_counters(pernic=True)[self.network_card].bytes_sent
        while True:
            now_bytes = psutil.net_io_counters(pernic=True)[self.network_card].bytes_sent
            now_time = time.time()
            down_speed = (((now_bytes - last_bytes) / (now_time - last_time)) / 1000000.00)*8.00
            self.upload_speed_var.set("Upload speed: {:.3f} Mbps".format(down_speed))
            last_time = now_time
            last_bytes = now_bytes
            time.sleep(1)

def main():
    root = tk.Tk()
    app = UploadDownloadMeter(root)
    root.title("Simple DU Meter")
    app.root.mainloop()   


if __name__ == "__main__":
    main()
