import os
import shutil
import datetime

input_dir = "FCS/"
output_dir = "Destination/"

chkDate = '2023-02-27 15:00'
datetime_obj = datetime.datetime.strptime(chkDate, '%Y-%m-%d %H:%M')

count1 = 0
count2 = 0
for root, dirs, files in os.walk(input_dir):
	for file in files:
		count1 += 1
		path = os.path.join(root, file)
		file_ctime = os.path.getctime(path)
		file_ctime = datetime.datetime.fromtimestamp(file_ctime)
		if ( file_ctime.date() == datetime_obj.date() and 
					file_ctime.time() > datetime_obj.time()) :

			new_path = "/".join(path.split("/")[1:])
			dest_file = os.path.join(output_dir + new_path)
			dest_dir = os.path.dirname(dest_file)
			if not os.path.exists(dest_dir):
				os.makedirs(dest_dir)
			shutil.copy(path, dest_file)
			count2 += 1