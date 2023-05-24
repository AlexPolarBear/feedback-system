import requests
import json
import time

from json_interface import JSON_Interface

class DB_Client:
    url_preffix = "http://example.com"
    feedback_need_to_update = True
    score_need_to_update = True

    @staticmethod
    def set_url_preffix(given_url_preffix):
        DB_Client.url_preffix = given_url_preffix

    @staticmethod
    def get_all_courses():
        return DB_Client.__get('/courses')

    @staticmethod
    def get_all_metrics():
        return DB_Client.__get('/metrics')

    @staticmethod
    def get_all_feedback():
        feedback = DB_Client.__get('/feedback')
        DB_Client.feedback_need_to_update = False
        return feedback
    
    @staticmethod
    def get_all_score():
        score = DB_Client.__get('/score')
        DB_Client.score_need_to_update = False
        return score
    
    @staticmethod
    def add_feedback(feedback_item):
        DB_Client.feedback_need_to_update = True
        DB_Client.__post('/feedback', feedback_item)

    @staticmethod
    def add_or_replace_score(score_item):
        DB_Client.score_need_to_update = True
        DB_Client.__post('/feedback', score_item)

    

    # PRIVATE METHODS

    @staticmethod
    def __get(url_suffix):
        # Temporary plug
        case = {
            '/courses': '../data/course.json',
            '/metrics': '../data/metrics.json',
            '/feedback': '../data/feedback.json',
            '/score': '../data/score.json',
        }
        filename = case.get(url_suffix, 'Unknown')
        return JSON_Interface.load_data_from_json(filename)

        url = DB_Client.url_preffix + url_suffix
        response = requests.get(url)
        data = []
        if response.status_code == 200:
            data = json.loads(response.text)
        else:
            DB_Client.__log_error(url, response)
        return data
    
    @staticmethod
    def __post(url_suffix, object):
        url = DB_Client.url_preffix + url_suffix
        response = requests.post(url, json=object)

        if response.status_code == 200:
            print("Feedback item submitted successfully!")
        else:
            DB_Client.__log_error(url, response)

    @staticmethod
    def __log_error(url, response):
        error_msg = f"""
Bad request:
url: {url}
status_code: {response.status_code}
            """
        print(error_msg)
        
    

    
