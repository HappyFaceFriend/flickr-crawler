from flickr_api import set_api_key, search_photos, get_photoURL
from image_download import download_image

#Get API key from txt file
with open("api_key.txt" , 'r', encoding='utf-8') as file:
    api_key = file.readline().strip()

set_api_key(api_key)

result = get_photoURL("52942512659")
print(result)

# Example usage
image_url = result["sizes"]["Original"]["source"]  # Replace with the actual image URL

download_image(image_url, "results/images/52942512659.jpg")

'''
search_results = search_photos("portrait with landscape", per_page = 500, page = 1, sort = "interestingness_desc")["photos"]

for photo in search_results:
    photo_id = photo["id"]
    photo_title = photo["title"]
    print("Photo ID:", photo_id)
    print("Title:", photo_title)
    print("-----")
'''
