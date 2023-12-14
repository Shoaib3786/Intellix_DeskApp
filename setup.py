
"""
Objective:
1. Program objective is to take client's camera APIs and database credential.
2. Then make a binary files from it and store it locally.
3. Make this program as .exe file. 
4. This file will run only for once at the time of setup.
"""

import os
import shutil
import pickle
import json

class ClientCredentials():
    
    def __init__(self):
        
        # For making dictionary of camera URLs
        self.currentCam = {}
        self.camUrlDic = {}
        self.buttApiDic = {}

        # For making dictionary of client 
        self.clientCred_Dic = {}
        self.client_detail_dic = {}

        self.basic_path = os.getcwd()
        mainData_path = os.path.join(self.basic_path,'IntellixApp_data')
        
        if os.path.exists(mainData_path): 
            os.chdir(self.basic_path)     # Change to a different directory
            shutil.rmtree(mainData_path)  # Remove the previous existing directory
            os.mkdir(os.path.join(self.basic_path,'IntellixApp_data'))
            os.chdir(os.path.join(self.basic_path,'IntellixApp_data'))
            FinalBasic_path = os.getcwd()
            print('FinalBasic_path: ', FinalBasic_path)

        else:
            os.mkdir(os.path.join(self.basic_path,'IntellixApp_data'))
            os.chdir(os.path.join(self.basic_path,'IntellixApp_data'))
            FinalBasic_path = os.getcwd()
            print('FinalBasic_path: ', FinalBasic_path)

        self.filename_cli_log = os.path.join(self.basic_path,'IntellixApp_data','cli_log.txt')
        self.filename_camera_log = os.path.join(self.basic_path,'IntellixApp_data','camera_log.config')

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
    
    def makeClientCredFile(self):
        self.clientCred_Dic = self.create_credential_dictionary()
        with open(self.filename_cli_log, 'wb') as file:
            x = pickle.dump(self.clientCred_Dic, file)
        print('file made done ')

    def get_non_null_input_camera_url(self,prompt):
        while True:
            user_input = input(prompt)
            if user_input.strip():
                return user_input
            else:
                print("Please enter a non-null value.")

    def create_url_dictionary(self):
        i = 1
        while True:
            self.buttApiDic = {}  # each iteration create a new dic
            self.camUrlDic = {}

            prompt = input('Enter the number for the operations: \n \t1. Add camera \t2. Exit\nEnter: ')
            
            if prompt == '1':
                print('# Camera-'+str(i))
                self.cameraNumber = i  # add number
                self.camURL = self.get_non_null_input_camera_url(f"Enter Camera-{i} local IP: ")
                
                self.leftStart_but = self.get_non_null_input_camera_url("Left start button API: ")
                self.leftStop_but = self.get_non_null_input_camera_url("Left stop button API: ")
                
                self.rightStart_but = self.get_non_null_input_camera_url("Right start button API: ")
                self.rightStop_but = self.get_non_null_input_camera_url("Right stop button API: ")
                
                self.upStart_but = self.get_non_null_input_camera_url("Up start button API: ")
                self.upStop_but = self.get_non_null_input_camera_url("Up stop button API: ")
                
                self.downStart_but = self.get_non_null_input_camera_url("Down start button API: ")
                self.downStop_but = self.get_non_null_input_camera_url("Down stop button API: ")
                
                self.zoomInStart_but = self.get_non_null_input_camera_url("Zoom-In start button API: ")
                self.zoomInStop_but = self.get_non_null_input_camera_url("Zoom-In stop button API: ")
                
                self.zoomOutStart_but = self.get_non_null_input_camera_url("Zoom-Out start button API: ")
                self.zoomOutStop_but = self.get_non_null_input_camera_url("Zoom-Out stop button API: ")
                
                self.focusInStart_but = self.get_non_null_input_camera_url("Focus-In start button API: ")
                self.focusInStop_but = self.get_non_null_input_camera_url("Focus-In stop button API: ")
                
                self.focusOutStart_but = self.get_non_null_input_camera_url("Focus-Out start button API: ")
                self.focusOutStop_but = self.get_non_null_input_camera_url("Focus-Out stop button API: ")

                """camUrlDic has 2 keys: camUrl, buttonApi"""
                self.camUrlDic['camUrl'] = self.camURL  
                self.buttApiDic['leftStart_but'] = self.leftStart_but
                self.buttApiDic['leftStop_but'] = self.leftStop_but
                
                self.buttApiDic['rightStart_but'] = self.rightStart_but
                self.buttApiDic['rightStop_but'] = self.rightStop_but
                
                self.buttApiDic['upStart_but'] = self.upStart_but
                self.buttApiDic['upStop_but'] = self.upStop_but
                
                self.buttApiDic['downStart_but'] = self.downStart_but
                self.buttApiDic['downStop_but'] = self.downStop_but
                
                self.buttApiDic['zoomInStart_but'] = self.zoomInStart_but
                self.buttApiDic['zoomInStop_but'] = self.zoomInStop_but
                
                self.buttApiDic['zoomOutStart_but'] = self.zoomOutStart_but
                self.buttApiDic['zoomOutStop_but'] = self.zoomOutStop_but
                
                self.buttApiDic['focusInStart_but'] = self.focusInStart_but
                self.buttApiDic['focusInStop_but'] = self.focusInStop_but
                
                self.buttApiDic['focusOutStart_but'] = self.focusOutStart_but
                self.buttApiDic['focusOutStop_but'] = self.focusOutStop_but
                
                self.camUrlDic['buttonsApi'] = self.buttApiDic
            
                 
                yield self.camUrlDic, i

                i += 1
                print('\n')

            else:
                # come out of the loop.
                break  

    def makeCameraUrlFile(self):
        self.currentCam = {}
        # CameraDic = self.create_url_dictionary()

        for entry, i in enumerate(self.create_url_dictionary()):
            self.currentCam['camera_'+str(entry)] = i
               
        # self.allcam = CameraDic
        with open(self.filename_camera_log, 'w') as file:
            json.dump(self.currentCam, file, indent=2)  # 'indent' parameter adds indentation for readability

        print('file made done')

# make the object of the ClientCredentials
obj = ClientCredentials()

print("MAKE CLIENT'S CAMERA APIs FILE: ")
obj.makeCameraUrlFile()     # make the client camera url.
print('\n\n')
print("MAKE CLIENT'S DATA CREDENTIAL FILE: ")
obj.makeClientCredFile()    # make client credential files


