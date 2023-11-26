
from cryptography.fernet import Fernet
import os
 
class decryptCSV():

    def __init__(self, encrypted_file_path, intellixAllData_path):
        self.encrypted_file_path = encrypted_file_path
        self.Keyfile_path = os.path.join(intellixAllData_path, 'keyLog')

        with open(self.Keyfile_path, 'rb') as readkeyFile:
            self.key = readkeyFile.read()
        self.cipher_suite = Fernet(self.key)

    # Function to decrypt a file
    def decrypt_file(self):
        with open(self.encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
            
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        return decrypted_data


