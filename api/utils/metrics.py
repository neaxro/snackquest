import time
from functools import wraps

from flask import request
from prometheus_client import Counter, Summary
from api.utils.config import Config


class Metrics:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Metrics, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        config = Config()

        self.service_name = config.METRICS_APP_NAME

        self.REQUEST_COUNT = Counter(
            f"{config.METRICS_PREFIX}_request_count",
            "Number of requests",
            ["method", "endpoint", "service"],
        )
        self.REQUEST_TIME = Summary(
            f"{config.METRICS_PREFIX}_request_time",
            "Time spent processing request",
            ["method", "endpoint", "service"],
        )
        self.REQUEST_LATENCY = Summary(
            f"{config.METRICS_PREFIX}_request_latency",
            "Request latency",
            ["method", "endpoint", "service"],
        )


metrics = Metrics()


def count_requests(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        metrics.REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint,
            service=metrics.service_name,
        ).inc()  # Increment request count
        return func(*args, **kwargs)

    return wrapper


def time_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with metrics.REQUEST_TIME.labels(
            method=request.method,
            endpoint=request.endpoint,
            service=metrics.service_name,
        ).time():  # Measure time taken by request
            return func(*args, **kwargs)

    return wrapper


def latency_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        latency = time.time() - start_time
        metrics.REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.endpoint,
            service=metrics.service_name,
        ).observe(
            latency
        )  # Record latency
        return response

    return wrapper
