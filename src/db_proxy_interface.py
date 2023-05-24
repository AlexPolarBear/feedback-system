import json
import os

from db_client import DB_Client
from json_interface import JSON_Interface

class DB_Proxy_Interface:
    @staticmethod
    def get_all_courses():
        filename = '../data/course.json'
        if os.path.exists(filename):
            return JSON_Interface.load_data_from_json(filename)
        courses = DB_Client.get_all_courses()
        JSON_Interface.store_data_to_json(filename, courses)
        return courses
    
    @staticmethod
    def get_course_by_id(course_id):
        courses = DB_Proxy_Interface.get_all_courses()
        for course in courses:
            if course['id'] == course_id:
                return course

    @staticmethod      
    def get_courses_by_user_request(request):
        # TODO: Need to return courses that match user request
        return DB_Proxy_Interface.get_all_courses()

    @staticmethod  
    def get_all_feedback():
        filename = '../data/review.json'
        if DB_Client.feedback_need_to_update == False and os.path.exists(filename):
            return JSON_Interface.load_data_from_json(filename)
        feedback = DB_Client.get_all_feedback()
        JSON_Interface.store_data_to_json(filename, feedback)
        return feedback

    @staticmethod        
    def get_feedback_by_course_id(course_id):
        feedback = DB_Proxy_Interface.get_all_feedback()
        return [feedback_item for feedback_item in feedback if feedback_item['course_id'] == course_id]

    @staticmethod  
    def get_all_metrics():
        filename = '../data/metrics.json'
        if os.path.exists(filename):
            return JSON_Interface.load_data_from_json(filename)
        metrics = DB_Client.get_all_metrics()
        JSON_Interface.store_data_to_json(filename, metrics)
        return metrics

    @staticmethod     
    def get_metric_name_by_id(metric_id):
        metrics = DB_Proxy_Interface.get_all_metrics()
        for metric in metrics:
            if metric['id'] == metric_id:
                return metric['name']

    @staticmethod         
    def get_all_score():
        filename = '../data/score.json'
        if DB_Client.score_need_to_update == False and os.path.exists(filename):
            return JSON_Interface.load_data_from_json(filename)
        score = DB_Client.get_all_score()
        JSON_Interface.store_data_to_json(filename, score)
        return score
            
    @staticmethod  
    def get_metric_score_by_chat_id(course_id, metric_id, chat_id):
        score_data = DB_Proxy_Interface.get_all_score()
        for score_item in score_data:
            if score_item['author_id'] == chat_id and score_item['metric_id'] == metric_id and score_item['course_id'] == course_id:
                return score_item['score']
        return None

    @staticmethod  
    def get_metric_score_by_metric_id(course_id, metric_id, chat_id):
        score_data = DB_Proxy_Interface.get_all_score()
        summary_score, estimator_count = 0, 0
        for score_item in score_data:
            if score_item['metric_id'] == metric_id and score_item['course_id'] == course_id:
                summary_score += score_item['score']
                estimator_count += 1 
        if estimator_count == 0:
            return 'нет оценок'
        score_string = "{:.2f}/10".format(summary_score / estimator_count)
        personal_score = DB_Proxy_Interface.get_metric_score_by_chat_id(course_id, metric_id, chat_id)
        if personal_score != None:
            score_string += " <b>({})</b>".format(personal_score)
        return score_string
        

    @staticmethod  
    def add_or_replace_score(chat_id, metric_id, course_id, score):
        new_score_item = {
            "metric_id": metric_id,
            "course_id": course_id,
            "author_id": chat_id,
            "score": score
        }
        DB_Client.add_or_replace_score(new_score_item)


    @staticmethod  
    def add_feedback(course_id, chat_id, review_text):
        new_feedback_item = {
            'course_id': course_id,
            'author_id': chat_id,
            'text': review_text
        }
        DB_Client.add_feedback(new_feedback_item)
        
    # RECOMENDATION SECTION

    # temporary artificial method
    @staticmethod  
    def get_tag_by_id(id):
        tag = {
            "id": id,
            "title": 'tag-{}'.format(id),
            "type": None
        }
        return tag

    @staticmethod  
    def get_all_tags():
        return [DB_Proxy_Interface.get_tag_by_id(id) for id in range(4)]

    @staticmethod  
    def get_user_tags():
        return [DB_Proxy_Interface.get_tag_by_id(id) for id in range(4)]

    