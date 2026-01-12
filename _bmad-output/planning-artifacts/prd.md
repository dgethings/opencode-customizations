---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish']
inputDocuments: ['README.md', 'AGENTS.md', 'skills/youtube-obsidian/SKILL.md']
documentCounts:
  briefCount: 0
  researchCount: 0
  brainstormingCount: 0
  projectDocsCount: 2
workflowType: 'prd'
classification:
  projectType: developer_tool
  domain: scientific/ai_evaluation
  complexity: medium
  projectContext: brownfield
---

# Product Requirements Document - opencode-customizations

**Author:** Dave
**Date:** 2026-01-11

## Success Criteria

### User Success

Dave can assign tasks to opencode agents with confidence that they will execute reliably. When an agent fails, Dave receives clear explanations of what went wrong and actionable guidance for improvement. The eval system enables Dave to build a family of AI agents (3-4 agents with dozens of skills/tools over 6 months) to help manage daily challenges related to ADHD, reducing cognitive load and time required to oversee agent behavior.

**Key Success Moments:**
- Dave runs an eval and gets a clear score (e.g., 0.85) with pass/fail status
- Dave sees the created obsidian note with checkmarks validating structure correctness
- When eval fails, Dave immediately understands WHY it failed and WHAT would fix it
- After automated optimization converges, Dave trusts agent will execute correctly 90% of time
- For the 10% of agent failures, eval reports them clearly so Dave can handle exceptions

### Business Success

Note: This is a personal project, not a commercial venture. Success is defined by personal utility and reliability rather than revenue or user growth.

**Personal Impact Metrics:**
- 90% of agent tasks execute correctly without Dave's intervention
- Time saved on agent oversight and debugging
- Increased confidence in delegating tasks to agents
- Ability to scale to dozens of skills/tools across multiple agents

**6-Month Milestones:**
- 3-4 agents operational
- Dozens of skills/tools with eval coverage
- Measurable improvement in daily task management efficiency

### Measurable Outcomes

- **Agent Reliability**: 90% of agent tasks execute correctly after passing evals
- **Eval Accuracy**: Scores correlate with real-world agent performance
- **Optimization Efficiency**: Converges within 50 iterations or plateau detection
- **Developer Confidence**: Dave trusts agents with 90%+ success rate tasks
- **Time to Debug**: Failures are explained clearly within minutes, not hours

## Product Scope & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-solving MVP - smallest implementation that proves we can effectively evaluate agent skills and provide actionable feedback. Focus on validating that an opencode agent can execute a skill, use correct scripts, and produce expected output.

**Resource Requirements:** Solo developer (Dave) working part-time. MVP designed for minimal complexity with manual validation to keep scope achievable.

### MVP Feature Set (Phase 1)

**Core User Journeys Supported:**
- Dave runs eval for youtube-obsidian skill and verifies agent executes correctly
- Basic validation that agent used skill scripts (not web search) and wrote note to correct location

**Must-Have Capabilities:**
- CLI command to run eval (`uv run evals/eval_youtube_obsidian.py`)
- Execute youtube-obsidian skill through opencode agent
- Parse agent usage logs to verify correct script usage (get_youtube_data.py)
- Verify no web search was used for metadata
- Check obsidian note was written to VAULT_PATH ("./output/")
- Display simple eval score (pass/fail based on script usage and note creation)
- Show created obsidian note
- Manual note structure review by Dave (no automated validation)

**Out of Scope for MVP:**
- Automated obsidian note structure validation (manual review only)
- Automated prompt improvement recommendations
- Retry logic for failed evals
- Checkpointing and resumability
- Detailed failure explanations (basic pass/fail only)
- Configurable eval parameters (hardcoded for MVP)
- Skills other than youtube-obsidian
- DSPy integration (deferred to Phase 2)

### Post-MVP Features

**Phase 2 (Growth):**
- Automated note structure validation (frontmatter fields, sections, tags)
- Detailed failure explanations with specific failure points
- Automated prompt improvement recommendations
- Retry logic (up to 3 consecutive failures)
- Configurable eval parameters (thresholds, iteration limits)
- Basic checkpointing for resumability
- Integration with DSPy or similar Python eval frameworks
- Documentation for writing evals for new skills

**Phase 3 (Vision - Expansion):**
- Fully automated prompt optimization loops (LLM generates suggestions, applies them, re-runs)
- Plateau detection and max iteration limits (50 iterations)
- Multiple skills supported beyond youtube-obsidian
- Comprehensive checkpointing and resumability
- CI/CD integration with GitHub
- Automated eval triggering on skill bug reports
- "eval-creator" skill to generate eval scaffolding for new skills
- Monitoring dashboard for agent reliability over time
- TypeScript support for opencode skills

### Risk Mitigation Strategy

**Technical Risks:**
- Parsing opencode agent logs may be complex. **Mitigation**: Start with simple string pattern matching to detect script names in logs; validate against known golden cases.
- Agent behavior non-determinism may cause flaky evals. **Mitigation**: MVP focuses on binary pass/fail for critical behaviors (script usage, output location); Phase 2 will add tolerance ranges for partial credit.

**Market Risks:**
- (N/A - personal project, no market validation needed)

**Resource Risks:**
- Solo developer with limited time. **Mitigation**: Extremely lean MVP with manual validation reduces complexity; clear feature boundaries prevent scope creep; Phase 1 success provides motivation for continued development.

## User Journeys

### User Journey 1: Dave - Successful Skill Eval (Happy Path)

**Opening Scene:**
It's a Tuesday morning. Dave has just finished updating youtube-obsidian skill's prompt after discovering agent wasn't properly using skill's Python script. He wants to verify his fix works before committing to repo.

**Rising Action:**
Dave opens terminal, navigates to project directory, and types:
```bash
uv run evals/eval_youtube_obsidian.py
```

He watches as eval system starts up. It loads golden test case (public domain YouTube video), sets up mock VAULT_PATH to "./output/", and instructs opencode agent to execute skill.

The agent runs. Dave sees progress indicators:
- "Agent executing youtube-obsidian skill..."
- "Checking tool usage logs..."
- "Validating obsidian note structure..."

**Climax:**
The eval completes and displays a clear report:

```
Eval Score: 0.85
Status: PASS ✓

Validation Results:
✓ Frontmatter contains all required fields (title, youtube_id, tags, youtube_url)
✓ Frontmatter values are correct and properly formatted
✓ All content sections present (summary, description, transcript)
✓ Tags relevant and within limits (12/15)
✓ Agent used skill script (get_youtube_data.py) for metadata
✓ Agent did NOT use web search
✓ Note written to correct VAULT_PATH (./output/)

Created Note Preview:
---
title: Big Buck Bunny
youtube_id: aqz-KE-bpKQ
tags: ["animation", "public domain", "open source"]
---
[Note content preview...]

Recommendations:
No improvements needed. Skill is performing optimally.
```

**Resolution:**
Dave feels confident. The eval confirms his fix worked. He commits skill to repo, then adds it to his opencode setup. He trusts that when he asks agents to use this skill, they'll execute correctly 90% of time. The eval system has saved him hours of manual testing and debugging.

### User Journey 2: Dave - Failed Eval with Improvement Recommendations

**Opening Scene:**
Dave is working on a new version of youtube-obsidian. He's added instructions about using internal write tool for obsidian note. He runs eval to test it.

**Rising Action:**
The eval runs... but this time, score comes back lower.

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

**Resolution:**
Dave reads recommendation and immediately understands the problem. The agent is using a hardcoded path instead of the environment variable. He updates SKILL.md prompt with the clearer instruction and example, then runs the eval again.

This time: **Score: 0.95, Status: PASS ✓**

Dave commits the improved skill.

### User Journey 3: Dave - Unexpected Eval Failure (Debug Recovery)

**Opening Scene:**
Dave is testing a modification to the eval scoring logic - he's adjusting the weight of the "note structure" validation. He runs the eval, expecting to see the new scoring in action.

**Rising Action:**
The eval starts running, but suddenly stops with an error:

```
Eval System Error: Exception during validation
Status: FAILED (System Error)

Error Details:
- Stage: Note Structure Validation
- Exception: KeyError: 'tags' not found in frontmatter
- Timestamp: 2026-01-11 14:32:15

What Happened:
The eval system encountered an unexpected error while validating the
obsidian note structure. This is likely a bug in the eval code, not a
skill failure.

Logs:
Full debug logs written to: /Users/dgethings/git/opencode-customizations/_bmad-output/eval-logs/2026-01-11_143215_eval.log

Checkpoints:
Last successful checkpoint saved at: step-3-agent-execution
Checkpoint file: /Users/dgethings/git/opencode-customizations/_bmad-output/checkpoints/eval_2026-01-11_143215_checkpoint.json

Next Steps:
1. Review the error log for full stack trace
2. Check the checkpoint to see state before failure
3. Fix the eval system code
4. Resume from checkpoint or restart eval
```

**Climax:**
Dave examines the logs at `eval-logs/2026-01-11_143215_eval.log`:

```
[DEBUG] 14:32:10 - Loading golden test case: test_cases.json
[DEBUG] 14:32:11 - Test case: Standard Watch URL (aqz-KE-bpKQ)
[DEBUG] 14:32:12 - Agent execution started
[INFO]  14:32:14 - Agent completed successfully
[DEBUG] 14:32:14 - Loading created note from: ./output/Big Buck Bunny.md
[DEBUG] 14:32:14 - Parsing frontmatter...
[DEBUG] 14:32:14 - Frontmatter parsed: {title: "Big Buck Bunny", youtube_id: "aqz-KE-bpKQ"}
[DEBUG] 14:32:14 - Note structure validation started
[ERROR] 14:32:15 - KeyError: 'tags' not found in frontmatter
         at eval_validators.py:142 in validate_note_structure()
         Stack trace:
           File "evals/eval_youtube_obsidian.py", line 87, in run_eval
             score = validate_note_structure(note_path)
           File "evals/eval_validators.py", line 142, in validate_note_structure
             tags = note_metadata['tags']
         KeyError: 'tags'
```

Dave realizes his scoring logic change broke the frontmatter parsing - he's trying to access tags that might not exist. The checkpoint shows the eval had completed agent execution and loaded the note successfully, so he doesn't need to re-run that part.

**Resolution:**
Dave fixes the bug in `eval_validators.py` by adding a safe check for tags, then restarts the eval from the checkpoint. The eval completes successfully this time with a score of 0.88. Dave commits the fix, knowing the eval system itself is now more robust.

## Domain-Specific Requirements

### Research Methodology

- **Representative Test Cases**: Evals must use test cases that accurately reflect real-world agent usage scenarios to ensure validity
- **Bias Prevention**: Evaluation criteria should be designed to avoid bias toward specific agent implementation patterns or approaches
- **Score Validation**: Eval scores must correlate with actual agent performance in real-world tasks; periodic validation against ground truth required

### AI/ML Considerations

- **Non-Deterministic Behavior**: Agent outputs may vary slightly between runs; eval scoring should tolerate reasonable variance while detecting significant failures
- **Output Variance Handling**: Define acceptable tolerance ranges for scoring when agents produce functionally equivalent but structurally different outputs
- **Edge Case Coverage**: Test cases should include edge cases, unusual inputs, and boundary conditions to expose hidden agent behaviors
- **Agent Behavior Patterns**: Recognize that AI agents may use different valid approaches to achieve the same goal; evals should assess correctness, not implementation approach

### Technical Constraints

- **Performance**: Evals must complete within 1-2 minutes per run; optimization loops should converge within ~1 hour
- **Reliability**: Eval system failure rate must be <1%; any eval failures require clear reporting with actionable debug information
- **Observability**: Comprehensive logging required for AI agent debugging:
  - Full agent execution logs (DEBUG mode)
  - Tool usage tracking (which scripts/tools were called)
  - Intermediate state checkpoints for resumability
  - Stack traces and error context for system failures
- **Retry Mechanism**: Failed evals should retry up to 3 consecutive times before reporting to developer
- **Checkpointing**: Save progress at key stages to enable resumability after failures

### Risk Mitigations

- **False Negatives**: Implement scoring thresholds and tolerance ranges to avoid failing agents that perform correctly but use different approaches
- **False Positives**: Validate eval criteria against golden test cases to ensure passing scores indicate real agent reliability
- **Eval System Bugs**: <1% failure rate requirement with retry logic and comprehensive logging to minimize eval system errors affecting assessment
- **Infinite Loops**: Max 50 optimization iterations with plateau detection to prevent optimization cycles from running indefinitely

## Developer Tool Specific Requirements

### Project-Type Overview

The eval system is a Python-based developer tool that provides automated evaluation and prompt optimization for opencode agent skills. It leverages existing Python evaluation frameworks (e.g., DSPy) rather than building from scratch, focusing on practical implementation patterns and documentation that enable developers to add evals to their skills.

### Technical Architecture Considerations

**Language Support:**
- Python-only for MVP
- Integration with Python package ecosystem (pip/uv)
- Leverage existing Python eval frameworks (DSPy, etc.) rather than reinventing evaluation logic
- Future consideration: TypeScript support for opencode skills (deferred until Dave gains TS familiarity)

**Package Management:**
- Use `uv` as package manager (consistent with existing opencode-customizations setup)
- Eval system itself is a repo-level tool (not a pip-installable package)
- Skills include their own eval scripts in the `evals/` directory
- Dependencies managed via project-level pyproject.toml or requirements.txt

**Evaluation Framework Integration:**
- Integrate with DSPy or similar Python evaluation frameworks for core eval logic
- Use framework capabilities for scoring, metric calculation, and prompt optimization
- Build custom validation logic on top of framework for skill-specific checks (e.g., obsidian note structure)
- Framework abstraction layer to allow swapping or upgrading evaluation backends in future

### Implementation Considerations

**Reference Implementation:**
- youtube-obsidian eval serves as primary example and template for other skills
- Eval structure and patterns documented through this reference implementation
- No separate "hello world" template needed - youtube-obsidian eval demonstrates all patterns

**Documentation Requirements:**

1. **Writing Evals for New Skills:**
   - How to structure an eval script in `evals/` directory
   - How to define validation functions for skill-specific outputs
   - How to configure golden test cases
   - How to set evaluation criteria and scoring weights
   - How to integrate with DSPy framework (or alternative)

2. **Configuration Guide:**
   - How to set passing score threshold per eval
   - How to configure max iteration limits and plateau detection
   - How to set retry logic parameters
   - How to configure checkpoint behavior
   - How to customize logging levels

3. **Interpreting Eval Results:**
   - How to read eval score and pass/fail status
   - How to understand validation checkmarks
   - How to act on failure recommendations
   - How to review created outputs (e.g., obsidian notes)
   - How to interpret iteration history and convergence metrics

4. **Debugging Guide:**
   - How to locate and read debug logs
   - How to use checkpoints for resumability
   - How to troubleshoot eval system errors vs. skill failures
   - How to handle non-deterministic agent behavior
   - Common failure patterns and solutions

**Future Tooling (Vision):**
- "eval-creator" skill to automate eval generation for new skills (similar to existing skill-creator)
- This would ask user questions about their skill and generate eval scaffolding automatically

## Functional Requirements

### Eval Execution

- FR1: Developer can run eval for youtube-obsidian skill via CLI command
- FR2: Developer can specify YouTube video URL as input to eval
- FR3: Developer can configure VAULT_PATH environment variable for test output directory

### Agent Execution

- FR4: Eval system can execute youtube-obsidian skill through opencode agent
- FR5: Eval system can pass YouTube video URL to agent skill execution
- FR6: Eval system can retrieve output created by agent skill execution

### Behavior Validation

- FR7: Eval system can parse agent usage logs to identify executed scripts
- FR8: Eval system can verify agent used get_youtube_data.py script for metadata extraction
- FR9: Eval system can verify agent did not use web search for metadata
- FR10: Eval system can verify agent used internal write tool for note creation
- FR11: Eval system can verify agent wrote note to path specified by VAULT_PATH environment variable

### Output Validation

- FR12: Eval system can detect if obsidian note file was created
- FR13: Eval system can display path of created obsidian note
- FR14: Eval system can display content of created obsidian note
- FR15: Eval system can indicate pass/fail status based on validation results

### Test Case Management

- FR16: Eval system can load golden test cases from test_cases.json file
- FR17: Eval system can use public domain YouTube video with transcript from golden test cases

### Logging & Debugging

- FR18: Eval system can display error message when agent execution fails
- FR19: Eval system can display error message when script usage validation fails
- FR20: Eval system can display error message when output creation validation fails

## Non-Functional Requirements

### Performance

- **NFR-1**: Eval completes execution within 1-2 minutes for youtube-obsidian skill test case
- **NFR-2**: Eval execution time exceeding 5 minutes indicates system failure (likely LLM provider constraints or downtime)

### Integration

(None - no integration concerns for MVP)

### Reliability

- **NFR-3**: Eval system automatically retries on failure, up to 3 consecutive attempts
- **NFR-4**: Eval system stops retrying if same error occurs 3 consecutive times and reports failure to developer
- **NFR-5**: Eval system has <1% failure rate (system errors, not skill failures)
- **NFR-6**: False positive rate (passing agents that should fail) is below 5%
- **NFR-7**: False negative rate (failing agents that should pass) is below 5%
