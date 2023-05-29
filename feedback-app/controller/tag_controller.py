import json
from flask import Response, request

from controller import bp
from model.tags import Tags
from repository.tags_repository import TagsRepository


repository = TagsRepository()


@bp.route("/tags", methods=['GET'])
def get_all_tags():
    tags = repository.get_all_tags()
    return json.dumps(tags, default=lambda x: x.__dict__, ensure_ascii=False)


@bp.route("/tags/<id>", methods=['GET'])
def get_one_metric(id: int):
    tag = repository.get_one_tag(id)
    if tag is None:
        return Response(json.dumps({"message": "tag с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return json.dumps(tag, default=lambda x: x.__dict__, ensure_ascii=False)


@bp.route("/tags", methods=['POST'])
def add_tag():
    content = request.get_json()
    title = content.get("title", None)
    typed = content.get("type", None)

    if title is None or type(title) is not str:
        return Response(json.dumps({"message": "title должен быть валидной строкой"}, 
                                   ensure_ascii=False), 
                        status=422, 
                        mimetype='application/json')
    if typed is None or type(typed) is not str:
        return Response(json.dumps({"message": "type должен быть валидной строкой"}, 
                                   ensure_ascii=False), 
                        status=422, 
                        mimetype='application/json')
    
    entity = Tags()
    entity.type = typed
    entity.title = title
    repository.add_tag(entity)


@bp.route("/tags/delete/<id>", methods=['DELETE'])
def delete_tag(id: int):
    metric = repository.delete_tag(id)
    if metric is not None:
        return Response(json.dumps({"message": "metric с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return Response(json.dumps({"message": "metric успешно удален"}, 
                               ensure_ascii=False), 
                    status=200, 
                    mimetype='application/json')


@bp.route("/tags/update/type/<id>", methods=['POST'])
def update_tag_type(id: int):
    content = request.get_json()
    typed = content.get("type", None)
    
    if typed is None or type(typed) is not str:
        return Response(json.dumps({"message": "type должен быть валидной строкой"}, 
                                   ensure_ascii=False), 
                        status=422, 
                        mimetype='application/json')
    
    entity = Tags()
    entity.type = typed
    repository.update_tag_type(id, entity)
    return Response(json.dumps({"message": "tag type успешно изменен"}, 
                               ensure_ascii=False), 
                    status=200,
                    mimetype='application/json')


@bp.route("/tags/update/title/<id>", methods=['POST'])
def update_tag_title(id: int):
    content = request.get_json()
    title = content.get("title", None)

    if title is None or type(title) is not str:
        return Response(json.dumps({"message": "title должен быть валидной строкой"},
                                   ensure_ascii=False), 
                        status=422,
                        mimetype='application/json')
    
    entity = Tags()
    entity.title = title

    repository.update_tag_title(id, entity)
    return Response(json.dumps({"message": "tag title успешно изменен"},
                               ensure_ascii=False), 
                    status=200,
                    mimetype='application/json')
