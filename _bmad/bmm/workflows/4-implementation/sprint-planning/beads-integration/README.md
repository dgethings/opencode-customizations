# Beads Integration Workflow

Integrates BMAD sprint planning with Beads/Bd issue tracking system for seamless story tracking.

## Overview

This workflow bridges BMAD's structured planning with Beads' lightweight issue tracking:

- **BMAD**: PRD → Architecture → Epics → Stories → Sprint Planning
- **Beads**: Daily issue tracking with dependency support
- **Integration**: Bi-directional sync between the two systems

## When to Use

Run this workflow **after** completing the BMAD `sprint-planning` workflow:

1. BMAD creates `sprint-status.yaml` with all stories and their statuses
2. Run `beads-integration` to sync stories to Beads issues
3. Track daily development in Beads
4. Sync Beads updates back to BMAD for sprint reviews

## Workflow Location

```
_bmad/bmm/workflows/4-implementation/sprint-planning/beads-integration/
```

## Components

### Files

- `workflow.yaml` - Workflow configuration
- `instructions.md` - Step-by-step execution instructions
- `integration-state-template.yaml` - Template for tracking story→issue mappings
- `README.md` - This file

### Outputs

- `{implementation_artifacts}/beads-integration-state.yaml` - Mapping between BMAD stories and Beads issues
- `{implementation_artifacts}/scripts/bmad-to-beads.sh` - Script to push BMAD status to Beads
- `{implementation_artifacts}/scripts/beads-to-bmad.sh` - Script to pull Beads status to BMAD
- `{implementation_artifacts}/scripts/sync-status.sh` - Full bidirectional sync

## Status Mapping

| BMAD Status | Beads Label | Description |
|-------------|-------------|-------------|
| backlog | backlog | Story only in epic file |
| ready-for-dev | ready | Story file created, ready for dev |
| in-progress | in-progress | Developer actively working |
| review | review | Ready for code review |
| done | done | Story completed |

## Quick Start

### 1. Ensure Sprint Status Exists

```bash
# Run BMAD sprint planning first
/bmad:bmm:workflows:sprint-planning
```

### 2. Run Beads Integration

```bash
# Load the beads-integration workflow
/bmad:bmm:workflows:beads-integration
```

The workflow will:
- Verify Beads is initialized
- Load sprint-status.yaml
- Check existing integration state
- Configure Beads labels
- Create/update Beads issues
- Set up dependencies
- Generate sync scripts

### 3. Track Development in Beads

```bash
# List ready stories
bd list --label ready

# Start working on a story
bd set-state in-progress <issue-id>

# Mark as done
bd set-state done <issue-id>
```

### 4. Sync Back to BMAD

```bash
# Pull Beads updates to BMAD sprint-status.yaml
bash _bmad-output/implementation-artifacts/scripts/beads-to-bmad.sh
```

## Workflow Steps

### Step 1: Verify Beads Setup
- Checks if Beads is initialized
- Offers to initialize if not present

### Step 2: Load Sprint Status
- Parses sprint-status.yaml
- Filters active stories (ready-for-dev and above)
- Identifies epic assignments

### Step 3: Load Integration State
- Checks for existing story→issue mappings
- Loads or creates integration state file

### Step 4: Configure Beads Labels
- Creates BMAD-specific labels: backlog, ready, in-progress, review, done
- Creates epic tracking labels: epic-1, epic-2, etc.
- Creates priority labels: p1, p2, p3

### Step 5: Sync BMAD Stories to Beads Issues
- For each story:
  - If mapped: Update existing Beads issue
  - If unmapped: Create new Beads issue
- Sets title, description, status label, epic label, priority

### Step 6: Set Up Dependencies
- Creates sequential dependencies within epics
- Story 1.1 → Story 1.2 → Story 1.3, etc.

### Step 7: Generate Integration State
- Saves story→issue mappings to YAML file
- Records sync timestamp and statistics

### Step 8: Generate Sync Scripts
- Creates helper scripts for bidirectional sync

### Step 9: Validate and Report
- Validates all sync operations
- Reports on issues created/updated
- Provides next steps

## Integration State File

Location: `{implementation_artifacts}/beads-integration-state.yaml`

```yaml
generated: "2026-01-11T22:30:00+0400"
project: opencode-customizations
sync_mode: bidirectional

mappings:
  1-1-user-authentication: opencode-customizations-100
  1-2-account-management: opencode-customizations-101

skipped: []

labels:
  - backlog
  - ready
  - in-progress
  - review
  - done
  - epic

priorities:
  - p1
  - p2
  - p3

last_sync:
  timestamp: "2026-01-11T22:30:00+0400"
  direction: bidirectional
  stories_synced: 2
  issues_created: 2
  issues_updated: 0
```

## Sync Scripts

### bmad-to-beads.sh

Pushes BMAD sprint-status.yaml to Beads:

```bash
bash _bmad-output/implementation-artifacts/scripts/bmad-to-beads.sh
```

**What it does:**
- Reads sprint-status.yaml
- Updates issue labels based on BMAD status
- Updates titles and descriptions
- Records sync in integration state

### beads-to-bmad.sh

Pulls Beads issue status to BMAD:

```bash
bash _bmad-output/implementation-artifacts/scripts/beads-to-bmad.sh
```

**What it does:**
- Queries Beads for all tracked issues
- Maps Beads labels to BMAD statuses
- Updates sprint-status.yaml
- Preserves unmapped stories

### sync-status.sh

Full bidirectional sync:

```bash
bash _bmad-output/implementation-artifacts/scripts/sync-status.sh
```

**What it does:**
1. Pushes BMAD changes to Beads
2. Pulls Beads updates to BMAD
3. Resolves conflicts (manual intervention)
4. Updates integration state

## Beads Commands Reference

### Issue Management

```bash
# Create issue
bd create --title "Story Title" --description "Description"

# Show issue details
bd show <issue-id>

# List issues
bd list
bd list --label ready
bd list --label in-progress

# Edit issue
bd edit <issue-id> --title "New Title"

# Close issue
bd close <issue-id>

# Delete issue
bd delete <issue-id>
```

### Status Management

```bash
# Set operational state
bd set-state ready <issue-id>
bd set-state in-progress <issue-id>
bd set-state done <issue-id>
```

### Label Management

```bash
# Add label
bd label add <issue-id> ready

# Remove label
bd label remove <issue-id> backlog

# Create label
bd label create p1
```

### Dependencies

```bash
# Add dependency
bd deps add <issue-id-1> <issue-id-2>

# Remove dependency
bd deps remove <issue-id-1> <issue-id-2>

# Show dependencies
bd deps show <issue-id>
```

### Comments

```bash
# Add comment
bd comments add <issue-id> "Progress update"

# List comments
bd comments list <issue-id>
```

## Workflow Integration

The beads-integration workflow fits into BMAD's Phase 4 (Implementation):

```
Phase 3: Solutioning
  ├─ create-architecture
  ├─ create-epics-and-stories
  └─ implementation-readiness

Phase 4: Implementation
  ├─ sprint-planning (creates sprint-status.yaml)
  ├─ beads-integration (syncs to Beads) ← NEW
  └─ Actual development (tracked in Beads)
```

## Best Practices

1. **Run after sprint planning**: Always run beads-integration after sprint-planning completes
2. **Regular syncs**: Sync Beads changes back to BMAD before sprint reviews
3. **Label consistency**: Use the predefined BMAD labels for consistency
4. **Dependency tracking**: Set up dependencies for complex story relationships
5. **State management**: Use `bd set-state` to track story progress

## Troubleshooting

### Beads not initialized

```bash
cd /Users/dgethings/git/opencode-customizations
bd init
```

### Issues with sync scripts

Ensure scripts are executable:
```bash
chmod +x _bmad-output/implementation-artifacts/scripts/*.sh
```

### Integration state corrupted

Delete the integration state file and re-run the workflow:
```bash
rm _bmad-output/implementation-artifacts/beads-integration-state.yaml
```

## Related Workflows

- `sprint-planning` - Creates sprint-status.yaml (required input)
- `document-project` - Analyzes existing codebase (for brownfield)
- `create-epics-and-stories` - Creates stories from PRD

## Future Enhancements

Potential improvements for the integration:

- [ ] Automatic sync on Beads issue state changes (daemon)
- [ ] Bidirectional conflict resolution
- [ ] Sprint burndown chart generation
- [ ] Integration with pull requests (mark stories as 'review' when PR created)
- [ ] Support for additional tracking systems (Jira, Linear, etc.)
