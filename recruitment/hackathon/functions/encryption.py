# from cryptography.fernet import Fernet
# import os.path
# from os import path
# from simplecrypt import encrypt, decrypt
# from Crypto.Cipher import XOR
# import base64
from math import ceil

# password_key = 'Trutech1'
# https://en.wikipedia.org/wiki/Transposition_cipher#Columnar_transposition
key = 4


def encrypt(plaintext):
    ciphertext = [''] * key
    for col in range(key):
        position = col
        while position < len(plaintext):
            ciphertext[col] += plaintext[position]
            position += key
    return ''.join(ciphertext)


def decrypt(ciphertext):
    n_Columns, n_Rows = ceil(len(ciphertext) / key), key
    n_ShadedBoxes = (n_Columns * n_Rows) - len(ciphertext)
    plaintext = [''] * n_Columns
    col, row = 0, 0
    for symbol in ciphertext:
        plaintext[col] += symbol
        col += 1
        if (col == n_Columns) or (col == n_Columns - 1 and row >= n_Rows - n_ShadedBoxes):
            col = 0
            row += 1
    return ''.join(plaintext)


'''
def simple_encryption(string_to_encrypt):
    return encrypt(password_key, string_to_encrypt)


def simple_decryption(string_to_decrypt):
    return decrypt(password_key, string_to_decrypt)

DEPRICATED COMPLEX ENCRYPTION DECRYPTION CODE

# Create an encryption for storing mobile number of user
def return_encryption_key():

    # check if a key already exists in the program
    if path.exists("encryption.key"):
        file = open('encryption.key', 'rb')
        key = file.read()  # The key will be type bytes
        file.close()
    else:
        key = Fernet.generate_key()
        file = open('encryption.key', 'wb')
        file.write(key)  # The key is type bytes still
        file.close()

    fern = Fernet(key)

    return fern


# Code that encrypts the data
def encrypt_data(string_to_encrypt):
    fern_key = return_encryption_key()
    return fern_key.encrypt(string_to_encrypt.encode())


# Code that decrypts the data
def decrypt_data(string_to_decrypt):
    fern_key = return_encryption_key()
    return fern_key.encrypt(string_to_decrypt)
'''