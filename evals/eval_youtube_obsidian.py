#!/usr/bin/env python3
import argparse
import glob
import json
import logging
import os
import subprocess
import sys
import traceback
from pathlib import Path

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "skills",
        "youtube-obsidian",
        "scripts",
    ),
)

from get_youtube_data import (
    extract_video_id,
    generate_tags,
    sanitize_filename,
)


def load_test_cases():
    """Load test cases from test_cases.json."""
    test_data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "skills",
        "youtube-obsidian",
        "test_data",
    )
    test_cases_file = os.path.join(test_data_dir, "test_cases.json")

    if not os.path.exists(test_cases_file):
        print(f"Warning: {test_cases_file} not found. Using default test cases.")
        return [
            {
                "name": "Standard Watch URL",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "video_id": "dQw4w9WgXcQ",
                "expected_title": (
                    "Rick Astley - Never Gonna Give You Up (Official Music Video)"
                ),
            }
        ]

    with open(test_cases_file, encoding="utf-8") as f:
        return json.load(f)


def evaluate_url_parsing():
    """Evaluate URL parsing accuracy."""
    print("\n=== Evaluating URL Parsing ===")
    test_cases = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/v/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ]

    passed = 0
    total = len(test_cases)

    for url, expected_id in test_cases:
        try:
            result = extract_video_id(url)
            if result == expected_id:
                passed += 1
                print(f"✓ PASS: {url} -> {result}")
            else:
                print(f"✗ FAIL: {url} -> {result} (expected {expected_id})")
        except Exception as e:
            print(f"✗ ERROR: {url} -> {e}")

    print(f"\nURL Parsing: {passed}/{total} tests passed ({passed / total * 100:.1f}%)")
    return passed, total


def evaluate_filename_sanitization():
    """Evaluate filename sanitization."""
    print("\n=== Evaluating Filename Sanitization ===")
    test_cases = [
        ('Test: "File" <Name>', "Test File Name"),
        ("Test/File/Name\\Backslash", "TestFileNameBackslash"),
        ("Test|?*Name", "TestName"),
        ("A" * 150, "A" * 97 + "..."),
        ("", "video"),
    ]

    passed = 0
    total = len(test_cases)

    for input_name, expected in test_cases:
        result = sanitize_filename(input_name)
        if result == expected:
            passed += 1
            print(f"✓ PASS: '{input_name[:30]}...' -> '{result}'")
        else:
            print(
                f"✗ FAIL: '{input_name[:30]}...' -> '{result}' (expected '{expected}')"
            )

    print(
        f"\nFilename Sanitization: {passed}/{total} tests passed "
        f"({passed / total * 100:.1f}%)"
    )
    return passed, total


def evaluate_tag_generation():
    """Evaluate tag generation."""
    print("\n=== Evaluating Tag Generation ===")
    test_cases = [
        {
            "title": "Python Tutorial",
            "description": "Learn Python programming",
            "transcript": "python programming tutorial",
            "youtube_tags": ["python", "coding"],
            "expected_tags": ["python", "coding", "programming", "tutorial"],
        },
        {
            "title": "Machine Learning With Python",
            "description": "Learn ML algorithms",
            "transcript": "machine learning python data",
            "youtube_tags": [],
            "expected_tags": ["machine learning", "data", "python"],
        },
    ]

    passed = 0
    total = len(test_cases)

    for i, case in enumerate(test_cases):
        result = generate_tags(
            case["title"],
            case["description"],
            case["transcript"],
            case["youtube_tags"],
        )

        expected_present = all(tag in result for tag in case["expected_tags"])

        if expected_present and len(result) <= 15:
            passed += 1
            print(f"✓ PASS: Test case {i + 1} - Tags: {result}")
        else:
            print(f"✗ FAIL: Test case {i + 1}")
            print(f"  Expected tags present: {case['expected_tags']}")
            print(f"  Got: {result}")
            print(f"  Expected tags present: {expected_present}")
            print(f"  Tag count within limit: {len(result) <= 15}")

    print(
        f"\nTag Generation: {passed}/{total} tests passed ({passed / total * 100:.1f}%)"
    )
    return passed, total


def evaluate_test_cases():
    """Evaluate using test cases from test_cases.json."""
    print("\n=== Evaluating Test Cases ===")
    test_cases = load_test_cases()

    passed = 0
    total = len(test_cases)

    for case in test_cases:
        try:
            url = case["url"]
            expected_id = case["video_id"]

            result_id = extract_video_id(url)

            if result_id == expected_id:
                passed += 1
                print(f"✓ PASS: {case['name']} - {url}")
            else:
                print(
                    f"✗ FAIL: {case['name']} - Got ID {result_id}, "
                    f"expected {expected_id}"
                )
        except Exception as e:
            print(f"✗ ERROR: {case['name']} - {e}")

    print(f"\nTest Cases: {passed}/{total} tests passed ({passed / total * 100:.1f}%)")
    return passed, total


# Default timeout for agent execution (5 minutes per NFR-2)
DEFAULT_TIMEOUT = 300


def execute_agent(
    video_url: str, vault_path: str, verbose: bool = False
) -> tuple[bool, str, str | None]:
    """Execute youtube-obsidian skill through opencode agent.

    Args:
        video_url: YouTube video URL to process
        vault_path: Directory path for obsidian note output
        verbose: Enable debug logging

    Returns:
        Tuple of (success: bool, logs: str, error: str | None)
    """
    # Prepare environment with VAULT_PATH
    env = os.environ.copy()
    env["VAULT_PATH"] = vault_path

    # Get project root for working directory
    project_root = str(Path(__file__).parent.parent.parent)

    # Build subprocess command
    script_path = os.path.join(
        project_root, "skills", "youtube-obsidian", "scripts", "get_youtube_data.py"
    )
    command = [sys.executable, script_path, video_url, "", ""]

    # Execute subprocess
    try:
        if verbose:
            logging.debug(f"Subprocess command: {command}")
            logging.debug(f"VAULT_PATH set to: {vault_path}")

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=DEFAULT_TIMEOUT,
            env=env,
            cwd=project_root,
        )

        if verbose:
            logging.debug(f"Agent stdout: {process.stdout}")
            logging.debug(f"Agent stderr: {process.stderr}")

        if process.returncode == 0:
            logging.info("Agent execution completed successfully")
            return True, process.stdout, None
        else:
            logging.error(
                f"Agent execution failed with returncode {process.returncode}"
            )
            return False, process.stdout, process.stderr

    except subprocess.TimeoutExpired:
        error = "Execution timeout after 5 minutes"
        logging.error(error)
        return False, "", error
    except Exception as e:
        error = f"Unexpected error: {e}"
        logging.error(error)
        return False, "", error


def check_output_file(
    vault_path: str, verbose: bool = False
) -> tuple[bool, str | None]:
    """Check for obsidian note file creation in VAULT_PATH directory.

    Args:
        vault_path: Directory path to check for .md files
        verbose: Enable debug logging

    Returns:
        Tuple of (file_exists: bool, file_path: str | None)
    """
    logging.info(f"Checking for obsidian note in {vault_path}")

    # Use glob to find all .md files in vault_path
    md_files = glob.glob(os.path.join(vault_path, "*.md"))

    if verbose:
        logging.debug(f"Found .md files: {md_files}")

    if not md_files:
        if verbose:
            logging.debug("No .md files found in vault_path")
        return False, None

    # Return most recent file based on modification time
    most_recent_file = max(md_files, key=os.path.getmtime)

    if verbose:
        logging.debug(f"Most recent file: {most_recent_file}")

    return True, most_recent_file


def determine_pass_fail(
    file_exists: bool, file_path: str | None, vault_path: str
) -> str:
    """Determine and display pass/fail status based on output detection.

    Args:
        file_exists: Whether output file was detected
        file_path: Path to detected file (if exists)
        vault_path: Directory path checked for output

    Returns:
        Pass/fail status: "PASS" or "FAIL"
    """
    print("\n" + "=" * 60)
    print("Output Detection Results")
    print("=" * 60)

    if file_exists and file_path:
        print("\nPASS ✓")
        print(f"Created Note: {file_path}")
        logging.info(f"Obsidian note detected: {file_path}")
        return "PASS"
    else:
        print("\nFAIL ✗")
        print("No obsidian note file was created")
        print(f"Checked directory: {vault_path}")
        logging.warning("No obsidian note file was created")
        return "FAIL"


def main():
    """Main entry point for eval execution with error handling."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Evaluate youtube-obsidian skill",
        epilog=(
            "Example: uv run evals/eval_youtube_obsidian.py "
            "--video-url https://www.youtube.com/watch?v=VIDEO_ID"
        ),
    )
    parser.add_argument(
        "--video-url", type=str, required=True, help="YouTube video URL to evaluate"
    )
    parser.add_argument(
        "--vault-path",
        type=str,
        default="./output/",
        help="Directory path for obsidian note output (default: ./output/)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Enable DEBUG logging (default: False)",
    )
    args = parser.parse_args()

    try:
        # Configure logging
        log_level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format="[%(levelname)s] %(message)s",
            force=True,  # Override any existing logging configuration
        )

        # Execute agent
        logging.info(f"Executing agent with video URL: {args.video_url}")
        agent_success, agent_logs, agent_error = execute_agent(
            args.video_url, args.vault_path, args.verbose
        )

        # Check for agent execution failure
        if not agent_success:
            print("Eval System Error: Agent execution failed")
            if "timeout" in str(agent_error).lower():
                print("Error Type: subprocess.TimeoutExpired")
            else:
                print("Error Type: Exception")
            print(f"Error Message: {agent_error}")
            if not args.verbose:
                print("Run with --verbose for more details")
            sys.exit(1)

        # Print agent execution results
        if agent_success:
            print("\n✅ Agent execution succeeded")
            if args.verbose:
                print(f"Logs:\n{agent_logs}")

        # Check for output file (Story 1.3)
        file_exists, file_path = check_output_file(args.vault_path, args.verbose)

        # Determine and display pass/fail status (Story 1.3)
        eval_status = determine_pass_fail(file_exists, file_path, args.vault_path)

        # Check for output validation failure
        if eval_status == "FAIL":
            print("Validation Error: Obsidian note not created")
            print(f"Checked directory: {args.vault_path}")
            if not args.verbose:
                print("Run with --verbose for more details")
            sys.exit(1)

        # Run evaluation tests
        print("=" * 60)
        print("YouTube-Obsidian Skill Evaluation")
        print("=" * 60)

        all_passed = 0
        all_total = 0

        passed, total = evaluate_url_parsing()
        all_passed += passed
        all_total += total

        passed, total = evaluate_filename_sanitization()
        all_passed += passed
        all_total += total

        passed, total = evaluate_tag_generation()
        all_passed += passed
        all_total += total

        passed, total = evaluate_test_cases()
        all_passed += passed
        all_total += total

        print("\n" + "=" * 60)
        print(
            f"Overall Results: {all_passed}/{all_total} tests passed "
            f"({all_passed / all_total * 100:.1f}%)"
        )
        print(f"Output Detection Status: {eval_status}")
        print("=" * 60)

        # Success
        if all_passed == all_total:
            print("\n✅ All evaluation tests passed!")
            sys.exit(0)
        else:
            print(f"\n❌ {all_total - all_passed} test(s) failed.")
            sys.exit(1)

    except Exception as e:
        print("Eval System Error: Unexpected exception during validation")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        if args.verbose:
            traceback.print_exc()
        else:
            print("Run with --verbose for more details")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
