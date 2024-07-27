import socket
import threading
import rsa
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, END
from tkinter import ttk

public_key, private_key = rsa.newkeys(2048)  # Increased key size for better security
public_partner = None

# Create a tkinter window with a themed style
root = tk.Tk()
root.title("Secure Chat")
style = ttk.Style()
style.theme_use("clam")  # Change the theme as needed

# Colors for messages
user_color = "blue"
partner_color = "green"

# Create a scrolled text widget for displaying messages (set state to 'disabled')
chat_display = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=40, height=20, state='disabled', font=("Helvetica", 12)
)
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create an entry widget for typing messages
message_entry = Entry(root, width=30)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Create a button for sending messages
def send_message():
    message = message_entry.get()
    if message:
        client.send(rsa.encrypt(message.encode(), public_partner))
        chat_display.configure(state='normal')  # Set state to normal to allow editing
        chat_display.tag_configure("user", foreground=user_color)
        chat_display.insert(tk.END, "You: " + message + "\n", "user")
        chat_display.configure(state='disabled')  # Set state back to disabled
        message_entry.delete(0, tk.END)

send_button = Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Function to send a message when the Enter key is pressed
def on_enter(event):
    send_message()

# Bind the Enter key to the send_message function
root.bind('<Return>', on_enter)

choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.52.1", 9997))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.52.1", 9997))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()

# Function to continuously receive and display messages
def receive_messages():
    while True:
        message = rsa.decrypt(client.recv(1024), private_key).decode()
        
        chat_display.configure(state='normal')  # Set state to normal to allow editing
        chat_display.tag_configure("partner", foreground=partner_color)
        chat_display.insert(tk.END, "Partner: " + message + "\n", "partner")
        chat_display.configure(state='disabled')  # Set state back to disabled

# Start a thread for receiving messages
threading.Thread(target=receive_messages).start()

# Run the tkinter main loop
root.mainloop()
