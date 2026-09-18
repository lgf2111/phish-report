# PhishReport

[![CI](https://github.com/lgf2111/phish-report/actions/workflows/ci.yml/badge.svg)](https://github.com/lgf2111/phish-report/actions/workflows/ci.yml)

A simple command-line tool that checks if a message looks like phishing.
You paste a suspicious message and say what you did (clicked a link, gave a
password, etc). The app sends the message to an AI, applies our rules, and
gives you a priority, a score and a checklist of what to do. Reports are saved
to a file so you can look at them later.

This is our INF team project (Phase 1). It is written in plain Python using
functions only (no classes), split into four "manager" files.

## How it fits together

```
you  ->  io_manager  ->  ai_manager  ->  logic_manager  ->  data_manager
        (ask/print)     (call the AI)    (the rules)        (save to file)
```

| File | What it does | Owner |
| --- | --- | --- |
| `app/io_manager.py` | Menu, questions and printing (all input/print live here) | Lee Guan Feng |
| `app/ai_manager.py` | Sends the message to the Groq API, checks the reply | Pair A |
| `app/logic_manager.py` | The rules: priority, score, checklist | Pair B |
| `app/data_manager.py` | Saves and loads reports (`reports.json`) | Pair C |
| `app/main.py` | Runs the menu and connects the four managers | shared |

## First-time setup

You need Python 3 installed. Then, from the project folder:

```bash
# 1. make a virtual environment (a private space for our packages)
python3 -m venv .venv

# 2. turn it on
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows

# 3. install what we need
pip install -r requirements.txt

# 4. add your API key
cp .env.example .env             # then open .env and paste your Groq key
```

Your key goes in `.env` like this:

```
GROQ_API_KEY=your_key_here
```

`.env` is gitignored, so your key never gets uploaded. Get a free key from the
Groq console (https://console.groq.com).

## Running the app

With the virtual environment turned on:

```bash
python app/main.py
```

You will see a menu:

```
=== PhishReport ===
1. Check a new message
2. View saved reports
3. Quit
```

Pick **1**, paste a message, answer the questions, and you get a result like:

```
Priority: high
Score: 90
What to do:
 - Recover your account through the official website.
 - Tell IT.
```

## Running the tests

The tests check the rules in `logic_manager` using fake AI answers, so they
run without the internet and without a key:

```bash
pytest
```

## Running in Docker

Docker makes the app run the same on everyone's laptop (this is graded). You
need Docker Desktop open. There is a helper script so you don't have to
remember the commands:

```bash
chmod +x docker.sh     # first time only
./docker.sh build      # build the image
./docker.sh run        # run the app (reads your key from .env)
./docker.sh test       # run the tests in the container
./docker.sh clean      # delete the image
```

## How we work together (Git)

Please don't commit straight to `main`. Instead:

```bash
git checkout main
git pull                              # get the latest
git checkout -b feat/your-thing       # make a branch for your work
# ... do your work, then ...
git add <your files>
git commit -m "short description of what you did"
git push -u origin feat/your-thing
```

Then open a Pull Request on GitHub and ask a teammate to review before
merging. Small, frequent commits with clear messages are what we're graded on,
so commit as you go rather than one big dump at the end.

## Code rules and automatic checks

Every push and pull request is checked automatically by GitHub Actions (you
don't run these yourself, they just run online). If something goes red, click
the failed check to see why. There are three checks:

**1. No classes allowed.** This is the big one. The assignment requires the
whole app to be written with functions only - **no `class` anywhere**. It's an
instant-fail rule for the grade, so CI will block any code in `app/` that
contains a class. If your check fails with a "found a class definition"
message, rewrite it using plain functions.

**2. Lint (ruff).** We run `ruff`, a linter that flags things like unused
imports, bad import order and over-long lines. To avoid surprises:

- Install the **Ruff extension** in your IDE (VS Code: search "Ruff"). It
  underlines problems as you type and can auto-fix them on save.
- Or run it yourself before pushing:

  ```bash
  ruff check .          # show problems
  ruff check . --fix    # fix the easy ones automatically
  ```

**3. Tests.** The tests in `tests/` run automatically. If you change the rules
in `logic_manager`, update or add a test so it still passes.

## Notes

- The AI reply is JSON with three true/false fields: `credential_request`,
  `suspicious`, `insufficient_context`. `logic_manager` turns those (plus what
  you did) into the priority.
- Never put real passwords or codes into the app. Use fake/sample messages.
- `reports.json` is created when you run the app and is gitignored.
