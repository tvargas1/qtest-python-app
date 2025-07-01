import pytest
from src.models.task import Task

def test_task_creation():
    task = Task(title="Test Task", description="Test Description", priority="high")
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "high"
    assert not task.completed
    assert task.id is None  # Ensure task_id is None when not provided

def test_task_to_dict():
    task = Task(title="Test Task", description="Test Description", priority="high", task_id=1)
    task_dict = task.to_dict()
    assert isinstance(task_dict, dict)
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "Test Description"
    assert task_dict["priority"] == "high"
    assert not task_dict["completed"]

def test_task_from_dict():
    task_dict = {
        "id": 1,
        "title": "Test Task",
        "description": "Test Description",
        "priority": "high",
        "completed": False
    }
    task = Task.from_dict(task_dict)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "high"
    assert not task.completed