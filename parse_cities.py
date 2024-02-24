import json

# specify the file path
file_path = "current.city.list.json"

# load data from JSON file
with open(file_path, 'r', encoding='utf-8', errors='ignore') as json_file:
    data = json.load(json_file)

# holds data
parsed_data = []

# goes through json
for city in data:
    # creates new dictionary 
    new_entry = {
            'name' : city['name'],
            'id' : city['id']
        }
    # adds to dictionary
    parsed_data.append(new_entry)

# sorts data based off id
sorted(parsed_data, key=lambda x: x['id'])

# specify the file path
file_path = "parsed_cities.json"

# write dictionary to JSON file
with open(file_path, 'w') as json_file:
    json.dump(parsed_data, json_file, indent=4)

print(f"Data has been written to {file_path}")
