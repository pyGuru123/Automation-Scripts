[In reply to Abhishek]
import os
import time
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folder = '1aoonhCebvI5DddvJVGTzBvWs2BPn_yXN'

directory = "/Volumes/g2track/Shared/Egnyte Audit Reports/2022/Abhi"

last_upload = None
if os.path.exists('upload-info.txt'):
  with open('upload-info.txt') as file:
    last_upload = float(file.read())
    last_upload = datetime.fromtimestamp(last_upload)

for file in os.listdir(directory):
  filename=os.path.join(directory, f)
  if os.path.isfile(filename):
    timestamp = os.path.getctime(filename)
    creation_date = datetime.fromtimestamp(timestamp)
    if last_upload:
      if creation_date > last_upload:
          gfile = drive.CreateFile({'parents' : [{'id' : folder}],'title' : f})
          gfile.SetContentFile(filename )
          gfile.Upload()

with open('upload-info.txt', 'w') as file:
  now = datetime.now()
  timestamp = datetime.timestamp(now)
  file.write(str(timestamp))