# Project Structure

## Repository Overview

**Type:** Monolith
**Name:** opencode-customizations
**Purpose:** A collection of customizations and skill packages for Opencode AI, enabling automation workflows and integrations.

## Directory Structure

```
opencode-customizations/
├── _bmad/                    # BMAD framework (internal)
│   ├── bmm/                  # BMAD methodology workflows
│   ├── core/                 # Core workflow engine
│   └── _config/              # BMAD configuration
├── _bmad-output/             # BMAD workflow artifacts
│   └── planning-artifacts/   # Generated PRD, architecture, epics
├── skills/                   # Skill packages for Opencode
│   └── youtube-obsidian/     # YouTube to Obsidian skill
│       ├── scripts/          # Python scripts
│       ├── test_data/        # Test fixtures
│       └── SKILL.md          # Skill documentation
├── scripts/                  # Root-level scripts
├── evals/                    # Evaluation scripts
├── docs/                     # Project documentation output
├── .beads/                   # Beads issue tracking
├── .github/                  # GitHub workflows
├── .venv/                    # Python virtual environment
├── node_modules/             # Node.js dependencies
├── package.json              # JavaScript/TypeScript config
├── pyproject.toml            # Python project config
├── tsconfig.json             # TypeScript config
├── bun.lock                  # Bun lockfile
├── AGENTS.md                 # Agent guidelines
└── README.md                 # Project readme
```

## Key Directories

- **`skills/`**: Contains Opencode skill packages that extend AI capabilities
- **`_bmad/`**: BMAD (BMad Method) framework for structured project development
- **`_bmad-output/`**: Generated artifacts from BMAD workflows (PRD, architecture, etc.)
- **`scripts/`**: Executable scripts at project root
- **`evals/`**: Evaluation scripts for testing skills

## Technology Stack

- **Language:** Python 3.11+, TypeScript 5+
- **Package Manager:** Python (uv/setuptools), Bun (JavaScript/TypeScript)
- **Testing:** pytest (Python)
- **Code Quality:** ruff (Python), basedpyright (type checking)
