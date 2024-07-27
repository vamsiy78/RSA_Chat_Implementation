import socket
import threading
import rsa
import tkinter as tk
from tkinter import scrolledtext, Button, END

public_key, private_key = rsa.newkeys(2048)  # Increased key size for better security
public_partner = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9997))  # Bind to all available interfaces
server.listen()

host_ip = socket.gethostbyname(socket.gethostname())
print("Server IP:", host_ip)  # Print server's IP address

client, _ = server.accept()
client.send(public_key.save_pkcs1("PEM"))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

# GUI setup
root = tk.Tk()
root.title("Server Chat")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20, state='disabled', font=("Helvetica", 12))
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

message_entry = tk.Entry(root, width=30)
message_entry.grid(row=1, column=0, padx=10, pady=10)

def send_message():
    message = message_entry.get()
    if message:
        client.send(rsa.encrypt(message.encode(), public_partner))
        chat_display.configure(state='normal')
        chat_display.tag_configure("user", foreground="blue")
        chat_display.insert(tk.END, "You: " + message + "\n", "user")
        chat_display.configure(state='disabled')
        message_entry.delete(0, tk.END)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

def receive_messages():
    while True:
        message = rsa.decrypt(client.recv(1024), private_key).decode()
        chat_display.configure(state='normal')
        chat_display.tag_configure("partner", foreground="green")
        chat_display.insert(tk.END, "Partner: " + message + "\n", "partner")
        chat_display.configure(state='disabled')

threading.Thread(target=receive_messages).start()

def on_enter(event):
    send_message()

root.bind('<Return>', on_enter)

root.mainloop()


