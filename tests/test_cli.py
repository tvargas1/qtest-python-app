"""
Unit tests for the CLI module.
"""

import pytest
import os
import sys
import tempfile
from unittest.mock import patch
from src.cli import main
from src.services.task_service import TaskService


@pytest.fixture
def temp_task_file():
    """Create a temporary task file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_filename = temp.name
    
    # Patch the config directory and storage file path
    original_join = os.path.join
    
    def mock_join(*args, **kwargs):
        if len(args) >= 3 and args[-2] == "config" and args[-1] == "tasks.json":
            return temp_filename
        return original_join(*args, **kwargs)
    
    with patch('os.path.join', side_effect=mock_join):
        yield temp_filename
    
    # Clean up
    if os.path.exists(temp_filename):
        os.remove(temp_filename)


@patch('sys.argv')
def test_cli_add_task(mock_argv, temp_task_file):
    """Test adding a task via CLI."""
    # Mock command line arguments
    mock_argv.__getitem__.side_effect = lambda idx: {
        0: 'cli.py',
        1: 'add',
        2: 'Test Task',
        3: '-d',
        4: 'Test Description',
        5: '-p',
        6: 'high'
    }.get(idx)
    
    # Capture stdout
    with patch('sys.stdout') as mock_stdout:
        main()
    
    # Check if task was added
    service = TaskService(temp_task_file)
    tasks = service.get_all_tasks()
    
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].description == "Test Description"
    assert tasks[0].priority == "high"


@patch('sys.argv')
def test_cli_list_tasks(mock_argv, temp_task_file):
    """Test listing tasks via CLI."""
    # Add some tasks first
    service = TaskService(temp_task_file)
    service.add_task("Task 1", "Description 1")
    service.add_task("Task 2", "Description 2")
    
    # Mock command line arguments for list command
    mock_argv.__getitem__.side_effect = lambda idx: {
        0: 'cli.py',
        1: 'list'
    }.get(idx, None)
    
    # Capture stdout
    with patch('sys.stdout') as mock_stdout:
        main()
    
    # We can't easily check the exact output format, but we can verify main() ran without errors


@patch('sys.argv')
def test_cli_complete_task(mock_argv, temp_task_file):
    """Test completing a task via CLI."""
    # Add a task first
    service = TaskService(temp_task_file)
    task = service.add_task("Task to complete")
    
    # Mock command line arguments for complete command
    mock_argv.__getitem__.side_effect = lambda idx: {
        0: 'cli.py',
        1: 'complete',
        2: str(task.id)
    }.get(idx, None)
    
    # Capture stdout
    with patch('sys.stdout') as mock_stdout:
        main()
    
    # Check if task was completed
    updated_task = service.get_task_by_id(task.id)
    assert updated_task.completed is True


@patch('sys.argv')
def test_cli_delete_task(mock_argv, temp_task_file):
    """Test deleting a task via CLI."""
    # Add a task first
    service = TaskService(temp_task_file)
    task = service.add_task("Task to delete")
    
    # Mock command line arguments for delete command
    mock_argv.__getitem__.side_effect = lambda idx: {
        0: 'cli.py',
        1: 'delete',
        2: str(task.id)
    }.get(idx, None)
    
    # Capture stdout
    with patch('sys.stdout') as mock_stdout:
        main()
    
    # Check if task was deleted
    tasks = service.get_all_tasks()
    assert len(tasks) == 0