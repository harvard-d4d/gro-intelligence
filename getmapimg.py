import pdf2image
import os
#pip install pdf2image
from PIL import Image

for filename in os.listdir('pdfs_decrypted'):
	images = pdf2image.convert_from_path('pdfs_decrypted/' + filename) #pdf path
	if len(images) > 0:
		print (filename)
		images[-1].crop((105, 406, 2219, 1243)).save('map_data/imgs/' + filename[:-3] + 'png') #save path
