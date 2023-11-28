# Group#: G14
# Student Names: Mitul Pandey and James Zhang

#Content of client.py; to complete/implement

from tkinter import *
import socket
import threading
from multiprocessing import current_process #only needed for getting the current process name

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """
    
    def __init__(self,window):
        self.window = window
        self.window.title("tk")
        self.setupGUI()
        self.setupNetwork()

    def setupGUI(self):
        # Here, we will add two labels
        self.label1 = Label(self.window, text="Client{}".format(current_process().name[-1]))
        self.label1.pack(padx=0, pady=0, anchor='w')

        self.message_label = Label(self.window, text="Message:")
        self.message_label.pack(padx=0, pady=5, anchor='w', side=LEFT)
        self.message_entry = Entry(self.window, width=40)
        self.message_entry.pack(padx=10, pady=5, side=LEFT)
        self.message_entry.bind("<Return>", lambda x: self.sendMessage())

        self.label2 = Label(self.window, text="Chat History:")
        self.label2.pack(padx=0, pady=0, anchor='w')

        self.message_listbox = Listbox(self.window, height=20, width=50)
        self.message_listbox.pack(padx=10, pady=10)

        # self.send_button = Button(self.window, text="Send", command=self.sendMessage)
        # self.send_button.pack(pady=10)


    def setupNetwork(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 55555))

        # New thread for receiving messages
        receive_thread = threading.Thread(target=self.receiveMessage)
        receive_thread.start()

    def sendMessage(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode())
            self.displayMessage("You: {}".format(message))
            self.message_entry.delete(0, END)
    
    def receiveMessage(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.message_listbox.insert(END, message)
            except ConnectionAbortedError:
                break
    
    def displayMessage(self, message):
        self.message_listbox.insert(END, message + "\n")
        self.message_listbox.see(END)

def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()