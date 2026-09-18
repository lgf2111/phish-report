# Features and Contributions

This file records who built what, so everyone gets credit for their work.
Add a row when you finish a feature. Link the pull request if you can.

## Contributions

| Feature | Description | Owner | Status | PR / commit |
| --- | --- | --- | --- | --- |
| MVP (minimal working app) | First end-to-end version: the four managers wired together through `main.py` so a message goes input → AI → rules → save → display | Lee Guan Feng | Done | #? |
| DeepSeek AI integration | `ai_manager.py` calls the DeepSeek API, requests JSON and validates the reply | Lee Guan Feng | Done | #? |
| Business rules | `logic_manager.py`: five-tier priority, score and checklist | Lee Guan Feng (starter, to be extended by Pair B) | Done | #? |
| JSON storage | `data_manager.py`: save/load/query reports to `reports.json` | Lee Guan Feng (starter, to be extended by Pair C) | Done | #? |
| Offline tests | `tests/test_logic_manager.py`: tests the rules with fake AI answers, no live API | Lee Guan Feng | Done | #? |
| Docker | `Dockerfile` plus `docker.sh` helper so the app runs the same on any laptop | Lee Guan Feng | Done | #? |
| GitHub Actions CI | `.github/workflows/ci.yml`: runs tests and builds/tests the Docker image on every push and PR | Lee Guan Feng | Done | #1 |
| Project docs | `README.md` (setup/run guide) and this file | Lee Guan Feng | Done | #? |

## To do (up for grabs)

Replace the owner when you pick one up.

| Feature | Description | Owner |
| --- | --- | --- |
| Input collection & validation | Flesh out `io_manager.py`: nicer prompts, stronger validation and re-prompting | Lee Guan Feng |
| Real AI error handling | Retries and clear messages for timeouts / bad JSON in `ai_manager.py` | Pair A |
| Extended rules | More rules and a full decision table in `logic_manager.py` | Pair B |
| Report filtering | Use `query()` to filter saved reports by priority in the menu | Pair C |
| Report status updates | Let users mark a report as handled / ignored | TBD |

## How to add your credit

1. Do your work on a branch and open a pull request (see the README).
2. When it is merged, add a row above with your name and the PR number.
3. Keep descriptions short - one line is enough.
