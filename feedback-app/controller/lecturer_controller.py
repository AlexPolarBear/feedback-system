import json
from flask import Response, request

from controller import bp
from model.lecturer import Lecturer
from repository.lecturer_repository import LecturerRepository


repository = LecturerRepository()


@bp.route("/lecturers", methods=['POST'])
def add_lecturer() -> Response:
    content = request.get_json()
    name = content.get("name", None)

    if name is None or type(name) is not str:
        msg = json.dumps({"message": "name должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    
    entity = Lecturer()
    entity.name = name

    lecturer = repository.add_lecturer(entity)
    if lecturer is None:
        msg = json.dumps({"message": "не удалось добавить преподавателя"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    msg = json.dumps({"message": "преподаватель успешно сохранен"}, ensure_ascii=False)
    return Response(msg, status=201, mimetype='application/json')


@bp.route("/lecturers/name/<name>", methods=['GET'])
def get_id_by_name(name: str) -> Response:
    lecturer = repository.get_id_by_lecturer_name(name)
    if lecturer is None:
        msg = json.dumps({"message": "преподаватель с данным именем отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    return Response(lecturer, status=200, mimetype='application/json')


@bp.route("/lecturers/delete/<id>", methods=['DELETE'])
def delete_lecturer(id: int) -> Response:
    lecturer = repository.delete_lecturer(id)
    if lecturer is None:
        msg = json.dumps({"message": "преподаватель с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "преподаватель успешно удален"}, ensure_ascii=False)
    return Response(msg, status=202, mimetype='application/json')


@bp.route("/lecturers", methods=['GET'])
def get_all_lecturer() -> Response:
    lecturers = repository.get_all_lecturer()
    if lecturers is None:
        msg = json.dumps({"message": "невозможно получить список преподавателей"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    json_list = json.dumps(lecturers, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/lecturers/id/<id>", methods=['GET'])
def get_one_lecturer(id: int) -> Response:
    lecturer = repository.get_one_lecturer(id)
    if lecturer is None:
        msg = json.dumps({"message": "преподаватель с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    json_list = json.dumps(lecturer, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/lecturers/update/<id>", methods=['POST'])
def update_lecturer(id: int) -> Response:
    content = request.get_json()
    name = content.get("name", None)
    if name is None or type(name) is not str:
        msg = json.dumps({"message": "name должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')

    entity = Lecturer()
    entity.name = name
    lecturer = repository.update_lecturer(id, entity)
    if lecturer is None:
        msg = json.dumps({"message": "преподаватель с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "преподаватель успешно изменен"}, ensure_ascii=False)
    return Response(msg, status=201, mimetype='application/json')
