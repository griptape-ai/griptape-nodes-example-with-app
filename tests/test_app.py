"""Tests for the Gradio application."""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from app import create_ui, run_worker


def test_create_ui() -> None:
    """Test that the UI is created successfully."""
    demo = create_ui()
    assert demo is not None


def test_run_worker_success() -> None:
    """Test successful worker execution."""
    mock_result = MagicMock()
    mock_result.stdout = "Worker output"
    mock_result.stderr = ""
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        output = run_worker()

    assert "Worker output" in output


def test_run_worker_timeout() -> None:
    """Test worker timeout handling."""
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 30)):
        output = run_worker()

    assert "Error: Worker process timed out" in output


def test_run_worker_process_error() -> None:
    """Test worker process error handling."""
    mock_error = subprocess.CalledProcessError(1, "cmd")
    mock_error.stdout = "stdout content"
    mock_error.stderr = "stderr content"

    with patch("subprocess.run", side_effect=mock_error):
        output = run_worker()

    assert "Error: Worker process failed" in output
    assert "exit code 1" in output


def test_run_worker_missing_file() -> None:
    """Test handling of missing worker.py file."""
    with patch("pathlib.Path.exists", return_value=False):
        output = run_worker()

    assert "Error: worker.py not found" in output


def test_run_worker_with_stderr() -> None:
    """Test worker execution with stderr output."""
    mock_result = MagicMock()
    mock_result.stdout = "Worker output"
    mock_result.stderr = "Warning: something"
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        output = run_worker()

    assert "Worker output" in output
    assert "Warnings/Errors:" in output
    assert "Warning: something" in output


def test_worker_script_exists() -> None:
    """Test that worker.py exists in the expected location."""
    worker_path = Path(__file__).parent.parent / "worker.py"
    assert worker_path.exists(), "worker.py should exist in the project root"


def test_worker_script_runs() -> None:
    """Test that worker.py can be executed successfully."""
    worker_path = Path(__file__).parent.parent / "worker.py"

    result = subprocess.run(
        [sys.executable, str(worker_path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=5,
    )

    assert result.returncode == 0, f"worker.py failed with: {result.stderr}"
    assert len(result.stdout) > 0, "worker.py should produce output"
