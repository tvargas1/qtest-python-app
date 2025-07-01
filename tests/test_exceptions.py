"""
Unit tests for custom exceptions in the task manager application.
"""

import pytest
from src.utils.exceptions import (
    TaskManagerException,
    TaskNotFoundException,
    InvalidTaskDataException
)


def test_task_manager_exception():
    """Test that TaskManagerException can be raised and caught properly."""
    # Test raising the exception with a message
    with pytest.raises(TaskManagerException) as excinfo:
        raise TaskManagerException("Test exception message")
    
    assert str(excinfo.value) == "Test exception message"
    
    # Test that it's a proper subclass of Exception
    assert issubclass(TaskManagerException, Exception)


def test_task_not_found_exception():
    """Test that TaskNotFoundException can be raised and caught properly."""
    # Test raising the exception with a message
    with pytest.raises(TaskNotFoundException) as excinfo:
        raise TaskNotFoundException("Task with ID 123 not found")
    
    assert str(excinfo.value) == "Task with ID 123 not found"
    
    # Test inheritance
    assert issubclass(TaskNotFoundException, TaskManagerException)
    
    # Test that it can be caught as a TaskManagerException
    try:
        raise TaskNotFoundException("Test")
    except TaskManagerException:
        caught = True
    
    assert caught


def test_invalid_task_data_exception():
    """Test that InvalidTaskDataException can be raised and caught properly."""
    # Test raising the exception with a message
    with pytest.raises(InvalidTaskDataException) as excinfo:
        raise InvalidTaskDataException("Invalid priority value")
    
    assert str(excinfo.value) == "Invalid priority value"
    
    # Test inheritance
    assert issubclass(InvalidTaskDataException, TaskManagerException)
    
    # Test that it can be caught as a TaskManagerException
    try:
        raise InvalidTaskDataException("Test")
    except TaskManagerException:
        caught = True
    
    assert caught