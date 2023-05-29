from json_interface import JSON_Interface

config = JSON_Interface.load_data_from_json('../data/config.json')

bot_token = config['bot_token']

max_page_items_count = 10