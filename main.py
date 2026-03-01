from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database on startup."""
    database.init_db()
    yield


app = FastAPI(
    title="Tuck Advisors – ABC Synergy API",
    description="Serves and updates the AI-generated M&A synergy analysis for potential ABC buyers.",
    version="1.0.0",
    lifespan=lifespan,
)


class AppendRequest(BaseModel):
    content: str


@app.get("/analysis", summary="Get current analysis")
def get_analysis() -> dict:
    """
    Returns the current markdown analysis string stored in the database.
    Run seed.py first if the database has not been initialized.
    """
    markdown = database.get_content()
    if markdown is None:
        raise HTTPException(
            status_code=404,
            detail="No analysis found. Run `python seed.py` to initialize the database.",
        )
    return {"markdown": markdown}


@app.post("/analysis", summary="Append to analysis")
def append_analysis(body: AppendRequest) -> dict:
    """
    Appends the provided string to the end of the existing markdown analysis
    as a new sentence, then persists the result.
    """
    if not body.content.strip():
        raise HTTPException(status_code=422, detail="'content' must not be empty.")

    current = database.get_content()
    if current is None:
        raise HTTPException(
            status_code=404,
            detail="No analysis found. Run `python seed.py` to initialize the database.",
        )

    updated = current.rstrip() + "\n\n" + body.content.strip()
    database.set_content(updated)
    return {"markdown": updated}
