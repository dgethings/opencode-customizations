# Beads Integration - Sprint Planning to Issue Tracking

<critical>The workflow execution engine is governed by: {project-root}/_bmad/core/tasks/workflow.xml</critical>
<critical>You MUST have already loaded and processed: {project-root}/_bmad/bmm/workflows/4-implementation/sprint-planning/beads-integration/workflow.yaml</critical>
<critical>Communicate in {communication_language} with {user_name}</critical>

## 📚 Overview

This workflow integrates BMAD's sprint planning with Beads/Bd issue tracking system, enabling seamless tracking of stories from planning to implementation.

**Integration Benefits:**
- Track BMAD stories as Beads issues with full dependency support
- Sync story statuses between BMAD sprint-status.yaml and Beads
- Maintain bidirectional consistency
- Leverage Beads' lightweight issue tracking for daily development

<workflow>

<step n="0.5" goal="Discover and load project documents">
  <invoke-protocol name="discover_inputs" />
  <note>After discovery, {sprint_status_content} is available from sprint-status.yaml</note>
</step>

<step n="1" goal="Verify Beads setup">
<action>Check if Beads is initialized in the project</action>

<ask>Is Beads already initialized for this project? (y/n)</ask>

<check if="n">
  <action>Initialize Beads if not set up</action>
  <ask>Would you like to initialize Beads now? (y/n)</ask>

  <check if="y">
    <action>Run bd init command</action>
    <output>✅ Beads initialized successfully!</output>
  </check>

  <check if="n">
    <output>⚠️  Skipping Beads integration - Beads not initialized</output>
    <action>Exit workflow</action>
  </check>
</check>

<check if="y">
  <action>Verify Beads configuration</action>
  <action>Check for existing beads issues</action>
</check>
</step>

<step n="2" goal="Load sprint status and parse stories">
<action>Parse sprint-status.yaml to extract:</action>

- All stories with their current status
- Story keys and titles
- Epic assignments
- Dependencies (inferred from story order within epics)

<action>Filter stories by status:</action>

- `ready-for-dev`, `in-progress`, `review`, `done` → **Active sprint stories**
- `backlog` → **Future work** (optional sync)

<output>Found {{active_story_count}} active stories for sync</output>
</step>

<step n="3" goal="Load existing integration state">
<action>Check if integration state file exists:</action>

- File: {integration_state_file}
- Purpose: Track mapping between BMAD stories and Beads issues
- Contains: story_key → beads_issue_id mappings

<check if="integration state exists">
  <action>Load existing mappings</action>
  <output>Loaded {{existing_mapping_count}} existing story-to-issue mappings</output>
</check>

<check if="integration state does not exist">
  <action>Create fresh integration state</action>
  <output>Creating new integration state file</output>
</check>
</step>

<step n="4" goal="Configure Beads labels">
<action>Ensure required Beads labels exist for BMAD integration:</action>

<ask>Configure Beads labels? (y/n)</ask>

<check if="y">
  <action>Create/update Beads labels:</action>

  ```bash
  # BMAD workflow labels
  bd label create backlog || echo "Label exists"
  bd label create ready || echo "Label exists"
  bd label create in-progress || echo "Label exists"
  bd label create review || echo "Label exists"
  bd label create done || echo "Label exists"

  # Epic tracking labels
  bd label create epic || echo "Label exists"

  # Priority labels
  bd label create p1 || echo "Label exists"
  bd label create p2 || echo "Label exists"
  bd label create p3 || echo "Label exists"
  ```

  <output>✅ Beads labels configured</output>
</check>

<check if="n">
  <output>⚠️  Skipping label configuration (issues may lack proper labels)</output>
</check>
</step>

<step n="5" goal="Sync BMAD stories to Beads issues">
<action>For each story in active sprint:</action>

<check if="story already mapped in integration state">
  <action>Update existing Beads issue</action>

  <action>Mapping: story_key → existing_beads_issue_id</action>

  <action>Update issue details:</action>

  ```bash
  bd edit {{beads_issue_id}} --title "{{story_title}}"

  # Update status label
  bd label remove {{beads_issue_id}} backlog ready in-progress review done
  bd label add {{beads_issue_id}} {{beads_status_label}}

  # Update epic label
  bd label remove {{beads_issue_id}} epic-*
  bd label add {{beads_issue_id}} epic-{{epic_num}}
  ```

  <output>Updated: {{story_key}} → {{beads_issue_id}}</output>
</check>

<check if="story not mapped">
  <action>Create new Beads issue</action>

  <ask>Create new Beads issue for "{{story_title}}"? (y/n)</ask>

  <check if="y">
    <action>Create issue with BMAD context:</action>

    ```bash
    bd create \
      --title "{{story_title}}" \
      --description "BMAD Story: {{story_key}}\n\nEpic: {{epic_title}}\n\n{{story_description}}" \
      --priority "{{priority}}" \
      --label "{{beads_status_label}}" \
      --label "epic-{{epic_num}}"
    ```

    <action>Capture returned beads_issue_id</action>
    <action>Store mapping: story_key → beads_issue_id</action>

    <output>✅ Created: {{story_key}} → {{beads_issue_id}}</output>
  </check>

  <check if="n">
    <output>Skipped: {{story_key}}</output>
    <action>Mark as skipped in integration state</action>
  </check>
</check>
</step>

<step n="6" goal="Set up dependencies in Beads">
<action>Analyze story dependencies based on BMAD epic structure:</action>

- Story 1.x → Story 1.(x+1): Sequential dependency within epic
- Cross-epic dependencies: Manual setup based on story descriptions

<ask>Set up Beads dependencies? (y/n)</ask>

<check if="y">
  <action>Create sequential dependencies for each epic:</action>

  ```bash
  # Example: 1-1-user-auth → 1-2-account-mgmt
  bd deps add {{story_1_issue_id}} {{story_2_issue_id}}
  ```

  <output>✅ Set up {{dependency_count}} dependencies</output>
</check>

<check if="n">
  <output>⚠️  Skipping dependency setup (manage manually in Beads)</output>
</check>
</step>

<step n="7" goal="Generate integration state file">
<action>Create or update {integration_state_file} with:</action>

<template-output>integration_state</template-output>
</step>

<step n="8" goal="Generate sync scripts">
<action>Create helper scripts for bidirectional sync:</action>

**Script 1: bmad-to-beads.sh** - Push BMAD status to Beads

**Script 2: beads-to-bmad.sh** - Pull Beads status to BMAD

**Script 3: sync-status.sh** - Full bidirectional sync

<ask>Generate sync scripts? (y/n)</ask>

<check if="y">
  <action>Create scripts in {implementation_artifacts}/scripts/</action>
  <action>Make scripts executable</action>
  <output>✅ Generated sync scripts</output>
</check>

<check if="n">
  <output>⚠️  Skipping script generation</output>
</check>
</step>

<step n="9" goal="Validate and report">
<action>Perform validation checks:</action>

- [ ] All active stories mapped to Beads issues
- [ ] All Beads issues have correct status labels
- [ ] All Beads issues have epic labels
- [ ] Dependencies configured (if requested)
- [ ] Integration state file valid YAML
- [ ] Sync scripts executable (if generated)

<action>Display completion summary to {user_name} in {communication_language}:</action>

**Beads Integration Complete**

- **Active Stories Synced:** {{synced_count}}
- **New Issues Created:** {{new_issue_count}}
- **Updated Issues:** {{updated_count}}
- **Dependencies Set:** {{dependency_count}}
- **Integration State:** {integration_state_file}

**Next Steps:**

1. Review Beads issues: `bd list --label "ready"`
2. Start development: `bd set-state in-progress <issue-id>`
3. Track progress: `bd show <issue-id>`
4. Sync back to BMAD: Use generated sync scripts

**Bidirectional Sync:**

To sync Beads changes back to BMAD sprint-status.yaml:
```bash
cd /Users/dgethings/git/opencode-customizations
bash _bmad-output/implementation-artifacts/scripts/beads-to-bmad.sh
```

</step>

</workflow>

## Status Mapping

### BMAD → Beads Labels

| BMAD Status | Beads Label |
|-------------|-------------|
| backlog | backlog |
| ready-for-dev | ready |
| in-progress | in-progress |
| review | review |
| done | done |

### Epic Mapping

BMAD epics are tracked as Beads labels:
- Epic 1 → label: `epic-1`
- Epic 2 → label: `epic-2`
- etc.

## Integration State File Format

```yaml
# Beads Integration State
generated: {date}
project: {project_name}

# Story → Beads Issue mappings
mappings:
  1-1-user-auth: beads-123
  1-2-account-mgmt: beads-124

# Skipped stories
skipped:
  - 2-1-story-title

# Last sync timestamp
last_sync: {timestamp}
```

## Sync Scripts

### bmad-to-beads.sh

Pushes BMAD sprint-status.yaml to Beads issues:
- Reads sprint-status.yaml
- Updates issue labels based on BMAD status
- Updates titles and descriptions

### beads-to-bmad.sh

Pulls Beads issue status to BMAD sprint-status.yaml:
- Queries Beads for all tracked issues
- Updates story status in sprint-status.yaml
- Preserves unmapped stories

### sync-status.sh

Full bidirectional sync:
1. Push BMAD status to Beads
2. Pull Beads updates to BMAD
3. Resolve conflicts (manual intervention required)
4. Update integration state

## Usage Examples

### Create new issue manually

```bash
bd create-form
# Set labels: ready, epic-1
# Set priority: p1
```

### Move story to in-progress

```bash
bd set-state in-progress beads-123
```

### Add dependency

```bash
bd deps add beads-123 beads-124
```

### Sync back to BMAD

```bash
bash _bmad-output/implementation-artifacts/scripts/beads-to-bmad.sh
```

### Check sprint progress

```bash
# BMAD view
cat _bmad-output/implementation-artifacts/sprint-status.yaml

# Beads view
bd list --label "in-progress"
```
