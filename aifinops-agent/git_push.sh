#!/bin/bash
set -e

echo "[GIT] Switching to aifinops-bootstrap branch..."
git checkout -B aifinops-bootstrap

echo "[GIT] Adding files..."
git add .

echo "[GIT] Committing..."
git commit -m "Add aifinops-agent package, API server, and installer" || echo "Nothing to commit."

echo "[GIT] Pushing..."
git push origin aifinops-bootstrap

if gh auth status >/dev/null 2>&1; then
  gh pr create --base main --head aifinops-bootstrap \
    --title "Add aifinops-agent onboarding system" \
    --body "This PR adds pip-agent, API server, GPU installer, connect flow."
else
  echo "gh CLI not logged in. Run: gh auth login"
fi

echo "=== DONE: Check GitHub for PR."
