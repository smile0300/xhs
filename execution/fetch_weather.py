import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

KMA_API_KEY = os.getenv("KMA_API_KEY")

# 제주도 주요 지역 격자 좌표
REGIONS = {
    "jeju_city": {"name": "제주시", "nx": 52, "ny": 38},
    "seogwipo": {"name": "서귀포시", "nx": 52, "ny": 33},
    "seongsan": {"name": "성산", "nx": 57, "ny": 34},
    "gosan": {"name": "고산", "nx": 48, "ny": 36}
}

def fetch_weather(target_date, nx, ny):
    """
    기상청 단기예보 API 호출 (getVilageFcst)
    target_date: YYYYMMDD
    """
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    
    # 단기예보는 보통 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300에 발표됨
    # 여기서는 가장 최근 발표 시간을 고정하거나 파라미터화할 수 있음. 
    # 일단 0500 발표 기준 (당일 예보 포함)
    base_time = "0500" 
    
    params = {
        "serviceKey": KMA_API_KEY,
        "numOfRows": 1000,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": target_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['response']['header']['resultCode'] != '00':
            print(f"Error from KMA: {data['response']['header']['resultMsg']}")
            return None
            
        items = data['response']['body']['items']['item']
        return items
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def process_weather_data(items, target_date):
    """
    API 결과에서 필요한 정보 추출
    - 요약 데이터 (최저/최고기온 등)
    - 시간대별 데이터 (기온, 하늘상태, 강수확률 등)
    """
    summary = {
        "tmp_min": None,
        "tmp_max": None,
        "pop": 0,
        "sky": 1,
        "wsd": 0
    }
    hourly = []
    
    # 시간대별 정리를 위해 딕셔너리 사용
    hourly_map = {}

    for item in items:
        if item['fcstDate'] == target_date:
            time = item['fcstTime']
            if time not in hourly_map:
                hourly_map[time] = {"time": f"{time[:2]}:{time[2:]}", "tmp": None, "sky": 1, "pty": 0, "pop": 0}
            
            category = item['category']
            val = item['fcstValue']
            
            if category == 'TMN':
                summary['tmp_min'] = float(val)
            elif category == 'TMX':
                summary['tmp_max'] = float(val)
            elif category == 'POP':
                summary['pop'] = max(summary['pop'], int(val))
                hourly_map[time]['pop'] = int(val)
            elif category == 'SKY':
                summary['sky'] = int(val)
                hourly_map[time]['sky'] = int(val)
            elif category == 'PTY':
                hourly_map[time]['pty'] = int(val)
            elif category == 'TMP':
                hourly_map[time]['tmp'] = float(val)
            elif category == 'WSD':
                summary['wsd'] = max(summary['wsd'], float(val))
                
    # 시간순 정렬
    sorted_times = sorted(hourly_map.keys())
    hourly = [hourly_map[t] for t in sorted_times]
    
    return {"summary": summary, "hourly": hourly}

def main(date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%Y%m%d")
        
    all_weather = {}
    for region_id, info in REGIONS.items():
        print(f"Fetching weather for {info['name']}...")
        items = fetch_weather(date_str, info['nx'], info['ny'])
        if items:
            processed = process_weather_data(items, date_str)
            all_weather[region_id] = processed
            all_weather[region_id]['name'] = info['name']
            
    output_path = os.path.join(".tmp", f"weather_{date_str}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_weather, f, ensure_ascii=False, indent=2)
    
    print(f"Weather data saved to {output_path}")
    return all_weather


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else None
    main(target)
