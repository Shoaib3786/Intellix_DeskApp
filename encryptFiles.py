
from cryptography.fernet import Fernet
import os


class encryptCSV():

    def __init__(self, csv_filepath, intellixAllData_path):
        # Generate a key for encryption (you should keep this key secret)
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.csvfile_path = csv_filepath
        self.Keyfile_path = os.path.join(intellixAllData_path, 'keyLog')

        with open(self.Keyfile_path, 'wb') as keyFile:
            keyFile.write(self.key)

        self.encrypt_file()


    # Function to encrypt a file
    def encrypt_file(self):
        with open(self.csvfile_path, 'rb') as file:
            file_data = file.read()
        encrypted_data = self.cipher_suite.encrypt(file_data)
        
        with open(self.csvfile_path+"_encrypt" + '.enc', 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        os.remove(self.csvfile_path)


