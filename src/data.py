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
        
def get_feedback_by_course_id(course_id):
    feedback_data = load_data('../data/feedback.json')
    return [feedback_item for feedback_item in feedback_data if feedback_item['course_id'] == course_id]

def add_feedback(course_id, feedback_text):
    feedback_data = load_data('../data/feedback.json')
    max_id = max([feedback_item["id"] for feedback_item in feedback_data])
    new_feedback = {
        'id': max_id + 1,
        'course_id': course_id,
        'text': feedback_text  
    }
    feedback_data.append(new_feedback)
    store_data('../data/feedback.json', feedback_data)

# faculty.json: [{id, name}]
# direction.json: [{id, faculty_id, name}]
# courses.json: [{id, [direction.id], name}]
# feedback.json: [{id, course.id, text}]