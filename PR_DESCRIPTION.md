Title: Improve frontend: OSRM routing, dynamic health badges, CI & push helpers

Summary
- Replaces static header badges with dynamic health/status badges that reflect backend and Flipkart state.
- Improves map diversion lines: attempts OSRM routing to follow roads and falls back to straight lines when routing fails.
- Adds push helper scripts, a minimal CI workflow, and a repo-wide syntax checker that excludes virtualenvs to avoid editor noise.

Files changed (high level)
- `app_old.py`: dynamic header badges (`get_system_status()`), OSRM routing helper (`get_route_osrm()`), diversion plotting enhancements.
- `.github/workflows/ci.yml`: minimal compile CI for Python files.
- `scripts/check_syntax.py`: repo-wide syntax compile tool (skips `venv` and common folders).
- `.vscode/settings.json`: excludes `venv` from VS Code analysis to remove permission errors.
- `push_to_github.bat` / `push_to_github.sh`: helper scripts to create and push the `frontend-update` branch.

Testing performed
- Ran `scripts/check_syntax.py` — all project `.py` files compile successfully (skips `venv`).
- Verified map routing uses OSRM geometry when available and falls back gracefully.
- Created and pushed `frontend-update` branch to the target remote; GitHub shows the PR suggestion URL.

How to review locally
1. Start backend (from backend repo):
   - Set `API_URL` to point at the backend (example for local backend): `set API_URL=http://127.0.0.1:8000` (PowerShell: `$env:API_URL='http://127.0.0.1:8000'`).
   - Run backend: `python -m uvicorn src.api:app --host 127.0.0.1 --port 8000`.
2. Run frontend:
   - `streamlit run app_old.py` (or `app.py` depending on your entrypoint).
3. Verify dynamic header badges reflect backend/Flipkart state and that map diversion lines follow roads for routed segments.

Merge checklist
- [ ] Confirm CI passes on the PR (compile-only check will run automatically).
- [ ] Optional: run end-to-end smoke test with backend running locally and check header badges + map routing.
- [ ] Approve and merge via GitHub UI or use the command line merge below.

Command-line merge (if you prefer):
```
# ensure main is up-to-date
git checkout main
git pull origin main
# merge the feature branch
git fetch origin
git merge --no-ff origin/frontend-update -m "Merge frontend-update: OSRM routing + dynamic badges"
git push origin main
```

Notes & next steps
- OSRM demo server is used by default; consider switching to a production routing provider (OpenRouteService/Mapbox/self-host OSRM) for reliability.
- If you want, I can open the PR on GitHub using your token or paste this content into the PR for you — tell me how you'd like to proceed.
