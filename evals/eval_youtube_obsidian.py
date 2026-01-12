#!/usr/bin/env python3
import argparse
import json
import logging
import os
import subprocess
import sys
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

    # Build subprocess command
    command = ["uv", "run", "scripts/get_youtube_data.py", video_url, "", ""]

    # Get project root for working directory
    project_root = str(Path(__file__).parent.parent.parent)

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


def main():
    """Run the youtube-obsidian skill evaluation.

    Parses command-line arguments and executes evaluation tests.

    Args:
        --video-url: YouTube video URL to evaluate (required)
        --vault-path: Output directory for obsidian notes (default: ./output/)
        --verbose: Enable debug logging (default: False)

    Returns:
        int: Exit code (0 for success, 1 for test failures)
    """
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

    # Print agent execution results
    if agent_success:
        print("\n✅ Agent execution succeeded")
        if args.verbose:
            print(f"Logs:\n{agent_logs}")
    else:
        print(f"\n❌ Agent execution failed: {agent_error}")
        if args.verbose and agent_logs:
            print(f"Logs:\n{agent_logs}")

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
    print("=" * 60)

    if all_passed == all_total:
        print("\n✅ All evaluation tests passed!")
        return 0
    else:
        print(f"\n❌ {all_total - all_passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
