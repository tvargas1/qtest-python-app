import pytest
import os
import json
import tempfile
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.exceptions import TaskNotFoundException

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

def test_add_task_with_defaults(task_service):
    """Test adding a task with default values."""
    task = task_service.add_task("Simple Task")
    assert isinstance(task, Task)
    assert task.title == "Simple Task"
    assert task.description == ""
    assert task.priority == "medium"
    assert task.id == 1  # First task should have ID 1

def test_get_all_tasks(task_service):
    task_service.add_task("Task 1")
    task_service.add_task("Task 2")
    tasks = task_service.get_all_tasks()
    assert len(tasks) == 2
    assert all(isinstance(task, Task) for task in tasks)

def test_get_all_tasks_with_filter(task_service):
    """Test getting tasks with completed filter."""
    # Add one active and one completed task
    task1 = task_service.add_task("Active Task")
    task2 = task_service.add_task("Completed Task")
    task_service.complete_task(task2.id)
    
    # Get only active tasks
    active_tasks = task_service.get_all_tasks(show_completed=False)
    assert len(active_tasks) == 1
    assert active_tasks[0].id == task1.id
    assert not active_tasks[0].completed
    
    # Get all tasks
    all_tasks = task_service.get_all_tasks(show_completed=True)
    assert len(all_tasks) == 2

def test_get_task_by_id(task_service):
    task = task_service.add_task("Test Task")
    found_task = task_service.get_task_by_id(task.id)
    assert found_task.id == task.id
    assert found_task.title == task.title

def test_get_task_by_id_not_found(task_service):
    """Test getting a task with a non-existent ID."""
    with pytest.raises(TaskNotFoundException) as excinfo:
        task_service.get_task_by_id(999)
    
    assert "Task with ID 999 not found" in str(excinfo.value)

def test_update_task(task_service):
    task = task_service.add_task("Original Title")
    updated_task = task_service.update_task(task.id, title="Updated Title")
    assert updated_task.title == "Updated Title"

def test_update_task_multiple_fields(task_service):
    """Test updating multiple fields of a task."""
    task = task_service.add_task("Original Title", "Original Description", "low")
    
    updated_task = task_service.update_task(
        task.id,
        title="Updated Title",
        description="Updated Description",
        priority="high",
        completed=True
    )
    
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"
    assert updated_task.priority == "high"
    assert updated_task.completed is True

def test_update_task_not_found(task_service):
    """Test updating a non-existent task."""
    with pytest.raises(TaskNotFoundException):
        task_service.update_task(999, title="Updated Title")

def test_complete_task(task_service):
    task = task_service.add_task("Test Task")
    completed_task = task_service.complete_task(task.id)
    assert completed_task.completed

def test_complete_task_not_found(task_service):
    """Test completing a non-existent task."""
    with pytest.raises(TaskNotFoundException):
        task_service.complete_task(999)

def test_delete_task(task_service):
    task = task_service.add_task("Test Task")
    deleted_task = task_service.delete_task(task.id)
    assert deleted_task.id == task.id
    with pytest.raises(TaskNotFoundException):
        task_service.get_task_by_id(task.id)

def test_delete_task_not_found(task_service):
    """Test deleting a non-existent task."""
    with pytest.raises(TaskNotFoundException):
        task_service.delete_task(999)

def test_search_tasks(task_service):
    """Test searching for tasks by keyword."""
    # Add some tasks
    task_service.add_task("Buy groceries", "Get milk and eggs")
    task_service.add_task("Pay bills", "Electricity and water")
    task_service.add_task("Call mom", "Ask about the recipe")
    
    # Search in titles
    results = task_service.search_tasks("buy")
    assert len(results) == 1
    assert results[0].title == "Buy groceries"
    
    # Search in descriptions
    results = task_service.search_tasks("milk")
    assert len(results) == 1
    assert results[0].title == "Buy groceries"
    
    # Search with multiple matches
    results = task_service.search_tasks("a")
    assert len(results) == 3  # All tasks should match
    
    # Search with no matches
    results = task_service.search_tasks("xyz")
    assert len(results) == 0

def test_search_tasks_case_insensitive(task_service):
    """Test that search is case insensitive."""
    task_service.add_task("UPPERCASE TASK", "UPPERCASE DESCRIPTION")
    
    results = task_service.search_tasks("uppercase")
    assert len(results) == 1
    
    results = task_service.search_tasks("LOWERCASE")
    assert len(results) == 0

def test_load_and_save_tasks():
    """Test that tasks are properly saved to and loaded from file."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_filename = temp.name
    
    try:
        # Create a service and add tasks
        service1 = TaskService(temp_filename)
        task1 = service1.add_task("Task 1", "Description 1")
        task2 = service1.add_task("Task 2", "Description 2")
        
        # Create a new service instance that should load the tasks
        service2 = TaskService(temp_filename)
        loaded_tasks = service2.get_all_tasks()
        
        # Verify tasks were loaded correctly
        assert len(loaded_tasks) == 2
        assert loaded_tasks[0].title == "Task 1"
        assert loaded_tasks[1].title == "Task 2"
        
        # Verify IDs were preserved
        assert loaded_tasks[0].id == task1.id
        assert loaded_tasks[1].id == task2.id
    
    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

def test_load_tasks_from_invalid_json():
    """Test loading tasks from an invalid JSON file."""
    # Create a temporary file with invalid JSON
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(b"This is not valid JSON")
        temp_filename = temp.name
    
    try:
        # Create a service that should handle the invalid JSON
        service = TaskService(temp_filename)
        tasks = service.get_all_tasks()
        
        # Should start with an empty task list
        assert len(tasks) == 0
    
    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.remove(temp_filename)