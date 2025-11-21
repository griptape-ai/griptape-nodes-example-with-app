# griptape-nodes-example-with-app

A Streamlit web application for generating audio content using AI-powered Griptape Nodes workflows with a sophisticated multi-tab interface.

## Features

- Multi-tab interface for organizing workflow inputs (World, Character, Data Experts, Speechwriter, Music Coach, Generation)
- JSON validation and auto-formatting for game data input
- Real-time audio generation with voice and music outputs
- Voice generation controls (stability, speed, voice preset)
- Quick voice-only regeneration without re-running entire workflow
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

The application is organized into six tabs:

1. **World**: Define the rules and context of your world
2. **Character**: Define who the character is and how they think
3. **Data Experts**: Configure three data experts and a summarizer
4. **Speechwriter**: Define the debriefing monologue style (includes audio delivery instructions)
5. **Music Coach**: Configure music generation guidelines
6. **Generation**: Execute the workflow and view outputs

#### Generation Tab

The Generation tab has a two-column layout:

**Left Column (Game Data)**:
- Paste your JSON game data
- Format JSON button for auto-formatting
- Real-time JSON validation with error messages
- Input disabled while workflow is running

**Right Column (Voice Settings & Execution)**:
- **Voice Settings**:
  - **Stability**: Creative, Natural, or Robust (affects voice consistency)
  - **Speed**: 0.7 to 1.2 (adjustable in 0.01 increments for fine control)
  - **Voice**: 15 voice preset options
  - All settings disabled while workflow is running
- **Execution Buttons**:
  - **"Run Griptape Nodes Workflow to Generate Audio"** (before first run) or **"Re-run entire Griptape Nodes workflow"** (after first run)
  - **"Re-run voice generation"** (appears after first run, enabled only when voice settings change) - quickly regenerates voice audio without re-running the full workflow
- **Outputs** (after generation):
  - Voice and music audio players
  - Debriefing monologue (includes audio tags for TTS delivery)
  - Retrospective section with markdown support

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
4. When the user clicks "Run Griptape Nodes Workflow to Generate Audio" (or "Re-run entire Griptape Nodes workflow"):
   - All inputs from all tabs are gathered
   - JSON game data is validated before submission
   - Voice settings (stability, speed, voice_preset) are captured
   - The `LocalWorkflowExecutor` executes the workflow with all inputs and `run_voice_generation_only=False`
   - The workflow generates voice and music audio files
   - Voice parameter tracking is updated for change detection
5. When the user adjusts voice settings and clicks "Re-run voice generation":
   - Only voice-related parameters are sent to the workflow
   - The workflow skips data analysis and monologue generation
   - Only the voice audio is regenerated with new settings
   - Music audio and text outputs remain unchanged
6. Results are displayed in the Generation tab with:
   - Audio players for voice and music
   - Debriefing monologue text output
   - Markdown retrospective analysis
7. The workflow maintains state across executions via the cached `LocalWorkflowExecutor`

### Workflow Pipeline

The AI-powered workflow processes data through multiple stages:

1. **Data Analysis**: Raw JSON data is analyzed by three specialized data experts, each focusing on different aspects
2. **Summarization**: A summarizer agent consolidates the experts' findings into a coherent analysis
3. **Debriefing Generation**: The speechwriter (informed by character personality and world context) creates a concise debriefing monologue with audio delivery tags
4. **Parallel Audio Processing**:
   - **Voice Path**: Text-to-Speech with configurable stability, speed, and voice preset → Voice audio
   - **Music Path**: Music coach analyzes the monologue's tone → Music generation → Music audio
5. **Retrospective**: Data experts reconvene to identify what additional data would have improved their analysis
6. **Output**: Returns debriefing monologue, voice audio, music audio, and retrospective

## Workflow Details

The included workflow ([published_nodes_workflow.py](published_nodes_workflow.py)) orchestrates an AI-powered audio generation pipeline.

### Workflow Inputs

The workflow accepts the following inputs through the "Start Flow" node:

- `world_rules`: Context and rules for the world setting
- `character_definition`: Character traits and personality
- `data_expert_1`, `data_expert_2`, `data_expert_3`: Three data expert configurations
- `summarizer`: Summarizer configuration
- `speechwriter_rules`: Guidelines for debriefing creation (includes audio delivery instructions)
- `music_coach_rules`: Music coaching guidelines
- `game_data`: JSON string containing mission/game data
- `stability`: Voice stability setting (Creative, Natural, or Robust)
- `speed`: Voice speed (0.7 to 1.2)
- `voice_preset`: Voice preset name (e.g., "James", "Rachel", etc.)
- `run_voice_generation_only`: Boolean flag to skip full workflow and only regenerate voice audio

### Workflow Outputs

The workflow returns through the "End Flow" node:

- `was_successful`: Boolean indicating success/failure
- `result_details`: Details about workflow execution
- `voice_audio_artifact`: AudioUrlArtifact containing voice audio
- `music_audio_artifact`: AudioUrlArtifact containing music audio
- `speechwriter_output`: Generated debriefing monologue with audio tags
- `retrospective`: Markdown-formatted analysis from data experts

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
