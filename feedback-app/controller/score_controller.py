import json
from flask import Response, request
from datetime import datetime

from controller import bp
from model.scores import Scores
from repository.score_repository import ScoreRepository


repository = ScoreRepository()


@bp.route("/scores", methods=['GET'])
def get_all_scores():
    scores = repository.get_all_scores()
    return json.dump(scores, default=lambda x: x.__dict__, ensure_ascii=False)


@bp.route("/scores/<id>", methods=['GET'])
def get_one_score(id: int):
    score = repository.get_one_score(id)
    if score is None:
        return Response(json.dumps({"message": "score с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return json.dump(score, default=lambda x: x.__dict__, ensure_ascii=False)



@bp.route("/scores", methods=['POST'])
def add_or_upd_score():
    content = request.get_json()
    metric_id = content.get("metric_id", None)
    course_id = content.get("course_id", None)
    author_id = content.get("author_id", None)
    score = content.get("score", None)

    def response (field: int):
        if field is None or type(field) is not int:
            return Response(json.dumps({"message": "'{field}' должен быть числом"}, 
                                       ensure_ascii=False), 
                            status=422, 
                            mimetype='application/json')
    response(metric_id)
    response(course_id)
    response(author_id)
    response(score)

    entity = Scores()
    entity.metric_id = metric_id
    entity.course_id = course_id
    entity.author_id = author_id
    entity.date = datetime.now()
    entity.score = score

    repository.add_or_update_score(entity)
    return Response(json.dumps({"message": "score успешно сохранен"}), 
                    status=200, 
                    mimetype='application/json')


@bp.route("/scores/delete/<id>", methods=['DELETE'])
def delete_score(id: int):
    score = repository.delete_score(id)
    if score is None:
        return Response(json.dumps({"message": "score с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return Response(json.dumps({"message": "score успешно удален"}, 
                                ensure_ascii=False),
                    status=200,
                    mimetype='application/json')

# @bp.route("/scores/update/<id>", methods=['POST'])
# def update_score(id: int):
#     content = request.get_json()
#     score = content.get("score", None)

#     if score is None or type(score) is not int:
#         return Response(json.dumps({"message": "score должен быть числом"}), 
#                         status=422,
#                         mimetype='application/json')

#     entity = Scores()
#     entity.date = datetime.now()
#     entity.score = score

#     repository.update_score(id, entity)
#     return Response(json.dumps({"message": "score успешно изменен"}), 
#                     status=200,
#                     mimetype='application/json')
