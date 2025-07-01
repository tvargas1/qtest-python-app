"""
Unit tests for the Streamlit app module.

Note: These tests focus on the non-UI logic in the app.py file.
Full UI testing would require a different approach with tools like Selenium.
"""

import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
import streamlit as st
from src.services.task_service import TaskService


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit functions."""
    with patch('streamlit.set_page_config'), \
         patch('streamlit.title'), \
         patch('streamlit.write'), \
         patch('streamlit.sidebar.title'), \
         patch('streamlit.sidebar.radio', return_value="View Tasks"), \
         patch('streamlit.header'), \
         patch('streamlit.columns', return_value=[MagicMock(), MagicMock()]), \
         patch('streamlit.checkbox', return_value=False), \
         patch('streamlit.selectbox', return_value="All"), \
         patch('streamlit.info'), \
         patch('streamlit.container', return_value=MagicMock()), \
         patch('streamlit.markdown'), \
         patch('streamlit.expander', return_value=MagicMock()), \
         patch('streamlit.button', return_value=False), \
         patch('streamlit.divider'), \
         patch('streamlit.form', return_value=MagicMock()), \
         patch('streamlit.text_input', return_value="Test Task"), \
         patch('streamlit.text_area', return_value="Test Description"), \
         patch('streamlit.select_slider', return_value="Medium"), \
         patch('streamlit.form_submit_button', return_value=True), \
         patch('streamlit.success'), \
         patch('streamlit.error'), \
         patch('streamlit.experimental_rerun'):
        yield


@pytest.fixture
def temp_task_service():
    """Create a TaskService with a temporary file."""
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_filename = temp.name
    
    service = TaskService(temp_filename)
    yield service
    
    # Clean up
    if os.path.exists(temp_filename):
        os.remove(temp_filename)


def test_display_tasks_page(mock_streamlit, temp_task_service):
    """Test the display_tasks_page function."""
    from src.app import display_tasks_page
    
    # Add some tasks
    temp_task_service.add_task("Task 1", "Description 1")
    temp_task_service.add_task("Task 2", "Description 2", priority="high")
    
    # Call the function
    display_tasks_page(temp_task_service)
    
    # Since we're mocking Streamlit, we can't easily verify the UI,
    # but we can verify the function runs without errors


def test_add_task_page(mock_streamlit, temp_task_service):
    """Test the add_task_page function."""
    from src.app import add_task_page
    
    # Call the function
    add_task_page(temp_task_service)
    
    # Check if a task was added
    tasks = temp_task_service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].description == "Test Description"
    assert tasks[0].priority == "medium"  # lowercase in the code


def test_search_tasks_page(mock_streamlit, temp_task_service):
    """Test the search_tasks_page function."""
    from src.app import search_tasks_page
    
    # Add some tasks
    temp_task_service.add_task("Buy groceries", "Get milk and eggs")
    temp_task_service.add_task("Pay bills", "Electricity and water")
    
    # Mock the text_input to return a search keyword
    with patch('streamlit.text_input', return_value="groceries"):
        search_tasks_page(temp_task_service)
        
    # Again, we can't easily verify the UI output,
    # but we can verify the function runs without errors