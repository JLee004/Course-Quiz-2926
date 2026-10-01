"""FastAPI routes for the local learning quiz."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .questions import BY_ID, CATEGORIES, LEGACY_IDS, QUESTIONS, public_question

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Software and AI Service Learning Quiz", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class AnswerRequest(BaseModel):
    question_id: str
    selected_index: int | None = None


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/questions")
def get_questions():
    return {"version": 2, "categories": CATEGORIES, "legacy_ids": LEGACY_IDS,
            "questions": [public_question(q) for q in QUESTIONS]}


@app.post("/api/answers")
def check_answer(request: AnswerRequest):
    question = BY_ID.get(request.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    if question["kind"] == "choice":
        selected = request.selected_index
        if selected is None or not 0 <= selected < len(question["options"]):
            raise HTTPException(status_code=422, detail="Choose one of the listed answers")
        return {
            "kind": "choice",
            "correct": selected == question["correct"],
            "correct_index": question["correct"],
            "explanation": question["explanation"],
            "wrong": question["wrong"],
            "diagram": question.get("diagram"),
            "source": question.get("source"),
        }

    # This route deliberately receives no submitted code and runs no code or SQL.
    if request.selected_index is not None:
        raise HTTPException(status_code=422, detail="Coding questions do not use choices")
    return {
        "kind": "code",
        "reference": question["reference"],
        "syntax": question["syntax"],
        "service": question["service"],
        "pitfall": question["pitfall"],
        "source": question.get("source"),
    }
