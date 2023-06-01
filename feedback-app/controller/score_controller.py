import json
from flask import Response, request
from datetime import datetime

from controller import bp
from model.scores import Scores
from repository.score_repository import ScoreRepository


repository = ScoreRepository()


@bp.route("/scores", methods=['GET'])
def get_all_scores() -> Response:
    scores = repository.get_all_scores()
    if scores is None:
        msg = json.dump({"message": "невозможно получить список счетчиков"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    json_list = json.dumps(scores, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/scores/<id>", methods=['GET'])
def get_one_score(id: int) -> Response:
    score = repository.get_one_score(id)
    if score is None:
        msg = json.dump({"message": "счетчик с данным id отсутсвует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    json_list = json.dumps(score, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/scores", methods=['POST'])
def add_or_upd_score() -> Response:
    content = request.get_json()
    metric_id = content.get("metric_id", None)
    course_id = content.get("course_id", None)
    author_id = content.get("author_id", None)
    score = content.get("score", None)
    def response (field: int):
        if field is None or type(field) is not int:
            msg = json.dump({"message": "{field} должен быть числом"}, ensure_ascii=False)
            return Response(msg, status=422, mimetype='application/json')
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
    score = repository.add_or_update_score(entity)
    if score is None:
        msg = json.dump({"message": "счетчик с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "счетчик успешно добавлен/изменен"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')


@bp.route("/scores/delete/<id>", methods=['DELETE'])
def delete_score(id: int) -> Response:
    score = repository.delete_score(id)
    if score is None:
        msg = json.dump({"message": "счетчик с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "счетчик успешно удален"}, ensure_ascii=False)
    return Response(msg, status=200, mimetype='application/json')

# @bp.route("/scores/update/<id>", methods=['POST'])
# def update_score(id: int) -> Response:
#     content = request.get_json()
#     score = content.get("score", None)
#     if score is None or type(score) is not int:
#         msg = json.dump({"message": "score должен быть числом"}, ensure_ascii=False)
#         return Response(msg, status=422, mimetype='application/json')

#     entity = Scores()
#     entity.date = datetime.now()
#     entity.score = score
#     score = repository.update_score(id, entity)
#     if score is None:
#         msg = json.dump({"message": "счетчик с данным id отсутствует"}, ensure_ascii=False)
#         return Response(msg, status=422, mimetype='application/json')
#     msg = json.dumps({"message": "счетчик успешно изменен"}, ensure_ascii=False)
#     return Response(msg, status=200, mimetype='application/json')