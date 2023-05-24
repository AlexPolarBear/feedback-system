import json
from flask import Response, request

from controller import bp
from model.metric import Metric
from repository.metric_repository import MetricRepository


repository = MetricRepository()


@bp.route("/metrics", methods=['GET'])
def get_all_metrics():
    metrics = repository.get_all_metric()
    return json.dumps(metrics, default=lambda x: x.__dict__)


@bp.route("/metrics/<id>", methods=['GET'])
def get_one_metric(id: int):
    metric = repository.get_one_metric(id)
    if metric is None:
        return Response(json.dumps({"message": "metric с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return metric.__dict__


@bp.route("/metrics", methods=['PUT'])
def add_metric():
    content = request.get_json()
    name = content.get("name", None)

    if name is None or type(name) is not str:
        return Response(json.dumps({"message": "name должен быть валидной строкой"}, 
                                   ensure_ascii=False), 
                        status=422, 
                        mimetype='application/json')
    
    entity = Metric()
    entity.name = name
    repository.add_metric(entity)


@bp.route("/metrics/delete/<id>", methods=['DELETE'])
def delete_metric(id: int):
    metric = repository.delete_metric(id)
    if metric is None:
        return Response(json.dumps({"message": "metric с данным id отсутсвует"}, 
                                   ensure_ascii=False),
                        status=422,
                        mimetype='application/json')
    return Response(json.dumps({"message": "metric успешно удален"}, 
                               ensure_ascii=False), 
                    status=200, 
                    mimetype='application/json')


@bp.route("/metrics/update/<id>", methods=['POST'])
def update_metric(id: int):
    content = request.get_json()
    name = content.get("name", None)

    if name is None or type(name) is not str:
        return Response(json.dumps({"message": "name должен быть валидной строкой"}), 
                        status=422,
                        mimetype='application/json')
    
    entity = Metric()
    entity.name = name

    repository.update_metric(id, entity)
    return Response(json.dumps({"message": "metric успешно изменен"}), 
                    status=200,
                    mimetype='application/json')
