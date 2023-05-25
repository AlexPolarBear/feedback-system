import os
import sys

from db_proxy_interface import DB_Proxy_Interface
from json_interface import JSON_Interface

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the path to the 'ranking' directory
ranking_dir = os.path.join(current_dir, '..', '..', 'ranking', 'ranking_system')

# Add the 'ranking' directory to sys.path
sys.path.append(ranking_dir)

from rankingSystem import RankingSystem
from io_rankingSystem import IO_RankingSystem 

class Ranking_Interface:
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
        JSON_Interface.store_data_to_json('../data/courses.json', courses)
        print(courses)
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