import os
import glob
import time
from datetime import datetime
import shutil
from xml.dom import minidom
import logging



for oneFile in minidom.parse('fileconfig.xml').getElementsByTagName('file'):
        source = oneFile.getElementsByTagName("source")[0].firstChild.data.replace('\"','')
        sourcePath = oneFile.getElementsByTagName("sourcepath")[0].firstChild.data.replace('\"','')
        mockPath = oneFile.getElementsByTagName("mockpath")[0].firstChild.data.replace('\"','')
        
        

   

                            ########################################################################    
         
        path = sourcePath
        mock = mockPath
            #we shall store all the file names in this list
        filelist = []
        todelete = []
        #chkDate = "18/02/2023"
        chkDate = '2023-02-27 15:00'
        #chkTime = "06:00"
        date_time_obj = datetime.strptime(chkDate, '%Y-%m-%d %H:%M')
        date = date_time_obj.date()    #date we passed
        #print(date)
        time = date_time_obj.time()     #time we passed
        #print(time)
        #print(date)
        for root, dirs, files in os.walk(path):
	          for file in files:
            #append the file name to the list
		          filelist.append(os.path.join(root,file))

#print all the file names

        for file_path in filelist:
            #if time.strftime('%d/%m/%Y :: %H:%M',time.gmtime(os.path.getmtime(file_path))) >= "06/02/2022 :: 06:00":
        #timestamp_str = time.strftime(  '%d/%m/%Y :: %H:%M',time.gmtime(os.path.getmtime(file_path))) 
        #date = time.strftime(  '%d/%m/%Y',time.gmtime(os.path.getmtime(file_path))) 
        #time = time.strftime(  '%H:%M',time.gmtime(os.path.getmtime(file_path))) 
        #if timestamp_str>= "06/02/2022 :: 06:00":
            c_timestamp = os.path.getctime(file_path)
            
# convert creation timestamp into DateTime object
            c_datestamp = datetime.fromtimestamp(c_timestamp)
            filedate =  c_datestamp.date()       #get the date of the file
            filetime = c_datestamp.time()        #get the time of the file  
            #print(filedate)
            #print('Created Date/Time on:', c_datestamp, file_path)
           # print( c_datestamp , file_path)
        
           
            if(filedate == date and filetime >= time):        #check the date and time
               shutil.move(file_path, mock)
               print( c_datestamp , file_path)

           

       