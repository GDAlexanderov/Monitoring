import threading
import time

from app.state import state
from app.metrics import queue_size_metric, errors_total


def cpu_burn_worker():
    end_time = time.time() + 60

    while time.time() < end_time:
        x = 0
        for i in range(500000):
            x += i * i

    state.cpu_attack = False


def start_cpu_attack():
    if state.cpu_attack:
        return

    state.cpu_attack = True

    thread = threading.Thread(target=cpu_burn_worker, daemon=True)
    thread.start()


def memory_leak_worker():
    while state.memory_attack:
        state.memory_storage.append("X" * 1024 * 1024)
        time.sleep(1)


def start_memory_leak():
    if state.memory_attack:
        return

    state.memory_attack = True

    thread = threading.Thread(target=memory_leak_worker, daemon=True)
    thread.start()


def stop_memory_leak():
    state.memory_attack = False


def generate_queue(size: int):
    state.queue_size += size
    queue_size_metric.set(state.queue_size)


def process_queue():
    if state.queue_size > 0:
        state.queue_size -= 1

    queue_size_metric.set(state.queue_size)


def enable_errors():
    state.error_mode = True


def disable_errors():
    state.error_mode = False


def register_error():
    state.errors += 1
    errors_total.inc()