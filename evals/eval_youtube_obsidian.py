#!/usr/bin/env python3
import json
import os
import sys

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


def main():
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
