# This script takes a folder with an html file and images as input. The images in the folder are used in the html img tags in 
# the src attribute. The output is an html file with the base64 encoding of these images embedded in the img tags, so as to eliminate
# dependency on the files.
# Run using terminal/cmd and pass the address to the folder as input

# Example contents of the input folder:
	# index.html, img01.jpg, img02.png, img45.jpg
	# These image files are being used in the src attribute of the img tags of index.html.
	# Our goal is to remove this direct dependency of the files and instead have base64 encodings of these images in the img tags
# Output:
	# new.html (Contains img tags with base64 encodings of the image files)

from bs4 import BeautifulSoup
from PIL import Image
import base64, glob, os, cv2

# A dictionary that has img files as keys and their base64 encodings as values
base64_dict = dict()

# The address to input folder
directory = input()
img_tags = ""

for filename in os.listdir(directory):

	# If the file in the directory is an image file
	if filename.endswith(".jpg") or filename.endswith(".png"):
		with open(os.path.join(directory, filename), "rb") as image_file:
			
			# Base64 encoding of the current image file
			encoded_string = base64.b64encode(image_file.read())
			
			# Store the encoding in the base64_dict with filename as the key
			base64_dict[filename] = encoded_string.decode('utf-8')
	
	# If the file is the html file
	else:
		with open(os.path.join(directory, filename), "rb") as html_file:
		
			# BeautifulSoup object of the html file
			soup = BeautifulSoup(html_file, 'html.parser')
			
			# Find all img tags of the html file
			img_tags = soup.findAll('img')

# Loop to iterate over all the img tags
for img_tag in img_tags:

	# Checking if the current tag's src (this would be the filename) is in the base64_dict
    if img_tag['src'] in base64_dict:
	    
		# Replace the filename in the src with the base64 string
        img_tag['src'] = "data:image/png;base64, " + str(base64_dict.get(img_tag['src']))

# Create a new output html file
with open(directory+'\\new.html', 'w') as f:
	
	# Writing the content of the beautifulsoup object of the html file in the new output file
    f.write(str(soup))
    f.close()
