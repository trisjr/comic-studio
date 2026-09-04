---
description: Ingest content from ClickUp Task/Comment/Doc or GitHub Issue into the SSOT documentation system
---

Workflow to ingest data from external sources (ClickUp, GitHub), auto-classify, and store in the correct location within `docs/`.

**Input**: URL of a ClickUp Task, ClickUp Comment, ClickUp Doc, or GitHub Issue.
Examples:

- `/opsx-ingest https://app.clickup.com/t/abc123`
- `/opsx-ingest https://app.clickup.com/t/abc123?comment=cm_456`
- `/opsx-ingest https://app.clickup.com/d/doc_abc123`
- `/opsx-ingest https://github.com/owner/repo/issues/42`

---

## Steps

### Step 0: Validate Input

- If **no URL** follows `/opsx-ingest` → Ask User: _"Please provide a ClickUp Task, Comment, Doc, or GitHub Issue URL."_
- **DO NOT proceed** without a valid URL.

### Step 1: Parse URL & Fetch Content

Analyze the URL to determine the platform and extract information:

**ClickUp Task:**

- Pattern: `app.clickup.com/t/<task_id>` or contains `/t/` followed by an ID
- Action: `clickup_get_task(task_id, detail_level: "summary")`
- Output: title, description, tags, status

**ClickUp Comment:**

- Pattern: URL contains `comment=<comment_id>` or `?comment=`
- Action:
  1. `clickup_get_task(task_id, detail_level: "summary")` — get parent context
  2. `clickup_get_task_comments(task_id)` — get comments, filter by `comment_id`
- Output: task context + specific comment content

**ClickUp Doc:**

- Pattern: `app.clickup.com/d/<document_id>`
- Action: `clickup_list_document_pages(document_id)` then `clickup_get_document_pages(document_id, page_ids)`
- Output: document pages content

**GitHub Issue:**

- Pattern: `github.com/<owner>/<repo>/issues/<number>`
- Action: `github_issue_read(method: "get", owner, repo, issue_number)`
- Output: title, body, labels

**NOTE**: If URL matches no pattern → Report error and ask User for a valid URL.

### Step 1.5: Deduplication Check

After successful fetch, AI **MUST** check whether this content has been ingested before:

**1.5a. Task URL, Doc URL, or GitHub Issue:**

1. **Normalize URL:** Strip unnecessary query parameters (except `?comment=`) and trailing `/` before searching.
2. **Action:** Use `grep_search` to find the **exact normalized URL** within `docs/`.
3. **If match found:**
   - Notify User: _"This URL is already stored at: `[file path]`. Would you like to:"_
     - **Skip** → End workflow.
     - **Review existing file** → Display current file content, then ask if User wants to create a new one.
   - **DO NOT auto-create** a new file without User approval.
4. **If NOT found** → Continue to Step 2 (AI Triage).

**1.5b. Comment URL (supplement to parent Task):**

Comments on a Task are typically supplementary info. Handle differently:

1. **Action:** Extract `task_id` from URL (strip `?comment=...`). Use `grep_search` to find parent task URL (`app.clickup.com/t/<task_id>`) in `docs/`.
2. **If parent file found:**
   - Notify: _"Parent task is already stored at `[file path]`. I'll merge the comment content into this file and append the comment URL to `source`. OK?"_
   - User confirm → **Merge content** into appropriate section + **Append comment URL** to `source` in YAML frontmatter.
   - **DO NOT create a new file.**
3. **If parent NOT found** → Continue to Step 2 (treat as new content).

### Step 2: AI Triage — Classify Content

Based on fetched content, classify into one of 3 types:

| Type         | Detection Signals                                                              |
| :----------- | :----------------------------------------------------------------------------- |
| **document** | Business flow, use case, requirement, spec, RFC, feature, enhancement          |
| **bug**      | Steps to reproduce, expected vs actual, crash, error, broken, defect, hotfix   |
| **hybrid**   | Contains BOTH a bug description AND new requirement/spec worth documenting     |

**Non-Interruption Rule (Single Approval):**

AI MUST NOT pause the pipeline to ask questions at this step. Auto-classify using best logical inference and continue silently through Content Engineering (Step 2.5) and Routing (Step 3) to present a single Triage Report for approval.

### Step 2.5: Content Engineering (MANDATORY)

After classification, AI **MUST** transform raw content into project-standard format **BEFORE** generating files. Never copy raw content verbatim from source.

**2.5a. Template & Sample File Reference:**

1. Read the corresponding template file (if exists):
   - Story → `docs/022-User-Stories/Backlog/Story-Template.md` + reference sample `Story-Request-OTP.md`
   - Epic → `docs/022-User-Stories/Epics/Epic-Template.md`
   - Others → Reference `knowledge-base/99-Templates/Documents-Template.md`
2. If the target directory already has real files (not templates) → Read **1 sample file** to understand the current format.

**2.5b. Standardize Frontmatter:**

Generate **complete** YAML frontmatter per `Documents-Template.md`:

```yaml
---
id: {TYPE}-{NNN}            # e.g., Story-Login-Email, Bug-003
type: {document_type}        # story, epic, bug-report, prd, use-case, spec, adr... (DO NOT use "user-story")
status: draft
project: {project_name}     # Extract from ClickUp context (tags, list name) or ask User
owner: "@[Active-Role-Name]" # MANDATORY: Auto-populate with currently active Role (e.g., "@Business Analyst", NOT the literal string "@role")
source:
  - "{original URL}"
linked-to: [[Related-Doc]]  # AI MUST use grep_search with key terms to auto-discover and populate related docs from `docs/`. Do not wait for User.
tags: [tag1, tag2]           # Extract from Task/Issue tags/labels
created: YYYY-MM-DD
---
```

**2.5c. Content Transformation by Type:**

| Type | Transform Requirements |
| :--- | :--------------------- |
| **User Story** | Convert raw description to **INVEST** structure: `**As a** [persona], **I want to** [action], **So that** [benefit].` |
| **Acceptance Criteria** | Decompose logic into **Happy Path** and **Unhappy Path** flows using **BDD/Gherkin** format: `**Given** [context] **When** [action] **Then** [expected result]` — enabling QA to write automated Test Cases. |
| **Bug Report** | Ensure completeness: Description, Steps to Reproduce, Expected vs Actual, Impact Analysis. |
| **Requirement / Spec** | Structure by standard sections for the document type (PRD, BRD, Use Case...). |
| **Noise Reduction** | (Especially for Comment/Issue) MUST remove social chatter (greetings, name tags, simple agreements). ONLY keep core business insights and decisions. |

**2.5d. Media Preservation:**

MUST NOT remove or summarize away Markdown Image Links `![...](url)`, iframes, or Tables containing configuration data from the original content. Insert them intact into the target document structure.

### Step 3: Route by Type

---

#### 3A. Type `document`

**Static Directory Lookup** — Use the mapping table below (DO NOT read `000-Index.md`):

| Content relates to...     | Store at                           | Naming Convention          |
| :------------------------ | :--------------------------------- | :------------------------- |
| PRD                       | `docs/020-Requirements/`           | `PRD-{Name}.md`            |
| BRD                       | `docs/020-Requirements/BRD/`       | `BRD-{NNN}-{Title}.md`     |
| Use Case                  | `docs/020-Requirements/Use-Cases/` | `UC-{NN}-{Title}.md`       |
| Epic                      | `docs/022-User-Stories/Epics/`     | `Epic-{Title}.md`          |
| User Story                | `docs/022-User-Stories/Backlog/`   | `Story-{Title}.md`         |
| ADR / RFC                 | `docs/030-Specs/Architecture/`     | `ADR-{NNN}-{Title}.md`     |
| Technical Spec            | `docs/030-Specs/`                  | `Spec-{Feature}.md`        |
| API Spec                  | `docs/030-Specs/API/`              | `Endpoint-{Name}.md`       |
| DB Schema                 | `docs/030-Specs/Schema/`           | `DB-Entity-{Name}.md`      |
| Bug Report                | `docs/035-QA/Reports/`             | `Bug-{NNN}-{Title}.md`     |
| Test Case                 | `docs/035-QA/Test-Cases/`          | `TC-{Feature}-{NNN}.md`    |
| UI/UX / Design System     | `docs/040-Design/`                 | Per specific type          |
| Research / Analysis       | `docs/050-Research/`               | `Analysis-{Topic}.md`      |
| Guide / Manual            | `docs/060-Manuals/User-Guide/`     | `{Topic}.md`               |
| Release Notes             | `docs/070-Deployment/Releases/`    | `Release-{Version}.md`     |
| Incident Report           | `docs/080-Operations/Incidents/`   | `Incident-{NNN}-{Date}.md` |

Process:

1. AI selects target directory and designs complete Markdown content in memory (including file name, naming convention, and YAML frontmatter).
   - *Note*: If target directory does not exist, Agent must proactively create the full parent directory tree when writing the file.
2. Proceed to Step 3D (Triage Report).

---

#### 3B. Type `bug`

1. Design complete Bug Report content in memory using this mandatory structure:

   ```markdown
   ---
   id: Bug-{NNN}
   type: bug-report
   status: open
   source:
     - "{original URL}"
   severity: [Critical/High/Medium/Low]  # AI auto-assesses from content
   created: YYYY-MM-DD
   linked-to: [[Related-Doc]]            # Auto Cross-Reference
   tags: [tag1, tag2]
   ---

   # Bug Report: [Title]

   ## Description
   [Summarized from original content]

   ## Steps to Reproduce
   [Extracted or inferred from content]

   ## Expected Behavior
   [Extracted]

   ## Actual Behavior
   [Extracted]

   ## Impact Analysis
   [Initial impact description]
   ```

2. Scan `docs/035-QA/Reports/` to auto-increment `{NNN}` and determine the future file name: `Bug-{NNN}-{Title}.md`.
3. Proceed to Step 3D (Triage Report).
4. *Post-Triage note:* After User approval and file creation, ask User if they want to activate the `requirement-impact` skill to analyze this bug's impact on existing Requirements.

---

#### 3C. Type `hybrid`

1. Engineer both **Bug Report** and **Document Extraction** content in memory in parallel.
2. Determine storage parameters for both document types.
3. Proceed to Step 3D (Triage Report).

---

#### 3D. Triage Report & Save File (Single Approval)

After silently completing all engineering and routing from 3A/3B/3C, present **ONE consolidated report**:

```markdown
📦 Triage Report:
- Source: [ClickUp/GitHub URL]
- AI Classification: [Document / Bug Report / Hybrid]

✅ Files to generate:
1. File: `docs/path/to/file.md`
   - Linked-to: [Auto-discovered related docs via AI Search]
   - Content Preview:
   > (Condensed Markdown excerpt or outline of generated content)
2. File (if Hybrid): `docs/path/to/bug/file.md`...

❓ Approve to write files and update related MOCs? (Approve / Edit abc)
```

- If User **Approves** → Write files, update MOC indexes (`Requirements-MOC.md`, `QA-MOC.md`...), and proceed to Step 4.
- If User wants to **Edit** → Adjust the draft and re-present.

---

### Step 4: Completion & Suggestions

After completion, always display:

```
✅ /opsx-ingest complete!
- Source: [original URL]
- Type: [document/bug/hybrid]
- Files created/updated: [list]

💡 Suggested next steps:
- /opsx-ingest <another URL> — Continue ingesting data
- /opsx-ff — Create a change to fix bug or implement feature
- /opsx-explore — Need to discuss the ingested content further
```

---

## Guardrails

- **Single Approval Gate**: Agent may silently process the entire pipeline (classify, engineer, route). The ONLY mandatory User confirmation point is **Step 3D (Triage Report)** — before writing files to disk. Exception: Step 1.5 (Dedup) also requires User decision if duplicates are detected.
- **Anti-Hallucination**: Only generate content based on actually fetched data. Do not fabricate information.
- **Dedup-First**: Must check for duplicate URLs in `docs/` (Step 1.5) before classifying and creating new files. Never skip this step.
- **No Silent Overwrite**: If a file already exists at the target location, notify User and ask: append, overwrite, or create new file.
- **Minimal Token**: Use `detail_level: "summary"` for ClickUp tasks. Do not fetch all comments unless the URL specifically targets a comment.
- **Media Preservation**: Absolutely preserve Image Links, Tables, iframes from original source. Must not summarize or remove them.
- **Traceability**: Every generated file must record the original URL in the `source` field of YAML frontmatter.
