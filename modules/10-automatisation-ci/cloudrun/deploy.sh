#!/usr/bin/env bash
# Déploie le service revue-scr sur Cloud Run, clé API dans Secret Manager.
# Prérequis : gcloud authentifié, projet sélectionné, facturation active.
# Usage : PROJECT_ID=mon-projet ./deploy.sh
set -euo pipefail
cd "$(dirname "$0")"
: "${PROJECT_ID:?définir PROJECT_ID}"
REGION="${REGION:-europe-west9}"          # Paris
SERVICE="${SERVICE:-revue-scr}"
SECRET="${SECRET:-anthropic-api-key}"
SA="${SERVICE}-sa@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud services enable run.googleapis.com secretmanager.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com --project "$PROJECT_ID"

# 1. Secret : créé une fois, la valeur est lue sur stdin (jamais dans l'historique shell).
if ! gcloud secrets describe "$SECRET" --project "$PROJECT_ID" >/dev/null 2>&1; then
  echo "Colle la clé API Anthropic puis Ctrl-D :"
  gcloud secrets create "$SECRET" --project "$PROJECT_ID" --data-file=-
fi

# 2. Compte de service dédié, seul autorisé à lire le secret.
gcloud iam service-accounts describe "$SA" --project "$PROJECT_ID" >/dev/null 2>&1 ||
  gcloud iam service-accounts create "${SERVICE}-sa" --project "$PROJECT_ID"
gcloud secrets add-iam-policy-binding "$SECRET" --project "$PROJECT_ID" \
  --member "serviceAccount:$SA" --role roles/secretmanager.secretAccessor >/dev/null

# 3. Référentiel embarqué dans l'image (source unique : le skill du repo).
mkdir -p referentiel
cp ../../../.claude/skills/scr-marche/SKILL.md referentiel/SKILL.md

# 4. Build (Cloud Build) + déploiement, accès authentifié uniquement.
gcloud run deploy "$SERVICE" --project "$PROJECT_ID" --region "$REGION" --source . \
  --service-account "$SA" --no-allow-unauthenticated \
  --set-secrets "ANTHROPIC_API_KEY=${SECRET}:latest" \
  --memory 512Mi --max-instances 3 --timeout 300

URL="$(gcloud run services describe "$SERVICE" --project "$PROJECT_ID" --region "$REGION" --format 'value(status.url)')"
echo "Service : $URL"
echo "Test : curl -H \"Authorization: Bearer \$(gcloud auth print-identity-token)\" $URL/health"
