import pytest
import re
from datetime import datetime
from src.models.task import Task

def test_task_creation():
    task = Task(title="Test Task", description="Test Description", priority="high")
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "high"
    assert not task.completed
    assert task.id is None  # Ensure task_id is None when not provided

def test_task_creation_with_all_parameters():
    """Test task creation with all parameters specified."""
    task = Task(
        title="Complete Task",
        description="Detailed description",
        priority="low",
        completed=True,
        created_at="2023-01-01 12:00:00",
        task_id=42
    )
    assert task.title == "Complete Task"
    assert task.description == "Detailed description"
    assert task.priority == "low"
    assert task.completed is True
    assert task.created_at == "2023-01-01 12:00:00"
    assert task.id == 42

def test_task_default_created_at():
    """Test that created_at gets a default value when not provided."""
    task = Task(title="Test Task")
    
    # Verify created_at is a string in the expected format (YYYY-MM-DD HH:MM:SS)
    assert isinstance(task.created_at, str)
    
    # Check format using regex
    date_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    assert re.match(date_pattern, task.created_at)
    
    # Ensure it's a valid datetime string by parsing it
    datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S")

def test_task_to_dict():
    task = Task(title="Test Task", description="Test Description", priority="high", task_id=1)
    task_dict = task.to_dict()
    assert isinstance(task_dict, dict)
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Test Task"
    assert task_dict["description"] == "Test Description"
    assert task_dict["priority"] == "high"
    assert not task_dict["completed"]
    assert "created_at" in task_dict

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

def test_task_from_dict_with_minimal_data():
    """Test creating a task from a dictionary with only required fields."""
    task_dict = {
        "id": 1,
        "title": "Minimal Task"
    }
    task = Task.from_dict(task_dict)
    assert task.id == 1
    assert task.title == "Minimal Task"
    assert task.description == ""  # Default value
    assert task.priority == "medium"  # Default value
    assert not task.completed  # Default value
    assert task.created_at is None  # Default value is None when not provided

def test_task_str_representation():
    """Test the string representation of a Task."""
    # Test active task
    task = Task(title="Test Task", priority="high", task_id=1)
    expected_str = "Task 1: Test Task (Active, high priority)"
    assert str(task) == expected_str
    
    # Test completed task
    task = Task(title="Completed Task", priority="low", completed=True, task_id=2)
    expected_str = "Task 2: Completed Task (Completed, low priority)"
    assert str(task) == expected_str