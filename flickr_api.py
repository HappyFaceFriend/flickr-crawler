import requests
import json

import time

api_key = "NONE"
sleep_seconds = 1

# Set your Flickr API key
def set_api_key(key : str):
    global api_key
    api_key = key
    
# Set sleep time after each API call
def set_sleep_time(seconds = 1):
    global sleep_seconds
    sleep_seconds = seconds

# Method to search photos by text. (flickr.photos.search)
def search_photos(text : str, per_page = 100, page = 1, sort = "relevance", upload_date_boundaries = (0, 1)):
    endpoint = "https://api.flickr.com/services/rest/"

    params = {
        "method": "flickr.photos.search",
        "api_key": api_key,
        "text": text,
        "per_page" : per_page,
        "page" : page,
        "sort" : sort,
        "content_type" : 1,
        "format": "json",
        "nojsoncallback": 1,
        "privacy_filter" : 1,
        "min_upload_date": upload_date_boundaries[0],
        "max_upload_date": upload_date_boundaries[1],
    }
    if upload_date_boundaries == (0, 1):
        params.pop("min_upload_date")
        params.pop("max_upload_date")
    try:
        response = requests.get(endpoint, params=params)
        data = json.loads(response.text)

        time.sleep(sleep_seconds)
        # Process the response and extract the desired information
        # You can test results here : https://www.flickr.com/services/api/explore/flickr.photos.search
        if data["stat"] == "ok":
            photos = data["photos"]["photo"]
            pages = data["photos"]["pages"]
            total = data["photos"]["total"]
            return {"pages" : pages, "total" : total, "photos" : photos}

        else:
            raise Exception("Error : Got a bad response. \n" + data["message"])
    except Exception as e:
        raise Exception("Error : search_photos failed to get response or the response was corrupted. Read the error message below. \n" + str(e))


# Method to get urls of all available sizes of a photo. (flickr.photos.getSizes)
def get_photoURLs(photo_id : str):
    endpoint = "https://api.flickr.com/services/rest/"
    params = {
        "method": "flickr.photos.getSizes",
        "api_key": api_key,
        "photo_id": photo_id,
        "format": "json",
        "nojsoncallback": 1,
    }
    try:
        response = requests.get(endpoint, params=params)
        data = json.loads(response.text)
        time.sleep(sleep_seconds)

        # Process the response and extract the desired information
        # Can test results here : https://www.flickr.com/services/api/explore/flickr.photos.getSizes
        if data["stat"] == "ok":
            candownload = data["sizes"]["candownload"] == 1
            sizes = {}
            for size_data in data["sizes"]["size"]:
                sizes[size_data["label"]] = {"width" : size_data["width"], "height" : size_data["height"], "source" : size_data["source"], "url" : size_data["url"]}
            return {"candownload" : candownload, "sizes" : sizes}

        else:
            raise Exception("Error : Got a bad response. \n" + data["message"])
    except Exception as e:
        raise Exception("Error : get_photoURLs failed to get response or the response was corrupted. Read the error message below. \n" + str(e))