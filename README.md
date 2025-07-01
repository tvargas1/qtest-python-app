# Task Manager

A simple task management application with both CLI and web interfaces. This application allows users to efficiently manage their tasks through either a command-line interface for quick operations or a user-friendly web interface built with Streamlit.

## Features

- Add, view, update the tasks
- Mark tasks as complete
- Search for tasks by keyword
- Filter tasks by status and priority
- Command-line interface for quick task management
- Web interface built with Streamlit for a user-friendly experience

## Software Stack

- **Python 3.6+**: Core programming language
- **Streamlit**: Web interface framework
- **JSON**: Data storage format (no database required)
- **Pytest**: Testing framework

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Project Structure

```
task_manager_project/
├── config/                 # Configuration files and task storage
│   └── tasks.json          # JSON file storing task data
├── docs/                   # Documentation
├── src/                    # Source code
│   ├── models/             # Data models
│   │   └── task.py         # Task model
│   ├── services/           # Business logic
│   │   └── task_service.py # Task management service
│   ├── utils/              # Utility modules
│   │   └── exceptions.py   # Custom exceptions
│   ├── app.py              # Streamlit web application
│   └── cli.py              # Command-line interface
├── tests/                  # Test cases
│   ├── test_task_model.py  # Tests for Task model
│   └── test_task_service.py# Tests for TaskService
├── setup.py                # Package setup script
└── requirements.txt        # Project dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd task_manager_project
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install the package in development mode (optional):
   ```
   pip install -e .
   ```

## Usage

### Command-line Interface

Run the CLI application:

```
python -m src.cli
```

Or if you installed the package:

```
task-manager
```

Available commands:

- Add a task: `python -m src.cli add "Task title" -d "Task description" -p high`
- List tasks: `python -m src.cli list`
- List all tasks including completed: `python -m src.cli list -a`
- Complete a task: `python -m src.cli complete <task-id>`
- Delete a task: `python -m src.cli delete <task-id>`
- Search for tasks: `python -m src.cli search <keyword>`
- View task details: `python -m src.cli view <task-id>`

### Web Interface

Run the Streamlit web application:

```
streamlit run src/app.py
```

The web interface provides the following pages:
- View Tasks: Display and manage all tasks
- Add Task: Create new tasks
- Search Tasks: Find tasks by keyword

## Testing

The project includes comprehensive unit tests for all Python classes and modules. The tests are organized in the `tests` directory:

- `test_task_model.py`: Tests for the Task class
- `test_task_service.py`: Tests for the TaskService class
- `test_exceptions.py`: Tests for custom exception classes
- `test_cli.py`: Tests for the command-line interface
- `test_app.py`: Tests for the Streamlit web application

### Running Tests

To run all tests:

```bash
python -m pytest
```

### Test Coverage

To run tests with coverage reporting:

```bash
python -m pytest --cov=src
```

For a detailed HTML coverage report:

```bash
python -m pytest --cov=src --cov-report=html
```

This will generate a coverage report in the `htmlcov` directory. Open `htmlcov/index.html` in a browser to view the report.

### Test Structure

The tests follow these principles:

1. **Unit Tests**: Each class and its methods are tested independently
2. **Fixtures**: Common test setup is handled with pytest fixtures
3. **Mocking**: External dependencies are mocked for isolated testing
4. **Edge Cases**: Tests include handling of edge cases and error conditions

## Deployment

### Local Deployment

For local usage, simply run the application as described in the Usage section.

### Streamlit Cloud Deployment

To deploy the web interface on Streamlit Cloud:

1. Push your code to a GitHub repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and point it to your GitHub repository
4. Configure the app to run `src/app.py`

### Other Deployment Options

- **Docker**: You can containerize the application for consistent deployment across environments
- **Heroku**: Deploy the Streamlit app to Heroku using their Python buildpack
- **AWS/GCP/Azure**: Deploy to cloud platforms using their respective Python hosting services

## Development

To set up a development environment:

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install development dependencies: `pip install -e ".[dev]"`

## License

[MIT License](LICENSE)
