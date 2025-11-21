"""Tests for the Streamlit application."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app import execute_workflow_async


@pytest.mark.asyncio
async def test_execute_workflow_async_success() -> None:
    """Test successful workflow execution."""
    # Create mock AudioUrlArtifact-like objects
    mock_voice_artifact = MagicMock()
    mock_voice_artifact.value = "file:///path/to/voice.wav"

    mock_music_artifact = MagicMock()
    mock_music_artifact.value = "file:///path/to/music.mp3"

    mock_executor = MagicMock()
    mock_executor.arun = AsyncMock()
    mock_executor.output = {
        "End Flow": {
            "was_successful": True,
            "result_details": "Success",
            "voice_audio_artifact": mock_voice_artifact,
            "music_audio_artifact": mock_music_artifact,
            "speechwriter_output": "This is a test speech.",
            "acting_coach_output": "Deliver with confidence.",
            "retrospective": "# Retrospective\n\nEverything went well.",
        }
    }

    with (
        patch("app.get_workflow_executor", return_value=mock_executor),
        patch("app._ensure_workflow_context"),
        patch("streamlit.session_state", {"executor_initialized": True}),
    ):
        result = await execute_workflow_async(
            world_rules="Test world",
            character_definition="Test character",
            data_expert_1="Expert 1",
            data_expert_2="Expert 2",
            data_expert_3="Expert 3",
            summarizer="Summarizer",
            speechwriter_rules="Speech rules",
            acting_coach_rules="Acting rules",
            music_coach_rules="Music rules",
            game_data='{"test": "data"}',
        )

    assert result["was_successful"] is True
    assert result["result_details"] == "Success"
    assert result["voice_audio_artifact"].value == "file:///path/to/voice.wav"
    assert result["music_audio_artifact"].value == "file:///path/to/music.mp3"
    assert result["speechwriter_output"] == "This is a test speech."
    assert result["acting_coach_output"] == "Deliver with confidence."
    assert "Retrospective" in result["retrospective"]


@pytest.mark.asyncio
async def test_execute_workflow_async_no_output() -> None:
    """Test workflow execution when workflow returns None."""
    mock_executor = MagicMock()
    mock_executor.arun = AsyncMock()
    mock_executor.output = None

    with (
        patch("app.get_workflow_executor", return_value=mock_executor),
        patch("app._ensure_workflow_context"),
        patch("streamlit.session_state", {"executor_initialized": True}),
    ):
        result = await execute_workflow_async(
            world_rules="Test world",
            character_definition="Test character",
            data_expert_1="Expert 1",
            data_expert_2="Expert 2",
            data_expert_3="Expert 3",
            summarizer="Summarizer",
            speechwriter_rules="Speech rules",
            acting_coach_rules="Acting rules",
            music_coach_rules="Music rules",
            game_data='{"test": "data"}',
        )

    assert result["was_successful"] is False
    assert "Workflow did not produce output" in result["result_details"]


@pytest.mark.asyncio
async def test_execute_workflow_async_exception() -> None:
    """Test workflow execution when an exception occurs."""
    mock_executor = MagicMock()
    mock_executor.arun = AsyncMock(side_effect=RuntimeError("Workflow failed"))

    with (
        patch("app.get_workflow_executor", return_value=mock_executor),
        patch("app._ensure_workflow_context"),
        patch("streamlit.session_state", {"executor_initialized": True}),
    ):
        result = await execute_workflow_async(
            world_rules="Test world",
            character_definition="Test character",
            data_expert_1="Expert 1",
            data_expert_2="Expert 2",
            data_expert_3="Expert 3",
            summarizer="Summarizer",
            speechwriter_rules="Speech rules",
            acting_coach_rules="Acting rules",
            music_coach_rules="Music rules",
            game_data='{"test": "data"}',
        )

    assert result["was_successful"] is False
    assert "Workflow failed" in result["result_details"]


@pytest.mark.asyncio
async def test_execute_workflow_async_with_workflow_error() -> None:
    """Test workflow execution when the workflow reports an error."""
    mock_executor = MagicMock()
    mock_executor.arun = AsyncMock()
    mock_executor.output = {
        "End Flow": {
            "was_successful": False,
            "result_details": "Agent processing error",
        }
    }

    with (
        patch("app.get_workflow_executor", return_value=mock_executor),
        patch("app._ensure_workflow_context"),
        patch("streamlit.session_state", {"executor_initialized": True}),
    ):
        result = await execute_workflow_async(
            world_rules="Test world",
            character_definition="Test character",
            data_expert_1="Expert 1",
            data_expert_2="Expert 2",
            data_expert_3="Expert 3",
            summarizer="Summarizer",
            speechwriter_rules="Speech rules",
            acting_coach_rules="Acting rules",
            music_coach_rules="Music rules",
            game_data='{"test": "data"}',
        )

    assert result["was_successful"] is False
    assert result["result_details"] == "Agent processing error"
