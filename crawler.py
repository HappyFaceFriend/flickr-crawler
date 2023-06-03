import file_utils
import flickr_api

from tqdm import tqdm

import csv
import os

PER_PAGE = 100
PAGE_START = 1
PAGE_END = 500

TEXT = "portrait with landscape"
TAG_MODE = "all"
SORT = "relevance"

API_KEY_FILE_PATH = "api_key.txt"

OUTPUT_CSV_PATH = f"results/datas/{TEXT}.csv"
OUTPUT_IMAGE_DIR = "results/images/"


#Get API key from txt file
with open(API_KEY_FILE_PATH, 'r', encoding='utf-8') as file:
    api_key = file.readline().strip()
    flickr_api.set_api_key(api_key)


output_dir = os.path.dirname(OUTPUT_CSV_PATH)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

data_keys = ["id", "title"]
with open(OUTPUT_CSV_PATH, mode='w', encoding = 'utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames = data_keys)
    writer.writeheader()


for page_num in range(PAGE_START, PAGE_END + 1):
    #API request
    search_response = flickr_api.search_photos(TEXT, per_page = PER_PAGE, page = page_num, sort = SORT)
    search_results = search_response["photos"]

    #Download the photos
    downloaded_photos = []
    for searched_record in tqdm(search_results, desc = f"Page {page_num}"):
        #API reqeust
        photo_data = flickr_api.get_photoURL(searched_record["id"])

        #Download photo if avilable.
        if photo_data["candownload"]:
            image_url = photo_data["sizes"]["Original"]["source"]
            file_utils.download_and_save_image(image_url, OUTPUT_IMAGE_DIR + searched_record["id"] + ".jpg")
            downloaded_photos.append(searched_record)

            with open(OUTPUT_CSV_PATH, mode='a', encoding = 'utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames = data_keys)
                line = {key: searched_record[key] for key in data_keys}
                writer.writerow(line)

    print(f"Downloaded {len(downloaded_photos)} / {len(search_results)}")
    