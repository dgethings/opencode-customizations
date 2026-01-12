---
stepsCompleted: ['step-01-validate-prerequisites', 'step-02-design-epics', 'step-03-create-stories', 'step-04-final-validation']
inputDocuments: ['/Users/dgethings/git/opencode-customizations/_bmad-output/planning-artifacts/prd.md', '/Users/dgethings/git/opencode-customizations/_bmad-output/planning-artifacts/architecture.md']
validationStatus: 'PASSED'
validationDate: '2026-01-12'
---

# opencode-customizations - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for opencode-customizations, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

**Eval Execution:**
- FR1: Developer can run eval for youtube-obsidian skill via CLI command
- FR2: Developer can specify YouTube video URL as input to eval
- FR3: Developer can configure VAULT_PATH environment variable for test output directory

**Agent Execution:**
- FR4: Eval system can execute youtube-obsidian skill through opencode agent
- FR5: Eval system can pass YouTube video URL to agent skill execution
- FR6: Eval system can retrieve output created by agent skill execution

**Behavior Validation:**
- FR7: Eval system can parse agent usage logs to identify executed scripts
- FR8: Eval system can verify agent used get_youtube_data.py script for metadata extraction
- FR9: Eval system can verify agent did not use web search for metadata
- FR10: Eval system can verify agent used internal write tool for note creation
- FR11: Eval system can verify agent wrote note to path specified by VAULT_PATH environment variable

**Output Validation:**
- FR12: Eval system can detect if obsidian note file was created
- FR13: Eval system can display path of created obsidian note
- FR14: Eval system can display content of created obsidian note
- FR15: Eval system can indicate pass/fail status based on validation results

**Test Case Management:**
- FR16: Eval system can load golden test cases from test_cases.json file
- FR17: Eval system can use public domain YouTube video with transcript from golden test cases

**Logging & Debugging:**
- FR18: Eval system can display error message when agent execution fails
- FR19: Eval system can display error message when script usage validation fails
- FR20: Eval system can display error message when output creation validation fails

### NonFunctional Requirements

**Performance:**
- NFR-1: Eval completes execution within 1-2 minutes for youtube-obsidian skill test case
- NFR-2: Eval execution time exceeding 5 minutes indicates system failure (likely LLM provider constraints or downtime)

**Reliability:**
- NFR-3: Eval system automatically retries on failure, up to 3 consecutive attempts
- NFR-4: Eval system stops retrying if same error occurs 3 consecutive times and reports failure to developer
- NFR-5: Eval system has <1% failure rate (system errors, not skill failures)
- NFR-6: False positive rate (passing agents that should fail) is below 5%
- NFR-7: False negative rate (failing agents that should pass) is below 5%

### Additional Requirements

**Technical Constraints:**
- Python-only implementation for MVP
- Use `uv` as package manager (consistent with existing opencode-customizations setup)
- Integration with DSPy or similar Python evaluation frameworks (deferred to Phase 2 for MVP)
- Eval system itself is a repo-level tool (not a pip-installable package)
- Skills include their own eval scripts in the `evals/` directory
- Dependencies managed via project-level pyproject.toml or requirements.txt
- CLI command to run eval: `uv run evals/eval_youtube_obsidian.py`

**MVP Scope Limitations:**
- No automated obsidian note structure validation (manual review only)
- No retry logic for failed evals
- No checkpointing and resumability
- Hardcoded eval parameters (not configurable)
- Support only youtube-obsidian skill for MVP

**Observability Requirements:**
- Full agent execution logs (DEBUG mode)
- Tool usage tracking (which scripts/tools were called)
- Intermediate state checkpoints for resumability (Phase 2)
- Stack traces and error context for system failures

**Domain-Specific Requirements:**
- Representative test cases for validity
- Bias prevention in evaluation criteria
- Score validation against ground truth
- Tolerance for non-deterministic agent behavior
- Edge case coverage in test cases
- Acceptance of different valid agent implementation approaches

**Architecture Note:**
The Architecture document appears incomplete (only contains frontmatter). Technical implementation details such as API contracts, data models, and infrastructure requirements were not available for extraction.

### FR Coverage Map

FR1: Epic 1 - Run eval via CLI command
FR2: Epic 3 - Specify YouTube URL as input
FR3: Epic 3 - Configure VAULT_PATH environment variable
FR4: Epic 1 - Execute youtube-obsidian skill through agent
FR5: Epic 1 - Pass YouTube video URL to agent
FR6: Epic 1 - Retrieve output from agent execution
FR7: Epic 2 - Parse agent logs for executed scripts
FR8: Epic 2 - Verify agent used get_youtube_data.py
FR9: Epic 2 - Verify agent did not use web search
FR10: Epic 2 - Verify agent used internal write tool
FR11: Epic 2 - Verify note written to VAULT_PATH
FR12: Epic 1 - Detect if obsidian note file was created
FR13: Epic 3 - Display path of created note
FR14: Epic 3 - Display content of created note
FR15: Epic 1 - Indicate pass/fail status
FR16: Epic 3 - Load golden test cases from test_cases.json
FR17: Epic 3 - Use public domain video from test cases
FR18: Epic 1 - Display error message when agent execution fails
FR19: Epic 2 - Display error message when script usage validation fails
FR20: Epic 1 - Display error message when output creation validation fails

NFR-1: Epic 4 - Complete within 1-2 minutes
NFR-2: Epic 4 - Timeout at 5 minutes indicates failure
NFR-3: Epic 4 - Auto-retry on failure (up to 3 attempts)
NFR-4: Epic 4 - Stop retrying after 3 consecutive errors
NFR-5: Epic 4 - <1% system failure rate
NFR-6: Epic 5 - False positive rate <5%
NFR-7: Epic 5 - False negative rate <5%

## Epic List

### Epic 1: Basic Eval Execution
Dave can execute the youtube-obsidian eval and see a pass/fail result with basic error messages.
**FRs covered:** FR1, FR4, FR5, FR6, FR12, FR15, FR18, FR20

### Epic 2: Agent Behavior Validation
Dave can verify that the agent used the correct tools (get_youtube_data.py script, internal write tool) and did not use web search.
**FRs covered:** FR7, FR8, FR9, FR10, FR11, FR19

### Epic 3: Test Case Management & Enhanced Output
Dave can run multiple test cases, view detailed output content, and get comprehensive validation results.
**FRs covered:** FR2, FR3, FR13, FR14, FR16, FR17

### Epic 4: Reliability & Performance Optimization
The eval system is reliable (auto-retry, <1% failure rate) and performs within acceptable time limits.
**FRs covered:** NFR-1, NFR-2, NFR-3, NFR-4, NFR-5

### Epic 5: Accuracy & Scoring
Eval scores accurately reflect agent performance with minimal false positives/negatives.
**FRs covered:** NFR-6, NFR-7

## Epic 1: Basic Eval Execution

Dave can execute the youtube-obsidian eval and see a pass/fail result with basic error messages.

### Story 1.1: CLI Entry Point

As a developer,
I want a CLI command that launches the eval system,
So that I can easily run evaluations for the youtube-obsidian skill from the terminal.

**Acceptance Criteria:**

**Given** I have the project checked out and dependencies installed via `uv`
**When** I run `uv run evals/eval_youtube_obsidian.py` from the project root
**Then** the CLI parses successfully without errors
**And** the system accepts a `--video-url` argument for the YouTube video URL
**And** the system accepts a `--vault-path` argument for the output directory (defaults to "./output/")
**And** the system accepts a `--verbose` flag to enable DEBUG logging (defaults to False)
**And** a help message is displayed when I run with `--help` showing all available options

**Given** I provide an invalid argument to the CLI
**When** I run the command
**Then** the system displays a clear error message about the invalid argument
**And** the system exits with a non-zero status code

**Given** I omit required arguments
**When** I run the command without `--video-url`
**Then** the system displays an error message indicating `--video-url` is required
**And** the system exits with a non-zero status code

### Story 1.2: Agent Execution

As a developer,
I want the eval system to execute the youtube-obsidian skill through the opencode agent,
So that I can test whether the agent properly uses the skill to create obsidian notes.

**Acceptance Criteria:**

**Given** I have a valid YouTube video URL
**When** the eval system executes the youtube-obsidian skill through opencode agent
**Then** the agent receives the video URL as input
**And** the agent executes the skill using the skill's defined tools
**And** the system captures the agent's execution logs
**And** the system waits for agent execution to complete

**Given** the VAULT_PATH environment variable is set
**When** the agent skill executes
**Then** the agent has access to the VAULT_PATH environment variable
**And** the VAULT_PATH value is accessible to the skill for writing output

**Given** agent execution completes successfully
**When** the eval system retrieves the output
**Then** the system can access any files created by the agent
**And** the system records the execution status

**Given** agent execution fails (timeout or error)
**When** the failure is detected
**Then** the system records the failure reason
**And** no retry attempt is made (MVP constraint)

### Story 1.3: Output Detection & Pass/Fail

As a developer,
I want the eval system to detect whether an obsidian note was created and determine pass/fail status,
So that I can quickly understand if the agent execution was successful.

**Acceptance Criteria:**

**Given** agent execution has completed
**When** the eval system checks for the obsidian note file
**Then** the system looks for markdown files in the VAULT_PATH directory
**And** the system identifies if at least one .md file was created
**And** the system records whether the output file exists

**Given** the agent created an obsidian note file
**When** the eval system determines pass/fail status
**Then** the system displays "PASS ✓" status
**And** the system displays the path to the created note file

**Given** the agent did not create an obsidian note file
**When** the eval system determines pass/fail status
**Then** the system displays "FAIL ✗" status
**And** the system displays "No obsidian note file was created"
**And** the system displays the VAULT_PATH that was checked

**Given** the eval has completed (pass or fail)
**When** the system displays the final result
**Then** the system shows the overall eval status
**And** the system displays a simple pass/fail indicator
**And** the system shows the path where output was expected (VAULT_PATH)

### Story 1.4: Basic Error Handling

As a developer,
I want clear error messages when the eval system fails,
So that I can quickly understand what went wrong and how to fix it.

**Acceptance Criteria:**

**Given** agent execution fails (timeout or exception)
**When** the eval system detects the failure
**Then** the system displays "Eval System Error: Agent execution failed"
**And** the system displays the error type (e.g., TimeoutException, ValueError)
**And** the system displays the error message
**And** the system sets the overall eval status to "FAILED"

**Given** output validation fails (note file not found)
**When** the eval system detects the validation failure
**Then** the system displays "Validation Error: Obsidian note not created"
**And** the system displays the expected output location (VAULT_PATH)
**And** the system sets the overall eval status to "FAIL"

**Given** an unexpected system exception occurs
**When** the eval system catches the exception
**Then** the system displays "Eval System Error: Unexpected exception during validation"
**And** the system displays the exception type and message
**And** the system sets the overall eval status to "FAILED (System Error)"

**Given** verbose mode is enabled (`--verbose` flag)
**When** any error occurs
**Then** the system displays the full stack trace in addition to the error message
**And** the system logs detailed debug information

**Given** verbose mode is disabled (default)
**When** any error occurs
**Then** the system displays only the error message without stack trace
**And** the system suggests enabling `--verbose` for more details

## Epic 2: Agent Behavior Validation

Dave can verify that the agent used the correct tools (get_youtube_data.py script, internal write tool) and did not use web search.

### Story 2.1: Agent Log Parsing

As a developer,
I want the eval system to parse the agent's execution logs,
So that I can identify which scripts and tools the agent used during execution.

**Acceptance Criteria:**

**Given** agent execution has completed
**When** the eval system parses the agent's execution logs
**Then** the system reads the log file generated during agent execution
**And** the system searches for tool/script usage patterns in the logs
**And** the system extracts a list of all tools/scripts that were invoked
**And** the system stores the extracted tool/script list for validation

**Given** verbose mode is enabled
**When** the logs are parsed
**Then** the system displays "Parsing agent execution logs..." message
**And** the system shows the raw log lines containing tool usage patterns
**And** the system displays the extracted list of tools/scripts

**Given** the logs contain no tool usage patterns
**When** the parsing completes
**Then** the system records that no tools/scripts were detected
**And** the system logs a warning that tool usage could not be determined

**Given** the logs are missing or unreadable
**When** the system attempts to parse them
**Then** the system displays a warning: "Unable to parse agent logs"
**And** the system continues with validation using available information

### Story 2.2: Script Usage Validation

As a developer,
I want to verify that the agent used the get_youtube_data.py Python script for metadata extraction,
So that I can confirm the agent is using the skill's intended implementation rather than falling back to web search.

**Acceptance Criteria:**

**Given** agent logs have been parsed
**When** the eval system validates script usage
**Then** the system checks if "get_youtube_data.py" appears in the extracted tool/script list
**And** the system records whether the script was found

**Given** the agent used get_youtube_data.py script
**When** the validation completes
**Then** the system displays "✓ Agent used skill script (get_youtube_data.py) for metadata"
**And** the system marks this validation as PASSED
**And** the system includes this check in the overall validation results

**Given** the agent did NOT use get_youtube_data.py script
**When** the validation completes
**Then** the system displays "✗ Agent did NOT use skill script (get_youtube_data.py)"
**And** the system marks this validation as FAILED
**And** the system recommends: "Update SKILL.md to emphasize using the get_youtube_data.py script"

**Given** script usage cannot be determined (logs unavailable)
**When** the validation runs
**Then** the system displays "? Unable to determine script usage"
**And** the system marks this validation as INCONCLUSIVE
**And** the system includes a note suggesting manual review

### Story 2.3: Web Search Detection

As a developer,
I want to verify that the agent did not use web search for metadata,
So that I can ensure the agent is using the skill's dedicated script rather than generic web search.

**Acceptance Criteria:**

**Given** agent logs have been parsed
**When** the eval system checks for web search usage
**Then** the system searches for web search patterns (e.g., "web_search", "search_web", "browser")
**And** the system determines if web search was invoked during agent execution
**And** the system records whether web search was detected

**Given** the agent did NOT use web search
**When** the validation completes
**Then** the system displays "✓ Agent did NOT use web search"
**And** the system marks this validation as PASSED
**And** the system includes this check in the overall validation results

**Given** the agent used web search
**When** the validation completes
**Then** the system displays "✗ Agent used web search (should use get_youtube_data.py)"
**And** the system marks this validation as FAILED
**And** the system recommends: "Update SKILL.md to explicitly instruct agent to use get_youtube_data.py instead of web search"

**Given** web search usage cannot be determined
**When** the validation runs
**Then** the system displays "? Unable to determine web search usage"
**And** the system marks this validation as INCONCLUSIVE
**And** the system includes a note suggesting manual review

### Story 2.4: Internal Write Tool Validation

As a developer,
I want to verify that the agent used the internal write tool and wrote the note to the correct VAULT_PATH,
So that I can confirm the agent is respecting the environment variable and using the correct output mechanism.

**Acceptance Criteria:**

**Given** agent logs have been parsed
**When** the eval system validates internal write tool usage
**Then** the system checks for internal write tool patterns in logs (e.g., "write", "file_write")
**And** the system determines if the internal write tool was invoked
**And** the system records whether internal write tool was found

**Given** the agent used the internal write tool
**When** the validation completes
**Then** the system displays "✓ Agent used internal write tool for note creation"
**And** the system marks this validation as PASSED
**And** the system includes this check in the overall validation results

**Given** the agent did NOT use the internal write tool
**When** the validation completes
**Then** the system displays "✗ Agent did NOT use internal write tool"
**And** the system marks this validation as FAILED
**And** the system recommends: "Update SKILL.md to instruct agent to use internal write tool for creating obsidian notes"

**Given** the agent used the internal write tool
**When** the system validates the output path
**Then** the system checks the log for the path argument passed to the write tool
**And** the system compares the path to the VAULT_PATH environment variable value
**And** the system records whether the path matches VAULT_PATH

**Given** the note was written to the correct VAULT_PATH
**When** the path validation completes
**Then** the system displays "✓ Note written to correct VAULT_PATH ({VAULT_PATH})"
**And** the system marks this validation as PASSED

**Given** the note was written to a different path
**When** the path validation completes
**Then** the system displays "✗ Note written to wrong location ({actual_path} instead of {expected_path})"
**And** the system marks this validation as FAILED
**And** the system recommends: "Update SKILL.md with: 'CRITICAL: The note MUST be written to the path specified by VAULT_PATH environment variable. Do not use hardcoded paths.'"

**Given** path usage cannot be determined from logs
**When** the validation runs
**Then** the system displays "? Unable to verify write path from logs"
**And** the system marks this validation as INCONCLUSIVE
**And** the system includes a note suggesting manual review of the created note location

**Given** any validation fails in this story
**When** the system reports the failure
**Then** the system displays an error message: "Validation Error: Agent behavior validation failed"
**And** the system includes specific details about which validation failed
**And** the system provides actionable recommendations for fixing the issue

## Epic 3: Test Case Management & Enhanced Output

Dave can run multiple test cases, view detailed output content, and get comprehensive validation results.

### Story 3.1: Test Case File Loading

As a developer,
I want the eval system to load golden test cases from a JSON file,
So that I can run multiple test scenarios without specifying them individually each time.

**Acceptance Criteria:**

**Given** a test_cases.json file exists in the evals/ directory
**When** the eval system is invoked
**Then** the system loads the test_cases.json file
**And** the system parses the JSON structure
**And** the system extracts the list of test cases

**Given** the test_cases.json file has the expected structure
**When** the test cases are loaded
**Then** the system validates each test case has required fields (video_url, expected_output_path)
**And** the system creates a list of valid test cases to run
**And** the system displays "Loaded {count} test cases from test_cases.json"

**Given** a specific test case is selected from the loaded test cases
**When** the eval system runs the eval
**Then** the system uses the video URL from the selected test case
**And** the system validates against the expected output path from the test case
**And** the system references the test case ID in the validation results

**Given** the test_cases.json file is missing or invalid JSON
**When** the system attempts to load it
**Then** the system displays an error: "Error: Unable to load test_cases.json"
**And** the system displays the specific JSON parsing error or file not found error
**And** the system falls back to using CLI-provided arguments (if available)
**And** the system exits with a non-zero status code

**Given** the test_cases.json file exists but has missing required fields
**When** the system parses the test cases
**Then** the system displays a warning for each invalid test case
**And** the system skips invalid test cases and continues with valid ones
**And** the system displays "Loaded {count} valid test cases (skipped {invalid_count} invalid)"

**Given** verbose mode is enabled
**When** test cases are loaded
**Then** the system displays the full test case structure for each loaded test case
**And** the system shows which fields were found and validated
**And** the system displays any warnings about skipped test cases

### Story 3.2: Enhanced Output Display

As a developer,
I want to see the path and content of the created obsidian note,
So that I can manually review the note structure and content for correctness.

**Acceptance Criteria:**

**Given** an obsidian note file has been created by the agent
**When** the eval system displays the results
**Then** the system displays the full path to the created note file
**And** the system displays "Created Note:" header
**And** the system shows the file path in an easily copyable format

**Given** the note file exists and is readable
**When** the system displays the note content
**Then** the system reads the entire file content
**And** the system displays the content in a formatted, readable manner
**And** the system preserves markdown formatting (headers, lists, code blocks)
**And** the system displays "---" separator between validation results and note content

**Given** the note content is large (>500 lines)
**When** the system displays the note
**Then** the system displays the first 100 lines
**And** the system displays "..." to indicate truncated content
**And** the system displays a note: "Note truncated - view full file at: {file_path}"

**Given** the note file cannot be read (permission error, corrupted file)
**When** the system attempts to display the content
**Then** the system displays a warning: "Unable to read note file content"
**And** the system displays the error message
**And** the system still displays the file path for manual review
**And** the system does not fail the eval due to this issue

**Given** verbose mode is enabled
**When** displaying note content
**Then** the system displays the total number of lines in the note
**And** the system displays the file size in bytes
**And** the system shows the last modified timestamp

**Given** verbose mode is disabled (default)
**When** displaying note content
**Then** the system displays only the note content without metadata
**And** the system keeps the output concise for easy reading

### Story 3.3: Comprehensive Validation Report

As a developer,
I want to see all validation checks with clear pass/fail indicators and detailed results,
So that I can quickly understand which aspects of the agent's behavior passed or failed.

**Acceptance Criteria:**

**Given** all validations have completed
**When** the eval system displays the final results
**Then** the system displays a "Validation Results:" header
**And** the system lists each validation check on a separate line
**And** each check is preceded by a clear pass/fail/inconclusive indicator (✓, ✗, or ?)

**Given** all validations passed
**When** the validation results are displayed
**Then** the system displays each check with "✓" prefix
**And** the system shows a descriptive message for each passed check
**And** the system displays "Status: PASS ✓" after all checks

**Given** some validations failed
**When** the validation results are displayed
**Then** the system displays failed checks with "✗" prefix
**And** the system shows a clear error message explaining why the check failed
**And** the system displays "Status: FAIL ✗" after all checks
**And** the system displays a "Recommendations:" section with actionable suggestions

**Given** some validations were inconclusive
**When** the validation results are displayed
**Then** the system displays inconclusive checks with "?" prefix
**And** the system shows a message explaining why the result could not be determined
**And** the system includes a note suggesting manual review for those checks

**Given** the eval system has calculated an overall score
**When** the results are displayed
**Then** the system displays "Eval Score: {score}" at the top of the results
**And** the score is displayed as a decimal between 0 and 1
**And** the system displays the score with pass/fail status (PASS if score >= 0.8, FAIL if < 0.8)

**Given** verbose mode is enabled
**When** the validation results are displayed
**Then** the system displays the score calculation breakdown
**And** the system shows which checks contributed to the score
**And** the system displays the weight of each check in the calculation

**Given** recommendations are needed for failed checks
**When** the results are displayed
**Then** the system displays a "Recommendations:" section
**And** each recommendation is numbered and provides specific guidance
**And** recommendations reference the specific validation check they address
**And** recommendations are actionable (e.g., "Update SKILL.md with...")

**Given** no recommendations are needed (all passed)
**When** the results are displayed
**Then** the system displays "Recommendations: No improvements needed"
**And** the system indicates the skill is performing optimally

**Given** the eval ran with a specific YouTube URL
**When** the results are displayed
**Then** the system displays the video URL that was tested
**And** the system displays the VAULT_PATH that was used
**And** the system displays the execution time

## Epic 4: Reliability & Performance Optimization [PHASE 2 - DEFERRED]

The eval system is reliable (auto-retry, <1% failure rate) and performs within acceptable time limits.

**FRs covered:** NFR-1, NFR-2, NFR-3, NFR-4, NFR-5

**Status:** Deferred to Phase 2 (outside MVP scope)
**Reason:** MVP scope constraints specify "No retry logic for failed evals" and "No checkpointing and resumability"

### Story 4.1 [Phase 2]: Execution Time Tracking

As a developer,
I want to see how long each eval takes to execute,
So that I can monitor performance and detect potential issues.

**Acceptance Criteria:**

**Given** an eval is running
**When** the eval starts and completes
**Then** the system records the start time and end time
**And** the system calculates the total execution duration
**And** the system displays "Execution time: {duration}" in the results

**Given** the execution time exceeds 2 minutes
**When** the time is displayed
**Then** the system displays the time in minutes:seconds format
**And** the system notes that this is above the optimal range (1-2 minutes)

**Given** the execution time is within 1-2 minutes
**When** the time is displayed
**Then** the system displays the time in seconds
**And** no warning is displayed

### Story 4.2 [Phase 2]: Timeout Detection

As a developer,
I want the eval system to detect when execution exceeds 5 minutes,
So that I can identify system failures or LLM provider issues.

**Acceptance Criteria:**

**Given** an eval is running
**When** execution time exceeds 5 minutes
**Then** the system detects the timeout
**And** the system terminates the agent execution
**And** the system displays "Error: Execution timeout - exceeded 5 minutes"
**And** the system sets the overall eval status to "FAILED"
**And** the system notes that this may indicate LLM provider constraints or downtime

**Given** timeout is detected
**When** the system reports the failure
**Then** the system records the timeout event for failure rate tracking
**And** the system displays the actual execution time before timeout

### Story 4.3 [Phase 2]: Auto-Retry Logic

As a developer,
I want the eval system to automatically retry on transient failures,
So that I don't have to manually re-run failed evals.

**Acceptance Criteria:**

**Given** an eval fails (timeout, connection error, etc.)
**When** the failure is detected
**Then** the system checks if the error is retryable (e.g., timeout, connection error, rate limit)
**And** the system increments the retry counter
**And** if retry count < 3, the system automatically retries the eval
**And** the system displays "Retrying... (attempt {current}/3)"

**Given** a retry attempt succeeds
**When** the retry completes successfully
**Then** the system displays "Success on attempt {current}"
**And** the system shows the final validation results
**And** the system records that retry was needed

**Given** all 3 retry attempts fail
**When** the last attempt fails
**Then** the system displays "All retry attempts failed"
**And** the system sets the overall eval status to "FAIL"
**And** the system displays the error from each attempt
**And** the system records that retry attempts were exhausted

**Given** the error is not retryable (e.g., invalid input, syntax error)
**When** the error is detected
**Then** the system does not retry
**And** the system displays the error immediately
**And** the system sets the overall eval status to "FAIL"

### Story 4.4 [Phase 2]: Consecutive Error Detection

As a developer,
I want the eval system to stop retrying if the same error occurs 3 consecutive times,
So that I don't waste time on systematic failures.

**Acceptance Criteria:**

**Given** an eval is being retried
**When** the same error occurs 3 consecutive times
**Then** the system detects the consecutive identical errors
**And** the system stops retrying
**And** the system displays "Stopped retrying - same error occurred 3 times"
**And** the system displays the error message
**And** the system sets the overall eval status to "FAIL"

**Given** consecutive errors are detected
**When** the system stops retrying
**Then** the system notes that this is likely a systematic issue (not transient)
**And** the system suggests reviewing the input configuration

**Given** errors differ between attempts
**When** retries continue
**Then** the system continues retrying up to the maximum of 3 attempts
**And** the consecutive error counter resets when a different error occurs

### Story 4.5 [Phase 2]: Failure Rate Tracking

As a developer,
I want to track the eval system's failure rate over time,
So that I can monitor reliability and ensure it stays below 1%.

**Acceptance Criteria:**

**Given** evals are being run
**When** each eval completes (pass or fail)
**Then** the system records the result (pass/fail) with timestamp
**And** the system stores the result in a failure rate log

**Given** I want to check the failure rate
**When** I run the eval with a `--stats` flag
**Then** the system calculates the failure rate over the last N evals (default: last 100)
**And** the system displays "System failure rate: {rate}% (based on {count} recent evals)"

**Given** the failure rate exceeds 1%
**When** the stats are displayed
**Then** the system displays a warning: "WARNING: Failure rate exceeds 1% threshold"
**And** the system suggests reviewing recent errors for patterns

**Given** the failure rate is below 1%
**When** the stats are displayed
**Then** the system displays "Failure rate is within acceptable range (<1%)"
**And** no warning is displayed

**Given** verbose mode is enabled
**When** stats are displayed
**Then** the system shows the breakdown of pass vs. fail counts
**And** the system displays the most recent failure reasons

## Epic 5: Accuracy & Scoring [PHASE 2 - DEFERRED]

Eval scores accurately reflect agent performance with minimal false positives/negatives.

**FRs covered:** NFR-6, NFR-7

**Status:** Deferred to Phase 2 (outside MVP scope)
**Reason:** MVP focuses on basic eval execution, validation, and output. Accuracy tracking and scoring calibration can be added in Phase 2.

### Story 5.1 [Phase 2]: Score Calculation

As a developer,
I want the eval system to calculate a meaningful score based on validation results,
So that I can quantify how well the agent performed.

**Acceptance Criteria:**

**Given** all validation checks have completed
**When** the eval system calculates the score
**Then** the system assigns a weight to each validation check (e.g., script usage: 0.3, no web search: 0.2, correct path: 0.2, output created: 0.3)
**And** the system sums the weighted scores of passed checks
**And** the system produces a final score between 0 and 1

**Given** all validation checks passed
**When** the score is calculated
**Then** the system displays "Eval Score: 1.00" (or 1.0)
**And** the system displays "Status: PASS ✓"

**Given** some validation checks failed
**When** the score is calculated
**Then** the system displays the calculated score (e.g., "Eval Score: 0.65")
**And** the system determines pass/fail based on threshold (default: 0.8)
**And** if score >= 0.8, the system displays "Status: PASS ✓"
**And** if score < 0.8, the system displays "Status: FAIL ✗"

**Given** some checks were inconclusive
**When** the score is calculated
**Then** the system excludes inconclusive checks from the score calculation
**And** the system recalculates weights based only on conclusive checks
**And** the system displays a note: "Score based on {count} conclusive checks (excluded {inconclusive_count} inconclusive)"

**Given** verbose mode is enabled
**When** the score is calculated
**Then** the system displays the score breakdown:
  - "Check X (weight: W.X): passed/failed - contributed +W.X / 0.0 to score"
  - Total: calculated score
**And** the system shows the pass/fail threshold value

### Story 5.2 [Phase 2]: False Positive/Negative Tracking

As a developer,
I want to track false positives and false negatives over time,
So that I can ensure the eval system's accuracy stays below 5% for both metrics.

**Acceptance Criteria:**

**Given** I have a set of golden test cases with known expected outcomes
**When** I run evals on these test cases
**Then** the system records each eval result (actual pass/fail)
**And** the system compares actual results to expected outcomes
**And** the system identifies false positives (should fail but passed) and false negatives (should pass but failed)

**Given** a false positive is detected
**When** the eval completes
**Then** the system records the false positive event
**And** the system logs the test case ID and validation results
**And** the system notes which validation checks incorrectly passed

**Given** a false negative is detected
**When** the eval completes
**Then** the system records the false negative event
**And** the system logs the test case ID and validation results
**And** the system notes which validation checks incorrectly failed

**Given** I want to check accuracy metrics
**When** I run the eval with a `--accuracy` flag
**Then** the system calculates false positive rate: false_positives / total_evals
**And** the system calculates false negative rate: false_negatives / total_evals
**And** the system displays:
  - "False Positive Rate: {rate}%"
  - "False Negative Rate: {rate}%"
  - "Based on: {count} evals with known expected outcomes"

**Given** either rate exceeds 5%
**When** the accuracy metrics are displayed
**Then** the system displays a warning: "WARNING: {False Positive/Negative} rate exceeds 5% threshold"
**And** the system suggests reviewing validation criteria or scoring weights

**Given** both rates are below 5%
**When** the accuracy metrics are displayed
**Then** the system displays "Accuracy metrics are within acceptable range (<5%)"
**And** no warning is displayed

**Given** verbose mode is enabled
**When** accuracy metrics are displayed
**Then** the system shows the breakdown of false positives and false negatives
**And** the system lists the specific test cases that contributed to each
**And** the system displays the validation results for those cases

### Story 5.3 [Phase 2]: Score Calibration

As a developer,
I want to validate that eval scores correlate with actual agent performance,
So that I can trust that passing scores mean the agent will work reliably.

**Acceptance Criteria:**

**Given** I have a set of golden test cases representing various scenarios
**When** I run evals on these test cases
**Then** the system records the scores for each test case
**And** the system compares scores to expected performance (based on manual review)

**Given** I manually review agent outputs and determine correct performance
**When** I record expected outcomes for test cases
**Then** the system accepts manual input for expected pass/fail per test case
**And** the system stores expected outcomes alongside eval scores

**Given** expected outcomes are recorded
**When** I run calibration analysis
**Then** the system calculates the correlation between scores and expected outcomes
**And** the system displays:
  - "High scores (>=0.8) should pass: {count}/{total} ({rate}%)"
  - "Low scores (<0.8) should fail: {count}/{total} ({rate}%)"
**And** the system reports overall calibration quality

**Given** calibration quality is high (>90% correlation)
**When** the analysis completes
**Then** the system displays "Calibration: EXCELLENT - Scores strongly correlate with performance"
**And** the system confirms that passing scores indicate reliable agent behavior

**Given** calibration quality is low (<90% correlation)
**When** the analysis completes
**Then** the system displays "Calibration: NEEDS IMPROVEMENT - Scores don't reliably indicate performance"
**And** the system suggests adjusting scoring weights or validation criteria
**And** the system recommends reviewing which checks are contributing to poor correlation

**Given** calibration analysis shows systematic issues
**When** the analysis completes
**Then** the system identifies which specific validation checks have poor correlation
**And** the system suggests recalibrating weights for those checks
**And** the system provides examples of misaligned scores

**Given** verbose mode is enabled
**When** calibration analysis is displayed
**Then** the system shows the full correlation matrix
**And** the system displays score distributions for pass vs. fail cases
**And** the system suggests optimal threshold adjustments if applicable
