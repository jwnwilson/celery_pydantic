# Celery Pydantic

A library that provides seamless integration between Celery and Pydantic models, allowing you to serialize and deserialize Pydantic models in Celery tasks.

## Installation

```bash
pip install celery-pydantic
```

## Usage

```python
from celery import Celery
from pydantic import BaseModel
from celery_pydantic import pydantic_celery

# Define your Pydantic model
class User(BaseModel):
    name: str
    age: int

# Create your Celery app
app = Celery('myapp')

# Configure the app to use Pydantic serialization
pydantic_celery(app)

# Use Pydantic models in your tasks
@app.task
def process_user(user: User):
    return user.name

# Call the task with a Pydantic model
user = User(name="John", age=30)
result = process_user.delay(user)
```

## Features

- Automatic serialization and deserialization of Pydantic models in Celery tasks
- Support for nested Pydantic models
- Maintains type safety throughout the task execution
- Compatible with Celery's result backend

## Testing

To run the tests locally:

1. `uv sync --all-extras`
2. `uv run pytest`

## Requirements

- Python 3.9+
- Celery 5.0+
- Pydantic 2.0+

## License

MIT License 