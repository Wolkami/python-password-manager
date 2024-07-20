from Crypto.Cipher import AES
import base64


# Функции для шифрования и дешифрования данных
def pad(data):
    # Дополнение данных до кратного размера блока AES (16 байт)
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)


def unpad(data):
    # Удаление дополнения из данных
    return data[:-ord(data[len(data) - 1:])]


def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(pad(data).encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')


def decrypt(enc_data, key):
    enc_data = base64.b64decode(enc_data)
    nonce = enc_data[:16]
    ciphertext = enc_data[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return unpad(cipher.decrypt(ciphertext)).decode('utf-8')
