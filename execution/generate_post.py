import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_xhs_post(weather_data, target_date):
    """
    날씨 데이터를 기반으로 샤오홍슈 게시물 생성
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 날씨 데이터를 텍스트로 정리
    weather_summary = ""
    for region_id, data in weather_data.items():
        summary = data['summary']
        weather_summary += f"- {data['name']}: 최저 {summary['tmp_min']}°C, 최고 {summary['tmp_max']}°C, 풍속 {summary['wsd']}m/s\n"


    prompt = f"""
당신은 샤오홍슈(Xiaohongshu)의 인기 여행 인플루언서입니다. 
제주도의 날씨를 안내하는 게시물을 중국어로 작성해주세요. (한국어 번역도 병기)

[날짜]
{target_date}

[날씨 데이터]
{weather_summary}

[게시물 양식 가이드]
📆 日期：{target_date} (요일 포함)
🕛 时间： (현재 시간) (实时更新)

📢 [今日天气重点 / Today's Weather]
- 제주도 전체적인 날씨 요약 (맑음/흐림, 강수여부)
- 주요 지역(제주시, 서귀포시) 기온 비교 및 특징 설명
- 바람 세기에 따른 야외 활동 적합성 언급

👕 [穿搭建议 / OOTD]
- 기온에 따른 옷차림 추천 (자켓, 코트, 선글라스 등)

✅ [旅行小贴士 / Tips]
- 추천 여행 코스나 주의사항 (예: 남부 지역 추천 등)

✈️ 마지막에 제주 여행 도우미 멘트와 해시태그 포함

결과는 마크다운 형식을 제외하고 텍스트로만 출력해줘.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return None

def main(date_str):
    input_path = os.path.join(".tmp", f"weather_{date_str}.json")
    if not os.path.exists(input_path):
        print(f"Weather data file not found: {input_path}")
        return
        
    with open(input_path, "r", encoding="utf-8") as f:
        weather_data = json.load(f)
        
    print("Generating XHS post with Gemini...")
    post_content = generate_xhs_post(weather_data, date_str)
    
    if post_content:
        output_path = os.path.join(".tmp", f"post_{date_str}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(post_content)
        print(f"Post content saved to {output_path}")
        print("\n--- Generated Post ---\n")
        print(post_content)
    else:
        print("Failed to generate post.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_post.py <YYYYMMDD>")
    else:
        main(sys.argv[1])
