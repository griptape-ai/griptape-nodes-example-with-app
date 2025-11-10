"""Main Gradio application for invoking Python subprocesses."""

import subprocess
import sys
from pathlib import Path

import gradio as gr


def run_worker() -> str:
    """Run the worker.py script as a subprocess and return its output.

    Returns:
        str: The output from the worker subprocess, or an error message.
    """
    worker_path = Path(__file__).parent / "worker.py"

    if not worker_path.exists():
        return f"Error: worker.py not found at {worker_path}"

    try:
        result = subprocess.run(  # noqa: S603  # Trusted local script execution
            [sys.executable, str(worker_path)],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return "Error: Worker process timed out after 30 seconds"
    except subprocess.CalledProcessError as e:
        return f"Error: Worker process failed with exit code {e.returncode}\n\nStderr:\n{e.stderr}\n\nStdout:\n{e.stdout}"

    output = result.stdout.strip()
    if result.stderr:
        output += f"\n\nWarnings/Errors:\n{result.stderr.strip()}"

    return output


def create_ui() -> gr.Blocks:
    """Create the Gradio user interface.

    Returns:
        gr.Blocks: The configured Gradio interface.
    """
    with gr.Blocks(title="Subprocess Runner") as demo:
        gr.Markdown("# Python Subprocess Runner")
        gr.Markdown("Click the button below to invoke the worker script as a subprocess.")

        with gr.Row():
            run_button = gr.Button("Run Worker", variant="primary", size="lg")

        output_text = gr.Textbox(
            label="Output",
            lines=10,
            placeholder="Output will appear here...",
            interactive=False,
        )

        run_button.click(
            fn=run_worker,
            inputs=[],
            outputs=output_text,
        )

    return demo


def main() -> None:
    """Main entry point for the application."""
    demo = create_ui()
    demo.launch()


if __name__ == "__main__":
    main()
