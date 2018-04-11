#!/usr/bin/env python
# encoding: utf-8

from aes import testAll, aes_encrypt, aes_decrypt

testAll()
Default_Text = (
    "The Advanced Encryption Standard (AES), also known by its "
    "original name Rijndael, is a specification for the encryption "
    "of electronic data established by the U.S. National Institute "
    "of Standards and Technology (NIST) in 2001.")
key = "AES_ENCRIPT_TEST"

text = input("\tData you want to encrypt: \n")
if not text:
    text = Default_Text
print("\n\tThis string will be encrypted:\n")
print(text)

encrypted = aes_encrypt(text, key)
print("\n\tEncrypted message is:\n")
print(encrypted.decode())

decrypted = aes_decrypt(encrypted, key)
print("\n\tDecrypted message is:\n")
print(decrypted.decode())
