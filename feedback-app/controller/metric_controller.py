import json
from flask import Response, request

from controller import bp
from model.metric import Metric
from repository.metric_repository import MetricRepository


repository = MetricRepository()


@bp.route("/metrics", methods=['GET'])
def get_all_metrics() -> Response:
    metrics = repository.get_all_metric()
    if metrics is None:
        msg = json.dumps({"message": "невозможно получить список метрик"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    json_list = json.dumps(metrics, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/metrics/<id>", methods=['GET'])
def get_one_metric(id: int) -> Response:
    metric = repository.get_one_metric(id)
    if metric is None:
        msg = json.dumps({"message": "метрика с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    json_list = json.dumps(metric, default=lambda x: x.__dict__, ensure_ascii=False)
    return Response(json_list, status=200, mimetype='application/json')


@bp.route("/metrics", methods=['POST'])
def add_metric() -> Response:
    content = request.get_json()
    name = content.get("name", None)
    if name is None or type(name) is not str:
        msg = json.dumps({"message": "name должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    
    entity = Metric()
    entity.name = name
    metric = repository.add_metric(entity)
    if metric is None:
        msg = json.dumps({"message": "не удалось добавить метрику"}, ensure_ascii=False)
        return Response(msg, status=400, mimetype='application/json')
    msg = json.dumps({"message": "метрика успешно добавлена"}, ensure_ascii=False)
    return Response(msg, status=201, mimetype='application/json')


@bp.route("/metrics/delete/<id>", methods=['DELETE'])
def delete_metric(id: int) -> Response:
    metric = repository.delete_metric(id)
    if metric is None:
        msg = json.dumps({"message": "метрика с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "метрика успешно удалена"}, ensure_ascii=False)
    return Response(msg, status=202, mimetype='application/json')


@bp.route("/metrics/update/<id>", methods=['POST'])
def update_metric(id: int) -> Response:
    content = request.get_json()
    name = content.get("name", None)
    if name is None or type(name) is not str:
        msg = json.dumps({"message": "name должен быть валидной строкой"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    
    entity = Metric()
    entity.name = name
    metric = repository.update_metric(id, entity)
    if metric is None:
        msg = json.dumps({"message": "метрика с данным id отсутствует"}, ensure_ascii=False)
        return Response(msg, status=422, mimetype='application/json')
    msg = json.dumps({"message": "метрика успешно изменена"}, ensure_ascii=False)
    return Response(msg, status=201, mimetype='application/json')
