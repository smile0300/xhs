from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import os
from datetime import datetime

app = FastAPI()

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EXECUTION_DIR = os.path.join(os.path.dirname(__file__), "..", "execution")
TMP_DIR = os.path.join(os.path.dirname(__file__), "..", ".tmp")

@app.get("/generate/{date_str}")
async def generate_post(date_str: str):
    """
    1. 날씨 데이터 페칭
    2. 게시물 생성
    3. 결과 반환
    """
    # 1. Fetch Weather
    try:
        # python 명령어가 환경에 따라 다를 수 있으므로 적절히 수정 필요
        # 우선 'python'으로 시도
        subprocess.run(["python", os.path.join(EXECUTION_DIR, "fetch_weather.py"), date_str], check=True)
    except Exception as e:
        # 'python' 실패 시 'py' 등으로 재시도 로직 추가 가능
        try:
            subprocess.run(["py", os.path.join(EXECUTION_DIR, "fetch_weather.py"), date_str], check=True)
        except:
            raise HTTPException(status_code=500, detail=f"Weather fetch failed: {str(e)}")

    # 2. Generate Post
    try:
        subprocess.run(["python", os.path.join(EXECUTION_DIR, "generate_post.py"), date_str], check=True)
    except Exception as e:
        try:
            subprocess.run(["py", os.path.join(EXECUTION_DIR, "generate_post.py"), date_str], check=True)
        except:
            raise HTTPException(status_code=500, detail=f"Post generation failed: {str(e)}")

    # 3. Read Result
    post_path = os.path.join(TMP_DIR, f"post_{date_str}.txt")
    if os.path.exists(post_path):
        with open(post_path, "r", encoding="utf-8") as f:
            content = f.read()
            return {"content": content}
    else:
        raise HTTPException(status_code=404, detail="Generated post not found")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
