@echo off
echo === Project Verification ===
echo.

echo Checking key files...
echo.

echo 1. bin/app.ts:
if exist bin\app.ts (
    echo    [OK] File exists
    echo    First 5 lines:
    powershell -Command "Get-Content bin\app.ts -TotalCount 5"
) else (
    echo    [ERROR] File not found
)
echo.

echo 2. lib/ai-agent-stack.ts:
if exist lib\ai-agent-stack.ts (
    echo    [OK] File exists
    echo    File size:
    powershell -Command "(Get-Item lib\ai-agent-stack.ts).Length"
    echo    bytes
) else (
    echo    [ERROR] File not found
)
echo.

echo 3. Lambda functions:
if exist lambda\google-ads\index.py (
    echo    [OK] google-ads exists
) else (
    echo    [ERROR] google-ads missing
)

if exist lambda\meta-ads\index.py (
    echo    [OK] meta-ads exists
) else (
    echo    [ERROR] meta-ads missing
)

if exist lambda\analytics\index.py (
    echo    [OK] analytics exists
) else (
    echo    [ERROR] analytics missing
)

if exist lambda\budget-optimizer\index.py (
    echo    [OK] budget-optimizer exists
) else (
    echo    [ERROR] budget-optimizer missing
)

if exist lambda\storage\index.py (
    echo    [OK] storage exists
) else (
    echo    [ERROR] storage missing
)

echo.
echo === Summary ===
echo If any files are missing, the project is incomplete.
echo.
pause
