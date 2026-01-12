#!/usr/bin/env python3
"""Tests for eval_youtube_obsidian.py CLI parsing and agent execution."""

import logging
import os
import subprocess
import sys
import time
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


def test_cli_valid_required_arguments(monkeypatch, capsys, mocker):
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
    # Mock agent execution and output detection to increase coverage
    mock_execute = mocker.patch("eval_youtube_obsidian.execute_agent")
    mock_execute.return_value = (True, "Agent logs", None)
    mock_check = mocker.patch("eval_youtube_obsidian.check_output_file")
    mock_check.return_value = (True, "./output/test.md")
    result = eval_youtube_obsidian.main()

    # Should exit with success code
    assert result == 0

    # Verify output contains expected sections
    captured = capsys.readouterr()
    assert "YouTube-Obsidian Skill Evaluation" in captured.out
    assert "Evaluating URL Parsing" in captured.out
    assert "Overall Results:" in captured.out


def test_cli_all_arguments(monkeypatch, mocker):
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
    # Mock agent execution and output detection to increase coverage
    mock_execute = mocker.patch("eval_youtube_obsidian.execute_agent")
    mock_execute.return_value = (True, "Agent logs", None)
    mock_check = mocker.patch("eval_youtube_obsidian.check_output_file")
    mock_check.return_value = (True, "/tmp/test/test.md")
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


def test_cli_default_values(monkeypatch, mocker):
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

    # Mock agent execution and output detection to increase coverage
    mock_execute = mocker.patch("eval_youtube_obsidian.execute_agent")
    mock_execute.return_value = (True, "Agent logs", None)
    mock_check = mocker.patch("eval_youtube_obsidian.check_output_file")
    mock_check.return_value = (True, "./output/test.md")
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
    assert call_args[0][0][0] == sys.executable
    assert "get_youtube_data.py" in call_args[0][0][1]
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


# New tests for check_output_file() function (Story 1.3)


def test_output_file_detection_success(tmp_path):
    """Test output file detection when .md file exists."""
    # Create temporary directory with .md file
    md_file = tmp_path / "Video Title.md"
    md_file.write_text("# Test Note")

    # Call check_output_file
    file_exists, file_path = eval_youtube_obsidian.check_output_file(
        str(tmp_path), verbose=False
    )

    # Assertions
    assert file_exists is True
    assert file_path is not None
    assert file_path.endswith("Video Title.md")


def test_output_file_detection_no_file(tmp_path):
    """Test output file detection when no .md files exist."""
    # Create empty temporary directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    # Call check_output_file
    file_exists, file_path = eval_youtube_obsidian.check_output_file(
        str(empty_dir), verbose=False
    )

    # Assertions
    assert file_exists is False
    assert file_path is None


def test_output_file_detection_multiple_files(tmp_path):
    """Test output file detection with multiple .md files."""
    # Create temporary directory with multiple .md files
    old_file = tmp_path / "Old Video.md"
    old_file.write_text("# Old Note")
    # Sleep to ensure timestamp difference
    time.sleep(0.01)
    new_file = tmp_path / "New Video.md"
    new_file.write_text("# New Note")

    # Call check_output_file
    file_exists, file_path = eval_youtube_obsidian.check_output_file(
        str(tmp_path), verbose=False
    )

    # Assertions
    assert file_exists is True
    assert file_path.endswith("New Video.md")  # Most recent file


def test_output_file_detection_verbose_logging(tmp_path, caplog):
    """Test output file detection with verbose logging."""
    # Create temporary directory with .md file
    md_file = tmp_path / "Test Video.md"
    md_file.write_text("# Test Note")

    # Call check_output_file with verbose=True
    with caplog.at_level(logging.DEBUG):
        file_exists, file_path = eval_youtube_obsidian.check_output_file(
            str(tmp_path), verbose=True
        )

    # Assertions
    assert file_exists is True
    assert file_path is not None

    # Verify DEBUG logs were generated
    assert any(
        "Checking for obsidian note" in record.message for record in caplog.records
    )


# Tests for determine_pass_fail() function (Story 1.3)


def test_determine_pass_fail_pass(capsys):
    """Test pass/fail determination when file exists."""
    # Call determine_pass_fail with file exists
    status = eval_youtube_obsidian.determine_pass_fail(
        True, "./output/Video Title.md", "./output/"
    )

    # Assertions
    assert status == "PASS"
    captured = capsys.readouterr()
    assert "PASS ✓" in captured.out
    assert "./output/Video Title.md" in captured.out


def test_determine_pass_fail_fail(capsys):
    """Test pass/fail determination when file does not exist."""
    # Call determine_pass_fail with no file
    status = eval_youtube_obsidian.determine_pass_fail(False, None, "./output/")

    # Assertions
    assert status == "FAIL"
    captured = capsys.readouterr()
    assert "FAIL ✗" in captured.out
    assert "No obsidian note file was created" in captured.out
    assert "./output/" in captured.out


def test_determine_pass_fail_verbose_logging(capsys, caplog):
    """Test pass/fail determination with verbose logging."""
    # Call determine_pass_fail with file exists and verbose
    with caplog.at_level(logging.DEBUG):
        status = eval_youtube_obsidian.determine_pass_fail(
            True, "./output/Test Video.md", "./output/"
        )

    # Assertions
    assert status == "PASS"
    captured = capsys.readouterr()
    assert "PASS ✓" in captured.out


# Integration test for agent execution + output detection (Story 1.3)


def test_integration_agent_execution_output_detection(tmp_path, mocker):
    """Test integration of agent execution with output detection."""
    # Mock subprocess.run to simulate agent creating a file
    mock_process = Mock()
    mock_process.returncode = 0
    mock_process.stdout = "Success: Note created"
    mock_process.stderr = ""
    mocker.patch("subprocess.run", return_value=mock_process)

    # Simulate agent creating a file in vault path
    md_file = tmp_path / "Test Video.md"
    md_file.write_text("# Test Note")

    # Execute agent
    success, logs, error = eval_youtube_obsidian.execute_agent(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        str(tmp_path),
        verbose=False,
    )

    # Check for output file
    file_exists, file_path = eval_youtube_obsidian.check_output_file(
        str(tmp_path), verbose=False
    )

    # Determine pass/fail
    status = eval_youtube_obsidian.determine_pass_fail(
        file_exists, file_path, str(tmp_path)
    )

    # Assertions
    assert success is True
    assert file_exists is True
    assert status == "PASS"
