import requests
import xml.etree.ElementTree as ET
import streamlit as st


def get_saju_data(year, month, day, hour, time_unknown):
    """한국천문연구원 API를 호출하여 날짜를 사주 8글자(간지)로 변환하는 함수"""

    try:
        # 1. 비밀금고에서 천문연구원 API 키 가져오기
        service_key = st.secrets["KASI_API_KEY"]

        # 2. API 주소 및 파라미터 세팅
        url = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getLunCalInfo"

        # API는 월과 일을 '01', '09' 같은 2자리 문자열로 요구합니다.
        params = {
            "solYear": str(year),
            "solMonth": f"{month:02d}",
            "solDay": f"{day:02d}",
            "ServiceKey": service_key
        }

        # 3. 천문연구원 서버에 데이터 요청 (응답 대기 시간 5초 제한)
        response = requests.get(url, params=params, timeout=5)

        # 4. 받아온 XML 데이터 해석
        if response.status_code == 200:
            root = ET.fromstring(response.text)

            # 세차(년), 월건(월), 일진(일) 한자 데이터 추출
            year_ganji = root.find('.//lunSecha')
            month_ganji = root.find('.//lunWolgeon')
            day_ganji = root.find('.//lunIljin')

            # 데이터를 성공적으로 찾았다면
            if year_ganji is not None:
                time_str = "모름" if time_unknown else f"{hour}시"

                # AI가 알아먹기 쉽게 문자열로 묶어서 반환
                return f"{year_ganji.text}(년) {month_ganji.text}(월) {day_ganji.text}(일) / 태어난 시간: {time_str}"

    except Exception as e:
        # 부스 운영 중 인터넷이 끊겨도 에러 창이 뜨지 않도록 숨김 처리
        print(f"사주 API 에러: {e}")

    # ==========================================
    # 5. 비상용 로직 (API 실패 시 작동)
    # ==========================================
    # 인터넷 문제로 API가 실패하면 띠(십이지)만 계산해서 AI에게 넘겨줍니다.
    # AI는 이 정보만으로도 충분히 그럴싸하게 운세를 지어낼 수 있습니다.
    zodiac_animals = ["원숭이", "닭", "개", "돼지", "쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양"]
    animal = zodiac_animals[year % 12]

    return f"{year}년생 ({animal}띠) - 상세 한자 데이터 누락됨"