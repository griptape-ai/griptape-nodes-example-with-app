# griptape-nodes-example-with-app

A simple Gradio application that demonstrates invoking a Python subprocess with a button click.

## Features

- Clean Gradio UI with a button to trigger subprocess execution
- Displays subprocess output in real-time
- Comprehensive error handling for subprocess failures
- Full development tooling (linting, type checking, spell checking)
- Test suite with pytest

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd griptape-nodes-example-with-app
```

2. Install dependencies using uv:
```bash
make install
```

This will create a virtual environment and install all required dependencies.

## Usage

Run the Gradio application:

```bash
make run
```

This will start the Gradio server and open the UI in your browser. Click the "Run Worker" button to invoke the worker subprocess.

## Development

### Available Commands

All development commands are available through the Makefile:

```bash
make install        # Install all dependencies
make check          # Run all checks (format, lint, type-check, spell-check)
make fix            # Auto-fix formatting and linting issues
make format         # Check code formatting
make lint           # Run linter
make type-check     # Run type checker
make spell-check    # Run spell checker
make test           # Run unit tests
make test-coverage  # Run tests with coverage report
make clean          # Remove build artifacts and caches
make run            # Run the Gradio app
```

### Development Workflow

1. Make your changes
2. Run `make check` or `make fix` to ensure code quality
3. Run `make test` to verify tests pass
4. Commit your changes

### Code Style

This project follows specific code style guidelines documented in [CLAUDE.md](CLAUDE.md). Key principles:

- Evaluate all failure cases first, success path at the end
- Use simple, readable logic flow
- No lazy imports (imports at top of file)
- Specific, narrow exception handling
- Include context in error messages

## Project Structure

```
.
├── app.py              # Main Gradio application
├── worker.py           # Example worker script (invoked as subprocess)
├── tests/              # Test suite
│   └── test_app.py     # Application tests
├── pyproject.toml      # Project dependencies and tool configuration
├── Makefile            # Development commands
├── CLAUDE.md           # Code style guidelines
└── README.md           # This file
```

## How It Works

1. The Gradio UI provides a simple interface with a button
2. When clicked, [app.py](app.py) invokes [worker.py](worker.py) as a subprocess
3. The subprocess output is captured and displayed in the UI
4. Errors are handled gracefully with informative messages

## Customization

To customize the worker behavior:

1. Edit [worker.py](worker.py) to perform your desired operations
2. The worker script can access environment variables, read files, make API calls, etc.
3. Output printed to stdout will be displayed in the Gradio UI

## License

See [LICENSE](LICENSE) for details.
