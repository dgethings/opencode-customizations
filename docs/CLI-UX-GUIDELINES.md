# CLI UX Guidelines for Eval System

**Document Version:** 1.0
**Date:** 2026-01-17
**Purpose:** Standardize CLI user experience across all eval commands

---

## Overview

This document defines CLI user experience (UX) guidelines for the eval system to ensure consistency as the tool grows. These guidelines apply to all eval commands and should be followed when implementing new features.

## Core Principles

1. **Clarity First:** Every message should be immediately understandable
2. **Progress Visibility:** Users should always know what's happening
3. **Actionable Errors:** Every error should suggest a specific fix
4. **Consistent Formatting:** Use standard indicators and structures
5. **Verbose Mode:** Optional detailed output for debugging

---

## Standard Indicators

### Pass/Fail/Unknown Status

| Status | Symbol | Description |
|--------|---------|-------------|
| Pass | ✓ | Check or eval passed successfully |
| Fail | ✗ | Check or eval failed |
| Warning | ⚠️ | Non-blocking issue requiring attention |
| Information | ℹ️ | Informational message |
| Unknown/Inconclusive | ? | Result cannot be determined |

### Color Standards (if terminal supports colors)

- **✓ Pass:** Green (`\033[92m`)
- **✗ Fail:** Red (`\033[91m`)
- **⚠️ Warning:** Yellow (`\033[93m`)
- **ℹ️ Info:** Blue (`\033[94m`)
- **? Unknown:** Gray (`\033[90m`)

**Note:** Only use colors if terminal supports them. Detect via environment variables or libraries like `colorama`.

---

## Output Format Standards

### 1. Success Output

**Format:**
```
Eval Score: 0.85
Status: PASS ✓

Validation Results:
✓ Frontmatter contains all required fields
✓ Frontmatter values are correct and properly formatted
✓ All content sections present
✓ Tags relevant and within limits (12/15)
✓ Agent used skill script (get_youtube_data.py) for metadata
✓ Agent did NOT use web search
✓ Note written to correct VAULT_PATH (./output/)
```

**Rules:**
- Score displayed first (0.00 to 1.00)
- Status line with indicator immediately after
- Each validation on separate line with indicator
- Specific details in parentheses when relevant

### 2. Failure Output

**Format:**
```
Eval Score: 0.65
Status: FAIL ✗

Validation Results:
✓ Frontmatter contains all required fields
✓ Frontmatter values are correct and properly formatted
✓ All content sections present
✓ Tags relevant and within limits
✓ Agent used skill script (get_youtube_data.py) for metadata
✓ Agent did NOT use web search
✗ Note written to wrong location (/tmp/output/ instead of ./output/)

Recommendations:
The agent is not respecting the VAULT_PATH environment variable.
Update SKILL.md to emphasize:

"CRITICAL: The note MUST be written to the path specified by VAULT_PATH
environment variable. Do not use hardcoded paths. Use the exact value
from VAULT_PATH."

Consider adding an example showing correct VAULT_PATH usage:
"Example: If VAULT_PATH='./output/', write to: ./output/Video Title.md"
```

**Rules:**
- Show all validations (both passed and failed)
- Failed validations displayed at end
- Provide specific failure details
- Include actionable recommendations section
- Recommendations include specific code/text examples

### 3. System Error Output

**Format:**
```
Eval System Error: Agent execution failed
Status: FAILED

Error Details:
- Error Type: TimeoutException
- Error Message: Agent did not respond within 5 minutes
- Timestamp: 2026-01-17 14:32:15
- Stage: Agent Execution

What Happened:
The eval system encountered a timeout during agent execution.
This may indicate LLM provider issues or network problems.

Logs:
Full debug logs written to: /Users/dgethings/git/opencode-customizations/_bmad-output/eval-logs/2026-01-17_143215_eval.log

Next Steps:
1. Review the error log for full stack trace
2. Check network connectivity
3. Verify LLM provider status
4. Retry the eval

To enable verbose logging, run with --verbose flag.
```

**Rules:**
- Clear error type classification
- Specific error message
- Timestamp included
- Stage identified (which step failed)
- Explanation in plain language
- Log file path always provided
- Specific next steps listed
- Reminder about verbose mode

---

## Error Message Standards

### Error Message Structure

**Template:**
```
[Error Category]: [Specific Error]

[Explanation of what happened]

[Suggested Action]
```

### Common Error Categories

| Category | Example | Recovery Action |
|----------|---------|-----------------|
| **Input Validation** | "Error: Invalid YouTube URL format" | Provide valid URL or run with --help |
| **Configuration** | "Error: YOUTUBE_API_KEY not set" | Set environment variable |
| **Execution** | "Error: Agent execution timed out" | Check network and retry |
| **Validation** | "Validation Error: Obsidian note not created" | Review agent output and skill prompt |
| **System** | "Eval System Error: Unexpected exception" | Run with --verbose and review logs |

### Error Message Best Practices

1. **Be Specific:** Don't say "Error occurred" - say "Error: Invalid YouTube URL"
2. **Provide Context:** Explain what operation was being performed
3. **Suggest Fix:** Always provide at least one actionable step
4. **Include Details:** Show the actual value that caused error when relevant
5. **Verbal Verbs:** Use past tense ("failed", "occurred", "completed")

**Good Example:**
```
Error: test_cases.json not found at evals/test_cases.json

The eval system could not load golden test cases from the expected location.

Fix Options:
1. Create evals/test_cases.json with test case definitions
2. Run eval with --video-url to skip test cases (MVP only)
```

**Bad Example:**
```
Error: Could not load file.
```

---

## Verbose Mode Guidelines

### Verbose Mode Indicators

**When Enabled (--verbose flag):**
- Display detailed progress messages
- Show full stack traces for errors
- Include intermediate values and calculations
- Show all log lines being processed

**When Disabled (default):**
- Show only essential information
- Display error messages without stack traces
- Suggest enabling verbose for debugging

### Verbose Output Format

**Progress Messages:**
```
[INFO] Loading test cases from evals/test_cases.json...
[INFO] Loaded 3 test cases
[INFO] Starting eval for test case: "Standard Watch URL (aqz-KE-bpKQ)"
[INFO] Executing agent with youtube-obsidian skill...
[INFO] Agent execution completed (duration: 45 seconds)
[INFO] Parsing agent usage logs...
[INFO] Extracted tools: ['get_youtube_data.py', 'write_file']
[INFO] Validating agent behavior...
[INFO] Checking output directory: ./output/
[INFO] Created note found: ./output/Big Buck Bunny.md
[INFO] All validations complete
```

**Error Messages (Verbose):**
```
[ERROR] TimeoutException occurred during agent execution
[ERROR] Stack trace:
  File "evals/eval_youtube_obsidian.py", line 87, in run_eval
    agent.execute(skill, video_url)
  File "opencode/agent.py", line 234, in execute
    await_response()
TimeoutException: Agent did not respond within 5 minutes

[INFO] Log file: /Users/dgethings/git/opencode-customizations/_bmad-output/eval-logs/2026-01-17_143215_eval.log
[INFO] Suggestion: Run with --verbose for more details
```

---

## Help Message Standards

### --help Output Format

```
Usage: uv run evals/eval_youtube_obsidian.py [OPTIONS]

Evaluates youtube-obsidian skill performance through opencode agent.

OPTIONS:
  --video-url <URL>       YouTube video URL to test (required)
  --vault-path <PATH>     Output directory for obsidian notes (default: "./output/")
  --verbose                Enable verbose logging with full debug output
  --help                   Display this help message

EXAMPLES:
  # Run eval with specific video URL
  uv run evals/eval_youtube_obsidian.py --video-url "https://www.youtube.com/watch?v=aqz-KE-bpKQ"

  # Run with custom vault path and verbose logging
  uv run evals/eval_youtube_obsidian.py --video-url "https://..." --vault-path "./my-vault/" --verbose

OUTPUT:
  Displays validation results with pass/fail indicators
  Shows created obsidian note content
  Provides recommendations for failures

For detailed output formatting, see: CLI-UX-GUIDELINES.md
```

**Rules:**
- Brief description at top
- Required/optional status clearly indicated
- Default values shown
- Multiple examples provided
- Cross-reference to documentation

---

## Progress Indicators

### Long-Running Operations

For operations taking >2 seconds, show progress:

```
Starting eval execution...
[=====>      ] 40% - Agent executing skill...
[==========> ] 80% - Validating output...
[=============] 100% - Complete
```

**Or for simpler output:**
```
✓ Loading test cases... (done in 0.2s)
✓ Executing agent... (done in 45s)
✓ Validating results... (done in 1.1s)
✓ Generating report... (done in 0.3s)
```

---

## File Display Standards

### Output File Display

**Format:**
```
Created Note: ./output/Big Buck Bunny.md

---
title: Big Buck Bunny
youtube_id: aqz-KE-bpKQ
tags: ["animation", "public domain", "open source"]
---

## Summary

Big Buck Bunny follows the story of three rabbits...

## Notes

- Created by Blender Foundation
- Released as public domain

## Description

Big Buck Bunny tells the story of three...

[Note content truncated - 415 lines total]
Full file: ./output/Big Buck Bunny.md
```

**Rules:**
- Display full file path first
- Show frontmatter with separator
- Show first ~50 lines of content
- Truncate long files with line count indicator
- Always provide full file path for manual review

---

## Cross-Reference Standards

When referencing other documentation:

```
For more information, see:
- PRD: planning_artifacts/prd.md
- Architecture: docs/architecture.md
- Epics: planning_artifacts/epics.md
- Writing Evals: docs/writing-evals-for-new-skills.md (coming in Phase 2)
- CLI UX Guidelines: docs/CLI-UX-GUIDELINES.md
```

---

## Future Enhancements

These guidelines will be enhanced in Phase 2 with:

1. **Interactive Mode:** Confirmations before destructive operations
2. **Configurable Output:** JSON/CSV export options
3. **Progress Bars:** Enhanced visual progress for long operations
4. **Terminal Detection:** Auto-enable colors when supported
5. **Internationalization:** Multi-language support (if needed)

---

## Checklist

When implementing or modifying eval CLI output, verify:

- [ ] Pass/fail indicators use standard symbols (✓/✗/?)
- [ ] Error messages include specific error type
- [ ] Every error provides at least one actionable fix
- [ ] Verbose mode shows stack traces and detailed progress
- [ ] Non-verbose mode is concise (no stack traces)
- [ ] File paths are always complete and copyable
- [ ] Help message includes examples and default values
- [ ] Progress shown for operations >2 seconds
- [ ] Consistent section headers ("Validation Results:", "Recommendations:")
- [ ] Cross-references to relevant documentation

---

**Last Updated:** 2026-01-17
**Maintained By:** Development Team
