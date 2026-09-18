# Features and Contributions

This file records who built what, so everyone gets credit for their work.
Add a row when you finish a feature. Link the pull request if you can.

## Done so far

The project scaffolding and DevOps setup are in place and the app runs end to
end. The four managers have working starter versions; their owners can still
extend them (see "Up for grabs" below).

Most of this so far is the foundation and DevOps work.

| Feature | Description | Owner | PR |
| --- | --- | --- | --- |
| Project setup & MVP wiring | Repo layout, `main.py` connecting the pipeline, and starter managers so the app runs end to end | Lee Guan Feng | early commits |
| Groq AI integration | `ai_manager` calls the Groq API (free tier), requests JSON and validates the reply | Lee Guan Feng | #4 |
| Docker | `Dockerfile` plus `docker.sh` helper (build/run/test/shell/clean) so the app runs the same on any laptop | Lee Guan Feng | #6 |
| GitHub Actions CI | `.github/workflows/ci.yml`: lint, tests and Docker build/test on every push and PR | Lee Guan Feng | #1 |
| Ruff lint in CI | Adds an automated code-style check (`ruff`) with `ruff.toml` config | Lee Guan Feng | #8 |
| No-class guard in CI | Fails the build if any `class` appears in `app/`, protecting the 100%-procedural instant-fail rule | Lee Guan Feng | #9 |
| CI status badge | Shows the pipeline status at the top of the README | Lee Guan Feng | #10 |
| Release automation | `.github/workflows/release.yml`: pushing a `v*` tag runs tests then publishes a GitHub Release with notes | Lee Guan Feng | #11 |
| Offline test suite | 24 tests across `logic_manager`, `ai_manager` and `data_manager`, all without the live API | Lee Guan Feng | #7 |
| Project docs | `README.md` (setup/run/rules guide) and this file | Lee Guan Feng | #12 |
| v1.0.0 release | First complete working, tested, containerised end-to-end release | Lee Guan Feng | tag v1.0.0 |

The starter versions of the four managers were added just to get the app
running; the owners below should replace/extend them and take the credit.

## Up for grabs (the real feature work)

Pick one, build it on a branch, open a PR, then add your name here.

| Feature | Description | Owner |
| --- | --- | --- |
| `io_manager.py` | Input collection, validation and re-prompting; the display functions | Lee Guan Feng |
| `ai_manager.py` | The Groq call, JSON parsing, schema validation and error handling | Pair A |
| `logic_manager.py` | The business rules: priority, score, checklist and the decision table | Pair B |
| `data_manager.py` | Save / load / query of reports, including missing/corrupt file handling | Pair C |
| Report filtering | Use `query()` to filter saved reports by priority in the menu | Pair C |
| Report status updates | Let users mark a report as handled / ignored | TBD |

## How to add your credit

1. Do your work on a branch and open a pull request (see the README).
2. When it is merged, move the feature into the "Done" table with your name
   and the PR number.
3. Keep descriptions short - one line is enough.
