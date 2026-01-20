#!/usr/bin/env python3
import argparse
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

# Add project root to sys.path for imports
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


# Default timeout for agent execution (5 minutes per NFR-2)
DEFAULT_TIMEOUT = 300


def test_agent_execution(test_case, vault_path, eval_bag_results):
    """EVAL PHASE: Execute youtube-obsidian agent with given test case.

    Args:
        test_case: Test case dict from test_cases.json
        vault_path: Directory path for obsidian note output
        eval_bag_results: Pytest fixture providing EvalResult storage

    Returns:
        Eval result dict stored in eval_bag for analysis phase
    """
    video_url = test_case["video_url"]
    expected_title = test_case["expected_title"]

    # Prepare environment with VAULT_PATH
    env = os.environ.copy()
    env["VAULT_PATH"] = vault_path

    # Get project root for working directory
    project_root = str(Path(__file__).parent.parent.parent)

    # Build subprocess command to run opencode CLI with agent
    script_path = os.path.join(
        project_root, "skills", "youtube-obsidian", "scripts", "get_youtube_data.py"
    )
    command = [sys.executable, script_path, video_url, "", ""]

    start_time = time.time()
    timeout_occurred = False
    agent_error = None
    exit_code = None
    stdout = None
    stderr = None

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=DEFAULT_TIMEOUT,
            env=env,
            cwd=project_root,
        )
        exit_code = process.returncode
        stdout = process.stdout
        stderr = process.stderr

    except subprocess.TimeoutExpired:
        timeout_occurred = True
        agent_error = "Execution timeout after 5 minutes"
        logging.error(agent_error)
    except Exception as e:
        agent_error = f"Unexpected error: {e}"
        logging.error(agent_error)

    execution_time = time.time() - start_time

    # Check for output file creation
    file_exists = False
    file_path = None
    try:
        md_files = list(Path(vault_path).glob("*.md"))
        if md_files:
            file_exists = True
            file_path = str(max(md_files, key=os.path.getmtime))
    except Exception as e:
        logging.warning(f"Could not check for output file: {e}")

    # Store result in eval_bag
    result = {
        "test_case_id": test_case["id"],
        "test_case_name": test_case["name"],
        "video_url": video_url,
        "execution_success": exit_code == 0 if exit_code is not None else False,
        "timeout_occurred": timeout_occurred,
        "agent_error": agent_error,
        "execution_time": execution_time,
        "file_created": file_exists,
        "file_path": file_path,
        "expected_title": expected_title,
        "tags": test_case.get("tags", []),
    }

    # Store in eval_bag for analysis phase
    pytest_evals.store_eval_result(result, eval_bag_results)

    return result


@pytest.mark.eval_analysis("eval_analysis")
def test_eval_analysis(eval_results):
    """ANALYSIS PHASE: Calculate metrics and determine pass/fail.

    Args:
        eval_results: Pytest fixture providing EvalResult objects

    Returns:
        Final pass/fail determination
    """
    # Collect results
    results = []
    for r in eval_results:
        results.append(r.result)

    if not results:
        print("Error: No eval results found in eval_bag")
        return "FAIL"

    total_cases = len(results)
    successful_executions = sum(1 for r in results if r["execution_success"])
    files_created = sum(1 for r in results if r["file_created"])
    timeouts = sum(1 for r in results if r["timeout_occurred"])

    success_rate = (successful_executions / total_cases * 100) if total_cases > 0 else 0
    file_creation_rate = (files_created / total_cases * 100) if total_cases > 0 else 0

    # Display per-case results
    print("\n" + "=" * 60)
    print("Per-Case Results")
    print("=" * 60)

    for result in results:
        status = (
            "✓ PASS"
            if result["execution_success"] and result["file_created"]
            else "✗ FAIL"
        )
        print(f"\n{status}: {result['test_case_name']} ({result['test_case_id']})")
        print(f"  Video URL: {result['video_url']}")
        print(f"  Execution: {'SUCCESS' if result['execution_success'] else 'FAILED'}")

        if result["timeout_occurred"]:
            print(f"  Timeout: YES (exceeded 5 minutes)")
        elif result["agent_error"]:
            print(f"  Error: {result['agent_error']}")

        print(f"  Output Created: {'YES' if result['file_created'] else 'NO'}")
        if result["file_created"] and result["file_path"]:
            print(f"  Output File: {result['file_path']}")

    # Display metrics summary
    print("\n" + "=" * 60)
    print("Summary Metrics")
    print("=" * 60)
    print(f"  Total Test Cases: {total_cases}")
    print(f"  Successful Executions: {successful_executions} ({success_rate:.1f}%)")
    print(f"  Files Created: {files_created} ({file_creation_rate:.1f}%)")
    print(f"  Timeouts: {timeouts}")

    # Determine overall pass/fail based on 80% threshold
    if success_rate >= 80.0 and file_creation_rate >= 80.0:
        overall_status = "PASS"
        print(f"\n✅ Overall Status: PASS (Success rate: {success_rate:.1f}% >= 80%)")
    else:
        overall_status = "FAIL"
        print(
            f"\n❌ Overall Status: FAIL (Success rate: {success_rate:.1f}% < 80%, "
            f"File creation rate: {file_creation_rate:.1f}%)"
        )

    return overall_status


def main():
    """Main entry point for eval execution with pytest-evals framework."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Evaluate youtube-obsidian skill",
        epilog=(
            "Example: uv run pytest evals/test_youtube_obsidian_eval.py --run-eval "
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
            force=True,
        )

        # Ensure output directory exists
        os.makedirs(args.vault_path, exist_ok=True)

        # Load test cases
        test_cases_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "evals",
            "test_data",
            "test_cases.json",
        )

        with open(test_cases_file, encoding="utf-8") as f:
            test_data = json.load(f)

        test_cases = test_data["test_cases"]

        # Run analysis phase (EVAL phase is automatic via pytest)
        overall_status = test_eval_analysis(test_results=None)

        # Exit with appropriate code
        sys.exit(0 if overall_status == "PASS" else 1)

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
