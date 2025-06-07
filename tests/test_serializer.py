import pytest
from pydantic import BaseModel
from celery import Celery
from celery_pydantic.serializer import (
    PydanticSerializer,
    pydantic_decoder,
    pydantic_dumps,
    pydantic_loads,
    pydantic_celery_app,
)


class SimpleModel(BaseModel):
    name: str
    age: int


class NestedModel(BaseModel):
    user: SimpleModel
    active: bool


def test_pydantic_serializer_simple_model():
    model = SimpleModel(name="John", age=30)
    serializer = PydanticSerializer()
    result = serializer.default(model)
    
    assert isinstance(result, dict)
    assert result["name"] == "John"
    assert result["age"] == 30
    assert "__module_path__" in result
    assert result["__module_path__"] == f"{SimpleModel.__module__}.{SimpleModel.__name__}"


def test_pydantic_serializer_nested_model():
    user = SimpleModel(name="John", age=30)
    model = NestedModel(user=user, active=True)
    serializer = PydanticSerializer()
    result = serializer.default(model)
    
    assert isinstance(result, dict)
    assert result["active"] is True
    assert isinstance(result["user"], dict)
    assert result["user"]["name"] == "John"
    assert result["user"]["age"] == 30
    assert "__module_path__" in result
    assert result["__module_path__"] == f"{NestedModel.__module__}.{NestedModel.__name__}"


def test_pydantic_serializer_non_pydantic():
    serializer = PydanticSerializer()
    result = serializer.default({"key": "value"})
    assert result == {"key": "value"}


def test_pydantic_decoder():
    data = {
        "name": "John",
        "age": 30,
        "__module_path__": f"{SimpleModel.__module__}.{SimpleModel.__name__}"
    }
    result = pydantic_decoder(data)
    
    assert isinstance(result, SimpleModel)
    assert result.name == "John"
    assert result.age == 30


def test_pydantic_decoder_non_pydantic():
    data = {"key": "value"}
    result = pydantic_decoder(data)
    assert result == data


def test_pydantic_dumps_loads_roundtrip():
    model = SimpleModel(name="John", age=30)
    serialized = pydantic_dumps(model)
    deserialized = pydantic_loads(serialized)
    
    assert isinstance(deserialized, SimpleModel)
    assert deserialized.name == model.name
    assert deserialized.age == model.age


def test_pydantic_dumps_loads_nested_roundtrip():
    user = SimpleModel(name="John", age=30)
    model = NestedModel(user=user, active=True)
    serialized = pydantic_dumps(model)
    deserialized = pydantic_loads(serialized)
    
    assert isinstance(deserialized, NestedModel)
    assert isinstance(deserialized.user, SimpleModel)
    assert deserialized.user.name == user.name
    assert deserialized.user.age == user.age
    assert deserialized.active is True


def test_pydantic_celery_app_configuration():
    app = Celery('test_app')
    pydantic_celery_app(app)
    
    assert app.conf.task_serializer == "pydantic"
    assert app.conf.result_serializer == "pydantic"
    assert app.conf.event_serializer == "pydantic"
    assert "application/x-pydantic" in app.conf.accept_content
    assert "application/json" in app.conf.accept_content
    assert "application/x-pydantic" in app.conf.result_accept_content
    assert "application/json" in app.conf.result_accept_content 