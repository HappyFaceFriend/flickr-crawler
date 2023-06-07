import requests
import os
import csv
import sys
import json


def check_and_create_dir(save_path):
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_dicts_csv(datas, desired_keys, save_path):
    check_and_create_dir(save_path)

    with open(save_path, mode='w', encoding = 'utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = desired_keys)
        writer.writeheader()
        for result in datas:
            record = {key: result[key] for key in desired_keys}
            writer.writerow(record)

#Create csv data file
def create_csv(output_csv_path, data_keys):
    check_and_create_dir(output_csv_path)
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


def set_log_to_file(output_file_path):
    check_and_create_dir(output_file_path)
    log_file = open(output_file_path, 'w', encoding='utf-8', buffering = 1)
    sys.stdout = log_file

def csv_to_json(csv_path, output_json_path):
    check_and_create_dir(output_json_path)
    data = read_from_csv(csv_path)
    json_data = json.dumps(data)
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)


def get_file_names_in_dir(dir_path):
    check_and_create_dir(dir_path)
    file_names = os.listdir(dir_path)
    return [file_name for file_name in file_names if os.path.isfile(os.path.join(dir_path, file_name))]