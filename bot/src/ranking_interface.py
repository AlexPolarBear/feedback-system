import os
import sys

from json_interface import JSON_Interface

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the path to the 'ranking' directory
ranking_dir = os.path.join(current_dir, '..', 'ranking_system')

# Add the 'ranking' directory to sys.path
sys.path.append(ranking_dir)
print(sys.path)

from rankingSystem import RankingSystem
from io_rankingSystem import IO_RankingSystem 

class Ranking_Interface:
    score_need_to_update = True
    feedback_need_to_update = True

    @staticmethod
    def add_user_if_not_exists(chat_id):
        user_json = Ranking_Interface.__get_io_rk_intance().load_user_json(chat_id=4)
        print(user_json)
        if user_json == None:
            new_user_json = {
                "chat_id": chat_id,
                "context": {},
                "direction": "Математика",
                "email": "st324324324",
                "name": "Иван Васильев"
            }
            Ranking_Interface.__get_io_rk_intance().save_user(**new_user_json)

    @staticmethod
    def add_tag_to_user(chat_id, tag_title):
        Ranking_Interface.__get_io_rk_intance().add_tag_to_user(chat_id, tag_title)


    @staticmethod
    def delete_tag_from_user(chat_id, tag_title):
        Ranking_Interface.__get_io_rk_intance().delete_tag_from_user(chat_id, tag_title)

    @staticmethod
    def get_user_tag_titles(chat_id):
        user_json = Ranking_Interface.__get_io_rk_intance().load_user_json(chat_id=chat_id)
        return user_json.context.keys()


    @staticmethod
    def get_courses_by_user_request(request):
        courses = Ranking_Interface.__get_rk_intance().get_top_suitable_courses_by_text(request)
        return courses
    
    @staticmethod
    def get_relevant_courses_for_user(chat_id):
        courses = Ranking_Interface.__get_rk_intance().get_top_relevant_UserCourse(chat_id, max_count=23)
        return courses

    @staticmethod
    def get_tag_titles_by_user_request(request):
        tags = Ranking_Interface.__get_rk_intance().get_top_suitable_tags_by_text(request)
        return list(map(lambda tag: tag['title'], tags))

    @staticmethod
    def get_all_unselected_tags(chat_id):
        all_tag_titles = Ranking_Interface.__get_io_rk_intance().get_all_tags().keys()
        user_tag_titles = Ranking_Interface.get_user_tag_titles(chat_id)
        return [tag_title for tag_title in all_tag_titles if tag_title not in user_tag_titles]
    
    ### Upcoming API

    @staticmethod
    def get_all_courses():
        courses = Ranking_Interface.__get_io_rk_intance()._get_courses_jsons()
        # print(courses)
        print('krysa')
        return courses
    
    @staticmethod
    def get_all_lecturers():
        return Ranking_Interface.__get_io_rk_intance().get_all_lecturers()

    @staticmethod
    def get_all_metrics():
        return Ranking_Interface.__get_io_rk_intance().get_all_metrics()

    @staticmethod
    def get_all_feedback():
        feedback = Ranking_Interface.__get_io_rk_intance().get_all_feedback()
        print(feedback)
        print('feedback')
        Ranking_Interface.feedback_need_to_update = False
        return feedback
    
    @staticmethod
    def get_all_score():
        score = Ranking_Interface.__get_io_rk_intance().get_all_score()
        print(score)
        print('score')
        Ranking_Interface.score_need_to_update = False
        return score
    
    @staticmethod
    def add_feedback(feedback_item):
        Ranking_Interface.feedback_need_to_update = True
        Ranking_Interface.__get_io_rk_intance().save_feedback(**feedback_item)

    @staticmethod
    def add_or_replace_score(score_item):
        Ranking_Interface.score_need_to_update = True
        Ranking_Interface.__get_io_rk_intance().save_score(**score_item)

    
    rk = None
    io_rk = None

    @staticmethod
    def __get_rk_intance():
        if Ranking_Interface.rk == None:
            Ranking_Interface.rk = RankingSystem()
        return Ranking_Interface.rk
    
    @staticmethod
    def __get_io_rk_intance():
        if Ranking_Interface.io_rk == None:
            Ranking_Interface.io_rk = IO_RankingSystem()
        return Ranking_Interface.io_rk