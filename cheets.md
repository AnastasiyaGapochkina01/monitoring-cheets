```
monitoring.coreos.com/v1

kubectl -n kube-prometheus-stack port-forward svc/prometheus-operated 9090:9090 --address 0.0.0.0

```

```yaml
node-exporter:
    image: prom/node-exporter
    container_name: "monitoring-server-exporter"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'
    restart: always
    ports:
      - 9200:9100
        
  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    container_name: cadvisor
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /cgroup:/cgroup:ro
    restart: unless-stopped
    ports:
      - 8080:8080

```

```yaml
relabel_configs:
  - source_labels: [__address__]
    target_label: __param_target
  - source_labels: [__param_target]
    target_label: instance
  - target_label: __address__
    replacement: 10.129.0.32:9115
```
