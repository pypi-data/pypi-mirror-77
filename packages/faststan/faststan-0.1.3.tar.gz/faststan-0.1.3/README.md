# FastSTAN

Easily deploy NATS Streaming subscribers using Python.

## Features

- Define subscribers using sync and async python functions
- Automatic data parsing and validation using type annotations and pydantic
- Support custom validation using any function
- Allow several subscribers on same channel
- Support all subscription configuration available in stan.py
- Healthcheck available using HTTP GET request to monitor the applications
- (TODO) Metrics available using HTTP GET requests to monitor subsriptions status
- All of FastAPI features

## Quick start

- Install the package from pypi:

```bash
pip install faststan
```

- Create your first subscriber. Create a file named `app.py` and write the following lines:

```python
from faststan.faststan import FastSTAN

app = FastSTAN()

@app.subscribe("demo")
def on_event(message: str):
    print(f"INFO :: Received new message: {message}")
```

- Start your subscriber:

```shell
uvicorn app:app
```

- Or if you are in a jupyter notebook environment, start the subscriptions:

```python
await app.start()
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
