@echo off
echo Closing existing Chrome...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo Launching Chrome with remote debug port 9222...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\Users\ThinK Pad\AppData\Local\Google\Chrome\User Data" ^
  --profile-directory=Default ^
  --start-maximized ^
  --no-first-run ^
  https://www.linkedin.com/feed/

echo.
echo Chrome launched! Wait for LinkedIn to load, then run:
echo   node post_linkedin.js
echo.
pause
