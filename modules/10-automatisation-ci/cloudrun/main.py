"""Service Cloud Run : revue d'une note de calcul SCR marché par Claude.

Le référentiel du skill `scr-marche` sert de prompt système (mis en cache : il est
identique d'une requête à l'autre). Clé API injectée par Secret Manager dans
ANTHROPIC_API_KEY — jamais dans l'image ni dans le code.

    POST /revue   {"note": "<texte de la note>"}  →  {"revue": "...", "usage": {...}}
    GET  /health
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Annotated

import anthropic
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")
REFERENTIEL = Path(
    os.environ.get(
        "REFERENTIEL_PATH",
        Path(__file__).resolve().parents[3] / ".claude/skills/scr-marche/SKILL.md",
    )
)

app = FastAPI(title="revue-scr", version="0.1.0")


class Demande(BaseModel):
    note: str = Field(min_length=20, max_length=100_000)


class Reponse(BaseModel):
    revue: str
    usage: dict[str, int]


@lru_cache
def systeme() -> str:
    return (
        "Tu es actuaire valideur de second niveau. Relis la note de calcul SCR marché fournie : "
        "erreurs certaines (avec article et correction), points d'attention, SCR corrigé. "
        "Le référentiel ci-dessous fait foi sur ta mémoire.\n\n<referentiel>\n"
        + REFERENTIEL.read_text(encoding="utf-8")
        + "\n</referentiel>"
    )


@lru_cache
def client_claude() -> anthropic.AsyncAnthropic:
    return anthropic.AsyncAnthropic()  # lit ANTHROPIC_API_KEY


@app.get("/health")
async def health() -> dict:
    return {"statut": "ok", "modele": MODEL}


@app.post("/revue", response_model=Reponse)
async def revue(
    demande: Demande, client: Annotated[anthropic.AsyncAnthropic, Depends(client_claude)]
) -> Reponse:
    try:
        reponse = await client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=[{"type": "text", "text": systeme(), "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": f"<note>\n{demande.note}\n</note>"}],
            thinking={"type": "adaptive"},
            output_config={"effort": "medium"},
            # Refus d'un classifieur de sécurité → relance serveur sur un modèle de repli.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except anthropic.RateLimitError as e:
        raise HTTPException(429, "limite de débit Claude atteinte, réessayer plus tard") from e
    except anthropic.APIStatusError as e:
        raise HTTPException(502, f"erreur API Claude ({e.status_code})") from e
    except anthropic.APIConnectionError as e:
        raise HTTPException(503, "API Claude injoignable") from e
    if reponse.stop_reason == "refusal":
        raise HTTPException(422, "requête refusée par les garde-fous du modèle")
    u = reponse.usage
    return Reponse(
        revue="\n".join(b.text for b in reponse.content if b.type == "text"),
        usage={
            "input": u.input_tokens,
            "output": u.output_tokens,
            "cache_write": u.cache_creation_input_tokens or 0,
            "cache_read": u.cache_read_input_tokens or 0,
        },
    )
