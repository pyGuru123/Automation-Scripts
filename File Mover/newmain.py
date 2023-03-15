import os

import shutil

from datetime import datetime

from xml.dom import minidom
import time
from os.path import getmtime




def copy_files(source_path, mock_path, date_time_obj):

    # Get the date and time components from the datetime object

    date = date_time_obj.date()

    time = date_time_obj.time()

    for root, dirs, files in os.walk(source_path):
       for file in files:
              fold = os.path.join(root, os.path.dirname(file))
              fold_date = datetime.fromtimestamp(getmtime(fold)).date()


              file_path = os.path.join(root, file)

              # Get the creation timestamp of the file

              c_timestamp = os.path.getctime(file_path)

              # Convert creation timestamp into a datetime object

              c_datestamp = datetime.fromtimestamp(c_timestamp)

              # Get the date and time components from the datetime object

              file_date = c_datestamp.date()

              file_time = c_datestamp.time()

              print(fold_date, file_date, fold)

              if  fold_date == date  and file_date == date and file_time >= time:
                  print('inside of if')

                  # Get the relative path of the file, relative to the source directory

                  relative_path = os.path.relpath(file_path, source_path)

                  # Construct the destination path in the backup directory

                  backup_path = os.path.join(mock_path, relative_path)

                  # Create any necessary directories in the backup path

                  os.makedirs(os.path.dirname(backup_path), exist_ok=True)

                  # Copy the file to the backup directory

                  shutil.copy2(file_path, backup_path)

                  print(c_datestamp, file_path)


##################### TO BE REMOVED #################################
date_string = '2023-03-02 06:39'
date_time_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
copy_files('FCS/', 'Destination/', date_time_obj)

#####################################################################



# Parse the XML configuration file

# xml_doc = minidom.parse('fileconfig.xml')

# for one_file in xml_doc.getElementsByTagName('file'):

#     source_path = one_file.getElementsByTagName("sourcepath")[0].firstChild.data.replace('\"', '')

#     mock_path = one_file.getElementsByTagName("mockpath")[0].firstChild.data.replace('\"', '')

#     date_string = '2023-02-28 06:00'

#     date_time_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M')



#     if not os.path.isdir(mock_path):

#         os.makedirs(mock_path)



#     copy_files(source_path, mock_path, date_time_obj)

