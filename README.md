# griptape-nodes-example-with-app

A Streamlit web application that demonstrates executing Griptape Nodes workflows with a simple, interactive interface.

## Features

- Clean Streamlit UI for interacting with AI agents
- Direct workflow execution (no subprocess overhead)
- Real-time workflow output display
- Conversational state maintained across runs
- Comprehensive error handling
- Full development tooling (linting, type checking, spell checking)
- VSCode debugging support

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key (for the Agent node)

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

3. Set up your environment variables:
```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## Usage

Run the Streamlit application:

```bash
make run
```

The app will automatically open in your browser at `http://localhost:8501`.

### Using the Interface

1. Enter your prompt in the text area (e.g., "Say hi")
2. Click "Run Workflow"
3. The AI agent will process your request and display the response
4. The workflow maintains conversational state between runs

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
make clean          # Remove build artifacts and caches
make run            # Run the Streamlit app
```

### Development Workflow

1. Make your changes
2. Run `make check` or `make fix` to ensure code quality
3. Commit your changes

### Debugging

Use VSCode's built-in debugger:

1. Open the Run and Debug view (Cmd+Shift+D)
2. Select "Debug Streamlit App" from the dropdown
3. Press F5 or click the green play button
4. Set breakpoints in [app.py](app.py) or [published_nodes_workflow.py](published_nodes_workflow.py)

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
├── app.py                        # Streamlit application
├── published_nodes_workflow.py   # Griptape Nodes workflow definition
├── pyproject.toml               # Project dependencies and tool configuration
├── Makefile                     # Development commands
├── CLAUDE.md                    # Code style guidelines
├── .env                         # Environment variables (API keys)
├── .env.example                 # Example environment variables
└── README.md                    # This file
```

## How It Works

1. The Streamlit app loads [published_nodes_workflow.py](published_nodes_workflow.py) which defines the Griptape Nodes workflow
2. When a user submits a prompt via the interface:
   - The app calls `aexecute_workflow()` from the workflow module
   - The user's prompt is passed to the workflow's "Start Flow" node
   - The workflow executes the Agent node with the prompt
   - The Agent's response is captured from the "End Flow" node output
3. Results are displayed in the Streamlit interface with success/error indicators
4. The workflow maintains state across executions, enabling conversational interactions

## Workflow Details

The included workflow ([published_nodes_workflow.py](published_nodes_workflow.py)) contains:

- **Start Flow node**: Accepts user input (prompt)
- **Text Input node**: Provides default text
- **Agent node**: Griptape AI agent that processes the prompt
- **End Flow node**: Returns the agent's response and execution status

### Workflow Inputs

- `prompt`: The user's message to the AI agent

### Workflow Outputs

- `output`: The agent's response
- `was_successful`: Boolean indicating if workflow completed successfully
- `result_details`: Additional details about execution

## Customization

To customize the workflow:

1. Edit [published_nodes_workflow.py](published_nodes_workflow.py) or create a new workflow file
2. Update the workflow import in [app.py](app.py) if using a different workflow
3. Modify the Streamlit interface in [app.py](app.py) as needed

## Troubleshooting

### Missing API Key

If you see an error about missing API keys:
1. Ensure your `.env` file exists (copy from `.env.example`)
2. Add your OpenAI API key: `OPENAI_API_KEY=sk-...`
3. Restart the application

### Workflow Execution Errors

Check the console output for detailed error messages. Common issues:
- Invalid API key
- Network connectivity problems
- Workflow configuration issues

### Streamlit Caching

If you see unexpected behavior, clear Streamlit's cache:
- Press 'C' in the app (or use the menu: Settings → Clear cache)

## License

See [LICENSE](LICENSE) for details.
