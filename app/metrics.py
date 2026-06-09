from prometheus_client import Counter, Gauge, Histogram

users_total = Gauge(
    "users_total",
    "Total users"
)

orders_total = Counter(
    "orders_total",
    "Orders created"
)

errors_total = Counter(
    "errors_total",
    "Errors count"
)

queue_size_metric = Gauge(
    "queue_size",
    "Queue size"
)

request_duration = Histogram(
    "request_duration_seconds",
    "Request duration"
)