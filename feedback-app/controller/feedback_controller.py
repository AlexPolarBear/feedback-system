import json
# import logging
from flask import Response, request
from datetime import datetime

from controller import bp
from model.feedback import Feedback
from repository.feedback_repository import FeedbackRepository


repository = FeedbackRepository()


@bp.route("/feedback", methods=['POST'])
def add_feedback():
    content = request.get_json()
    course_id = content.get("course_id", None)
    author_id = content.get("author_id", None)
    text = content.get("text", None)

    if course_id is None or type(course_id) is not int:
        return Response(json.dumps({"message": "course_id должен быть числом"}), 
                        status=422, 
                        mimetype='application/json')
    if author_id is None or type(author_id) is not int:
        return Response(json.dumps({"message": "course_id должен быть числом"}), 
                        status=422, 
                        mimetype='application/json')
    if text is None or type(text) is not str:
        return Response(json.dumps({"message": "text должен быть валидной строкой"}), 
                        status=422,
                        mimetype='application/json')
    
    entity = Feedback()
    entity.date = datetime.now()
    entity.text = text
    entity.author_id = author_id
    entity.course_id = course_id

    repository.add_feedback(entity)
    return Response(json.dumps({"message": "отзыв успешно сохранен"}), 
                    status=200, 
                    mimetype='application/json')


@bp.route("/feedback", methods=['GET'])
def get_all_feedbacks():
    feedbacks = repository.get_all_feedbacks()
    return json.dump(feedbacks, default=lambda x: x.__dict__)


@bp.route("/feedback/<id>", methods=['GET'])
def get_one_feedback(id: int):
    feedback = repository.get_one_feedback(id)
    if feedback is None:
        return Response(json.dumps({"message": "отзыв с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return feedback.__dict__


@bp.route("/feedback/delete/<id>", methods=['DELETE'])
def delete_feedback(id: int):
    feedback = repository.delete_feedback(id)
    if feedback is None:
        return Response(json.dumps({"message": "отзыв с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return Response(json.dumps({"message": "отзыв успешно удален"}, 
                                ensure_ascii=False),
                    status=200,
                    mimetype='application/json')

@bp.route("/feedback/update/<id>", methods=['POST'])
def update_feedback(id: int):
    content = request.get_json()
    text = content.get("text", None)

    if text is None or type(text) is not str:
        return Response(json.dumps({"message": "text должен быть валидной строкой"}), 
                        status=422,
                        mimetype='application/json')

    entity = Feedback()
    entity.date = datetime.now()
    entity.text = text

    repository.update_feedback(id, entity)
    return Response(json.dumps({"message": "отзыв успешно изменен"}), 
                    status=200,
                    mimetype='application/json')

