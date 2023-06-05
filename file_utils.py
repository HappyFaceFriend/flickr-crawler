import requests
import os
import csv

def download_and_save_image(url, save_path):
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
        return True
    return False

def save_dicts_csv(datas, desired_keys, save_path):
    output_dir = os.path.dirname(save_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(save_path, mode='w', encoding = 'utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = desired_keys)
        writer.writeheader()
        for result in datas:
            record = {key: result[key] for key in desired_keys}
            writer.writerow(record)

#Create csv data file
def create_csv(output_csv_path, data_keys):
        output_dir = os.path.dirname(output_csv_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_csv_path, mode='w', encoding = 'utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = data_keys)
            writer.writeheader()

#Read csv data file and return ids
def read_from_csv(output_csv_path):
    data = []
    file = open(output_csv_path, mode='r', encoding = 'utf-8', newline='')
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)
    file.close()
    return data
