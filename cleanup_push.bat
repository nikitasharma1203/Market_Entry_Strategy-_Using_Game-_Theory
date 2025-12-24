@echo off
REM === Step 1: Remove large file from history ===
git filter-branch --force --index-filter ^
  "git rm --cached --ignore-unmatch output_file.csv" ^
  --prune-empty --tag-name-filter cat -- --all

REM === Step 2: Delete old refs created by filter-branch ===
rd /s /q .git\refs\original

REM === Step 3: Expire reflog ===
git reflog expire --expire=now --all

REM === Step 4: Garbage collect (skip prompts automatically) ===
git gc --prune=now --aggressive --quiet

REM === Step 5: Force push cleaned history ===
git push origin main --force

echo.
echo === Cleanup and force push complete! ===
pause
