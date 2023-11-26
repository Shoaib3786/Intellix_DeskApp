
import os
import cv2
import mysql.connector

mydb = mysql.connector.connect(
    host="164.52.215.47",
    user="intellix_demo_user",
    password="3uKy6@5vx",
    database="intellix_demo",
)

mycursor = mydb.cursor()

def InsertData():
  
  path = 'students_pics/'
  for i in os.listdir(path):
      
      img_path=path+i
      print('i: ',i , '--' ,'image_path: ', img_path )


      frames = cv2.imread(img_path)
      _, img_encoded = cv2.imencode('.jpeg', frames)

      # Save these 2 data on the sql
      img_blob = img_encoded.tobytes()
      img_name = i.split('.')[0]

      mycursor.execute("""
                      INSERT INTO enroll_images (enrollment_id, photo)
                      VALUES (%s, %s)
                      """, (img_name, img_blob))
      mydb.commit()


InsertData()