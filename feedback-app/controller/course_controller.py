import json
from flask import Response, request

from controller import bp
from model.course import Course
from repository.course_repository import CourseRepository


repository = CourseRepository()


@bp.route("/courses", methods=['GET'])
def get_all_courses() -> Response:
    courses = repository.get_all()
    if courses is None:
        msg = json.dumps({"message": "невозможно получить список курсов"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    else:
        json_list = json.dumps(courses, default=lambda x: x.__dict__, ensure_ascii=False)
        return Response(json_list, status=200, mimetype='application/json')


@bp.route("/courses/<id>", methods=['GET'])
def get_one_course(id: int) -> Response:
    course = repository.get_one(id)
    if course is None:
        msg = json.dumps({"message": "курс с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    json_list = json.dumps(course, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/courses/add", methods=['POST'])
def add_course() -> Response:
    entity = new_get_json()
    res = repository.add_courses(entity)
    if res is None:
        msg = json.dumps({"message": "не удалось добавить курс"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    msg = json.dumps({"message": "курс успешно сохранен"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')
    

@bp.route("/courses/delete/<id>", methods=['DELETE'])
def delete_course(id: int) -> Response:
    course = repository.delete_course(id)
    if course is None:
        msg = json.dumps({"message": "курс с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "курс успешно удален"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')


@bp.route("/courses/update/<id>", methods=['POST'])
def update_course(id: int) -> Response:
    entity = new_get_json()
    course = repository.update_course(id, entity)
    if course is None:
        msg = json.dumps({"message": "курс с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "курс успешно изменен"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')


def new_get_json():
    """
    This method executes data receiving from json.
    """

    content = request.get_json()
    field_of_knowledge = content.get("field_of_knowledge", None)
    short_name = content.get("short_name", None)
    full_name = content.get("full_name", None)
    size = content.get("size", None)
    description = content.get("description", None)
    direction = content.get("direction", None)
    lecturer_id = content.get("lecturer_id", None)
    year = content.get("year", None)

    def response (field: str):
        if field is None or type(field) is not str:
            msg = json.dumps({"message": "{field} должен быть валидной строкой"}, ensure_ascii=False)
            return Response(msg, status=422, mimetype='application/json')
    response(field_of_knowledge)
    response(short_name)
    response(full_name)
    response(size)
    response(direction)
    response(description)
    response(year)

    if lecturer_id is None or type(lecturer_id) is not int:
        msg = json.dumps({"message": "lecturer_id должен быть числом"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    
    entity = Course()
    entity.field_of_knowledge = field_of_knowledge 
    entity.short_name = short_name
    entity.full_name = full_name
    entity.size = size
    entity.description = description
    entity.direction = direction
    entity.lecturer_id = lecturer_id
    entity.year = year
    return entity
