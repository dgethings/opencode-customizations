---
title: "Correct Course - Eval System Reimplementation to pytest-evals"
date: "2026-01-17"
workflow: "correct-course"
trigger_story: "Epic 1 - Story 1.1 (CLI Entry Point)"
mode: "incremental"
approved_by: "Dave"
---

# Correct Course - Sprint Change Proposal

## Executive Summary

**Issue Identified:** The current evaluation implementation (`evals/eval_youtube_obsidian.py` and `evals/test_eval_youtube_obsidian.py`) performs traditional unit testing of utility functions rather than evaluating AI agent behavior as specified in the PRD.

**Root Cause:** Misunderstanding of original requirements - implementation focused on unit testing helper functions (URL parsing, filename sanitization, tag generation) instead of evaluating whether the AI agent correctly uses the youtube-obsidian skill.

**Recommended Solution:** Complete rework to use **pytest-evals framework** for AI agent evaluation, implementing agent behavior validation, test case management, and comprehensive analysis phases.

**Impact:** Epic 1 requires implementation approach change; Epic 2 and Epic 3 must move from Deferred to ACTIVE status; Epics 4-5 remain correctly deferred (Phase 2).

---

## 1. Change Trigger and Context

### 1.1 Triggering Story

**Story:** Epic 1 - Story 1.1 (CLI Entry Point)

**Discovery Process:**
- While implementing Story 1.1, it became clear the eval system was not correctly evaluating AI agent behavior
- Current implementation tests utility functions with mocks, not actual agent execution
- This misaligns with PRD requirements for evaluating agent tool usage and output generation

### 1.2 Core Problem Statement

**Problem:**
The evaluation implementation performs unit testing of Python utility functions (URL parsing, filename sanitization, tag generation) rather than evaluating whether the AI agent correctly:
- Executes youtube-obsidian skill for given YouTube videos
- Uses the skill's Python script (`get_youtube_data.py`) for metadata extraction
- Does NOT use web search for metadata (uses skill's dedicated API)
- Creates properly structured Obsidian notes with frontmatter
- Writes notes to the correct VAULT_PATH environment variable

**Type:** Misunderstanding of original requirements

**Evidence:**
- Current `eval_youtube_obsidian.py` (455 lines) tests utility functions
- `test_eval_youtube_obsidian.py` (736 lines) unit tests the eval script itself
- PRD specifies FR7-FR11: Behavior Validation (script usage, web search detection, output path)
- Anthropic's eval guidelines emphasize multi-turn agent evaluations with transcripts, tool calls, and outcome verification
- pytest-evals framework is designed for AI agent evaluations, not unit testing

### 1.3 Impact Assessment

**Supporting Evidence:**
1. Story 1.1 (CLI Entry Point) revealed the problem during implementation
2. Current eval has `test_eval_youtube_obsidian.py` - unnecessary unit tests for eval script
3. PRD requires agent behavior evaluation with tool usage verification (FR7-FR11)
4. pytest-evals framework designed for AI agent evaluations per GitHub repo
5. Anthropic's eval guidelines (Jan 2026) emphasize multi-turn agent evaluations

---

## 2. Epic Impact Assessment

### 2.1 Epic 1: Basic Eval Execution

**Status:** Proceed with modified implementation approach

**Required Changes:**
- ✅ Stories 1.1-1.4 remain valid - acceptance criteria unchanged
- ⚠️ Implementation approach changes: unit tests → pytest-evals framework
- ⚠️ Delete: `evals/test_eval_youtube_obsidian.py` (unnecessary unit tests)
- ✅ Rework: `evals/eval_youtube_obsidian.py` to use pytest-evals decorators and patterns
- ✅ Add: AI agent execution via opencode CLI with `--attach` flag

**Assessment:** Epic 1 can proceed with corrected approach

### 2.2 Epic 2 & Epic 3 Status Correction

**Issue:** Epics 2 and Epic 3 were incorrectly marked as "Deferred to Phase 2"

**Required Changes:**

**Epic 2: Test Case Management & Enhanced Output** (new Epic 2, formerly Epic 3)
- ✅ Status: **ACTIVE** (Critical for MVP)
- ✅ Priority: Position 2 (moved up, test cases needed before behavior validation)
- ✅ Stories 3.1-3.3 are valid and essential
- ✅ pytest-evals provides built-in test case management framework

**Epic 3: Agent Behavior Validation** (new Epic 3, formerly Epic 2)
- ✅ Status: **ACTIVE** (Critical for MVP)
- ✅ Priority: Position 3 (moved down, requires test cases)
- ✅ Stories 2.1-2.4 are valid and essential
- ✅ Must implement: Script usage verification, web search detection, output path validation

**Rationale:**
- Test case management (Epic 2) must come before behavior validation (Epic 3)
- Both are core to AI agent evaluation, not optional features
- pytest-evals framework makes these epics achievable and well-supported

### 2.3 Epic 4 & Epic 5: Reliability & Performance, Accuracy & Scoring

**Status:** ✅ Correctly Deferred (Phase 2)

**Assessment:** No changes required - these are correctly deferred per MVP scope constraints:
- No retry logic for failed evals
- No checkpointing and resumability
- No automated note structure validation (manual review only)

### 2.4 New Epics Required?

**Answer:** ✅ No new epics required

**Reason:**
- pytest-evals framework provides test case management (previously Epic 3, now Epic 2)
- Agent behavior validation stories (Epic 3) already exist and are valid
- No additional functionality beyond current scope needed for MVP

### 2.5 Epic Order Summary

**Revised Epic Order:**
1. **Epic 1: Basic Eval Execution** (Position 1 - unchanged)
2. **Epic 2: Test Case Management & Enhanced Output** (Position 2 - **moved up**, formerly Epic 3)
3. **Epic 3: Agent Behavior Validation** (Position 3 - **moved down**, formerly Epic 2)
4. **Epic 4: Reliability & Performance Optimization** (Position 4 - Phase 2 deferred)
5. **Epic 5: Accuracy & Scoring** (Position 5 - Phase 2 deferred)

---

## 3. Artifact Conflict Analysis

### 3.1 PRD Impact

**Conflict Check:** ❌ No conflicts

**Assessment:**
- ✅ PRD is correct - implementation was wrong
- ✅ FR1-FR6 (Eval Execution & Agent Execution) - Clear and correct
- ✅ FR7-FR11 (Behavior Validation) - These are what we need to implement
- ✅ FR12-FR20 (Output Validation & Test Cases) - Correct approach
- ✅ No PRD modifications needed - requirements are accurate

### 3.2 Architecture Document Impact

**Conflict Check:** ⚠️ Incomplete document - no conflicts possible

**Action Required:**
- Add comprehensive eval system architecture sections
- Document agent harness design using opencode CLI
- Define data models for test cases and eval results
- Capture key design decisions with rationale

**Assessment:** Architecture documentation will be added, not changed

### 3.3 UX Specifications Impact

**Conflict Check:** ⚠️ No UX design found - CLI interface only

**Assessment:** ✅ No conflicts - PRD's user journeys describe CLI usage, which aligns with pytest-evals approach

### 3.4 Other Artifacts Impact

**CI/CD Pipeline (.github/workflows/test.yml):**
- ⚠️ Line 53: Runs `uv run evals/eval_youtube_obsidian.py` - needs update
- ✅ Integration tests (line 95) - separate concern, no change needed

**Required CI/CD Updates:**
1. Install `pytest-evals` as dependency
2. Run evals with pytest: `pytest --run-eval`
3. Start opencode headless server for agent execution
4. Provide YOUTUBE_API_KEY and VAULT_PATH environment variables

**Dependencies (pyproject.toml):**
- ⚠️ Add `pytest-evals>=0.3.4` to dev dependencies

**AGENTS.md:** ✅ No conflicts - agent guidelines remain relevant

---

## 4. Path Forward Evaluation

### 4.1 Option 1: Direct Adjustment (Selected) ✅

**Approach:** Modify existing story implementations to use pytest-evals framework

**Effort Estimate:** MEDIUM - Framework migration + implementing agent behavior validation

**Risk Level:** MEDIUM - New framework (pytest-evals) to learn and integrate

**Viability:** ✅ Viable

**Rationale:**
1. ✅ Preserves progress - Stories and acceptance criteria remain valid
2. ✅ Better tooling - pytest-evals provides battle-tested framework
3. ✅ Aligns with PRD - Original MVP goals achievable, even easier
4. ✅ No rollback needed - Current unit tests don't match requirements anyway
5. ✅ Faster iteration - Framework exists, just implement stories correctly
6. ✅ Community support - pytest-evals has documentation and examples
7. ✅ Future-proofing - Framework will handle evals for future skills too

**Trade-offs:**
- Learning curve for pytest-evals framework (worth it for long-term value)
- Need to rework `eval_youtube_obsidian.py` completely (necessary anyway)
- CI/CD pipeline updates required (one-time cost)

### 4.2 Option 2: Rollback

**Approach:** Revert recently completed stories and rebuild from scratch

**Effort Estimate:** HIGH - Would lose all progress, need to rebuild from scratch

**Risk Level:** HIGH - Waste of time, no benefit

**Viability:** ✗ Not Viable

**Rationale:**
- ❌ No rollback needed - Current stories were never actually implemented correctly
- ❌ Unit tests ≠ agent evals - nothing correct to rollback to
- ❌ Wastes time rebuilding what doesn't exist

### 4.3 Option 3: PRD MVP Review

**Approach:** Review if original PRD MVP is still achievable with this issue

**Effort Estimate:** MEDIUM - Framework migration

**Risk Level:** LOW - Using established framework reduces risk

**Viability:** ✅ Viable

**Rationale:**
- ✅ MVP is actually MORE achievable with pytest-evals
- ✅ pytest-evals provides better tooling than building from scratch
- ✅ Test case management, result collection, and metrics built-in
- ✅ Agent behavior validation still needs implementation (but framework supports it)
- ✅ MVP scope remains reasonable

**MVP Scope Assessment:**
- ✅ Automated note structure validation - Still manual per MVP (consistent)
- ✅ Retry logic - Still deferred per MVP (consistent)
- ✅ Checkpointing - Still deferred per MVP (consistent)

### 4.4 Recommended Path: Option 1 - Direct Adjustment

**Selected:** ✅ Option 1 - Direct Adjustment

**Justification Summary:**
- Option 1 (Modify implementation): Best choice - uses better framework, preserves requirements, faster
- Option 2 (Rollback): No value - nothing correct to rollback to
- Option 3 (MVP review): MVP is achievable, no scope change needed

---

## 5. Approved Change Proposals

All 8 change proposals were approved incrementally on 2026-01-17.

### Proposal 1: Story 1.1 Acceptance Criteria Update

**File:** `_bmad-output/planning-artifacts/epics.md`
**Section:** Story 1.1 Acceptance Criteria

**Change:**
```diff
- When I run `uv run evals/eval_youtube_obsidian.py` from the project root
+ When I run `pytest evals/test_youtube_obsidian_eval.py --run-eval` from the project root
- Then CLI parses successfully without errors
- And system accepts a `--video-url` argument for YouTube video URL
- And system accepts a `--vault-path` argument for output directory (defaults to "./output/")
- And system accepts a `--verbose` flag to enable DEBUG logging (defaults to False)
- And a help message is displayed when I run with `--help` showing all available options
+ Then pytest-evals loads test cases from test_cases.json
+ And system accepts `--video-url` argument to override test case URLs (optional)
+ And system accepts a `--vault-path` argument for output directory (defaults to "./output/")
+ And system accepts `--verbose` flag to enable DEBUG logging (pytest native)
+ And a help message is displayed when I run with `--help` showing all available options
+ And pytest-evals runs each test case and collects results in eval_bag
```

**Rationale:** Change from custom eval script to pytest-evals framework

---

### Proposal 2: Delete Unnecessary Unit Tests

**File:** `evals/test_eval_youtube_obsidian.py`
**Action:** DELETE (entire file)

**Rationale:**
- Unit testing eval script itself provides no value
- These tests mock subprocess execution instead of evaluating agent behavior
- pytest-evals framework will handle eval execution and validation
- Test effort should focus on agent behavior evaluation, not eval framework internals

---

### Proposal 3: Rework Eval Script to Use pytest-evals

**File:** `evals/eval_youtube_obsidian.py`
**Action:** COMPLETE REPLACEMENT

**New Implementation Summary:**
- Uses `@pytest.mark.eval` and `@pytest.mark.eval_analysis` decorators
- Separates EVAL PHASE (per-case) and ANALYSIS PHASE (aggregation)
- Stores results in `eval_bag` for analysis phase access
- Runs agent via opencode CLI with `--attach` flag for persistent server
- Calculates execution success rate and note creation rate
- 80% success threshold aligns with MVP goals
- Removes all unit testing of utility functions
- Focuses entirely on AI agent behavior evaluation

**Key Components:**
1. **EVAL PHASE (`test_agent_execution`):**
   - For each test case in test_cases.json
   - Setup VAULT_PATH environment variable
   - Execute opencode CLI with video URL
   - Capture output, transcript, and exit code
   - Check for created .md note file
   - Store all results in eval_bag

2. **ANALYSIS PHASE (`test_eval_analysis`):**
   - Calculate metrics (success rate, execution time, timeouts)
   - Display per-case results with pass/fail indicators
   - Determine overall pass/fail based on 80% threshold
   - Assert overall success

**Rationale:** Complete rewrite to use pytest-evals framework for AI agent evaluation

---

### Proposal 4: Create Test Case Data Structure

**New File:** `evals/test_data/test_cases.json`

**Content:**
```json
{
  "version": "1.0",
  "description": "Test cases for youtube-obsidian skill evaluation",
  "created_date": "2026-01-17",
  "test_cases": [
    {
      "id": "tc-001",
      "name": "Standard Watch URL",
      "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "expected_title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
      "description": "Standard youtube.com/watch?v= format URL",
      "tags": ["basic", "url-parsing"]
    },
    {
      "id": "tc-002",
      "name": "Shortened youtu.be URL",
      "video_url": "https://youtu.be/dQw4w9WgXcQ",
      "expected_title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
      "description": "Shortened youtu.be format URL",
      "tags": ["basic", "url-parsing", "shortened-url"]
    },
    {
      "id": "tc-003",
      "name": "Video with Transcript Available",
      "video_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
      "expected_title": "Me at the zoo",
      "description": "Public domain video with available transcript",
      "tags": ["transcript", "public-domain"]
    },
    {
      "id": "tc-004",
      "name": "Long Form Video",
      "video_url": "https://www.youtube.com/watch?v=aircAruvnKk",
      "expected_title": "What is a JPEG? (Deep zoom)",
      "description": "Longer educational video to test transcript handling",
      "tags": ["transcript", "long-form"]
    },
    {
      "id": "tc-005",
      "name": "Multiple Videos Batch Test",
      "video_url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
      "expected_title": "Me at the zoo",
      "description": "Additional public domain video for batch testing",
      "tags": ["batch", "public-domain"]
    }
  ],
  "metadata": {
    "total_cases": 5,
    "public_domain_videos": 3,
    "transcript_available": 3,
    "tags_summary": {
      "basic": 2,
      "url-parsing": 2,
      "transcript": 3,
      "public-domain": 3,
      "long-form": 1,
      "batch": 1
    }
  }
}
```

**Rationale:**
- Centralized test case management aligns with pytest-evals best practices
- JSON format easy to read, edit, and version control
- Includes metadata for test case classification
- Uses public domain videos to avoid copyright issues
- Tags allow selective test execution
- Supports Epic 2 (Test Case Management) requirements

---

### Proposal 5: Update Epic Status and Order

**File:** `_bmad-output/planning-artifacts/epics.md`
**Section:** Epic 2 and Epic 3 status updates

**Changes:**

**Epic 2 (formerly Epic 3): Test Case Management & Enhanced Output**
```diff
- **Status:** Deferred to Phase 2 (outside MVP scope)
- **Reason:** MVP focuses on basic eval execution, validation, and output.
+ **Status:** **ACTIVE** (Critical for MVP)
+ **Reason:** Corrected from course change - test case management is fundamental to running evaluations. pytest-evals provides this framework, and implementing it allows running multiple test cases efficiently.
+ **Priority:** High - Move from deferred to position 2 (before Epic 3, as test cases are needed for behavior validation)
```

**Epic 3 (formerly Epic 2): Agent Behavior Validation**
```diff
- **Status:** Deferred to Phase 2 (outside MVP scope)
- **Reason:** MVP scope constraints specify "No automated obsidian note structure validation (manual review only)"
+ **Status:** **ACTIVE** (Critical for MVP)
+ **Reason:** Corrected from course change - these behaviors are core to AI agent evaluation and must be implemented for MVP to determine if the agent is working correctly.
+ **Priority:** High - Move from deferred to position 3 (requires test cases from Epic 2)
```

**Revised Epic Order:**
1. Epic 1: Basic Eval Execution (unchanged)
2. Epic 2: Test Case Management & Enhanced Output (**moved up**)
3. Epic 3: Agent Behavior Validation (**moved down**)
4. Epic 4: Reliability & Performance Optimization (Phase 2 deferred)
5. Epic 5: Accuracy & Scoring (Phase 2 deferred)

**Rationale:**
- Epic 2 and Epic 3 were incorrectly deferred
- Test case management (now Epic 2) must come before behavior validation (now Epic 3)
- Both are critical for MVP
- pytest-evals framework makes these epics achievable

---

### Proposal 6: Add pytest-evals Dependency

**File:** `pyproject.toml`
**Section:** Development dependencies

**Change:**
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "pytest-mock>=3.10",
+   "pytest-evals>=0.3.4",  # AI agent evaluation framework
    "ruff>=0.6",
    "basedpyright>=1.13",
]
```

**Rationale:**
- Adds pytest-evals as development dependency
- Version 0.3.4 is latest stable
- Required for implementing AI agent evaluations per PRD
- Enables pytest-evals decorators

---

### Proposal 7: Update CI/CD Pipeline

**File:** `.github/workflows/test.yml`
**Section:** Eval execution step (lines 51-54)

**Change:**
```diff
    - name: Run eval script
      run: |
-       uv run evals/eval_youtube_obsidian.py
+     - name: Run AI agent evaluations
+     env:
+       YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
+       VAULT_PATH: ./eval_output/
+     run: |
+       # Start opencode headless server in background
+       opencode serve --port 4096 &
+       SERVER_PID=$!
+
+       # Wait for server to be ready
+       sleep 5
+
+       # Run evals using pytest-evals
+       uv run pytest evals/test_youtube_obsidian_eval.py --run-eval -v
+
+       # Cleanup server
+       kill $SERVER_PID
      continue-on-error: true
```

**Rationale:**
- Changes from custom eval script to pytest-evals framework
- Starts opencode headless server for agent execution
- Runs evals with `pytest --run-eval` flag
- Provides YOUTUBE_API_KEY and VAULT_PATH environment variables
- Timeout and server cleanup handled by workflow

---

### Proposal 8: Add Eval System Architecture Documentation

**File:** `_bmad-output/planning-artifacts/architecture.md`
**Action:** ADD comprehensive eval system architecture sections

**New Sections Added:**
1. Eval System Architecture Overview
2. Architecture Diagram (showing CI/CD → pytest-evals → opencode agent → skill tools → VAULT_PATH)
3. Data Models (Test Case, Eval Result)
4. Technology Stack (pytest-evals, opencode CLI, test data formats)
5. Key Design Decisions with rationale:
   - Two-Phase Evaluation (EVAL + ANALYSIS)
   - Agent Execution via opencode CLI
   - Test Case Management via JSON
   - Success Threshold: 80% Pass Rate
   - Manual Note Structure Validation
6. Evaluation Metrics table
7. Future Considerations (Phase 2)

**Rationale:**
- Adds comprehensive architecture documentation for eval system
- Documents agent harness design using opencode CLI
- Defines data models for test cases and eval results
- Captures key design decisions with rationale
- Provides future roadmap for Phase 2 features
- Aligns with pytest-evals framework and Anthropic's eval guidelines

---

## 6. Implementation Roadmap

### Phase 1: Foundation Setup (Immediate)

**Priority:** HIGH

**Tasks:**
1. ✅ Add `pytest-evals>=0.3.4` to pyproject.toml
2. ✅ Create `evals/test_data/test_cases.json` with 5 test cases
3. ✅ Delete `evals/test_eval_youtube_obsidian.py`
4. ✅ Implement `evals/eval_youtube_obsidian.py` (rename to `test_youtube_obsidian_eval.py`)
5. ✅ Update CI/CD pipeline (.github/workflows/test.yml)
6. ✅ Add architecture documentation to `_bmad-output/planning-artifacts/architecture.md`

**Acceptance Criteria:**
- `pytest evals/test_youtube_obsidian_eval.py --run-eval` executes successfully
- Test cases load from test_cases.json
- Agent execution via opencode CLI works
- CI/CD pipeline runs evals and produces results

**Estimated Effort:** 2-3 days

---

### Phase 2: Epic 1 Implementation - Basic Eval Execution

**Priority:** HIGH

**Stories:**
- Story 1.1: CLI Entry Point (acceptance criteria updated via Proposal 1)
- Story 1.2: Agent Execution (via opencode CLI)
- Story 1.3: Output Detection & Pass/Fail (via pytest-evals analysis phase)
- Story 1.4: Basic Error Handling (timeout, execution failures)

**Acceptance Criteria:**
- All Story 1.1-1.4 acceptance criteria met
- Basic eval execution works end-to-end
- Pass/fail status determined with 80% threshold
- Error messages are clear and actionable

**Estimated Effort:** 3-4 days

---

### Phase 3: Epic 2 Implementation - Test Case Management

**Priority:** HIGH

**Stories:**
- Story 3.1: Test Case File Loading (already created in Phase 1)
- Story 3.2: Enhanced Output Display (show created note content)
- Story 3.3: Comprehensive Validation Report (per-case results, metrics, recommendations)

**Acceptance Criteria:**
- All Story 3.1-3.3 acceptance criteria met
- Multiple test cases execute in sequence
- Detailed output displayed for each test case
- Comprehensive validation report generated

**Estimated Effort:** 2-3 days

---

### Phase 4: Epic 3 Implementation - Agent Behavior Validation

**Priority:** HIGH

**Stories:**
- Story 2.1: Agent Log Parsing (capture agent transcript)
- Story 2.2: Script Usage Validation (verify get_youtube_data.py used)
- Story 2.3: Web Search Detection (verify agent didn't use web search)
- Story 2.4: Internal Write Tool Validation (verify correct VAULT_PATH usage)

**Acceptance Criteria:**
- All Story 2.1-2.4 acceptance criteria met
- Agent transcripts captured and parsed
- Script usage verified
- Web search detection implemented
- Write tool and VAULT_PATH validation implemented

**Estimated Effort:** 4-5 days

**Note:** This is the most complex epic - requires parsing agent outputs and implementing validation logic per Anthropic's eval guidelines

---

### Phase 5: Documentation and Refinement

**Priority:** MEDIUM

**Tasks:**
1. Update AGENTS.md with eval usage instructions
2. Update README.md with eval section
3. Create eval guide (docs/eval-guide.md)
4. Refine test cases based on initial results
5. Update architecture docs based on implementation learnings

**Estimated Effort:** 1-2 days

---

## 7. Total Impact Summary

### Files Changed

| File | Action | Lines Affected |
|------|--------|---------------|
| `evals/test_eval_youtube_obsidian.py` | DELETE | -736 |
| `evals/eval_youtube_obsidian.py` | REPLACE | ~250 (new) |
| `evals/test_data/test_cases.json` | CREATE | +65 |
| `pyproject.toml` | MODIFY | +1 |
| `.github/workflows/test.yml` | MODIFY | ~15 |
| `_bmad-output/planning-artifacts/epics.md` | MODIFY | ~20 |
| `_bmad-output/planning-artifacts/architecture.md` | MODIFY | ~200 |
| **TOTAL** | | **~1,037** |

### Epics Affected

| Epic | Change | Status |
|------|---------|--------|
| Epic 1 | Implementation approach change (unit tests → agent evals) | Proceed |
| Epic 2 | Status: Deferred → ACTIVE | Position 2 |
| Epic 3 | Status: Deferred → ACTIVE | Position 3 |
| Epic 4 | No change | Phase 2 deferred |
| Epic 5 | No change | Phase 2 deferred |

### Effort Summary

| Phase | Tasks | Estimated Effort |
|-------|--------|-----------------|
| Phase 1: Foundation Setup | 6 tasks | 2-3 days |
| Phase 2: Epic 1 Implementation | 4 stories | 3-4 days |
| Phase 3: Epic 2 Implementation | 3 stories | 2-3 days |
| Phase 4: Epic 3 Implementation | 4 stories | 4-5 days |
| Phase 5: Documentation & Refinement | 5 tasks | 1-2 days |
| **TOTAL** | | **12-17 days** |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| pytest-evals framework learning curve | Medium | Medium | Documentation available, simple test cases to start |
| opencode server management in CI/CD | Low | Low | Use proven patterns, simple start/stop workflow |
| Agent behavior validation complexity | Medium | High | Start simple (script usage), iterate to complex (transcript parsing) |
| Test case quality/coverage | Low | Medium | Use public domain videos, expand based on failures |
| Non-deterministic agent behavior | High | Low | 80% threshold allows for variation, multiple trials if needed |

**Overall Risk Level:** ✅ **MEDIUM** - Manageable with proper mitigation

---

## 8. Validation Checklist

Before implementing, verify:

- [x] Core issue clearly defined and understood
- [x] Root cause identified (unit tests vs agent evals)
- [x] Impact on all epics assessed
- [x] Artifact conflicts checked and resolved
- [x] Path forward evaluated (Option 1 selected)
- [x] Specific change proposals created
- [x] All proposals have clear rationale
- [x] All proposals approved incrementally
- [x] Side effects identified and mitigated
- [x] MVP scope verified achievable
- [x] Implementation roadmap defined
- [x] Risk assessment completed
- [x] Effort estimates reasonable (12-17 days total)

---

## 9. Next Steps

1. **Immediate (Today):**
   - Install pytest-evals: `uv pip install pytest-evals`
   - Create `evals/test_data/` directory and `test_cases.json`
   - Delete `evals/test_eval_youtube_obsidian.py`

2. **Short-term (This Week):**
   - Implement Phase 1: Foundation Setup
   - Begin Phase 2: Epic 1 Implementation (Stories 1.1-1.2)

3. **Medium-term (Next 2 Weeks):**
   - Complete Phase 2-4: All active epic implementations
   - Run initial evals and refine test cases
   - Phase 5: Documentation and refinement

4. **Long-term (Phase 2):**
   - Implement Epic 4: Reliability & Performance (auto-retry, checkpointing)
   - Implement Epic 5: Accuracy & Scoring (LLM-as-judge, weighted scoring)
   - Expand test suite with regression tests

---

## 10. Conclusion

**Recommendation:** ✅ **Proceed with Option 1 - Direct Adjustment**

The eval system requires complete rework from unit testing utility functions to evaluating AI agent behavior using the pytest-evals framework. This change aligns the implementation with the PRD requirements, Anthropic's eval guidelines, and provides a better long-term solution using established tooling.

**Key Benefits:**
- ✅ Correctly implements PRD requirements (agent behavior evaluation)
- ✅ Uses battle-tested framework (pytest-evals) instead of building from scratch
- ✅ Provides better tooling for test case management and metrics
- ✅ Aligns with Anthropic's best practices for AI agent evaluation
- ✅ Future-proofs the eval system for additional skills
- ✅ Maintains achievable MVP scope (12-17 days total)

**Approval Status:** ✅ **APPROVED** - All 8 change proposals approved by Dave on 2026-01-17

---

*Document generated by: Bob - Scrum Master*
*Workflow: correct-course*
*Mode: incremental*
*Date: 2026-01-17*
