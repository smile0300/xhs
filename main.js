document.addEventListener('DOMContentLoaded', () => {
    const postDateInput = document.getElementById('post-date');
    const generateBtn = document.getElementById('generate-btn');
    const loading = document.getElementById('loading');
    const resultArea = document.getElementById('result-area');
    const postContent = document.getElementById('post-content');
    const copyBtn = document.getElementById('copy-btn');
    const hourlyArea = document.getElementById('hourly-area');
    const hourlyList = document.getElementById('hourly-list');

    // 날짜 범위 설정 (오늘 ~ 오늘+3일)
    const setupDatePicker = () => {
        const now = new Date();
        const today = now.toISOString().split('T')[0];
        
        const maxDate = new Date();
        maxDate.setDate(now.getDate() + 3);
        const maxStr = maxDate.toISOString().split('T')[0];

        postDateInput.value = today;
        postDateInput.min = today;
        postDateInput.max = maxStr;
    };

    setupDatePicker();

    const getSkyText = (sky, pty) => {
        if (pty > 0) {
            if (pty === 1) return '비 🌧️';
            if (pty === 2) return '비/눈 🌨️';
            if (pty === 3) return '눈 ❄️';
            if (pty === 4) return '소나기 🌦️';
        }
        if (sky === 1) return '맑음 ☀️';
        if (sky === 3) return '구름많음 ⛅';
        if (sky === 4) return '흐림 ☁️';
        return '미상';
    };

    const fetchHourly = async (dateStr) => {
        hourlyArea.style.display = 'none';
        
        try {
            const response = await fetch(`http://localhost:8000/hourly/${dateStr.replace(/-/g, '')}`);
            if (!response.ok) return;

            const data = await response.json();
            // 제주시 기준 (jeju_city)
            const jejuHourly = data.jeju_city.hourly;
            
            hourlyList.innerHTML = '';
            jejuHourly.forEach(item => {
                const div = document.createElement('div');
                div.className = 'hourly-item';
                div.innerHTML = `
                    <div class="hourly-time">${item.time}</div>
                    <div class="hourly-temp">${item.tmp}°C</div>
                    <div class="hourly-sky">${getSkyText(item.sky, item.pty)}</div>
                `;
                hourlyList.appendChild(div);
            });
            
            hourlyArea.style.display = 'block';
        } catch (error) {
            console.error('Hourly fetch failed:', error);
        }
    };

    // 초기 실행
    fetchHourly(postDateInput.value);

    // 날짜 변경 시 시간별 날씨 업데이트
    postDateInput.addEventListener('change', () => {
        fetchHourly(postDateInput.value);
    });

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
            const response = await fetch(`http://localhost:8000/generate/${selectedDate}`);
            if (!response.ok) {
                throw new Error('서버 에러가 발생했습니다. (기상청/Gemini 호출 실패)');
            }

            const data = await response.json();
            postContent.textContent = data.content;
            resultArea.style.display = 'block';
            resultArea.scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            console.error(error);
            alert(`오류 발생: ${error.message}\n\n백엔드 서버가 실행 중인지 확인해주세요.`);
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

