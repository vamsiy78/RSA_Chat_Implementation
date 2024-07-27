# RSA_Chat_Implementation

This is a secure chat application using RSA encryption to ensure that messages exchanged between clients are encrypted and protected. The application consists of three main components:

- **`main.py`**: A command-line interface (CLI) version of the chat application.
- **`mainui.py`**: A graphical user interface (GUI) version of the chat application using Tkinter.
- **`serv.py`**: A simplified server-side application for testing the GUI client.

## What is RSA?

RSA (Rivest-Shamir-Adleman) is one of the most widely used public-key cryptographic algorithms. It provides secure data transmission by using a pair of keys: a public key and a private key.

- **Public Key**: This key is used to encrypt data. It can be shared openly without compromising security.
- **Private Key**: This key is used to decrypt data. It must be kept secret and secure.

The RSA algorithm works in the following way:

1. **Key Generation**: Generate a pair of keys (public and private) using a process that involves large prime numbers.
2. **Encryption**: Data is encrypted with the recipient's public key. This means that only the recipient, who possesses the corresponding private key, can decrypt and read the data.
3. **Decryption**: The encrypted data is decrypted with the recipient's private key, ensuring that only the intended recipient can read the message.

RSA's security relies on the difficulty of factoring large numbers into their prime factors. As such, the RSA algorithm is effective at securing communications and data.

## Features

- **End-to-End Encryption**: Messages are encrypted with RSA before transmission and decrypted upon receipt, ensuring secure communication.
- **GUI Support**: The `mainui.py` provides a user-friendly interface for chatting, with color-coded messages.
- **CLI Support**: The `main.py` provides a basic command-line interface for chatting.
