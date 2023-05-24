from db_proxy_interface import DB_Proxy_Interface

def get_courses_by_user_request(request):
    # TODO: Need to return courses that match user request
    return DB_Proxy_Interface.get_all_courses()

def get_tags_by_user_request(request):
    return ['tag1', 'tag2', 'tag3']
