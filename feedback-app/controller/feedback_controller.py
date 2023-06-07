import json
from flask import Response, request
from datetime import datetime

from controller import bp
from model.feedback import Feedback
from repository.feedback_repository import FeedbackRepository


repository = FeedbackRepository()


@bp.route("/feedback", methods=['POST'])
def add_feedback() -> Response:
    content = request.get_json()
    course_id = content.get("course_id", None)
    author_id = content.get("author_id", None)
    text = content.get("text", None)

    if course_id is None or type(course_id) is not int:
        msg = json.dumps({"message": "course_id должен быть числом"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    if author_id is None or type(author_id) is not int:
        msg = json.dumps({"message": "author_id должен быть числом"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    if text is None or type(text) is not str:
        msg = json.dumps({"message": "text должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    
    entity = Feedback()
    entity.date = datetime.now()
    entity.text = text
    entity.author_id = author_id
    entity.course_id = course_id

    feedback = repository.add_feedback(entity)
    if feedback is None:
        msg = json.dumps({"message": "не удалось добавить отзыв"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    msg = json.dumps({"message": "отзыв успешно добавлен"}, ensure_ascii=False)
    return Response(msg, status=201, mimetype='application/json')


@bp.route("/feedback", methods=['GET'])
def get_all_feedbacks() -> Response:
    feedbacks = repository.get_all_feedbacks()
    if feedbacks is None:
        msg = json.dumps({"message": "невозможно получить список отзывов"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    json_list = json.dumps(feedbacks, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/feedback/<id>", methods=['GET'])
def get_one_feedback(id: int) -> Response:
    feedback = repository.get_one_feedback(id)
    if feedback is None:
        msg = json.dumps({"message": "отзыв с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    json_list = json.dumps(feedback, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/feedback/delete/<id>", methods=['DELETE'])
def delete_feedback(id: int) -> Response:
    feedback = repository.delete_feedback(id)
    if feedback is None:
        msg = json.dumps({"message": "отзыв с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "отзыв успешно удален"}, ensure_ascii=False)
    return Response(msg, status=202, mimetype='application/json')


@bp.route("/feedback/update/<id>", methods=['POST'])
def update_feedback(id: int) -> Response:
    content = request.get_json()
    text = content.get("text", None)
    if text is None or type(text) is not str:
        msg = json.dumps({"message": "text должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')

    entity = Feedback()
    entity.date = datetime.now()
    entity.text = text
    feedback = repository.update_feedback(id, entity)
    if feedback is None:
        msg = json.dumps({"message": "отзыв с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "отзыв успешно изменен"}, ensure_ascii=False)
    return Response(msg, status=201, mimetype='application/json')
