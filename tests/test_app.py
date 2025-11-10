"""Tests for the Streamlit application."""

from unittest.mock import AsyncMock, patch

import pytest

from app import execute_workflow, execute_workflow_async


@pytest.mark.asyncio
async def test_execute_workflow_async_success() -> None:
    """Test successful workflow execution."""
    mock_output = {
        "End Flow": {
            "output": "Hello from the agent!",
            "was_successful": True,
            "result_details": "Completed successfully",
        }
    }

    with patch("app.aexecute_workflow", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mock_output

        result = await execute_workflow_async("Say hello")

    assert result["output"] == "Hello from the agent!"
    assert result["was_successful"] == "true"
    assert result["result_details"] == "Completed successfully"
    mock_execute.assert_called_once()


@pytest.mark.asyncio
async def test_execute_workflow_async_empty_prompt() -> None:
    """Test workflow execution with empty prompt."""
    result = await execute_workflow_async("")

    assert result["output"] == ""
    assert result["was_successful"] == "false"
    assert "Prompt cannot be empty" in result["result_details"]


@pytest.mark.asyncio
async def test_execute_workflow_async_no_output() -> None:
    """Test workflow execution when workflow returns None."""
    with patch("app.aexecute_workflow", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = None

        result = await execute_workflow_async("Say hello")

    assert result["output"] == ""
    assert result["was_successful"] == "false"
    assert "Workflow did not produce output" in result["result_details"]


@pytest.mark.asyncio
async def test_execute_workflow_async_exception() -> None:
    """Test workflow execution when an exception occurs."""
    with patch("app.aexecute_workflow", new_callable=AsyncMock) as mock_execute:
        mock_execute.side_effect = RuntimeError("Workflow failed")

        result = await execute_workflow_async("Say hello")

    assert result["output"] == ""
    assert result["was_successful"] == "false"
    assert "Workflow failed" in result["result_details"]


def test_execute_workflow_sync_wrapper() -> None:
    """Test the synchronous wrapper for workflow execution."""
    mock_output = {
        "End Flow": {
            "output": "Sync test response",
            "was_successful": True,
            "result_details": "",
        }
    }

    with patch("app.aexecute_workflow", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mock_output

        result = execute_workflow("Test prompt")

    assert result["output"] == "Sync test response"
    assert result["was_successful"] == "true"
    mock_execute.assert_called_once()


def test_execute_workflow_sync_with_failure() -> None:
    """Test the synchronous wrapper when workflow fails."""
    mock_output = {
        "End Flow": {
            "output": "",
            "was_successful": False,
            "result_details": "Agent error",
        }
    }

    with patch("app.aexecute_workflow", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = mock_output

        result = execute_workflow("Test prompt")

    assert result["output"] == ""
    assert result["was_successful"] == "false"
    assert "Agent error" in result["result_details"]
