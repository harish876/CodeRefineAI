import gdown

# Google Drive file ID
file_id = '1N4AhhmUSwiQ0ea3O57YDooJGS5ERcs2l'

# Construct the direct download URL
url = f'https://drive.google.com/uc?id={file_id}'

# Download the file
output = 'downloaded_file.json'
gdown.download(url, output, quiet=False)

print(f'File downloaded successfully and saved as {output}')