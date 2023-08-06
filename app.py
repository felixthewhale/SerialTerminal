import tkinter as tk
from tkinter import ttk
import serial
from threading import Thread
import time

class SerialApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Serial Communication")

        self.ser = serial.Serial('COM3', 115200, timeout=1)
        self.ser.flush()

        self.send_frame = ttk.LabelFrame(root, text="Send")
        self.send_frame.pack(padx=10, pady=10, fill=tk.X)

        self.txt_send = ttk.Entry(self.send_frame, width=40)
        self.txt_send.grid(row=0, column=0, padx=10, pady=5)
        self.txt_send.bind('<Return>', self.send_data)

        self.btn_send = ttk.Button(self.send_frame, text="Send", command=self.send_data)
        self.btn_send.grid(row=0, column=1, padx=10, pady=5)

        self.receive_frame = ttk.LabelFrame(root, text="Receive")
        self.receive_frame.pack(padx=10, pady=10, fill=tk.X, expand=True)

        self.txt_receive = tk.Text(self.receive_frame, height=15, width=50)
        self.txt_receive.grid(row=0, column=0, padx=10, pady=5)

        self.running = True
        self.thread = Thread(target=self.receive_data)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def send_data(self, event=None):
        data = self.txt_send.get()
        self.ser.write(data.encode('utf-8'))
        self.txt_send.delete(0, tk.END)

    def receive_data(self):
        while self.running:
            if self.ser.in_waiting:
                data_line = self.ser.readline().decode('utf-8').rstrip()
                self.txt_receive.insert(tk.END, data_line + "\n")
                self.txt_receive.see(tk.END)

    def on_closing(self):
        self.running = False
        self.thread.join()
        self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialApp(root)
    root.mainloop()
