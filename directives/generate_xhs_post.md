# 샤오홍슈 날씨 게시물 생성 지침 (Gemini 프롬프트 가이드)

기상청에서 가져온 날씨 데이터를 기반으로 사용자 제공 양식에 맞춰 샤오홍슈(XHS) 게시물을 생성합니다.

## 입력 데이터
- `weather_data`: `fetch_weather_data.md`를 통해 정제된 데이터.
- `language`: 중국어(기본) 및 한국체 병기.

## 프롬프트 전략
1. **톤앤매너**: 감성적, 전문적, 친절함. 이모지 적극 활용.
2. **필수 섹션**:
    - 📆 날짜와 요일
    - 🕛 시간 (실시간 업데이트 표시)
    - 📢 [今日天气重点 / Today's Weather]
    - 👕 [穿搭建议 / OOTD]
    - ✅ [旅行小贴士 / Tips]
    - 🏷️ Hashtags

## 양식 예시 (사용자 제공)
```markdown
📆 日期：{date}（{day_of_week}）
🕛 时间： {time} (实时更新)

📢 [今日天气重点 / Today's Weather]
{weather_summary}

👕 [穿搭建议 / OOTD]
{ootd_suggestion}

✅ [旅行小贴士 / Tips]
{travel_tips}

🏷️ Hashtags
#济州岛天气预报 #济州岛{month}月 ...
```
