import file_utils
import flickr_api

from tqdm import tqdm

import csv
import os
import time

PER_PAGE = 100
PAGE_START = 5
PAGE_END = 600

TEXT = "portrait with landscape"

API_KEY_FILE_PATH = "api_key.txt"

OUTPUT_CSV_PATH = f"results/datas/{TEXT}.csv"
OUTPUT_IMAGE_DIR = "results/images/"


#Get API key from txt file
with open(API_KEY_FILE_PATH, 'r', encoding='utf-8') as file:
    api_key = file.readline().strip()
    flickr_api.set_api_key(api_key)


data_keys = ["id", "title"]
already_downloaded_ids = []

#Create csv data file if not exists
if not os.path.exists(OUTPUT_CSV_PATH):
    output_dir = os.path.dirname(OUTPUT_CSV_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(OUTPUT_CSV_PATH, mode='w', encoding = 'utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = data_keys)
        writer.writeheader()
else:
    #Retrieve all ids of downloaded images if csv data file exists
    file = open(OUTPUT_CSV_PATH, mode='r', encoding = 'utf-8', newline='')
    reader = csv.reader(file)
    for row in reader:
        if row:
            already_downloaded_ids.append(row[0])
    file.close()


total_downloaded_count = 0
total_skipped_count = 0

size_preference = ["Large", "Large 1024", "Medium 800", "Medium 640", "Original"]

for page_num in range(PAGE_START, PAGE_END + 1):
    #API request for search
    search_response = flickr_api.search_photos(TEXT, per_page = PER_PAGE, page = page_num)
    time.sleep(1) #sleep because 3600 request per hour limit
    search_results = search_response["photos"]

    #Download the photos
    downloaded_count = 0
    skipped_count = 0
    for searched_record in tqdm(search_results, desc = f"Page {page_num}"):
        try:
            #API reqeust for getSizes
            photo_id = searched_record["id"]
            unique_name = photo_id + searched_record["owner"]

            #Skip if already downloaded
            if unique_name in already_downloaded_ids:
                skipped_count += 1
                total_skipped_count += 1
                continue
            
            photo_data = flickr_api.get_photoURLs(photo_id)
            time.sleep(1) #sleep because 3600 request per hour limit

            #Set desired size
            download_size = "Original"
            for size in size_preference:
                if size in photo_data["sizes"].keys():
                    download_size = size
                    break
            if download_size == "Original" and not searched_record["candownload"]:
                download_size = photo_data["sizes"].keys()[-1]
            image_url = photo_data["sizes"][download_size]["source"]
        except:
            #Wait and skip if something went wrong
            try:
                print(f"\nFatal error on photo {searched_record['id']}, therefore ignoring this one")
            except:
                print("\nFatal error, therefore ignoring this one")
            time.sleep(60)
            continue

        #Download image
        file_utils.download_and_save_image(image_url, OUTPUT_IMAGE_DIR + unique_name + ".jpg")
        downloaded_count += 1
        total_downloaded_count += 1

        #Write to csv file
        searched_record["id"] = unique_name
        with open(OUTPUT_CSV_PATH, mode='a', encoding = 'utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = data_keys)
            line = {key: searched_record[key] for key in data_keys}
            writer.writerow(line)

    print(f"Downloaded {downloaded_count}, Skipped {skipped_count} out of {len(search_results)}")
    

print(f"All images downladed successfully!!")
print(f"Downloaded {total_downloaded_count}, Skipped {total_skipped_count}.")