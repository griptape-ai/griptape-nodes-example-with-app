# griptape-nodes-example-with-app

A Streamlit web application for generating audio content using AI-powered Griptape Nodes workflows with a sophisticated multi-tab interface.

## Features

- Multi-tab interface for organizing workflow inputs (World, Character, Data Experts, Speechwriter, Acting Coach, Music Coach, Generation)
- JSON validation for game data input
- Real-time audio generation with voice and music outputs
- Audio playback directly in the browser
- Persistent state across page refreshes
- Direct workflow execution (no subprocess overhead)
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

The application is organized into seven tabs:

1. **World**: Define the rules and context of your world
2. **Character**: Define who the character is and how they think
3. **Data Experts**: Configure three data experts and a summarizer
4. **Speechwriter**: Define the type of monologue the character should deliver (based on data analysis)
5. **Acting Coach**: Define how the monologue should be refined for tone and inflection (before TTS)
6. **Music Coach**: Configure music generation guidelines (based on the original monologue)
7. **Generation**: Execute the workflow and view outputs

#### Generation Tab

The Generation tab has a two-column layout:

**Left Column (Game Data)**:
- Paste your JSON game data
- Real-time JSON validation with error messages
- Run button disabled if JSON is invalid

**Right Column (Outputs)**:
- "Run Griptape Nodes Workflow to Generate Audio" button
- Voice and music audio players (after generation)
- Monologue outputs with tabs:
  - **Original Monologue**: The character's initial speech based on data analysis
  - **Massaged for TTS**: The acting coach's refined version (used for voice generation)
- Retrospective section with markdown support (data experts' feedback on what additional data would improve results)

All inputs persist across page refreshes, so you can safely reload the browser without losing your work.

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

### Application Flow

1. The Streamlit app loads [published_nodes_workflow.py](published_nodes_workflow.py) which defines the Griptape Nodes workflow
2. User inputs are organized across multiple tabs for better organization
3. Session state preserves all inputs across page refreshes
4. When the user clicks "Run Griptape Nodes Workflow to Generate Audio":
   - All inputs from all tabs are gathered
   - JSON game data is validated before submission
   - The `LocalWorkflowExecutor` executes the workflow with all inputs
   - The workflow generates voice and music audio files
5. Results are displayed in the Generation tab with:
   - Audio players for voice and music (local files)
   - Text outputs from speechwriter and acting coach
   - Markdown retrospective analysis
6. The workflow maintains state across executions via the cached `LocalWorkflowExecutor`

### Workflow Pipeline

The AI-powered workflow processes data through multiple stages:

1. **Data Analysis**: Raw JSON data is analyzed by three specialized data experts, each focusing on different aspects
2. **Summarization**: A summarizer agent consolidates the experts' findings into a coherent analysis
3. **Monologue Generation**: The character (informed by their personality and world context) creates a monologue based on the summary
4. **Parallel Processing**:
   - **Voice Path**: Acting coach refines the monologue for tone and inflection → Text-to-Speech → Voice audio
   - **Music Path**: Music coach analyzes the original monologue's tone → Music generation → Music audio
5. **Retrospective**: Data experts reconvene to identify what additional data would have improved their analysis
6. **Output**: Returns original monologue, refined monologue, voice audio, music audio, and retrospective

## Workflow Details

The included workflow ([published_nodes_workflow.py](published_nodes_workflow.py)) orchestrates an AI-powered audio generation pipeline.

### Workflow Inputs

The workflow accepts the following inputs through the "Start Flow" node:

- `world_rules`: Context and rules for the world setting
- `character_definition`: Character traits and personality
- `data_expert_1`, `data_expert_2`, `data_expert_3`: Three data expert configurations
- `summarizer`: Summarizer configuration
- `speechwriter_rules`: Guidelines for speech creation
- `acting_coach_rules`: Direction for line delivery
- `music_coach_rules`: Music coaching guidelines
- `game_data`: JSON object containing game-specific data

### Workflow Outputs

The workflow returns through the "End Flow" node:

- `was_successful`: Boolean indicating success/failure
- `voice_audio_path`: Path to generated voice audio file
- `music_audio_path`: Path to generated music audio file
- `speechwriter_output`: Generated speech text
- `acting_coach_output`: Acting direction and notes
- `retrospective`: Markdown-formatted analysis
- `error`: Error message (if applicable)

## Customization

### Updating Default Text Values

To change the default placeholder text for each tab:

1. Open [app.py](app.py:55-90)
2. Locate the `_initialize_session_state()` function
3. Update the default values for each session state variable

### Customizing the Workflow

To use a different workflow:

1. Edit [published_nodes_workflow.py](published_nodes_workflow.py) or create a new workflow file
2. Update the workflow import in [app.py](app.py:30) if using a different workflow
3. Ensure your workflow accepts the inputs defined in the "Workflow Inputs" section above
4. Ensure your workflow returns the outputs defined in the "Workflow Outputs" section above

### Modifying the Interface

To customize the Streamlit interface:

1. Open [app.py](app.py:178)
2. Modify the `main()` function to adjust layouts, add/remove tabs, or change styling

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
- Missing audio generation dependencies

### Invalid JSON Error

If you see "Invalid JSON" in the Generation tab:
1. Ensure your JSON is properly formatted
2. Use a JSON validator to check syntax
3. Verify all quotes are double quotes (not single quotes)
4. Check for trailing commas

### Audio Files Not Playing

If audio files don't play after generation:
1. Check that the workflow returned valid file paths
2. Verify the audio files exist at the returned paths
3. Ensure the audio format is supported by your browser
4. Check console for file path or permissions errors

### Streamlit Caching

If you see unexpected behavior, clear Streamlit's cache:
- Press 'C' in the app (or use the menu: Settings → Clear cache)
- Or restart the application with `make run`

## License

See [LICENSE](LICENSE) for details.
