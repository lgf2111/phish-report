# Features and Contributions

This file records who built what, so everyone gets credit for their work.
Add a row when you finish a feature. Link the pull request if you can.

## Done so far

The project scaffolding and DevOps setup are in place. The four managers have
working starter versions so the app runs end to end, but they are meant to be
built out by their owners (see "Up for grabs" below).

| Feature | Description | Owner | PR / commit |
| --- | --- | --- | --- |
| Project setup & MVP wiring | Repo layout, `main.py` connecting the pipeline, and starter stubs so the app runs end to end | Lee Guan Feng | #? |
| Offline tests | `tests/test_logic_manager.py`: tests the rules with fake AI answers, no live API | Lee Guan Feng | #? |
| Docker | `Dockerfile` plus `docker.sh` helper so the app runs the same on any laptop | Lee Guan Feng | #? |
| GitHub Actions CI | `.github/workflows/ci.yml`: runs tests and builds/tests the Docker image on every push and PR | Lee Guan Feng | #1 |
| Project docs | `README.md` (setup/run guide) and this file | Lee Guan Feng | #? |

The starter versions of the four managers were added just to get the app
running; the owners below should replace/extend them and take the credit.

## Up for grabs (the real feature work)

Pick one, build it on a branch, open a PR, then add your name here.

| Feature | Description | Owner |
| --- | --- | --- |
| `io_manager.py` | Input collection, validation and re-prompting; the display functions | Lee Guan Feng |
| `ai_manager.py` | The DeepSeek call, JSON parsing, schema validation and error handling | Pair A |
| `logic_manager.py` | The business rules: priority, score, checklist and the decision table | Pair B |
| `data_manager.py` | Save / load / query of reports, including missing/corrupt file handling | Pair C |
| Report filtering | Use `query()` to filter saved reports by priority in the menu | Pair C |
| Report status updates | Let users mark a report as handled / ignored | TBD |

## How to add your credit

1. Do your work on a branch and open a pull request (see the README).
2. When it is merged, move the feature into the "Done" table with your name
   and the PR number.
3. Keep descriptions short - one line is enough.
