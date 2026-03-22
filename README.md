# 샤오홍슈 날씨 게시물 생성기 실행 가이드

이 프로젝트는 기상청 API와 Google Gemini API를 연동하여 제주도 날씨 게시물을 자동으로 생성하는 웹앱입니다.

## 1. API 키 설정

`.env` 파일에 아래 키들을 설정해야 합니다.

- `KMA_API_KEY`: 기상청 API 키 (이미 설정됨)
- `GEMINI_API_KEY`: Google Gemini API 키

### Gemini API 키 발급 방법
1. [Google AI Studio](https://aistudio.google.com/app/apikey)에 접속합니다.
2. 'Create API key' 버튼을 눌러 키를 발급받습니다.
3. 발급받은 키를 `.env` 파일의 `GEMINI_API_KEY=` 뒤에 붙여넣으세요.

## 2. 프로젝트 실행 방법

### 백엔드 (FastAPI) 실행
1. 터미널에서 `xhs` 폴더로 이동합니다.
2. 필요한 라이브러리를 설치합니다:
   ```bash
   pip install requests python-dotenv google-generativeai fastapi uvicorn
   ```
3. 백엔드 서버를 실행합니다:
   ```bash
   cd backend
   python main.py
   ```

### 프론트엔드 (Vite) 실행
1. 새 터미널을 열고 `xhs/frontend` 폴더로 이동합니다.
2. 프론트엔드 서버를 실행합니다:
   ```bash
   npm run dev
   ```
3. 브라우저에서 출력된 주소(예: `http://localhost:5173`)로 접속합니다.

## 3. 주요 기능
- **날짜 선택**: 원하는 날짜의 날씨로 게시물을 생성할 수 있습니다. (기상청 예보 범위 내)
- **자동 생성**: 버튼 하나로 기상청 데이터 수집부터 Gemini 게시물 작성까지 완료됩니다.
- **프리미엄 UI**: 다크 모드와 글래스모피즘이 적용된 세련된 디자인을 제공합니다.
- **복사 기능**: 생성된 내용을 원클릭으로 복사하여 샤오홍슈에 바로 업로드할 수 있습니다.
