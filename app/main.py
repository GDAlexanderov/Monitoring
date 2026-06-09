from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.responses import HTMLResponse
from prometheus_client import generate_latest

from app.state import state
from app.metrics import users_total, orders_total

from app.simulator import (
    start_cpu_attack,
    start_memory_leak,
    stop_memory_leak,
    generate_queue,
    process_queue,
    enable_errors,
    disable_errors,
    register_error
)

app = FastAPI(title="Monitoring Lab")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )


@app.get("/stats")
def stats():
    return {
        "users": state.users,
        "orders": state.orders,
        "errors": state.errors,
        "queue_size": state.queue_size,
        "memory_chunks": len(state.memory_storage)
    }


@app.post("/users/create")
def create_users(count: int = 1):
    state.users += count
    users_total.set(state.users)

    return {"users": state.users}


@app.post("/orders/create")
def create_order():
    state.orders += 1
    orders_total.inc()

    return {"orders": state.orders}


@app.post("/queue/add")
def add_queue(count: int = 10):
    generate_queue(count)
    return {"queue_size": state.queue_size}


@app.post("/queue/process")
def queue_process():
    process_queue()
    return {"queue_size": state.queue_size}


@app.post("/chaos/cpu")
def cpu():
    start_cpu_attack()
    return {"message": "cpu attack started"}


@app.post("/chaos/memory/start")
def memory_start():
    start_memory_leak()
    return {"message": "memory leak started"}


@app.post("/chaos/memory/stop")
def memory_stop():
    stop_memory_leak()
    return {"message": "memory leak stopped"}


@app.post("/chaos/errors/on")
def errors_on():
    enable_errors()
    return {"message": "error mode enabled"}


@app.post("/chaos/errors/off")
def errors_off():
    disable_errors()
    return {"message": "error mode disabled"}


@app.get("/test")
def test():
    if state.error_mode:
        register_error()
        raise HTTPException(status_code=500, detail="simulated error")

    return {"status": "success"}

@app.get("/control", response_class=HTMLResponse)
def control_panel():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monitoring Lab Control Panel</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
            }

            button {
                width: 250px;
                padding: 12px;
                margin: 5px;
                font-size: 16px;
                cursor: pointer;
            }

            .section {
                margin-bottom: 30px;
            }
        </style>
    </head>

    <body>

        <h1>Monitoring Lab Control Panel</h1>

        <div class="section">
            <h2>Users</h2>

            <button onclick="fetch('/users/create?count=10', {method:'POST'})">
                +10 Users
            </button>

            <button onclick="fetch('/users/create?count=100', {method:'POST'})">
                +100 Users
            </button>
        </div>

        <div class="section">
            <h2>Orders</h2>

            <button onclick="fetch('/orders/create', {method:'POST'})">
                Create Order
            </button>
        </div>

        <div class="section">
            <h2>Queue</h2>

            <button onclick="fetch('/queue/add?count=50', {method:'POST'})">
                Add 50 Queue
            </button>

            <button onclick="fetch('/queue/add?count=500', {method:'POST'})">
                Add 500 Queue
            </button>

            <button onclick="fetch('/queue/process', {method:'POST'})">
                Process Queue
            </button>
        </div>

        <div class="section">
            <h2>Chaos</h2>

            <button onclick="fetch('/chaos/cpu', {method:'POST'})">
                CPU Attack
            </button>

            <button onclick="fetch('/chaos/memory/start', {method:'POST'})">
                Start Memory Leak
            </button>

            <button onclick="fetch('/chaos/memory/stop', {method:'POST'})">
                Stop Memory Leak
            </button>

            <button onclick="fetch('/chaos/errors/on', {method:'POST'})">
                Enable Errors
            </button>

            <button onclick="fetch('/chaos/errors/off', {method:'POST'})">
                Disable Errors
            </button>
        </div>

        <div class="section">
            <h2>Test Error</h2>

            <button onclick="fetch('/test')">
                Call /test
            </button>
        </div>

    </body>
    </html>
    """