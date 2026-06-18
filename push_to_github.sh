#!/usr/bin/env bash
# Push this frontend to the provided GitHub repository.
REMOTE_URL="https://github.com/bhoomika1705126/Sugama-Sanchara.git"
if [ ! -d .git ]; then
  git init
fi

git add .
if git diff --cached --quiet; then
  echo "No changes to commit"
else
  git commit -m "chore: add frontend Sugama Sanchara"
fi

git branch -M main

git remote remove origin 2>/dev/null || true

git remote add origin "$REMOTE_URL"

echo "Ensure you have set up git credentials (PAT) or SSH keys before pushing."

git push -u origin main
