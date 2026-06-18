@echo off
REM Push this frontend to the remote GitHub repository specified below.
SET REMOTE_URL=https://github.com/bhoomika1705126/Sugama-Sanchara.git
if not exist .git (
  git init
)
git add .
ngit commit -m "chore: add frontend Sugama Sanchara" || echo "No changes to commit"
ngit branch -M main
ngit remote remove origin 2>nul || echo ""
ngit remote add origin %REMOTE_URL%
echo Ensure you have configured git credentials (PAT or credential helper) to push to GitHub.
git push -u origin main
