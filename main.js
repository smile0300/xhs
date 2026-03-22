document.addEventListener('DOMContentLoaded', () => {
    const postDateInput = document.getElementById('post-date');
    const generateBtn = document.getElementById('generate-btn');
    const loading = document.getElementById('loading');
    const resultArea = document.getElementById('result-area');
    const postContent = document.getElementById('post-content');
    const copyBtn = document.getElementById('copy-btn');

    // 기본 날짜를 오늘로 설정
    const today = new Date().toISOString().split('T')[0];
    postDateInput.value = today;

    generateBtn.addEventListener('click', async () => {
        const selectedDate = postDateInput.value.replace(/-/g, '');
        if (!selectedDate) {
            alert('날짜를 선택해주세요!');
            return;
        }

        // UI 초기화
        loading.style.display = 'block';
        resultArea.style.display = 'none';
        generateBtn.disabled = true;

        try {
            // FastAPI 백엔드 호출 (8000 포트 가정)
            const response = await fetch(`http://localhost:8000/generate/${selectedDate}`);
            if (!response.ok) {
                throw new Error('서버 에러가 발생했습니다. (기상청/Gemini 호출 실패)');
            }

            const data = await response.json();
            postContent.textContent = data.content;
            resultArea.style.display = 'block';
            
            // 결과 영역으로 스크롤
            resultArea.scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            console.error(error);
            alert(`오류 발생: ${error.message}\n\n백엔드 서버가 실행 중인지, 혹은 API 키가 올바른지 확인해주세요.`);
        } finally {
            loading.style.display = 'none';
            generateBtn.disabled = false;
        }
    });

    copyBtn.addEventListener('click', () => {
        const text = postContent.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '복사 완료! ✅';
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        });
    });
});
