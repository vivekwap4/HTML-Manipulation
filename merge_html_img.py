#This script merges html files and images in a folder into a single output html file
#It also converts the image file into base64 encoding and uses the encoding in the img tag
#Run using terminal/cmd and pass the folder path as input


# Example of files for this scenario:
# eg.html, eg1.html, eg3.jpg, eg2.html, eg4.jpg
# Output file: new.html (With all the contents of eg.html, eg1.html, eg3.jpg, eg2.html, and eg4.jpg)
# The order of the content in the html will depend on how the initial files are named. The script will sort them alphabetically and then perform the merging

from bs4 import BeautifulSoup
from PIL import Image
import base64, glob, os, cv2, re

directory = input()

filelist = list()

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

for file in os.listdir(directory):
	filelist.append(filename)

# Sort files alphabetically	
filelist.sort(key=natural_keys)

#Create an output html file
final_html_file = open(directory+'\\new.html','w')

#Initial html code for the final output files
initial = '''<html>
<head></head>
<body></body>
</html>'''

# Write the initial html code into the output file
final_html_file.write(initial)
final_html_file.close()

# BeautifulSoup object of the output file
soup_final = BeautifulSoup(open(directory+'\\new.html'), 'html.parser')
	
# Iterate over every file in the folder
for file in filelist:

	#If the current file is an html file
	if file.endswith(".html") or file.endswith(".HTML"):
		html_file = open(directory+"\\"+file).read()
		
		# Beautifulsoup object of the current html file
		soup_temp = BeautifulSoup(html_file)
		
		# Body of the current html file
		soup_temp_body = soup_temp.find('body')
		
		# Returns an array of child tags of the body
		soup_temp_body_content = soup_temp_body.findChildren(recursive = False)
		
		#If the body has more than one child tags
		if len(soup_temp_body_content) is not 0:
			for content in soup_temp_body_content:
				soup_final.body.append(content)
		else:
			soup_final.body.append(soup_temp_body_content)
		
	
	#If the current file is an image file
	elif file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG") or file.endswith(".PNG"):
		with open(os.path.join(directory, file), "rb") as image_file:
			
			#Base64 encoding of the image
			encoded_string = base64.b64encode(image_file.read())
			
			#Create a temporary image tag 
			temp_tag ='''<img border="0" src="" /><br><hr>'''
			
			#Initialize a beautifulsoup object containing the temporary img tag
			soup_temp = BeautifulSoup(temp_tag)
			
			#Add the base64 encoding of the image in the temporary img tag
			final_img_tag = soup_temp.find('img')
			final_img_tag['src'] = "data:image/png;base64, " + encoded_string.decode('utf-8')
			
			#Add the img tag to the final merged file's body tag
			soup_final.body.append(soup_temp)
	else:
		continue

#Save the merged html string into the output file
with open(directory+'\\new.html', 'w') as f:
    f.write(str(soup_final.prettify()))
    f.close()
