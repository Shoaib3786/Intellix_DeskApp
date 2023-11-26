
"""
Objective:
1. Program objective is to take client's credential.
2. Then make a binary files from it and store it locally.
3. Make this program as .exe file. 
4. This file will run only for once at the time of setup.
"""

import os
import shutil
import pickle

class ClientCredentials():
    
    def __init__(self):
      
        # For making dictionary of client 
        self.clientCred_Dic = {}
        self.client_detail_dic = {}

        basic_path = os.getcwd()
        mainData_path = os.path.join(basic_path,'IntellixApp_data')
        
        if os.path.exists(mainData_path): 
            os.chdir(basic_path)  # Change to a different directory
            shutil.rmtree(mainData_path)  # Remove the previous existing directory
            os.mkdir(os.path.join(basic_path,'IntellixApp_data'))
            os.chdir(os.path.join(basic_path,'IntellixApp_data'))
            FinalBasic_path = os.getcwd()
            print('FinalBasic_path: ', FinalBasic_path)

        else:
            os.mkdir(os.path.join(basic_path,'IntellixApp_data'))
            os.chdir(os.path.join(basic_path,'IntellixApp_data'))
            FinalBasic_path = os.getcwd()
            print('FinalBasic_path: ', FinalBasic_path)

        self.filename = os.path.join(basic_path,'IntellixApp_data','cli_log.txt')

        self.host = None
        self.user = None
        self.password = None
        self.database = None

        # self.makeBinaryFile()  # on initializing itself create the file

    def get_non_null_input(self,prompt):
        while True:
            user_input = input(prompt)
            if user_input.strip():
                return user_input
            else:
                print("Please enter a non-null value.")

    def create_credential_dictionary(self):
        self.client_code = self.get_non_null_input("Enter client's code: ")
        self.host = self.get_non_null_input("Enter client's host IP: ")
        self.user = self.get_non_null_input("Enter client's userID: ")
        self.password = self.get_non_null_input("Enter password: ")
        self.database = self.get_non_null_input("Enter client's database: ")
        self.ImagesTable = self.get_non_null_input("Enter client's Images table: ")
        self.CSVTable = self.get_non_null_input("Enter client's CSV table: ")

        self.client_detail_dic['host'] = self.host
        self.client_detail_dic['user'] = self.user
        self.client_detail_dic['password'] = self.password
        self.client_detail_dic['database'] = self.database
        self.client_detail_dic['image_table'] = self.ImagesTable
        self.client_detail_dic['csv_table'] = self.CSVTable

        self.clientCred_Dic[str(self.client_code)] = self.client_detail_dic

        return self.clientCred_Dic
    

    def makeBinaryFile(self):
        self.clientCred_Dic = self.create_credential_dictionary()
        with open(self.filename, 'wb') as file:
            x = pickle.dump(self.clientCred_Dic, file)
        print('file made done ')


obj = ClientCredentials().makeBinaryFile()



