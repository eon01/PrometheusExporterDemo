# Demo Prometheus Exporter

This is a minimal Python application that exposes custom Prometheus metrics on port `8000`.
It can be used to test Prometheus scraping, relabeling, and visualization locally or in Docker.

---

## Features

* Exports three metrics:

  * `demo_requests_total`: Counter of simulated requests.
  * `demo_temperature_celsius`: Gauge with a random temperature value.
  * `demo_request_latency_seconds`: Histogram tracking simulated request latencies.
* Runs a built-in HTTP server on `/metrics`.
* Lightweight and dependency-free aside from `prometheus-client`.

---

## Run Locally (Python)

```bash
pip install prometheus-client
python app.py
```

Access metrics at: [http://localhost:8000/metrics](http://localhost:8000/metrics)

---

## Run in Docker

### Build

```bash
docker build -t demo-prom-app:latest .
```

### Run

```bash
docker run -d -p 8000:8000 demo-prom-app:latest
```

View metrics:

```bash
curl -s localhost:8000/metrics | head
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

---

## Notes

* The app runs continuously and updates metrics every few hundred milliseconds.
* You can modify the metric definitions in `app.py` to experiment with other types or label dimensions.
* Intended for learning, testing, and local development.

