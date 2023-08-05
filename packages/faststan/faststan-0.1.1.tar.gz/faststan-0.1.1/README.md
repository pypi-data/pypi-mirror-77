# FastSTAN

Easily deploy NATS Streaming subscribers using Python.

## Features

- [x] Define subscribers using sync and async python functions
- [x] Automatic data parsing and validation using type annotations and pydantic
- [x] Support custom validation using any function
- [x] Allow several subscribers on same channel

- [x] Healthcheck available using HTTP GET request to monitor the applications
- [ ] (TODO) Metrics available using HTTP GET requests
- [x] All of FastAPI features

## Quick start

- Install the package from pypi:

```bash
pip install faststan
```

- Create your first subscriber:

```python
from faststan.faststan import FastSTAN

app = FastSTAN()

@app.subscribe("demo")
def on_event(message: str):
    print(f"INFO :: Received new message: {message}")
```

- Start your subscriber:

```bash
uvicorn app:app
```

## Advanced features

### Using error callbacks

```python
from faststan.faststan import FastSTAN


app = FastSTAN()


def handle_error(error):
    print("ERROR: {error}")


@app.subscribe("demo", error_cb=handle_error)
def on_event(message: str):
    print(f"INFO :: Received new message: {message}")
```

### Using pydantic models

You can use pydantic models in order to automatically parse incoming messages:

```python
from pydantic import BaseModel
from faststan.faststan import FastSTAN


class Event(BaseModel):
    timestamp: int
    temperature: float
    humidity: float


app = FastSTAN()


@app.subscribe("event")
def on_event(event):
    msg = f"INFO :: {event.timestamp} :: Temperature: {event.temperature} | Humidity: {event.humidity}"
    print(msg)
```
