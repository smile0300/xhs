# 기상청 날씨 데이터 페칭 지침

제주도의 주요 지역별 날씨 정보를 기상청 단기예보 API를 통해 가져오는 절차를 정의합니다.

## 입력 파라미터
- `target_date`: `YYYYMMDD` 형식의 날짜 (초단기/단기 예보 범위 내).
- `regions`: 제주도의 주요 거점 (제주시, 서귀포시, 성산, 고산 등).

## 기상청 격자 좌표 (nx, ny)
- **제주시**: nx=52, ny=38
- **서귀포시**: nx=52, ny=33
- **성산**: nx=57, ny=34
- **고산**: nx=48, ny=36

## API 호출 정보
- **Base URL**: `http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst` (단기예보)
- **ServiceKey**: `.env`의 `KMA_API_KEY` 사용.
- **DataType**: `JSON`

## 출력 데이터 형식
```json
{
  "date": "2026-03-21",
  "regions": {
    "jeju_city": { "temp_min": 3, "temp_max": 9, "pop": 0, "sky": 1, "wsd": 1.2 },
    "seogwipo": { "temp_min": 6, "temp_max": 16, "pop": 0, "sky": 1, "wsd": 0.8 },
    ...
  }
}
```
