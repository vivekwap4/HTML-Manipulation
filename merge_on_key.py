# This script merges multiple html and image files into a single html file
# Also converts images to their base64 encodings and appends the encodings in the src attribute of the <img> tag
# The assumed scenario is that file names start with a common key but can differ after that. There could be multiple keys among multiple files
# Run from terminal/cmd, pass the address of folder containing all the files as the input

# Example of files for this scenario:
# key1001.html, key1002.html, key1003.jpg, key2001.html, key2002.jpg, key2003.html
# Output files: key1.html, key2.html
# The order of the content in the html will depend on how the initial files are named. The script will sort them alphabetically and then perform the merging

from bs4 import BeautifulSoup
from PIL import Image
import base64, glob, os, cv2, re

directory = input()

# Dictionary saves keys from filenames and the associated files as values
file_dict = dict()

prev_file = ""
cur_file = ""

html_folder_path = directory+'\\Output'
os.mkdir(html_folder_path)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#Initial html for the final output files
initial = '''<html>
<head></head>
<body></body>
</html>'''

# Read All the files in the directory 
for file in os.listdir(directory):

	#The key of the filename
	file_key = file.split("_")[0]
	
	if file_key not in file_dict:
		file_dict[file_key] = [file]
	else:
		file_dict[file_key].append(file)

#One key would be one output html file after merging all the files with the associated key
#Iterate over every key
for key in file_dict:
	
	#Create a new merged html file
	final_html_file = open(directory+'\\'+key+'.html','w')
	final_html_file.write(initial)
	final_html_file.close()
	
	#Get all the files associated with the current key
	file_list = file_dict[key]
	#Sort all the files according to their names
	file_list.sort(key=natural_keys)

	#BeautifulSoup object of the output file
	soup_final = BeautifulSoup(open(directory+'\\'+key+'.html'), 'html.parser')
	
	#Iterate over each file associated with the current key
	for file in file_list:
		
		#Check if this is the first file in the list of files
		if not prev_file:
			prev_file = file.split('_')[3]
		cur_file = file.split('_')[3]
		
		#If file is an html file
		if file.endswith(".html") or file.endswith(".HTML"):
			html_file = open(directory+'\\'+file).read()
			
			#BeautifulSoup object of the current html file
			soup_temp = BeautifulSoup(html_file)
			
			#Body of the current html file
			soup_temp_body = soup_temp.find('body')
			
			#Body content of the current html file. Returns an array of child tags
			soup_temp_body_content = soup_temp_body.findChildren(recursive = False)
			
			#Body content array could be of variable length depending on the number of child tags. Append the current file's body 
			#content to the final merged file's body tag
			if len(soup_temp_body_content) is not 0:
				for content in soup_temp_body_content:
					soup_final.body.append(content)
			else:
				soup_final.body.append(soup_temp_body)
			soup_final.body.append(soup_final.new_tag('br'))
			
			prev_file = cur_file
		
		#If the current file is an image		
		elif file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG") or file.endswith(".PNG"):
			with open(os.path.join(directory, file), "rb") as image_file:
			
				#Base64 encoding of the image
				encoded_string = base64.b64encode(image_file.read())
				
				#Create a temporary image tag 
				temp_tag ='''<img border="0" src="" /><br>'''
				
				#Initialize a beautifulsoup object containing the temporary img tag
				soup_temp = BeautifulSoup(temp_tag)
				
				#Add the base64 encoding of the image in the temporary img tag
				final_img_tag = soup_temp.find('img')
				final_img_tag['src'] = "data:image/png;base64, " + encoded_string.decode('utf-8')
				
				#Add the img tag to the final merged file's body tag
				soup_final.body.append(soup_temp)
		else:
			continue
	
	#Save the current merged file named after the key. This file is the output of merging of all the files associated with the key
	with open(html_folder_path+'\\'+key+'.html', 'w') as f:
		f.write(str(soup_final))
		f.close()
		
