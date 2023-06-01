import json
from flask import Response, request

from controller import bp
from model.tags import Tags
from repository.tags_repository import TagsRepository


repository = TagsRepository()


@bp.route("/tags", methods=['GET'])
def get_all_tags() -> Response:
    tags = repository.get_all_tags()
    if tags is None:
        msg = json.dump({"message": "невозможно получить список тегов"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    json_list = json.dumps(tags, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/tags/<id>", methods=['GET'])
def get_one_metric(id: int) -> Response:
    tag = repository.get_one_tag(id)
    if tag is None:
        msg = json.dump({"message": "тег с данным id отсутсвует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    json_list = json.dumps(tag, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/tags", methods=['POST'])
def add_tag() -> Response:
    content = request.get_json()
    title = content.get("title", None)
    typed = content.get("type", None)
    if title is None or type(title) is not str:
        msg = json.dump({"message": "title должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    if typed is None or type(typed) is not str:
        msg = json.dump({"message": "type должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    
    entity = Tags()
    entity.type = typed
    entity.title = title
    tag = repository.add_tag(entity)
    if tag is None:
        msg = json.dump({"message": "тег с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "тег успешно добавлен"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')


@bp.route("/tags/delete/<id>", methods=['DELETE'])
def delete_tag(id: int) -> Response:
    tag = repository.delete_tag(id)
    if tag is None:
        msg = json.dump({"message": "тег с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "тег успешно удален"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')


@bp.route("/tags/update/type/<id>", methods=['POST'])
def update_tag_type(id: int) -> Response:
    content = request.get_json()
    typed = content.get("type", None)
    if typed is None or type(typed) is not str:
        msg = json.dump({"message": "type должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    
    entity = Tags()
    entity.type = typed
    tag = repository.update_tag_type(id, entity)
    if tag is None:
        msg = json.dump({"message": "тег с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "тег type успешно изменен"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')


@bp.route("/tags/update/title/<id>", methods=['POST'])
def update_tag_title(id: int) -> Response:
    content = request.get_json()
    title = content.get("title", None)
    if title is None or type(title) is not str:
        msg = json.dump({"message": "title должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    
    entity = Tags()
    entity.title = title
    tag = repository.update_tag_title(id, entity)
    if tag is None:
        msg = json.dump({"message": "тег с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "тег title успешно изменен"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')
