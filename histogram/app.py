from prometheus_client import start_http_server, Histogram, Summary
import random
import time

REQUEST_LATENCY_HISTOGRAM = Histogram(
    'request_latency_seconds_histogram',
    'Время обработки запроса в секундах (гистограмма)',
    buckets=[0.1, 0.3, 1.0, 3.0, 10.0]
)

REQUEST_LATENCY_SUMMARY = Summary(
    'request_latency_seconds_summary',
    'Время обработки запроса в секундах (сводка)'
)

def process_request():
    latency = random.expovariate(1/0.5)
    time.sleep(latency)
    REQUEST_LATENCY_HISTOGRAM.observe(latency)
    REQUEST_LATENCY_SUMMARY.observe(latency)

if __name__ == "__main__":
    start_http_server(8000) 
    while True:
        process_request()
