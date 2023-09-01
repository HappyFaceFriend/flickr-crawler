import file_utils
import crawl_utils
import flickr_api
import time_utils

from tqdm import tqdm

import os
import time
import csv
import datetime

### Settings ##################
crawl_utils.log_error = True    #Set this to false if you don't want error messages

LOG_TO_FILE = True  #Set this to false if you want to print to console.
LOG_FILE_PATH = f"results/logs/log-{datetime.datetime.today().strftime('%y%m%d%H%M')}.txt"

API_KEY_FILE_PATH = "api_key.txt"  #Put your API Key at the first line of this file

PER_PAGE = 100  #max : 500
MAX_PHOTO_PER_QUERY = 4000 #4000 is recommended
SIZE_PREFERENCE = ["Large", "Large 1024", "Medium 800", "Medium 640", "Original"] #first is prioritized

TEXT = "portrait with landscape" #the search keyword
MIN_DATE = "2010/01/01"
MAX_DATE = "2023/09/02"
#Set to this to search up to today's photos.
#MAX_DATE = time_utils.unixtime2str(time_utils.today_unixtime())

OUTPUT_IMAGE_DIR = f"results/images/{TEXT}/"

def image_name_setter(photo_data):
    return f"f_{photo_data['id']}-{photo_data['owner']}.jpg"

OUTPUT_CSV_PATH = f"results/datas/{TEXT}.csv"
CSV_KEYS = ["id", "title", "owner", "name"]

def download_success_callback(photo_data):
    #Write to csv
    with open(OUTPUT_CSV_PATH, mode='a', encoding = 'utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = CSV_KEYS)
        photo_data["name"] = image_name_setter(photo_data)
        line = {key: photo_data[key] for key in CSV_KEYS}
        writer.writerow(line)

###############################

def crawl():
    if LOG_TO_FILE:
        file_utils.set_log_to_file(LOG_FILE_PATH)

    #Set API Key
    crawl_utils.set_api_key(API_KEY_FILE_PATH)


    total_downloaded_count = 0
    total_skipped_count = 0

    min_date = time_utils.str2unixtime(MIN_DATE)
    max_date = time_utils.str2unixtime(MAX_DATE)

    def binary_search_download(min_date, max_date):
        global total_skipped_count, total_downloaded_count
        l_date, r_date = min_date, max_date

        if l_date > r_date:
            l_date = r_date

        min_date_formatted = time_utils.unixtime2str(l_date)
        max_date_formatted = time_utils.unixtime2str(r_date)

        search_params = crawl_utils.SearchParams(TEXT, 1, l_date, r_date, PER_PAGE)

        total_count = crawl_utils.get_total_photo_count(search_params)
        if total_count == -1:
            print(f"Fatal Error!! : failed to search photos in [{min_date_formatted}~{max_date_formatted}], therefore skipping this timeframe")
            return
        
        if total_count <= MAX_PHOTO_PER_QUERY or l_date == r_date:
            max_page = max(total_count-1, 0) // PER_PAGE + 1
            
            search_params = crawl_utils.SearchParams(TEXT, 1, l_date, r_date, PER_PAGE)
            print(f"Downloading {min_date_formatted}~{max_date_formatted}")
            for page_num in tqdm(range(1, max_page + 1), desc=f"Downloading {min_date_formatted}~{max_date_formatted}"):
                search_params.page = page_num
                download_results = crawl_utils.downwload_single_page(search_params, SIZE_PREFERENCE, image_name_setter, OUTPUT_IMAGE_DIR, download_success_callback)
                if download_results is None:
                    print(f"Fatal Error!! : failed to search photos in [{min_date_formatted}~{max_date_formatted}] page {page_num}, therefore skipping this page")
                    continue
                print(f"Page {page_num} : {download_results}")
                total_downloaded_count += download_results["downloaded"]
                total_skipped_count += download_results["skipped"]
        else:
            mid_date = (l_date + r_date) // 2 
            binary_search_download(l_date, mid_date)
            binary_search_download(mid_date + 1, r_date)

    binary_search_download(min_date, max_date)

    print(f"All images downladed successfully!!")
    print(f"Downloaded {total_downloaded_count}, Skipped {total_skipped_count}.")


if __name__ == '__main__':
    crawl()