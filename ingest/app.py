"""Tiny fleet-health ingest API. Generic JSON. No customer data. No vendor protocols."""

import os
from typing import Any

import pymysql
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DATABASE_HOST = os.getenv("DATABASE_HOST", "127.0.0.1")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "3306"))
DATABASE_USER = os.getenv("DATABASE_USER", "ingest")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "ingest")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fleet")


class HealthIn(BaseModel):
    host: str = Field(min_length=1, max_length=128)
    cpu_pct: float = Field(ge=0, le=100)
    mem_pct: float = Field(ge=0, le=100)
    ok: bool


app = FastAPI(title="fleet-health-ingest", version="0.1.0")


def _connect() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest")
def ingest(payload: HealthIn) -> dict[str, Any]:
    try:
        conn = _connect()
    except pymysql.Error as exc:
        raise HTTPException(status_code=503, detail=f"database unavailable: {exc}") from exc

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO health_events (host, cpu_pct, mem_pct, ok)
                VALUES (%s, %s, %s, %s)
                """,
                (payload.host, payload.cpu_pct, payload.mem_pct, payload.ok),
            )
            event_id = cur.lastrowid
    finally:
        conn.close()

    return {"id": event_id, "stored": True}


@app.get("/latest")
def latest(limit: int = 20) -> dict[str, Any]:
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=400, detail="limit must be 1-200")

    try:
        conn = _connect()
    except pymysql.Error as exc:
        raise HTTPException(status_code=503, detail=f"database unavailable: {exc}") from exc

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, host, cpu_pct, mem_pct, ok, received_at
                FROM health_events
                ORDER BY id DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    for row in rows:
        if row.get("received_at") is not None:
            row["received_at"] = row["received_at"].isoformat()
        if row.get("cpu_pct") is not None:
            row["cpu_pct"] = float(row["cpu_pct"])
        if row.get("mem_pct") is not None:
            row["mem_pct"] = float(row["mem_pct"])
        row["ok"] = bool(row["ok"])

    return {"count": len(rows), "events": rows}
