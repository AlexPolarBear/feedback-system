from dataclasses import dataclass

@dataclass(init=False)
class Metric:
    id: int
    name: str


@dataclass
class Metric_get:
    id: int
    name: str
