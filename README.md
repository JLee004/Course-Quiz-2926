# Software and AI Service Learning Quiz

A local, beginner-friendly quiz served by FastAPI. All 21 original questions are preserved, with 49 new lessons: **70 total, comprising 49 multiple-choice and 21 coding exercises** (17 Python, including library exercises, and 4 PostgreSQL SQL).

## Run

From this folder in a terminal:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. Stop the quiz server with Ctrl+C.

If you want to leave another service on port 8000 running, use `--port 8002` instead and open <http://127.0.0.1:8002>.

## How it works

- `app/questions.py` preserves the original lessons. `app/curriculum.py` adds lessons and defines the seven topic tabs. Keep IDs unique and stable.
- Choose Programming thinking, Python practice, Data & pipelines, Building services, AI tools & systems, Testing & reliability, or Statistics for ML.
- Each topic saves its own position, drafts, hints, and ideas to practice again. Mixed practice covers the whole bank. The 70/30 mix applies across the bank; individual topic mixes vary.
- Original progress migrates into Mixed practice on the same browser origin. The old storage entry remains as a backup. Changing port or browser creates a different storage location.
- `app/main.py` serves the page and three API routes: health, public questions, and answer feedback. FastAPI validates incoming answer data.
- `app/static/` contains the browser interface. It shows one question at a time and saves progress in this browser's `localStorage`.
- Multiple-choice answers are graded by the API. Coding answers are **not executed or automatically graded**. Your code remains in the browser; after submission the API returns a reference solution and you can revise your draft as often as you like. Equivalent correct solutions count.
- There are no scores or attempt limits. An incorrect choice offers another try, hints, or an optional walkthrough. Every submitted exercise can be retried.
- Choose “I understand this idea” or “Keep this for practice,” or simply continue when ready. Incorrect choices and code walkthroughs are saved for more practice until you mark the idea understood. The end screen offers reflection and revisiting, without grades.
- Existing progress and drafts are preserved. The old answer data is used only to suggest ideas to revisit; no scores are shown.

## Practical exercises

Data & pipelines includes PostgreSQL aggregation/upserts, pandas cleaning/time aggregation/validated joins, and scikit-learn preprocessing. Statistics includes NumPy sample standard deviation, SciPy binomial probability, and binary cross-entropy for classifiers and neural networks. New coding lessons give explicit input assumptions, examples, three hints, and a reference answer.

The quiz itself still requires only FastAPI and Uvicorn. For optional practice in your own Python files, install the library packages inside a virtual environment:

```sh
python -m pip install -r requirements-practice.txt
```

This does not add an automatic grader. Some exercises assume fixtures or objects explicitly named in the prompt. Source links are included in relevant feedback.

## Scope

Progress is local to one browser profile, and clearing browser storage resets it. There are no accounts or PostgreSQL database in the app itself; PostgreSQL is a learning topic. The question bank is fixed in order so returning learners can continue. Submitted code is never sent to the API or run on the server.

An automatic coding grader would need an isolated, resource-limited Python runner and a disposable SQL database. Do not run learner code inside the web server process.

Reference material: [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/), [Python](https://wikidocs.net/book/18202), and [SQL/PostgreSQL/FastAPI](https://wikidocs.net/book/18203).

For a beginner-friendly map of the files and learning flow, see [PROJECT_GUIDE.md](PROJECT_GUIDE.md).
