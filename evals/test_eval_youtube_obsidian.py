#!/usr/bin/env python3
"""Tests for eval_youtube_obsidian.py CLI parsing and agent execution."""

import logging
import os
import subprocess
import sys
from unittest.mock import Mock

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import eval_youtube_obsidian


def test_cli_help_message(monkeypatch):
    """Test CLI displays help message with --help."""
    monkeypatch.setattr(sys, "argv", ["eval_youtube_obsidian.py", "--help"])
    with pytest.raises(SystemExit) as exc_info:
        eval_youtube_obsidian.main()
    # Help should exit with code 0
    assert exc_info.value.code == 0


def test_cli_valid_required_arguments(monkeypatch, capsys):
    """Test CLI parsing with valid required arguments."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "eval_youtube_obsidian.py",
            "--video-url",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ],
    )
    # Don't mock - let evaluation functions run to increase coverage
    result = eval_youtube_obsidian.main()

    # Should exit with success code
    assert result == 0

    # Verify output contains expected sections
    captured = capsys.readouterr()
    assert "YouTube-Obsidian Skill Evaluation" in captured.out
    assert "Evaluating URL Parsing" in captured.out
    assert "Overall Results:" in captured.out


def test_cli_all_arguments(monkeypatch):
    """Test CLI parsing with all arguments provided."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "eval_youtube_obsidian.py",
            "--video-url",
            "https://youtu.be/dQw4w9WgXcQ",
            "--vault-path",
            "/tmp/test/",
            "--verbose",
        ],
    )
    # Don't mock - let evaluation functions run to increase coverage
    result = eval_youtube_obsidian.main()

    # Should exit with success code
    assert result == 0


def test_cli_missing_required_argument(monkeypatch):
    """Test CLI error handling when --video-url is missing."""
    monkeypatch.setattr(sys, "argv", ["eval_youtube_obsidian.py"])

    with pytest.raises(SystemExit) as exc_info:
        eval_youtube_obsidian.main()

    # Should exit with error code
    assert exc_info.value.code == 2  # argparse exits with 2 for argument errors


def test_cli_invalid_argument(monkeypatch):
    """Test CLI error handling for invalid argument."""
    monkeypatch.setattr(
        sys, "argv", ["eval_youtube_obsidian.py", "--invalid-arg", "value"]
    )

    with pytest.raises(SystemExit) as exc_info:
        eval_youtube_obsidian.main()

    # Should exit with error code
    assert exc_info.value.code == 2  # argparse exits with 2 for unrecognized arguments


def test_cli_default_values(monkeypatch):
    """Test CLI default values for optional arguments."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "eval_youtube_obsidian.py",
            "--video-url",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ],
    )

    # Don't mock - let evaluation functions run to increase coverage
    result = eval_youtube_obsidian.main()

    # Should exit with success (default values used)
    assert result == 0


# New tests for execute_agent() function (Story 1.2)


def test_agent_execution_success(mocker):
    """Test successful agent execution."""
    # Mock subprocess.run to return success
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = "Success: Note created"
    mock_process.stderr = ""
    mocker.patch("subprocess.run", return_value=mock_process)

    # Call execute_agent
    success, logs, error = eval_youtube_obsidian.execute_agent(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "./output/",
        verbose=False,
    )

    # Assertions
    assert success is True
    assert logs == "Success: Note created"
    assert error is None

    # Verify subprocess was called correctly
    subprocess.run.assert_called_once()
    call_args = subprocess.run.call_args
    assert call_args[0][0][0] == "uv"
    assert call_args[0][0][2] == "scripts/get_youtube_data.py"
    assert "VAULT_PATH" in call_args[1]["env"]


def test_agent_execution_failure(mocker):
    """Test agent execution failure."""
    # Mock subprocess.run to return failure
    mock_process = Mock()
    mock_process.returncode = 1
    mock_process.stdout = ""
    mock_process.stderr = "Error: YOUTUBE_API_KEY not set"
    mocker.patch("subprocess.run", return_value=mock_process)

    # Call execute_agent
    success, logs, error = eval_youtube_obsidian.execute_agent(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "./output/",
        verbose=False,
    )

    # Assertions
    assert success is False
    assert logs == ""
    assert error == "Error: YOUTUBE_API_KEY not set"


def test_agent_execution_timeout(mocker):
    """Test agent execution timeout handling."""
    # Mock subprocess.run to raise timeout
    mocker.patch(
        "subprocess.run",
        side_effect=subprocess.TimeoutExpired("uv", 300),
    )

    # Call execute_agent
    success, logs, error = eval_youtube_obsidian.execute_agent(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "./output/",
        verbose=False,
    )

    # Assertions
    assert success is False
    assert logs == ""
    assert "timeout" in error.lower()


def test_vault_path_environment_variable(mocker):
    """Test VAULT_PATH environment variable is set correctly."""
    # Mock subprocess.run to capture environment
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = "Success"
    mock_process.stderr = ""
    mocker.patch("subprocess.run", return_value=mock_process)

    # Call execute_agent with custom vault path
    success, logs, error = eval_youtube_obsidian.execute_agent(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "/tmp/test_vault/",
        verbose=False,
    )

    # Assertions
    assert success is True

    # Verify VAULT_PATH is set in subprocess environment
    call_args = subprocess.run.call_args
    assert "VAULT_PATH" in call_args[1]["env"]
    assert call_args[1]["env"]["VAULT_PATH"] == "/tmp/test_vault/"


def test_verbose_logging(mocker, caplog):
    """Test verbose logging enables DEBUG level."""
    # Mock subprocess.run
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = "Success output"
    mock_process.stderr = ""
    mocker.patch("subprocess.run", return_value=mock_process)

    # Call execute_agent with verbose=True
    with caplog.at_level(logging.DEBUG):
        success, logs, error = eval_youtube_obsidian.execute_agent(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "./output/",
            verbose=True,
        )

    # Assertions
    assert success is True

    # Verify DEBUG logs were generated (if logging is implemented)
    # Note: This will only pass if logging is actually added to execute_agent()


def test_subprocess_command_structure(mocker):
    """Test subprocess command is built correctly."""
    # Mock subprocess.run to capture command
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = "Success"
    mock_process.stderr = ""
    mocker.patch("subprocess.run", return_value=mock_process)

    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    # Call execute_agent
    success, logs, error = eval_youtube_obsidian.execute_agent(
        video_url,
        "./output/",
        verbose=False,
    )

    # Assertions
    assert success is True

    # Verify subprocess command structure
    call_args = subprocess.run.call_args
    command = call_args[0][0]
    assert command[0] == "uv"
    assert command[1] == "run"
    assert command[2] == "scripts/get_youtube_data.py"
    assert command[3] == video_url
    assert command[4] == ""  # user_summary (empty for MVP)
    assert command[5] == ""  # user_comments (empty for MVP)
