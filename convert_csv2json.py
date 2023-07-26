import file_utils
import json

CSV_PATH = "../sandbox/datas/portrait with eiffel tower.csv"
JSON_PATH = "../sandbox/datas/d.json"

#Read CSV
data = file_utils.read_from_csv(CSV_PATH)

### Modify data here ###############
print(len(data))


####################################

#Write JSON
json_data = json.dumps(data)
with open(JSON_PATH, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)