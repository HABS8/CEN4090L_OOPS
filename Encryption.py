from Crypto.Cipher import AES
import string, base64


# declaration and initialisation of AESCipher class
class AESCipher(object):

    # class constructor that initializes the class variables of key and iv
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    # encrypts the raw variable
    def encrypt(self, raw):
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        ciphertext = self.cipher.encrypt(raw)
        encoded = base64.b64encode(ciphertext)
        return encoded

    # decrypts the raw variable
    def decrypt(self, raw):
        decoded = base64.b64decode(raw)
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        decrypted = self.cipher.decrypt(decoded)
        return str(decrypted, 'utf-8')

# initialize the key and iv variables
key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
iv = b'OWFJATh1Zowac2xr'

# declares the object cipher and initialize the key and iv variables for the object
cipher = AESCipher(key, iv)
