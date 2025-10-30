from prometheus_client import start_http_server, Counter, Gauge, Histogram
import random, time

REQS = Counter('demo_requests_total', 'Total demo requests')
TEMP = Gauge('demo_temperature_celsius', 'Demo temperature')
LAT  = Histogram('demo_request_latency_seconds', 'Request latency (seconds)', buckets=(.05, .1, .25, .5, 1, 2, 5))

PORT = 8000
start_http_server(PORT)

while True:
    with LAT.time():
        time.sleep(random.uniform(0.05, 0.4))
    REQS.inc()
    TEMP.set(20 + random.uniform(-2, 2))
















