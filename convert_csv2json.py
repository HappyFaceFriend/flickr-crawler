import file_utils
import json

CSV_PATH = "results/datas/portrait with landscape-3.csv"
JSON_PATH = "results/datas/portrait with landscape-3.json"

#Read CSV
data = file_utils.read_from_csv(CSV_PATH)

### Modify data here ###############




####################################

#Write JSON
json_data = json.dumps(data)
with open(JSON_PATH, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)