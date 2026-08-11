from typing import Dict, List

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_agent import generate_answer, load_history, summarize_history
from multi_agent import graph

from fastapi import Request
import time
from typing import Dict, List, Literal

from fastapi.responses import StreamingResponse

import sqlite3
from pathlib import Path
from datetime import datetime, timezone

db_path = Path(
    r"C:\Users\micro\Documents\ABTalksAI-Cohort\data\coverage.db"
)

# SQL FUNCTION


def save_message(session_id, role, content):
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO conversations (
                session_id,
                role,
                content,
                timestamp
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                session_id,
                role,
                content,
                datetime.now(timezone.utc).isoformat()
            )
        )
        conn.commit()



# PYDANTIC CLASSES

class ChatRequest(BaseModel):
    session_id: int
    member_id: int
    message: str


class SessionTurn(BaseModel):
    role: str
    message: str


class ChatResponse(BaseModel):
    session_id: int
    member_id: int
    answer: str
    structure: str
    chunk_ids: List[str]
    tool_result: dict | None
    history: List[SessionTurn]


class SessionState(BaseModel):
    session_id: int
    member_id: int
    history: List[SessionTurn]


# In-memory session store keyed by session_id.
# For future persistence, this can be replaced with a SQLite-backed store.
session_store: Dict[int, SessionState] = {}


def get_session(session_id: int, member_id: int) -> SessionState:
    session = session_store.get(session_id)
    if session is None:
        session = SessionState(session_id=session_id, member_id=member_id, history=[])
        session_store[session_id] = session
    elif session.member_id != member_id:
        session.member_id = member_id
    return session


app = FastAPI()

# Add middelware for timeout + error logging

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        print(
            f"{request.method} {request.url.path} "
            f"| status={status_code} "
            f"| time={elapsed_ms:.2f} ms"
        )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest):
    session = get_session(request.session_id, request.member_id)

    session.history.append(
        SessionTurn(role="user", message=request.message)
    )

    save_message(
        session_id=session.session_id,
        role="user",
        content=request.message
    )

    try:

 
        summarize_history(
            request.session_id,
            token_limit=2000
        )

        history = load_history(
            request.session_id,
            limit=10
        )

        result = await graph.ainvoke({
            "session_id": request.session_id,
            "question": request.message
        })

        context = result["context"]
        structure = result["structure"]
        chunk_ids = result["chunk_ids"]
        tool_result = result["tool_result"]
        instructions = result["instructions"]

        print("ROUTE:", result["route"])


        context += f"""
        Conversation history:
        {history}

        """

        def stream():
            assistant_turn = SessionTurn(
                role="assistant",
                message=""
            )
            session.history.append(assistant_turn)

            for token in generate_answer(request.message, context, instructions):
                assistant_turn.message += token

                response = ChatResponse(
                    session_id=session.session_id,
                    member_id=session.member_id,
                    answer=token,
                    structure=structure,
                    chunk_ids = chunk_ids,
                    tool_result=tool_result,
                    history=session.history,
                )

                yield f"data: {response.model_dump_json()}\n\n"
            
            save_message(
                session_id=request.session_id,
                role="assistant",
                content=assistant_turn.message
            )


        return StreamingResponse(
            stream(),
            media_type="text/event-stream"
        )

    except Exception as error:
        print("Chat endpoint error:", error)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )




@app.get("/history/{session_id}", response_model=SessionState)
def history(session_id: int):
    session = session_store.get(session_id)
    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    print("Session History:", session.history)

    return session