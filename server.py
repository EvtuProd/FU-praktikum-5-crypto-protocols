import socket
import threading
import json
import random

def load_config(filename='config.json'):
    with open(filename) as f:
        config = json.load(f)
    return config

# Функция для генерации ключей
def generate_keys():
    p = 23  # Простое число p
    g = 5   # Простой корень по модулю p

    b = random.randint(1, 10)  # Секретное число сервера
    B = pow(g, b, p)            # Открытый ключ сервера

    return p, g, b, B

# Функция для вычисления общего секрета
def calculate_secret_key(p, A, b):
    return pow(A, b, p)

# Функция для шифрования сообщения
def encrypt(message, key):
    encrypted_message = ""
    for char in message:
        encrypted_message += chr(ord(char) + key)
    return encrypted_message

# Функция для дешифрования сообщения
def decrypt(encrypted_message, key):
    decrypted_message = ""
    for char in encrypted_message:
        decrypted_message += chr(ord(char) - key)
    return decrypted_message

def handle_client(conn, addr):
    with conn:
        print('Connected by', addr)
        p, g, b, B = generate_keys()
        conn.sendall(str(B).encode())

        data = conn.recv(1024)
        A = int(data.decode())
        secret_key = calculate_secret_key(p, A, b)

        data = conn.recv(1024)
        decrypted_message = decrypt(data.decode(), secret_key)
        print('Received from client:', decrypted_message)

        message = "Hello, client!"
        encrypted_message = encrypt(message, secret_key)
        conn.sendall(encrypted_message.encode())

def server():
    config = load_config()
    host = config['SERVER_HOST']
    port = config['SERVER_PORT']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print('Server listening on', (host, port))

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    server()
