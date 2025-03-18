import gdown

# Google Drive file ID
file_id = '14uqfD0U96xSw1ZudAAq0h7pu5MkUGZQm'

# Construct the direct download URL
url = f'https://drive.google.com/uc?id={file_id}'

# Download the file
output = 'samples.json'
gdown.download(url, output, quiet=False)

print(f'File downloaded successfully and saved as {output}')