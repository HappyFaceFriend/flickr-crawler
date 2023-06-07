import flickr_api
import file_utils

import time
import csv
from tqdm import tqdm 
import requests
import json
import os
from typing import Callable

log_error = True
exception_sleep_seconds = 60

#parameters for flickr API's search
class SearchParams:
    def __init__(self, search_text : str, page : int, min_date : int, max_date : int, per_page = 100):
        self.search_text = search_text
        self.page = page
        self.min_date = min_date
        self.max_date = max_date
        self.per_page = per_page

#Get API key from txt file's first line and use it
def set_api_key(api_key_file_path):
    with open(api_key_file_path, 'r', encoding='utf-8') as file:
        api_key = file.readline().strip()
        flickr_api.set_api_key(api_key)

#Save the image in url
def download_and_save_image(url, output_image_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except:
        return False
    
    if response.status_code == 200:
        file_utils.check_and_create_dir(output_image_path)
        with open(output_image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    return False

#Download a photo by photo's id
def _download_photo(photo_id : str, size_preference : list, output_image_path : str):
    try:
        photo_urls = flickr_api.get_photoURLs(photo_id)
        #Get preferred image size
        download_size = "Original"
        for size in size_preference:
            if size in photo_urls["sizes"].keys():
                download_size = size
                break
            
        image_url = photo_urls["sizes"][download_size]["source"]
        download_success = download_and_save_image(image_url, output_image_path)
        if not download_success:
            raise Exception(f"Downloading {image_url} failed.")
    except Exception as e:
        raise Exception("Error : failed to download image. Read the error message below. \n" + str(e))

#Gets the total photo count of a search. Returns -1 if api call failed.
def get_total_photo_count(search_params : SearchParams, retry_on_exception = 1):
    retries = retry_on_exception + 1
    success = False
    while retries > 0 and (not success):
        retries -= 1
        try:
            search_result = flickr_api.search_photos(search_params.search_text, per_page = search_params.per_page, page = search_params.page, upload_date_boundaries = (search_params.min_date, search_params.max_date))
            success = True
        except Exception as e:
            if log_error:
                print(str(e))
            time.sleep(exception_sleep_seconds)
    if not success:
        return -1
    return search_result["total"]


#Downloads a single page and returns download results (count of success/failure) as a dictionary, and returns None if searching page failed. If you are trying to download a duplicate photo in the directory, it will skip it.
#output_image_name_setter : photo's data will be passed in, this function should return the filename, with extension at the end, and excluding directories.
#on_success_callback : this will be called with photo's data passed in when download was successful. Do logging stuff here.
def downwload_single_page(search_params : SearchParams, size_preference : list, output_image_name_setter : Callable[[dict], str], output_image_dir : str, on_success_callback : Callable[[dict], None], retry_on_exception = 1, enable_tqdm = True):
    download_results = {"downloaded" : 0, "skipped" : 0, "error" : 0}

    retries = retry_on_exception + 1
    success = False
    while retries > 0 and (not success):
        retries -= 1
        try:
            search_result = flickr_api.search_photos(search_params.search_text, per_page = search_params.per_page, page = search_params.page, upload_date_boundaries = (search_params.min_date, search_params.max_date))
            success = True
        except Exception as e:
            if log_error:
                print(str(e))
            time.sleep(exception_sleep_seconds)
    if not success:
        return None
    
    photo_datas = search_result["photos"]
    file_utils.check_and_create_dir(output_image_dir)
    already_downloaded_images = file_utils.get_file_names_in_dir(output_image_dir)

    collection = tqdm(photo_datas) if enable_tqdm else photo_datas
    for photo_data in collection:
        output_image_filename = output_image_name_setter(photo_data)

        if output_image_filename in already_downloaded_images:
            download_results["skipped"] += 1
            continue
        try:
            _download_photo(photo_data["id"], size_preference, f"{os.path.join(output_image_dir, output_image_filename)}")
        except Exception as e:
            download_results["error"] += 1
            if log_error:
                print(str(e))
            continue

        download_results["downloaded"] += 1
        already_downloaded_images.append(output_image_filename)
        on_success_callback(photo_data)

    return download_results
