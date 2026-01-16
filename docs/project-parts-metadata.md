# Project Parts Metadata

## Overview

This repository is a **monolith** with **1 part**.

## Parts

### Part 1: opencode-customizations

| Property | Value |
|----------|-------|
| **Part ID** | opencode-customizations |
| **Root Path** | `/Users/dgethings/git/opencode-customizations` |
| **Project Type ID** | library |
| **Primary Language** | Python 3.11+ |
| **Secondary Language** | TypeScript 5+ |
| **Purpose** | Reusable skill packages and customizations for Opencode AI |

## Technology Markers

- Python package: `pyproject.toml` ✓
- TypeScript configuration: `tsconfig.json` ✓
- JavaScript configuration: `package.json` ✓
- Project structure: Monolith (single cohesive codebase)

## Skill Packages

Currently contains **1 skill**:

1. **youtube-obsidian** - Extract YouTube video metadata and transcripts to create Obsidian markdown notes
   - Scripts: Python scripts for YouTube API integration
   - Test data: Fixtures for testing
   - Documentation: SKILL.md with usage instructions

## Integration Notes

- Uses BMAD framework (`_bmad/`) for project development workflows
- Output artifacts generated to `_bmad-output/`
- Issue tracking via Beads (`.beads/`)
- GitHub workflows in `.github/`
