import json 

class JSON_Interface:
    @staticmethod  
    def load_data_from_json(file_name):
        with open(file_name) as f:
            data = json.load(f)
        return data

    @staticmethod  
    def store_data_to_json(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
