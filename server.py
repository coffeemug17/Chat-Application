# Group#: G14
# Student Names: Mitul Pandey and James Zhang


from tkinter import *
import socket
import threading

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sents 
    the message to the other client.  
    It uses the tkinter module to create the GUI for the server client.
    See the project info/video for the specs.
    """
    # Here, we add a constructor for ChatServer class
    def __init__(self,window):
        self.window = window
        self.window.title("tk")
        self.setupGUI()
        self.setupNetwork()

    # Here, we add a function to setup the GUI
    def setupGUI(self):
        # Here, we will add two labels
        self.label1 = Label(self.window, text="Chat Server")
        self.label1.pack(padx=0, pady=0, anchor='w')
        self.label2 = Label(self.window, text="Chat History:")
        self.label2.pack(padx=0, pady=0, anchor='w')

        # Here, we will add a listbox for chat history
        self.message_listbox = Listbox(self.window, height=20, width=50)
        self.message_listbox.pack(padx=10, pady=10)

    # Here, we will add a function to setup the network connection and to handle clients
    def setupNetwork(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1",55555))
        # Only two clients allowed according to guidelines
        self.server_socket.listen(2)

        # List of client sockets and addresses
        self.client_sockets = []
        self.client_addresses = []
        self.chat_history = []

        # New thread for handling clients
        client1_thread = threading.Thread(target=self.handle_client, args=(0,))
        client1_thread.start()
        client2_thread = threading.Thread(target=self.handle_client, args=(1,))
        client2_thread.start()

    # Here, we will add a function to display messages in the chat history box
    def send_chat_history(self, client_socket):
        for message in self.chat_history:
            client_socket.send(message.encode())

    # Here, we would add a function to handle clients with distinct client numbers  
    def handle_client(self, client_number):
        client_socket, client_address = self.server_socket.accept()
        self.client_sockets.append(client_socket)
        self.client_addresses.append(client_address)

        # Send chat history to client
        self.send_chat_history(client_socket)

        while True:
            try:
                # Receive message from client
                message = client_socket.recv(1024).decode()
                if message:
                    self.message_listbox.insert(END, "Client {}: {}".format(client_number + 1, message))

                    # Send message to other client
                    for other_socket in self.client_sockets:
                        if other_socket != client_socket:
                            other_socket.send("Client {}: {}".format(client_number + 1, message).encode())
            except ConnectionAbortedError:
                break        

def main(): #Note that the main function is outside the ChatServer class
    window = Tk()
    ChatServer(window)
    window.mainloop()
    #May add more or modify, if needed
    try:
        # Keep the program running
        while True:
            pass
    except KeyboardInterrupt:
        # Close the server socket
        print("Server process terminated.")

if __name__ == '__main__': # May be used ONLY for debugging
    main()