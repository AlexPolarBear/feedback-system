import json

def load_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def store_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_faculties():
    faculty_data = load_data('../data/faculty.json')
    return faculty_data

def get_directions_by_faculty_id(faculty_id):
    direction_data = load_data('../data/direction.json')
    return [direction for direction in direction_data if direction['faculty_id'] == faculty_id]

def get_courses_by_direction_id(direction_id):
    course_data = load_data('../data/course.json')
    return [course for course in course_data if direction_id in course['direction_ids']]

def get_course_by_id(course_id):
    course_data = load_data('../data/course.json')
    for course in course_data:
        if course['id'] == course_id:
            return course
        
def get_review_by_course_id(course_id):
    review_data = load_data('../data/review.json')
    return [review_item for review_item in review_data if review_item['course_id'] == course_id]

def get_metrics():
    metrics = load_data('../data/metrics.json')
    return metrics

def get_metric_name_by_id(metric_id):
    metrics = load_data('../data/metrics.json')
    for metric in metrics:
        if metric['metric_id'] == metric_id:
            return metric['metric_name']
        
def get_metric_score_by_chat_id(course_id, metric_id, chat_id):
    score_data = load_data('../data/score.json')
    for score_item in score_data:
        if score_item['chat_id'] == chat_id and score_item['metric_id'] == metric_id and score_item['course_id'] == course_id:
            return score_item['score']
    return None

def get_metric_score_by_metric_id(course_id, metric_id, chat_id):
    score_data = load_data('../data/score.json')
    summary_score, estimator_count = 0, 0
    for score_item in score_data:
        if score_item['metric_id'] == metric_id and score_item['course_id'] == course_id:
            summary_score += score_item['score']
            estimator_count += 1 
    if estimator_count == 0:
        return 'нет оценок'
    score_string = "{:.2f}/10".format(summary_score / estimator_count)
    personal_score = get_metric_score_by_chat_id(course_id, metric_id, chat_id)
    if personal_score != None:
        score_string += " <b>({})</b>".format(personal_score)
    return score_string
    

# def add_score(course_id, metric_id, score):
#     metrics_data = load_data('../data/metrics.json')
#     for metric in metrics_data:
#         if metric['metric_id'] == metric_id:
#             for course in metric['courses']:
#                 if course['id'] == course_id:
#                     course['score'] += score
#                     course['estimator_count'] += 1
#     store_data('../data/metrics.json', metrics_data)

def add_or_replace_score(chat_id, metric_id, course_id, score):
    score_data = load_data('../data/score.json')
    already_exists = False
    for score_item in score_data:
        if score_item['chat_id'] == chat_id and score_item['metric_id'] == metric_id and score_item['course_id'] == course_id:
            score_item['score'] = score
            already_exists = True
    if not already_exists:
        new_score = {
            "chat_id": chat_id,
            "metric_id": metric_id,
            "course_id": course_id,
            "score": score
        }
        score_data.append(new_score)
    store_data('../data/score.json', score_data)

def add_review(course_id, review_text):
    review_data = load_data('../data/review.json')
    max_id = max([review_item["id"] for review_item in review_data])
    new_review = {
        'id': max_id + 1,
        'course_id': course_id,
        'text': review_text  
    }
    review_data.append(new_review)
    store_data('../data/review.json', review_data)

# faculty.json: [{id, name}]
# direction.json: [{id, faculty_id, name}]
# courses.json: [{id, [direction.id], name}]
# review.json: [{id, course.id, text}]