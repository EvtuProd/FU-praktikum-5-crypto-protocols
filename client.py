import socket
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

    a = random.randint(1, 10)  # Секретное число клиента
    A = pow(g, a, p)            # Открытый ключ клиента

    return p, g, a, A

# Функция для вычисления общего секрета
def calculate_secret_key(p, B, a):
    return pow(B, a, p)

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

def client():
    config = load_config()
    host = config['SERVER_HOST']
    port = config['SERVER_PORT']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        p, g, a, A = generate_keys()
        s.sendall(str(A).encode())

        data = s.recv(1024)
        B = int(data.decode())
        secret_key = calculate_secret_key(p, B, a)

        message = "Hello, server!"
        encrypted_message = encrypt(message, secret_key)
        s.sendall(encrypted_message.encode())

        data = s.recv(1024)
        decrypted_message = decrypt(data.decode(), secret_key)
        print('Received from server:', decrypted_message)

if __name__ == "__main__":
    client()
