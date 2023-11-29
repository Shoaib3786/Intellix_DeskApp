import csv
from io import StringIO
import shutil
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
from deepface import DeepFace
import mtcnn
import pandas as pd
import os
import pickle
import mysql.connector
from encryptFiles import encryptCSV
from decryptFiles import decryptCSV
import subprocess
import traceback
from hitApi_buttonTest import APIClientWidget

# Global variable
db_df = None


##### Display Recognised Image pop #####
class CustomImageDialog(QDialog):

    def __init__(self, image_cv, curr_image, stud_information , parent=None):
        super(CustomImageDialog, self).__init__(parent)

        self.stud_info = stud_information  # make student info

        # Convert OpenCV image to QImage
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        image_cv = cv2.resize(image_cv, (160, 100))
        height, width, channel = image_cv.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_cv.data, width, height, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)  # Convert QImage to QPixmap

        # Set the image as the content of the QDialog
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        # Set the text layout for the dialog
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        
        for key, value in self.stud_info.items():
            if key != 'coords':
                text_label = QLabel(f"<b>{key.capitalize()}</b>: {value}", self)
                text_label.setAlignment(Qt.AlignLeft)
                layout.addWidget(text_label)

        # Optional: Set other properties of the dialog
        self.setWindowTitle("Student Information")
        self.setGeometry(50, 150, 300, 400)  # Adjust the size of the dialog for custom design


class RecognizedImageDialog(QDialog):
    def __init__(self, image_np, stud_info,  parent=None):
        super(RecognizedImageDialog, self).__init__(parent)

        self.image_np = image_np
        self.Recog_student_info = stud_info
        self.Recog_student_pic = None

        # Get the geometry of the entire screen
        screen_geometry = QDesktopWidget().screenGeometry()
        
        self.rect_area = []  # Initialize the rectangular area as empty list
        
        layout = QVBoxLayout()
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        FlippedImage = cv2.cvtColor(self.image_np, cv2.COLOR_BGR2RGB)  # Avoid flipping the image       
        self.ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
        Pic = self.ConvertToQtFormat.scaled(screen_geometry.width(), screen_geometry.height(), Qt.KeepAspectRatio)

        self.pixmap = QPixmap.fromImage(Pic)
        self.image_label.setPixmap(self.pixmap)

        # Set the dialog size to the maximum screen size
        self.setWindowTitle("Recognized Image")

        # Set the layout for the dialog
        self.setLayout(layout)
    
    def setRectArea(self, coords):
        # Check if the image is not None and the dialog is fully initialized
        if self.image_np is not None and self.width() > 0 and self.height() > 0:
            # Calculate scaled coordinates based on the original image size and scaled image size
            x = int(coords[0] / self.image_np.shape[1] * self.pixmap.width() )
            y = int(coords[1] / self.image_np.shape[0] * self.pixmap.height() )
            w = int(coords[2] / self.image_np.shape[1] * self.pixmap.width())
            h = int(coords[3] / self.image_np.shape[0] * self.pixmap.height())

            # Set the rectangular area coordinates
            self.rect_area.append(QRect(x, y, w, h))

            self.update()
   
    def showUserInfoPopUp(self, event):
        for i, rect_area in enumerate(self.rect_area):
            if rect_area and rect_area.contains(event.pos()):
                db_image = self.Recog_student_info[i][f'user{i+1}']['database_face']
                curr_image = self.Recog_student_info[i][f'user{i+1}']['cropped_curr_face']
                user_info = self.Recog_student_info[i][f'user{i+1}']['stud_details']
                custom_dialog = CustomImageDialog(db_image,curr_image, user_info, parent=self)
                custom_dialog.exec_()

    def mousePressEvent(self, event):
        self.showUserInfoPopUp(event)


    # def paintEvent(self, event):
    #     painter = QPainter(self.image_label.pixmap())
    #     painter.setPen(QPen(QColor(255, 0, 0), 2))  # Red color, 2-pixel width

        # for rect_area in self.rect_area:
        #     if rect_area:

        #         # Ensure the rectangle coordinates are within the image dimensions
        #         x = max(0, rect_area.x())
        #         y = max(0, rect_area.y())
        #         w = min(self.image_np.shape[1] - x, rect_area.width())
        #         h = min(self.image_np.shape[0] - y, rect_area.height())

        #         painter.drawRect(QRect(x, y, w, h))

        # painter.end()

# Intro Screen - Client's code enter
class StartDialog(QDialog):
    def __init__(self, parent=None):
        super(StartDialog, self).__init__(parent)

        self.client_code = None  # Variable to store the input value

        label = QLabel("Intellix", self)
        label.setFont(QFont("Arial", 48, QFont.Bold))  # Set a larger font size
        label.setAlignment(Qt.AlignCenter)

        input_text = QLineEdit(self)
        input_text.setObjectName('input_text')  # Set the object name
        input_text.setFont(QFont("Arial", 16))  # Set a larger font size for the input field
        input_text.setPlaceholderText('Database code')
        input_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow horizontal and vertical expansion
        input_text.setMaximumWidth(800)  # Set the maximum width as needed
        input_text.setMaximumHeight(200)  # Set the maximum height as needed

        ok_button = QPushButton("OK", self)
        ok_button.setMaximumWidth(600)
        ok_button.clicked.connect(self.on_ok_button_clicked)

        label_layout = QHBoxLayout()
        label_layout.addWidget(label)

        central_layout = QVBoxLayout(self)
        central_layout.addStretch(2)  # Add stretch to center vertically
        central_layout.addLayout(label_layout)
        central_layout.addWidget(input_text, alignment=Qt.AlignCenter)  # Remove alignment settings
        central_layout.addWidget(ok_button, alignment=Qt.AlignCenter)   # Remove alignment settings
        central_layout.addStretch(2)  # Add stretch to center vertically

        # Set the dialog size to cover the whole screen
        screen_geometry = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())

        self.setWindowTitle("Intellix")

    def on_ok_button_clicked(self):
        # Retrieve the value from the input_text field when the OK button is clicked
        self.client_code = self.findChild(QLineEdit, 'input_text').text()
        
        # Pass the client_code to the DatabaseSetup class
        DatabaseSetup_Object = DatabaseSetup(self.client_code)
        
        self.accept()  # Close the dialog if needed

# Database setup
class DatabaseSetup():
    def __init__(self, clientCode):

        global db_df
        self.clientCode = clientCode
        self.clientCred_Dic = None
        self.clientCred_filepath = os.path.join(FinalBasic_path,'cli_log.txt')
        self.intellixApp_dataPath = os.path.join(FinalBasic_path)
        self.DBcsv_filepath = os.path.join(FinalBasic_path,'fetchedStudent_data.csv')
        self.DBcsv_filename = 'fetchedStudent_data.csv'  # used for encrypting and decrypting
        self.DBimageFolder_path = os.path.join(FinalBasic_path,'db_picsFolder')  # folder path for imagedata
        

        if 'cli_log.txt' not in os.listdir(self.intellixApp_dataPath):
            print('\n\n ELIF CONDITION OF DATA CLASS \n\n')
            print('Client DB Credentials file not in the directory Run the CRED_CLI.exe')


        elif 'fetchedStudent_data.csv' and 'db_picsFolder' not in os.listdir(self.intellixApp_dataPath):
            print('\n\n ELIF CONDITION OF DATA CLASS \n\n')

            # Get the database credential as dictionary
            self.clientCred_dic = self.load_credentialFromBinary() 

            # Get the object of mysql connection
            self.db_connect = self.connectDatabase()
            self.mycursor = self.db_connect.cursor()

            # Make db image directory locally
            self.Make_db_directory()  

            # Get student information as CSV file locally
            self.GetStudentDB_csv()
            
            ## [ENCRYPT ALL THE DATA FETCHED FROM THE DATABASE] ##

            # Encypting CSV files
            # demoCSVfile_path = "/Users/shoaib/Documents/MAIN/RNS/RNS Project/Face Recognition/fetchedStudent_data.csv"
            self.objEncrypt = encryptCSV(self.DBcsv_filepath, self.intellixApp_dataPath)

            self.objDecryptData = decryptCSV(self.DBcsv_filepath + "_encrypt" + '.enc', self.intellixApp_dataPath).decrypt_file()
            # You can now use Pandas to read the decrypted data
            Decrypt_df = pd.read_csv(StringIO(self.objDecryptData.decode()))


        else:
            print('\n\n ELSE CONDITION OF DATA CLASS \n\n')
            # demoCSVfile_path = "/Users/shoaib/Documents/MAIN/RNS/RNS Project/Face Recognition/fetchedStudent_data.csv"
            # print('Calling the decryption function to decrypt the csv file')
            self.objDecryptData = decryptCSV(self.DBcsv_filepath + "_encrypt" + '.enc', self.intellixApp_dataPath).decrypt_file()

            # You can now use Pandas to read the decrypted data
            Decrypt_df = pd.read_csv(StringIO(self.objDecryptData.decode()))
            print('\nPrinting Decrypt_df \n')
            print(Decrypt_df.head())

            db_df = Decrypt_df
             
    def connectDatabase(self):
        print("I'm in CONNECTDATABASE..")
        try:
            if str(self.clientCode) in self.clientCred_dic.keys():
               
                myDb = mysql.connector.connect(
                    host = str(self.clientCred_dic[str(self.clientCode)]['host']),
                    user = str(self.clientCred_dic[str(self.clientCode)]['user']),
                    password = str(self.clientCred_dic[str(self.clientCode)]['password']),
                    database = str(self.clientCred_dic[str(self.clientCode)]['database'])
                    )
               
                return myDb
        
            else:
                print("Client entered code doesn't matches cli_log")

        except Exception as e:
            print("Exception in connecting database is: ", e)

    # CODE FOR UNLOADING THE CREDENTIAL FILES
    def load_credentialFromBinary(self):
        
        try:
            with open(self.clientCred_filepath, 'rb') as file:
                loaded_data = pickle.load(file)

            return loaded_data
        
        except Exception as e:
            print('Exception in unloading the credential from binary is: ', e )

    # CODE FOR CREATING THE OS FOLDER FOR STORING THE DATA
    def create_folder(self, folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
        except FileExistsError:
            print(f"Folder '{folder_path}' already exists.")
    
    def save_image(self, image_data, folder_path, image_name):
        try:
            image_path = os.path.join(folder_path, image_name)
            with open(image_path, 'wb') as image_file:
                image_file.write(image_data)
            print(f"Image '{image_name}' saved to '{folder_path}'.")

        except Exception as e:
            print("Exception in save_image() function is: ", e)
    
    def Make_db_directory(self):
        try: 
            # Execute the SELECT query on Student_Image table
            self.mycursor.execute(f"SELECT enrollment_id, photo FROM {self.clientCred_dic[str(self.clientCode)]['image_table']}")
            self.imageResultsRows = self.mycursor.fetchall()

            # Display the retrieved data
            for row in self.imageResultsRows:
                stud_id, image_blob = row
                print(f"Student ID: {stud_id}")

                k = self.DBimageFolder_path + f"/{stud_id}"
                # print('folder_name before creating: ',k)

                self.create_folder(k)
                self.save_image(image_blob, k +'/', f'{stud_id}.jpeg')

                # print(os.getcwd())
                # # print('folder_name after creating: ',folder_name)

        except Exception as e:
            print("Exception in Making the local Image directory is: ", e)

    # CODE FOR CREATING CSV FILE
    def GetStudentDB_csv(self):
        try:
            # Execute the SELECT query on Student_Image table
            self.mycursor.execute(f"SELECT * FROM {self.clientCred_dic[str(self.clientCode)]['csv_table']}")
            csvResults = self.mycursor.fetchall()
            with open(self.DBcsv_filepath, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([column[0] for column in self.mycursor.description])
                writer.writerows(csvResults)
       
        except Exception as e:
            print("Exception in GetStudentDB_csv() is: ",e) 

# MainWindow
class MainWindow(QWidget):
    
    def __init__(self):

        super(MainWindow, self).__init__()

        # [REPLACE THESE NUMBERS WITH YOUR ORIGINAL CAMERA CHANNELS]
        self.number_list = range(1, 13)  # Replace this with your list of numbers
        
        
        self.current_index = 0

        global db_df  # for accesing the CSV file

        self.db_directory = os.path.join(FinalBasic_path,'db_picsFolder')

        self.VBL = QVBoxLayout()
        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.HBL = QHBoxLayout()

        self.ButtonUP = QPushButton('Cam-Controller')
        self.ButtonUP.clicked.connect(self.movementFeed)
        self.HBL.addWidget(self.ButtonUP, 0)

        self.MovementFeedWidget = QWidget()
        self.MovementFeedWidget.setVisible(False)
        self.MovementFeedLayout = QVBoxLayout(self.MovementFeedWidget)
        self.MovementFeedLayout.addWidget(QLabel("Cam-Controller Content"))

        self.VBL.addLayout(self.HBL)
        self.VBL.addWidget(self.MovementFeedWidget)


        self.CaptureBTN = QPushButton("Capture")
        self.CaptureBTN.clicked.connect(lambda: self.captureFrame(capture=True))
        self.HBL.addWidget(self.CaptureBTN, 0)

        self.SwitchBTN = QPushButton("Switch camera")
        self.SwitchBTN.clicked.connect(lambda: self.captureFrame(capture=False))
        self.HBL.addWidget(self.SwitchBTN, 0)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.HBL.addWidget(self.CancelBTN, 0)

        self.VBL.addLayout(self.HBL)

        self.url= 'rtsp://admin:admin@192.168.1.163:554/live/av0'
        self.videoChannel = cv2.VideoCapture(self.url)
        self.Worker = Worker(self.videoChannel, parent=self)
        
        self.Worker.start()
        self.Worker.ImageUpdate.connect(self.ImageUpdateSlot)
        self.recognized_image_dialog = None
        self.setLayout(self.VBL)


    def toggleMovementFeed(self):
        self.MovementFeedWidget.setVisible(not self.MovementFeedWidget.isVisible())
        self.MovementFeedWidget.raise_()  # Bring the Cam-Controller Widget to the front


    def switchButton(self):
         
        if self.current_index < len(self.number_list):
            # current_number = self.number_list[self.current_index]

            url = 'rtsp://admin:admin@192.168.1.163:554/live/av0'

            # print('current_number: ', current_number)
            # print('url: ', url)
            # self.label.setText(f'Current Number: {current_number}')
            self.videoChannel = cv2.VideoCapture(url)
            self.current_index += 1
        
        else: pass
            # self.label.setText('No more numbers.')


    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def showRecognizedImage(self, image_np):
        
        if not self.recognized_image_dialog:
            self.recognized_image_dialog = RecognizedImageDialog(image_np, stud_info=self.stud_dic_results, parent=self)
            
            # Retrieving the coordinates and sending to the RecognizedImageDialog class
            for i in range(len(self.stud_dic_results)):
                user = self.stud_dic_results[i][f'user{i+1}']
                print('user coord: ', user['coords'])
                self.recognized_image_dialog.setRectArea(user['coords'])
            
            self.recognized_image_dialog.show()

        else:
            self.recognized_image_dialog = RecognizedImageDialog(image_np, stud_info=self.stud_dic_results, parent=self)
            
            # Retrieving the coordinates and sending to the RecognizedImageDialog class
            for k in range(len(self.stud_dic_results)):
                user = self.stud_dic_results[k][f'user{k+1}']
                print('user coord: ', user['coords'])
                self.recognized_image_dialog.setRectArea(user['coords'])
    
            self.recognized_image_dialog.show()

    # os.remove('/Users/shoaib/Documents/MAIN/RNS/RNS Project/Face Recognition/students_pics/representations_facenet512.pkl')
    def RecogniseFaces(self, db_directory, curr_face):
        global db_df
        try:
            results = DeepFace.find(img_path = curr_face, db_path = db_directory, model_name='ArcFace', detector_backend='mtcnn', distance_metric='euclidean', enforce_detection=False)
            
            stud_info = []
            stud_dic = {}

            k = 1   # for giving unique key for accessing userID dictionary
            for result in results:

                print(len(result))   # testing to visualize the list of result len
                
                if (len(result) != 0):    # checking if the Recognise_df is not empty
                    
                    """Collecting the student info"""
                    pic_name = result.iloc[0]['identity'] # taking 0th index row because 0th index consist of min distance face
                    print(pic_name)
                    pic_confid = result.iloc[0]['ArcFace_euclidean']
                    print(pic_confid)

                    m = pic_name.split('/')
                    file_id = m[-2]+'/'+m[-1]
                    print('m: ', m)
                    print('file_id: ', file_id)
                    # Reading and Opening the face pictures using the file name 
                    # Using db_face for sending over the pop-up.
                    print('self.db_directory: ', self.db_directory)
                    print('file_id: ', file_id)
                    db_img_path = os.path.join(self.db_directory,file_id)
                    print('db_img_path: ', db_img_path)
                    db_face = cv2.imread(str(db_img_path))

                    print('file_id: ', file_id)
                    
                    file_id = m[-1]  # needed file_id as .jpeg extention to match with csv file 'no' column
                    print('file_id: ', file_id)
                    print('db_df length:', len(db_df))

                    # Now check if the file_id exist in the database df than fetch all details
                    if len(db_df) != 0:
                        for i in range(len(db_df['no'])):
                            df_row = db_df.iloc[i] 
                            if (df_row['no'] == file_id):
                        
                                # Getting the coordinates
                                x, y, w, h = result.iloc[0]['source_x'], result.iloc[0]['source_y'], result.iloc[0]['source_w'], result.iloc[0]['source_h']
                                # cropping the recognise the face to display the result.
                                x1, y1 = abs(x), abs(y)
                                x2 = abs(x + w)
                                y2 = abs(y + h)
                                # get face from the image by slicing out using coordinates & store it
                                crop_face = curr_face[y1:y2, x1:x2]  # y -> rows, x -> columns
                                df_dic = {
                                    'Name': df_row['name'],
                                    'Student Id': df_row['stud_id'],
                                    'Description': df_row['description'],
                                    'contact': df_row['contact'],
                                    'Center code': df_row['cen_code'],
                                    'Invoice number': df_row['invoic_num'],
                                    'Amount': df_row['amount'],
                                    'Total Amount': df_row['total_amount'],
                                    'Pay mode': df_row['pay_mode'],
                                    'Date': df_row['date'],
                                    'Status': df_row['status']
                                }
                                
                                cropped_face = crop_face
                                database_face = db_face

                                if (cropped_face is not None) and (database_face.any() != None):
                   
                                    stud_dic = {'user'+str(k): {
                                        'cropped_curr_face': cropped_face,
                                        'database_face': database_face,
                                        'stud_details': df_dic,
                                        'coords': [int(x), int(y), int(w), int(h)]
                                        }
                                    }
                                                            
                                else:
                                    
                                    cropped_face = None
                                    database_face = None

                                    stud_dic = {'user'+str(i): {
                                        'cropped_curr_face': None,
                                        'database_face': None,
                                        'stud_details': None,
                                        'coords': None
                                        }
                                    }

                                k = k+1
                                stud_info.append(stud_dic)
                                cv2.rectangle(curr_face, (x,y), (x+w,y+h), (0,255,0), 2)
    
                                break  # if person found then no need to search further entries

                            else: #  when db_row doesn't matches with the recog face name
                                continue

                    else:
                        print('CSV file data len is Null')
                            
            return stud_info

        except Exception as e:
            traceback.print_exc()
            print("Exception in recog is:", e)

    # Perform recognisation processing...
    def process_image(self): 

        try:

            # Final facial results -> consist of facial coord and recognised student info
            self.stud_dic_results = self.RecogniseFaces(self.db_directory, self.frame)

            cv2.imwrite('After_recognition.jpeg', self.frame)
            # cv2.imshow('Window after recog', self.frame)  # for verification

            # print('shape of the recog face: ', image_np.shape)
            print('stud_dic_results; ', self.stud_dic_results)

            # print('type stud_dic_results: ', type(stud_dic_results[0]))
            print('stud_dic_results.keys: ', self.stud_dic_results[0].keys())

           

        except Exception as e:
            traceback.print_exc()
            print(f"Exception in the recognition process is: {e}")
 
    def captureFrame(self, capture=True):
                
        print('self.url from capture frame: ', self.url)
        self.videoChannel = cv2.VideoCapture(self.url)
        
        if capture==True:
            # videoChannel = self.videoChannel
            ret, self.frame = self.videoChannel.read()
            if ret:
                # send the captured image for recognition.
                self.process_image()
                self.showRecognizedImage(self.frame)

        else:
            if self.current_index < len(self.number_list):
                current_number = self.number_list[self.current_index]

                self.url = f'rtsp://admin:admin123@192.168.1.2:554/H264?ch={current_number}&subtype=0'
                self.videoChannel = cv2.VideoCapture(self.url)
                self.Worker.setUrl(self.videoChannel)
                self.current_index += 1
            
            else:
                self.current_index = 0


    def CancelFeed(self):
        self.Worker.stop()

    def movementFeed(self):
        # if not hasattr(self, 'movObj') or not self.movObj.isVisible():
        #     self.movObj = APIClientWidget(FinalBasic_path)
        
        self.movObj = APIClientWidget(FinalBasic_path)
        
    def sizeHint(self):
        return QSize(800, 600)

    def resizeEvent(self, event):
        
        if self.width() == self.screen().geometry().width() or self.height() == self.screen().geometry().height():
            print("Window maximized")
            self.Worker.updateFrameSize()

        super().resizeEvent(event)

# Live Streaming worker that runs on another thread
class Worker(QThread):

    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, videoChannel, parent=None):
        super().__init__(parent)
        self.frameSize = (1080, 640)
        # self.url = 'rtsp://admin:admin@192.168.1.163:554/live/av0'
        self.videoChannel = videoChannel

    def setUrl(self, videoChannel):
        self.videoChannel = videoChannel

    def run(self):
        self.ThreadActive = True

        while self.ThreadActive:
            ret, frame = self.videoChannel.read()
            if ret:
                # Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # FlippedImage = cv2.flip(Image, 1)
                FlippedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Avoid flipping the image
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(self.frameSize[0], self.frameSize[1], Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                
    def stop(self):
        self.ThreadActive = False
        self.quit()

    def updateFrameSize(self):
        self.frameSize = (self.parent().width(), self.parent().height())


# CODE FOR HIDDING IMAGES DIRECTORY
def hide_directory(DBimageFolder_path):
    try:
        subprocess.run(["chflags", "hidden", DBimageFolder_path])
        print(f"Directory '{DBimageFolder_path}' is now hidden.")
    except Exception as e:
        print(f"Error in hiding Images directory is: {e}")


def unhide_directory(DBimageFolder_path):
    try:
        subprocess.run(["chflags", "nohidden", DBimageFolder_path])
        print(f"Directory '{DBimageFolder_path}' is now visible.")
    except Exception as e:
        print(f"Error unhiding directory: {e}")

    
if __name__ == "__main__":

    App = QApplication(sys.argv)

    print('\n CURRENT DIRECTORY: \n', os.getcwd(),'\n')

    basic_path = os.getcwd()
    FinalBasic_path = os.path.join(basic_path,'IntellixApp_data')
    
    if os.path.exists(FinalBasic_path):

        start_dialog = StartDialog()
        if start_dialog.exec_() == QDialog.Accepted:

            # Hide the Students images directory
            directory_images = os.path.join(basic_path,'IntellixApp_data','db_picsFolder')
            hide_directory(directory_images)

            # User clicked OK, start streaming
            Root = MainWindow()
            Root.show()

        sys.exit(App.exec_())


    else:
        print('IntellixApp_data directory not built, please run CRED_CLI.exe')
 
    