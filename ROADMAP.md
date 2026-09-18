# PhishReport Project Roadmap

## Critical issues to resolve before coding

These are unresolved proposal decisions, not confirmed implementation defects. Complete this checklist before dividing substantial implementation work. A small API feasibility experiment is part of this preparation.

| Priority | Issue | Required decision or evidence | Done |
| --- | --- | --- | --- |
| P0 | Current rules do not explicitly combine two AI-response fields. | Define at least one rule using two or more named AI fields, as required by Framework 1 section 2.3. A credential-request finding combined with a user action alone does not meet this requirement. | [ ] |
| P0 | Numeric scoring and routing are unspecified. | Define `evaluate(record)`, `score(record)` and `route(record)`: returned values, score range, formula, thresholds and outcome paths. The numeric score must use AI fields and serve ranking or thresholding. Describe it as a rule-based score, not a proven probability. | [ ] |
| P0 | Inputs do not fully support the proposed rules. | Explicitly collect whether the user clicked, downloaded or submitted information, and the category submitted. Receiving a link/file is different from acting on it. Never request actual passwords or OTPs. | [ ] |
| P0 | Exposure and uncertainty can produce misleading outcomes. | Decide what happens when a user reports sharing credentials but the AI sees no credential request, when suspicious indicators coexist with insufficient context, and when personal information or payments are involved. Define precedence and expected outcomes in a decision table. | [ ] |
| P0 | The API is an unverified dependency. | Verify the exact provider/model, credentials, cost or free quota, and a real request returning valid JSON. The proposal's named Kimi K3 API remains subject to verification. Agree on timeout, retry limit and failure behaviour. | [ ] |
| P0 | Repeatability and mandatory API processing need interpretation. | Ask the professor what “same output across separate runs on the same input” means, and whether viewing, filtering or updating existing reports requires another API call. Do not assume caching can bypass the API requirement. | [ ] |
| P0 | Topic approval is not established by the proposal alone. | Confirm instructor sign-off and that PhishReport does not duplicate another team's application. Framework 1 requires a one-paragraph problem statement by the end of Week 2, before Week 3. | [ ] |
| P1 | Shared data structures and interfaces are not agreed. | Approve exact field names, types, allowed values, function parameters, return values and failure structures. Distinguish processing state, assessment priority and user-updated report status. | [ ] |
| P1 | The proposal overstates safety. | Replace the claim about certifying a message as safe with the intended purpose: identifying indicators and supporting informed action. No indicators must not imply guaranteed safety. | [ ] |
| P1 | Delivery promises are too broad. | Define offline logic tests, Docker verification on all six laptops, report requirements and individual task ownership. Plan this work from the start. | [ ] |
| P1 | Repository identity is inconsistent. | Confirm the correct repository: the proposal's visible link ends in `phish-report`, but its destination ends in `pfd-team-project-p9g4`. Correct the proposal separately. | [ ] |

### Questions to take to the professor

1. Does repeatability mean reopening a saved assessment, deterministic decisions given fixed AI output, or identical results from fresh API calls on identical input?
2. Does “every record must pass through the API” apply only to new assessments, or also to viewing, filtering and status updates?
3. Has our topic received sign-off under the cohort's first-come, first-served rule?

Record the answers in the team's agreed design before implementing dependent behaviour. Other preparation can continue while awaiting clarification.

## Project vision and scope

PhishReport is a procedural Python command-line application that uses AI to interpret suspicious email, SMS and chat text. Explicit business rules combine validated AI findings with the user's reported actions to produce a priority, an explainable score and a predefined response checklist. Reports are stored locally in JSON for later retrieval.

**Core user journey:** enter a message and actions taken -> obtain validated AI findings -> apply rules, scoring and routing -> display and save the assessment -> retrieve and filter saved reports.

### First version

- Collect and validate message text, channel, optional sender and supported user actions.
- Process each new assessment through the real AI API.
- Validate structured AI output before using any fields.
- Evaluate, score and route the AI-enriched record.
- Display a reasoned assessment and checklist.
- Save reports, load them on startup and filter by priority.
- Handle invalid input, API failures and file errors without crashing.

### After the core flow works

- Add user-updated report status, with explicitly defined allowed values.
- Improve summaries and CLI usability without changing module boundaries.

### Outside Phase 1 scope

- Inbox integration, automatic message monitoring or a graphical interface.
- Visiting links, opening attachments or automatically changing accounts.
- Certifying a message or destination as safe.
- Class-based application design; classes belong to the later Phase 2 refactor.

## Framework requirements and module boundaries

| Module | Responsibilities | Required functions or behaviour |
| --- | --- | --- |
| `io_manager.py` | All terminal input and output; validate and normalise user input. | All `input()` and `print()` calls; return a clean dictionary with appropriate field types; display records, lists and results. |
| `ai_manager.py` | Prompt construction, API access, parsing and response validation. | `build_prompt(record)`, `call_api(prompt)`, `parse_response(raw)`, `validate_response(data)`. No priority/scoring/checklist decisions here. |
| `logic_manager.py` | Domain rules, numeric scoring and outcome routing. | `evaluate(record)`, `score(record)`, `route(record)`; at least one rule combining two or more AI-response fields. |
| `data_manager.py` | JSON persistence and retrieval. | `save(record)` after evaluation, `load()` on startup, `query(filter_fn)`; missing/corrupt file handling. |

A small main program coordinates the workflow and delegates user-facing messages to the I/O manager. Avoid circular imports and agree on who calls each function. Keep text fields as validated strings and convert choices or flags into the agreed types.

**Hard constraints:** no class definitions in team-authored code, AI essential to the main purpose, schema-validated JSON responses, CSV/JSON persistence, working Docker delivery and meaningful Git history. Framework 1 marks the procedural and AI-core constraints as instant-fail conditions.

## Six-person contribution plan (Suggestion - not fixed)

Use three pairs for initial feature ownership. Members M1-M6 are placeholders to replace with team names. Pair ownership does not replace individual tasks, commits and pull requests.

| Pair | Initial feature | Suggested individual starting tasks |
| --- | --- | --- |
| A: M1 + M2 | Input and AI processing | M1: input collection/validation and tests. M2: API request, JSON parsing/validation and tests. |
| B: M3 + M4 | Assessment and explanation | M3: evaluation/scoring and tests. M4: routing, checklist selection, result display and tests. |
| C: M5 + M6 | Persistence and report history | M5: save/load and file-error tests. M6: filter/query, history display and tests. |

Display functions contributed by any pair still belong in `io_manager.py`. Coordinate shared-file edits through small pull requests and the agreed interfaces.

| Round | Pair A | Pair B | Pair C |
| --- | --- | --- | --- |
| 1: Core implementation | Input and AI | Rules and assessment display | Storage and history |
| 2: Cross-review and robustness | Storage error paths | Input/API error paths | Rule boundaries and uncertainty cases |
| 3: Delivery focus | Automated checks | Docker and laptop verification coordination | End-to-end tests and setup guide |

Delivery work starts early; Round 3 is a focus period, not its starting date. Assign an integration coordinator each milestone and rotate the role. Everyone contributes to code, tests, review, documentation and Docker verification.

## Roadmap and completion gates

The week mapping below is a proposed team schedule. The supplied specification sets Week 2 topic selection, Week 3 pitching, Week 7 submission and Week 8 demo. Confirm any changed dates with the professor.

### Milestone 0 - Agree the design and prove feasibility

**Target:** before substantial feature implementation; topic sign-off by end of Week 2.

- [ ] Resolve the critical-issue checklist above.
- [ ] Agree on a decision table, including two-AI-field rules, score thresholds, routing and precedence.
- [ ] Approve example input, AI response, decision and saved-report dictionaries.
- [ ] Define all manager interfaces and error returns.
- [ ] Verify one real API request using fictional or sanitised content.
- [ ] Confirm repository access for all six members and lab-in-charges; everyone clones it.
- [ ] Create individually owned tasks with outcomes and reviewers.
- [ ] Capture the initial data-flow diagram and exception-handling matrix.

**Exit evidence:** approved topic, agreed interfaces/rules, a successful API feasibility result and a task plan for every member.

### Milestone 1 - One complete working assessment

**Suggested target:** Weeks 3-4, alongside the Week 3 pitch.

- [ ] Create the four manager files and the main coordinator using functions only.
- [ ] Process one fictional message through terminal input, real AI, validated JSON, business logic and storage.
- [ ] Implement initial `evaluate`, `score` and `route` behaviour.
- [ ] Display the result through the I/O manager.
- [ ] Restart and load the saved record.
- [ ] Add a Dockerfile and verify the first complete flow in Docker.
- [ ] Add initial offline logic tests and run them on pull requests.

**Exit evidence:** one input produces a validated, evaluated, displayed and persisted assessment in Docker; a restart retrieves it.

### Milestone 2 - Complete the agreed core behaviour

**Suggested target:** Weeks 4-5.

- [ ] Implement all approved input fields and re-prompt behaviour.
- [ ] Complete the decision table, score calculation and routes.
- [ ] Define and test “insufficient information” and “no clear indicators” separately.
- [ ] Implement report listing and `query(filter_fn)` filtering.
- [ ] Add status updates only after the core flow works and the API interpretation is settled.
- [ ] Keep API failure separate from a completed assessment.
- [ ] Ensure the assessed report retains the validated AI output and final decision.

**Exit evidence:** all supported user journeys work and have agreed expected results; modules integrate without incompatible field names or return types.

### Milestone 3 - Robustness and reproducibility

**Suggested target:** Weeks 5-6.

- [ ] Exercise connection failure, timeout, malformed JSON, missing fields and invalid field values.
- [ ] Verify bounded retries and behaviour after retries are exhausted.
- [ ] Test missing/corrupt data files; log errors, return an empty list and continue as required.
- [ ] Decide how to preserve a corrupt file before any subsequent save could overwrite it.
- [ ] Test blank messages, invalid choices and contradictory user answers.
- [ ] Verify repeatability according to the professor's clarified interpretation.
- [ ] Run offline logic tests inside Docker without live API access.
- [ ] Verify application execution on all six laptops and record results.
- [ ] Document runtime API credential configuration without committing credentials.

**Exit evidence:** the exception-handling matrix matches actual behaviour, automated checks pass and every team member has verified the container.

### Milestone 4 - Submission preparation

**Target:** before Week 7 submission.

- [ ] Freeze features and prioritise defects.
- [ ] Verify four functional managers, no class definitions and all `input()`/`print()` calls confined to I/O.
- [ ] Finish the engineering report: maximum five pages, with the data-flow diagram and exception-handling matrix together on one page.
- [ ] Include the offline automated test script and confirm it passes in Docker.
- [ ] Verify the root Dockerfile and documented application/test commands from a clean checkout.
- [ ] Ensure dependencies are installed within the container.
- [ ] Review Git history for descriptive, granular development commits and reviewed changes.
- [ ] Check the final repository URL, collaborator access and submission instructions.

**Exit evidence:** source code, engineering report, test script, repository history and Docker delivery are ready on the submission branch.

### Milestone 5 - Demonstration

**Target:** Week 8.

- [ ] Rehearse a normal assessment, a reported-exposure case and an uncertain case.
- [ ] Demonstrate persistence and filtering after restart.
- [ ] Be ready to explain graceful failure and run offline tests.
- [ ] Ensure every member can explain the complete pipeline and their own contributions.
- [ ] Explain the distinction between AI interpretation and procedural decisions.

## Minimum test plan

Expected outcomes must come from the agreed decision table, not from whatever the implementation happens to return.

| Test group | Required coverage |
| --- | --- |
| Rule logic | Two-AI-field rule combinations, score boundaries, precedence, routes and checklist selection. |
| Exposure and uncertainty | Credentials submitted with no AI credential finding; suspicious indicators with insufficient context; supported disclosure categories. |
| Response validation | Malformed JSON, missing keys, wrong types and invalid values. |
| Input | Blank required fields, unsupported choices and inconsistent action answers. |
| Persistence | Save/load across runs, filtering, missing file and corrupt file. |
| Integration | Real API assessment through all managers; API failure must not become a successful assessment. |
| Docker | Offline logic tests and application execution on all six laptops. |

Framework 1 explicitly requires offline `logic_manager` tests using hardcoded AI responses. Use functions and assertions or function-based tests. These fixtures support testing; the live application's assessment must still depend on the API.

## Git and collaboration agreement

- Every member owns small, reviewable tasks with clear acceptance criteria.
- Use focused branches, start from an up-to-date base and integrate regularly.
- Commit meaningful steps with descriptive messages; avoid a single end-of-project upload.
- Link pull requests to tasks and request another member's review.
- Include relevant tests and documentation with each change.
- Agree on a merge approach that preserves visible individual contribution evidence.
- Do not manufacture commits to meet an invented quota. The supplied documents require meaningful iterative history, not a numerical commit-frequency target.
- Record design decisions and review contributions as well as implementation work.

## Sources and status

- [Team Project Framework - Phase 1](Team%20Project%20Framework%20-%20Phase%201.pdf): architecture, functions, constraints and deliverables.
- [Team Project Specification](Team%20Project%20Specification.pdf): overall project requirements and Week 2/3/7/8 checkpoints.
- [Grading Criteria1](Grading%20Criteria1.pdf): assessment weights and performance descriptors.
- [Project Initial Details](Project%20Initial%20Details.pdf): initial proposal and repository submission requirements.
- [Current proposal](https://docs.google.com/document/d/1hig8lMgrtFNamitFrsCYAZJFb3f-eap-qaXCwYfKTW8/edit?tab=t.0): PhishReport scope reviewed on 18 September 2026.

This roadmap proposes sequencing and ownership; it does not confirm topic approval, API availability or completed work. Update the checkboxes and replace member placeholders as the team agrees and delivers each item. The Google Doc has not been edited.

## Deliverables dashboard

Use this section as the team's submission-readiness checklist. Unchecked means **not yet verified**, not necessarily not started. Check an item only when its acceptance criteria are met and evidence is linked. Assign an owner and have another member verify it. The milestone checklists above track the work needed to reach these outcomes.

### At-a-glance submission checklist

- [ ] **D1 - Topic sign-off:** instructor approval recorded; one-paragraph statement covers problem, data flow and business rules; topic uniqueness confirmed.
- [ ] **D2 - Procedural source code:** working CLI with all four managers; every source-code requirement below verified.
- [ ] **D3 - Engineering report:** at most five pages; data-flow diagram and exception-handling matrix together on one page.
- [ ] **D4 - Automated test script:** tests the core logic with hardcoded AI responses, runs without the live API and passes inside Docker.
- [ ] **D5 - Git repository:** correct accessible repository, descriptive granular commits showing iterative development, and required collaborators added.
- [ ] **D6 - Docker delivery:** root Dockerfile, working application on the submission branch, dependencies installed in the container and verification on all six laptops.

| ID | Owner | Reviewer | Evidence link / verification date |
| --- | --- | --- | --- |
| D1 | TBD | TBD | Instructor approval: pending |
| D2 | TBD | TBD | Submission commit and application demonstration: pending |
| D3 | TBD | TBD | Final report: pending |
| D4 | TBD | TBD | Test script and passing Docker test output: pending |
| D5 | TBD | TBD | Repository, history and access verification: pending |
| D6 | TBD | TBD | Dockerfile, run instructions and laptop checks: pending |

### Source-code acceptance checklist (D2)

- [ ] **Procedural constraint - instant-fail gate:** no class definitions in team-authored source or tests.
- [ ] **AI-core constraint - instant-fail gate:** every assessment record passes through the real API; removing AI processing breaks the main assessment purpose. Existing-record operations follow the professor's clarified interpretation.
- [ ] **Architecture:** all four manager files are functional, follow the required pipeline and have clear interfaces without circular dependencies.
- [ ] **I/O:** all `input()` and `print()` calls are in `io_manager.py`; required fields, types and ranges are validated with re-prompts; clean typed dictionaries and record/list/result displays are implemented.
- [ ] **AI functions:** `build_prompt`, `call_api`, `parse_response` and `validate_response` are implemented; prompts request JSON; required keys, types and ranges are validated before use.
- [ ] **AI failures and boundaries:** connection errors, timeouts and malformed responses are handled without crashing; errors are logged; domain decisions stay out of `ai_manager.py`.
- [ ] **Logic functions:** `evaluate`, `score` and `route` are implemented; scoring is numeric, derives from AI fields and supports ranking or thresholds.
- [ ] **Multi-condition rule:** at least one tested rule combines two or more fields from the AI response.
- [ ] **Persistence:** `save` writes evaluated records to JSON; `load` retrieves records on startup; `query(filter_fn)` returns matching records.
- [ ] **File failures:** missing files return an empty list; corrupt files are logged and handled without crashing, returning an empty list so the application can continue.
- [ ] **Repeatability:** behaviour across separate runs meets the professor's confirmed interpretation, with a recorded verification result.
- [ ] **PhishReport behaviour:** approved input/action fields, rule precedence, score, priority, checklist and uncertain outcomes match the team's decision table; API failure cannot appear as a successful assessment.

### Report and testing acceptance checklist (D3-D4)

- [ ] Report length is no more than five pages.
- [ ] Data-flow diagram shows how user input becomes an AI payload, validated findings, an evaluated record and stored data.
- [ ] Exception-handling matrix covers API connection failure, malformed API response, corrupt/missing data file and invalid user input.
- [ ] The diagram and exception-handling matrix appear together on one page.
- [ ] Offline tests use hardcoded sample AI responses and cover `evaluate`, `score` and `route`, including the two-AI-field rule.
- [ ] Expected results are defined from the agreed rules, including boundaries and conflicting/uncertain cases.
- [ ] Tests pass inside Docker without a live API connection; the command and result are recorded.

### Repository and Docker acceptance checklist (D5-D6)

- [ ] Correct repository URL is used consistently; all team members and lab-in-charges have required access; all members have cloned the repository.
- [ ] Initial-details document contains the required information and repository URL, is committed/pushed, and is submitted through the required channel.
- [ ] History contains descriptive, granular commits across development rather than one final dump.
- [ ] Branches and reviewed pull requests provide collaboration evidence; automated checks support the rubric's stronger DevOps expectations.
- [ ] Dockerfile is present at the repository root and builds from the submission branch.
- [ ] The documented container command produces working application output; API credential setup is documented without committing secrets.
- [ ] Dependencies require no manual installation outside the container.
- [ ] All six laptop checks below are complete for the submission version.

| Laptop verification | Member name | Submission commit tested | Date / result or blocker |
| --- | --- | --- | --- |
| M1 | TBD | Pending | Pending |
| M2 | TBD | Pending | Pending |
| M3 | TBD | Pending | Pending |
| M4 | TBD | Pending | Pending |
| M5 | TBD | Pending | Pending |
| M6 | TBD | Pending | Pending |

**Ready to submit:** D1-D6 are checked, their applicable acceptance checks pass, evidence refers to the submission version, and any instructor clarifications are recorded. This dashboard is manually maintained; it does not automatically inspect the code or repository.
