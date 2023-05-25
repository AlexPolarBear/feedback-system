import json
from flask import Response, request

from controller import bp
from model.lecturer import Lecturer
from repository.lecturer_repository import LecturerRepository


repository = LecturerRepository()


@bp.route("/lecturers", methods=['PUT'])
def add_lecturer():
    content = request.get_json()
    name = content.get("name", None)

    if name is None or type(name) is not str:
        return Response(json.dumps({"message": "name должен быть валидной строкой"}, 
                                   ensure_ascii=False), 
                        status=422, 
                        mimetype='application/json')
    
    entity = Lecturer()
    entity.name = name

    repository.add_lecturer(entity)


@bp.route("/lecturers/name/<name>", methods=['GET'])
def get_id_by_name(name: str):
    lecturer = repository.get_id_by_lecturer_name(name)
    if lecturer is None:
        return Response(json.dumps({"message": "лектор с данным именем отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return lecturer.__dict__


@bp.route("/lecturers/delete/<id>", methods=['DELETE'])
def delete_lecturer(id: int):
    lecturer = repository.delete_lecturer(id)
    if lecturer is None:
        return Response(json.dumps({"message": "лектор с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return Response(json.dumps({"message": "лектор успешно удален"}, 
                               ensure_ascii=False), 
                    status=200, 
                    mimetype='application/json')


@bp.route("/lecturers", methods=['GET'])
def get_all_lecturer():
    lecturers = repository.get_all_lecturer()
    return json.dumps(lecturers, default=lambda x: x.__dict__)


@bp.route("/lecturers/id/<id>", methods=['GET'])
def get_one_lecturer(id: int):
    lecturer = repository.get_one_lecturer(id)
    if lecturer is None:
        return Response(json.dumps({"message": "лектор с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return lecturer.__dict__


@bp.route("/lecturers/update/<id>", methods=['POST'])
def update_lecturer(id: int):
    content = request.get_json()
    name = content.get("name", None)

    if name is None or type(name) is not str:
        return Response(json.dumps({"message": "name должен быть валидной строкой"}), 
                        status=422,
                        mimetype='application/json')

    entity = Lecturer()
    entity.name = name

    repository.update_lecturer(id, entity)
    return Response(json.dumps({"message": "лектор успешно изменен"}), 
                    status=200,
                    mimetype='application/json')

