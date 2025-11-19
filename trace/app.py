from flask import Flask, jsonify
import sqlite3
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Инициализация трейсера
resource = Resource(attributes={"service.name": "python-flask-demo"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer_provider().get_tracer(__name__)

# Экспортер Jaeger
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
SQLite3Instrumentor().instrument()

def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
    c.execute('INSERT OR IGNORE INTO users (id, name) VALUES (1, "Alice")')
    c.execute('INSERT OR IGNORE INTO users (id, name) VALUES (2, "Bob")')
    conn.commit()
    conn.close()

@app.route('/')
def hello():
    return "Hello from OpenTelemetry + Jaeger tracing!"

@app.route('/users')
def get_users():
    with tracer.start_as_current_span("db-query"):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        rows = c.fetchall()
        conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)
