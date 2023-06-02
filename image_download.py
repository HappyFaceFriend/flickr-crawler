import requests
import os

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    if response.status_code == 200:
        # Create the directory if it doesn't exist
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("Image downloaded successfully.")
    else:
        print("Failed to download the image.")
