import threading
import os
import datetime

# from db_client import DB_Client
from ranking_interface import Ranking_Interface
from json_interface import JSON_Interface

class DB_Proxy_Interface:
    @staticmethod
    def get_all_courses():
        filename = '../data/courses.json'
        if os.path.exists(filename):
            return JSON_Interface.load_data_from_json(filename)
        courses = Ranking_Interface.get_all_courses()
        JSON_Interface.store_data_to_json(filename, courses)
        return courses
    
    @staticmethod
    def get_course_by_short_name(short_name):
        courses = DB_Proxy_Interface.get_all_courses()
        for course in courses:
            if course['short_name'] == short_name:
                return course

    @staticmethod
    def get_lecturer_name_by_id(lecturer_id):
        DB_Proxy_Interface.__update_all_lecturers()
        with DB_Proxy_Interface.lecturers_lock:
            name = DB_Proxy_Interface.ALL_LECTURERS[str(lecturer_id)]
            if name != None:
                return name
            return 'Unknown'

        
    @staticmethod        
    def get_feedback_for_course(course_short_name, lecturer_id):
        DB_Proxy_Interface.__update_all_feedback()
        course_feedback = []
        with DB_Proxy_Interface.feedback_lock:
            for feedback_key in DB_Proxy_Interface.ALL_FEEDBACK:
                print(feedback_key)
                if feedback_key[0] == course_short_name and feedback_key[2] == lecturer_id:
                    course_feedback.append(DB_Proxy_Interface.ALL_FEEDBACK[feedback_key])
        return course_feedback
    

    @staticmethod     
    def get_metric_name_by_id(metric_id):
        DB_Proxy_Interface.__update_all_metrics()
        with DB_Proxy_Interface.metrics_lock:
            return DB_Proxy_Interface.ALL_METRICS[metric_id]

            
    @staticmethod  
    def get_score_by_chat_id(course_short_name, chat_id, metric_id, lecturer_id):
        DB_Proxy_Interface.__update_all_score()
        score_key = course_short_name, chat_id, metric_id, lecturer_id
        with DB_Proxy_Interface.score_lock:
            score_item = DB_Proxy_Interface.ALL_SCORES.get(score_key)
            if score_item != None:
                return score_item['score']
            return None

    @staticmethod  
    def get_summary_score_for_course(course_short_name, chat_id, metric_id, lecturer_id):
        DB_Proxy_Interface.__update_all_score()
        summary_score, estimator_count = 0, 0
        with DB_Proxy_Interface.score_lock:
            for score_key in DB_Proxy_Interface.ALL_SCORES:
                if score_key[0] == course_short_name and score_key[2] == metric_id and score_key[3] == lecturer_id:
                    summary_score += DB_Proxy_Interface.ALL_SCORES[score_key]['score']
                    estimator_count += 1 
        if estimator_count == 0:
            return 'нет оценок'
        score_string = "{:.2f}/10".format(summary_score / estimator_count)
        personal_score = DB_Proxy_Interface.get_score_by_chat_id(course_short_name, chat_id, metric_id, lecturer_id)
        if personal_score != None:
            score_string += " <b>({})</b>".format(personal_score)
        return score_string

    @staticmethod  
    def add_or_replace_score(chat_id, metric_id, course_short_name, score, lecturer_id):
        new_score_item = {
            "metric_id": metric_id,
            "course_short_name": course_short_name,
            "author_id": chat_id,
            "score": score,
            "lecturer_id": lecturer_id,
            "date": DB_Proxy_Interface.__get_current_date()
        }
        Ranking_Interface.add_or_replace_score(new_score_item)


    @staticmethod  
    def add_feedback(course_short_name, chat_id, review_text, lecturer_id):
        new_feedback_item = {
            'course_short_name': course_short_name,
            'author_id': chat_id,
            'date': DB_Proxy_Interface.__get_current_date(),
            'lecturer_id': lecturer_id,
            'text': review_text,
            'feedback_id': None
        }
        Ranking_Interface.add_feedback(new_feedback_item)
        
    # STATIC VARIABLES

    ALL_LECTURERS = None
    lecturers_lock = threading.Lock()

    ALL_METRICS = None
    metrics_lock = threading.Lock() 

    ALL_SCORES = None    
    score_lock = threading.Lock() 

    ALL_FEEDBACK = None
    feedback_lock = threading.Lock() 

    # PRIVATE METHODS

    @staticmethod  
    def __update_all_lecturers():
        with DB_Proxy_Interface.lecturers_lock:
            if DB_Proxy_Interface.ALL_LECTURERS == None:
                DB_Proxy_Interface.ALL_LECTURERS = Ranking_Interface.get_all_lecturers()

    @staticmethod  
    def __update_all_feedback():
        if Ranking_Interface.feedback_need_to_update == True:
            feedback = Ranking_Interface.get_all_feedback()
            with DB_Proxy_Interface.feedback_lock:
                DB_Proxy_Interface.ALL_FEEDBACK = feedback

    @staticmethod
    def __update_all_metrics():
        with DB_Proxy_Interface.metrics_lock:
            if DB_Proxy_Interface.ALL_METRICS == None:
                DB_Proxy_Interface.ALL_METRICS = Ranking_Interface.get_all_metrics()

    @staticmethod  
    def get_all_metrics():
        DB_Proxy_Interface.__update_all_metrics()
        with DB_Proxy_Interface.metrics_lock:
            return list(DB_Proxy_Interface.ALL_METRICS.items())
        
    @staticmethod         
    def __update_all_score():
        if Ranking_Interface.score_need_to_update == True:
            score = Ranking_Interface.get_all_score()
            with DB_Proxy_Interface.score_lock:
                DB_Proxy_Interface.ALL_SCORES = score


    @staticmethod  
    def __get_current_date():
        current_date = datetime.date.today()
        formatted_date = current_date.strftime('%d.%m.%Y')
        return formatted_date