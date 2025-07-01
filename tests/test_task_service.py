import pytest
import os
import json
from src.services.task_service import TaskService
from src.models.task import Task

@pytest.fixture
def task_service():
    # Use a temporary file for testing
    test_file = "test_tasks.json"
    service = TaskService(test_file)
    yield service
    # Cleanup after tests
    if os.path.exists(test_file):
        os.remove(test_file)

def test_add_task(task_service):
    task = task_service.add_task("Test Task", "Test Description", "high")
    assert isinstance(task, Task)
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "high"

def test_get_all_tasks(task_service):
    task_service.add_task("Task 1")
    task_service.add_task("Task 2")
    tasks = task_service.get_all_tasks()
    assert len(tasks) == 2
    assert all(isinstance(task, Task) for task in tasks)

def test_get_task_by_id(task_service):
    task = task_service.add_task("Test Task")
    found_task = task_service.get_task_by_id(task.id)
    assert found_task.id == task.id
    assert found_task.title == task.title

def test_update_task(task_service):
    task = task_service.add_task("Original Title")
    updated_task = task_service.update_task(task.id, title="Updated Title")
    assert updated_task.title == "Updated Title"

def test_complete_task(task_service):
    task = task_service.add_task("Test Task")
    completed_task = task_service.complete_task(task.id)
    assert completed_task.completed

def test_delete_task(task_service):
    task = task_service.add_task("Test Task")
    deleted_task = task_service.delete_task(task.id)
    assert deleted_task.id == task.id
    with pytest.raises(Exception):
        task_service.get_task_by_id(task.id)