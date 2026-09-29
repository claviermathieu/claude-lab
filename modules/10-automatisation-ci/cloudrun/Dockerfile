FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
# Copié par deploy.sh depuis .claude/skills/scr-marche/SKILL.md
COPY referentiel/SKILL.md referentiel/SKILL.md
ENV REFERENTIEL_PATH=/app/referentiel/SKILL.md

# Cloud Run fournit $PORT ; utilisateur non root.
RUN useradd --create-home app
USER app
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
