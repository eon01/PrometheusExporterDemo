# Demo Prometheus Exporter

This is a minimal Python application that exposes custom Prometheus metrics with dynamic labels on port `8000`.
It can be used to test Prometheus scraping, relabeling, querying, and visualization locally or in Docker.

---

## Features

* Exports three metrics with multi-dimensional labels:

  * `demo_requests_total`: Counter of simulated requests.
  * `demo_temperature_celsius`: Gauge with a random temperature value.
  * `demo_request_latency_seconds`: Histogram tracking simulated request latencies.

* **Dynamic Labels**: Each metric includes labels for `env`, `region`, `version`, and `status` (where applicable):
  * `env`: Environment (dev, staging, production)
  * `region`: Geographic region (us-east-1, us-west-2, eu-west-1, ap-south-1)
  * `version`: Application version (v1.0.0, v1.1.0, v1.2.0, v2.0.0)
  * `status`: Request status (success, error, timeout)

* **Configurable via Environment Variables**: Labels can be fixed or randomized

* Runs a built-in HTTP server on `/metrics`.

* Lightweight and dependency-free aside from `prometheus-client`.

---

## Run Locally (Python)

```bash
pip install prometheus-client
python app.py
```

Access metrics at: [http://localhost:8000/metrics](http://localhost:8000/metrics)

### Configure Labels via Environment Variables

By default, all labels are randomly selected on each iteration. You can fix specific labels using environment variables:

```bash
# Fix all labels
export ENV=production
export REGION=us-east-1
export VERSION=v2.0.0
export STATUS=success
python app.py
```

```bash
# Mix fixed and random - only ENV is fixed, others are random
export ENV=production
python app.py
```

```bash
# All random (default behavior)
python app.py
```

---

## Run in Docker

### Build

```bash
docker build -t demo-prom-app:latest .
```

### Run

```bash
# Run with random labels (default)
docker run -d -p 8000:8000 demo-prom-app:latest

# Run with fixed labels
docker run -d -p 8000:8000 \
  -e ENV=production \
  -e REGION=us-east-1 \
  -e VERSION=v2.0.0 \
  -e STATUS=success \
  demo-prom-app:latest
```

View metrics:

```bash
curl -s localhost:8000/metrics | grep demo_
```

---

## Prometheus Configuration

Add this job to your `prometheus.yml` to start scraping the app:

```yaml
scrape_configs:
  - job_name: 'demo-app'
    static_configs:
      - targets: ['localhost:8000']
```

If Prometheus is running in another container, replace `localhost` with the Docker network name or host.

### Example PromQL Queries

With the multi-dimensional labels, you can run powerful queries:

```promql
# Total requests across all labels
sum(demo_requests_total)

# Error rate by environment
sum(rate(demo_requests_total{status="error"}[5m])) by (env)

# Request rate per region
sum(rate(demo_requests_total[5m])) by (region)

# Compare versions
sum(rate(demo_requests_total[5m])) by (version)

# P95 latency by environment and region
histogram_quantile(0.95, sum(rate(demo_request_latency_seconds_bucket[5m])) by (env, region, le))

# Success rate percentage
100 * sum(rate(demo_requests_total{status="success"}[5m])) / sum(rate(demo_requests_total[5m]))
```

---

## Label Configuration

| Label | Environment Variable | Possible Values (when random) | Used In Metrics |
|-------|---------------------|-------------------------------|-----------------|
| `env` | `ENV` | dev, staging, production | All metrics |
| `region` | `REGION` | us-east-1, us-west-2, eu-west-1, ap-south-1 | All metrics |
| `version` | `VERSION` | v1.0.0, v1.1.0, v1.2.0, v2.0.0 | All metrics |
| `status` | `STATUS` | success, error, timeout | Counter and Histogram only |

---

## Notes

* The app runs continuously and updates metrics every few hundred milliseconds.
* Labels are randomly selected on each iteration unless fixed via environment variables.
* This creates rich, multi-dimensional metrics perfect for testing Prometheus aggregations, dashboards, and alert rules.
* You can modify the metric definitions and label values in `app.py` to experiment with other dimensions.
* Intended for learning, testing, and local development.

