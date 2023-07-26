# flickr-crawler
Simple flickr crawler for downloading images, using flickr's APi with python.

## Usage
This crawler will get the same images as when you search on the website.

You can specify the search text, min & max dates.

The images will be stored to a directory, and the list of them will be saves as a csv.

Due to some mysterious limit of flickr's API, where you can only get about 4000 images with the same parameters, the crawler will perform binary search for the appropriate timeframe and let you download all images.

## How to run
1. Clone the repository
2. Open crawler.py and set necessary variables. Your API key should be stored in a text file(API_KEY_FILE_PATH).
3. Run crawler.py
