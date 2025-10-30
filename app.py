from prometheus_client import start_http_server, Counter, Gauge, Histogram
import random, time, os

# Define possible values for dynamic labels
ENVS = ['dev', 'staging', 'production']
REGIONS = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-south-1']
VERSIONS = ['v1.0.0', 'v1.1.0', 'v1.2.0', 'v2.0.0']
STATUSES = ['success', 'error', 'timeout']

# Read from environment variables or use None to indicate random selection
ENV_FIXED = os.getenv('ENV')
REGION_FIXED = os.getenv('REGION')
VERSION_FIXED = os.getenv('VERSION')
STATUS_FIXED = os.getenv('STATUS')

REQS = Counter('demo_requests_total', 'Total demo requests', ['env', 'region', 'version', 'status'])
TEMP = Gauge('demo_temperature_celsius', 'Demo temperature', ['env', 'region', 'version'])
LAT  = Histogram('demo_request_latency_seconds', 'Request latency (seconds)', ['env', 'region', 'version', 'status'], buckets=(.05, .1, .25, .5, 1, 2, 5))

PORT = 8000
start_http_server(PORT)

while True:
    # Randomly select label values for each iteration (only if not fixed via env vars)
    env = ENV_FIXED if ENV_FIXED else random.choice(ENVS)
    region = REGION_FIXED if REGION_FIXED else random.choice(REGIONS)
    version = VERSION_FIXED if VERSION_FIXED else random.choice(VERSIONS)
    status = STATUS_FIXED if STATUS_FIXED else random.choice(STATUSES)

    with LAT.labels(env=env, region=region, version=version, status=status).time():
        time.sleep(random.uniform(0.05, 0.4))
    REQS.labels(env=env, region=region, version=version, status=status).inc()
    TEMP.labels(env=env, region=region, version=version).set(20 + random.uniform(-2, 2))
