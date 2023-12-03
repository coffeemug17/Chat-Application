# Group#: G14
# Student Names: Mitul Pandey and James Zhang

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
        '''
        We use tkinters pack geometry manager to arrange basic geometry and use the grid geometry manager to get 
        the Chat message label and entry box to be on the same row. With the listbox below.
        '''

        #Client port label
        self.label1 = Label(self.window, text="Client{} @port #{}".format(current_process().name[-1], current_process().pid))
        self.label1.pack(anchor='w')

        #Entry frame
        entry_frame = Frame(self.window)
        entry_frame.pack(anchor='w', side=TOP)

        #Chat message label
        self.message_label = Label(entry_frame, text="Chat message:")
        self.message_label.grid(row=0, column=0)

        #Chat message entry box
        self.message_entry = Entry(entry_frame, width=25)
        self.message_entry.grid(row=0, column=1)
        # Bind the return key to the sendMessage function
        self.message_entry.bind("<Return>", lambda x: self.sendMessage())

        #Chat history label
        self.label2 = Label(self.window, text="Chat History:")
        self.label2.pack(anchor='w', side=TOP)

        #Message history. The height and width are configurable variables because they dominate the size of the GUI
        #and the width is used to center the message in the listbox
        self.message_listbox = Listbox(self.window, height=CLIENT_WINDOW_HEIGHT, width=CLIENT_WINDOW_WIDTH)
        self.message_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        #Scrollbar
        scrollbar = Scrollbar(self.window, command=self.message_listbox.yview)
        scrollbar.pack(side=LEFT, fill=Y)
        self.message_listbox.config(yscrollcommand=scrollbar.set)


    #Establish TCP connection
    def setupNetwork(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 55555))

        # New thread for receiving messages
        receive_thread = threading.Thread(target=self.receiveMessage)
        receive_thread.start()

    #Function for sending messages
    def sendMessage(self):
        message = self.message_entry.get()
        #Only send message if it is not empty
        if message:
            #Send message to server and display it in chat history box
            self.client_socket.send(message.encode())
            self.displayMessage(f"You: {message}")
            self.message_entry.delete(0, END)
    
    #Function for receiving messages from the server
    def receiveMessage(self):
        while True:
            try:
                #Receive message from server and display it in chat history box
                #Centre received message
                message = " "*int(CLIENT_WINDOW_WIDTH/2) + self.client_socket.recv(1024).decode()
                if message:
                    self.message_listbox.insert(END, message)
            except ConnectionAbortedError:
                break
    
    #Display message in history
    def displayMessage(self, message):
        self.message_listbox.insert(END, message + "\n")
        self.message_listbox.see(END)

def main(): #Note that the main function is outside the ChatClient class
    #Variables are global so they're accessible in the ChatClient object
    global CLIENT_WINDOW_HEIGHT
    global CLIENT_WINDOW_WIDTH
    CLIENT_WINDOW_HEIGHT = 10
    CLIENT_WINDOW_WIDTH = 70

    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed 

if __name__ == '__main__': # May be used ONLY for debugging
    main()