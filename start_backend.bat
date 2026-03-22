@echo off
set PYTHON_EXE="C:\Users\k9746\AppData\Local\Programs\Python\Python314\python.exe"

echo [1/3] 필요한 라이브러리 설치 중...
%PYTHON_EXE% -m pip install requests python-dotenv google-generativeai fastapi uvicorn

echo.
echo [2/3] 백엔드 폴더로 이동...
cd backend

echo.
echo [3/3] 백엔드 서버 실행 중 (FastAPI)...
%PYTHON_EXE% main.py

pause

