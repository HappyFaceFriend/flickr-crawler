import file_utils
import crawl_utils
import flickr_api

from tqdm import tqdm

import os
import time
import datetime



PER_PAGE = 100

MAX_PHOTO_PER_QUERY = 4000

MIN_DATE = "January 1, 2010"
MAX_DATE = "June 5, 2023"
#Set to this to search up to today's photos
#MAX_DATE = int(datetime.datetime.today().timestamp())

TEXT = "portrait with landscape"

API_KEY_FILE_PATH = "api_key.txt"

OUTPUT_CSV_PATH = f"results/datas/{TEXT}-2.csv"
OUTPUT_IMAGE_DIR = "results/images2/"

size_preference = ["Large", "Large 1024", "Medium 800", "Medium 640", "Original"]

#Set API Key
crawl_utils.set_api_key(API_KEY_FILE_PATH)


csv_keys = ["id", "title", "owner"]
already_downloaded_datas = []

#Retrieve all ids of downloaded images from csv file, create one if not exists
if not os.path.exists(OUTPUT_CSV_PATH):
    file_utils.create_csv(OUTPUT_CSV_PATH, csv_keys)
else:
    already_downloaded_datas = file_utils.read_from_csv(OUTPUT_CSV_PATH)


total_downloaded_count = 0
total_skipped_count = 0


min_date = int(datetime.datetime.strptime(MIN_DATE, "%B %d, %Y").timestamp())
max_date = int(datetime.datetime.strptime(MAX_DATE, "%B %d, %Y").timestamp())

def binary_search_download(min_date, max_date):
    global total_skipped_count, total_downloaded_count
    l_date, r_date = min_date, max_date

    search_response = flickr_api.search_photos(TEXT, per_page = 1, page = 1, upload_date_boundaries = (l_date, r_date))

    total_count = search_response["total"]
    if total_count > MAX_PHOTO_PER_QUERY:
        mid_date = (l_date + r_date) // 2 
        binary_search_download(l_date, mid_date)
        binary_search_download(mid_date + 1, r_date)
    else:
        max_page = max(total_count-1, 0) // PER_PAGE + 1
        
        min_date_formatted = datetime.datetime.fromtimestamp(min_date).strftime("%y/%m/%d")
        max_date_formatted = datetime.datetime.fromtimestamp(max_date).strftime("%y/%m/%d")
        for page_num in tqdm(range(1, max_page + 1), desc=f"Downloading {min_date_formatted}~{max_date_formatted}"):
            #API request for search
            search_response = flickr_api.search_photos(TEXT, per_page = PER_PAGE, page = page_num, upload_date_boundaries = (l_date, r_date))
            download_result = crawl_utils.download_search_results(search_response, size_preference, already_downloaded_datas, OUTPUT_IMAGE_DIR, OUTPUT_CSV_PATH, csv_keys, visualize = True)
            print(f"Page {page_num} : {download_result}")
            total_downloaded_count += download_result["downloaded"]
            total_skipped_count += download_result["skipped"]

binary_search_download(min_date, max_date)

print(f"All images downladed successfully!!")
print(f"Downloaded {total_downloaded_count}, Skipped {total_skipped_count}.")