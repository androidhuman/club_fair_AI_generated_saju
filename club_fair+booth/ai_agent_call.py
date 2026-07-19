import streamlit as st
import google.generativeai as genai


def generate_report_with_snack(name, saju_text, snacks):
    """사주 데이터를 바탕으로 Gemini API를 호출하여 분석지와 간식 처방을 생성하는 함수"""

    # 1. Streamlit 비밀금고에서 API 키를 꺼내와 구글 AI 서버에 인증
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # 2. 간식 리스트 텍스트화 (예: "초코파이, 하리보 젤리, 비타민 음료, 사탕")
    snack_list_text = ", ".join(snacks)

    # 3. 시스템 프롬프트: AI의 성격과 지시사항 세팅
    system_prompt = f"""
    너는 20대 대학생들을 대상으로 유쾌하고 센스 있게 사주를 풀이해 주는 '동아리 부스 마스코트 역술가'야.

    [임무]
    1. 제공된 사주 데이터를 바탕으로 사용자의 올해 운세, 학업운, 대인관계 등을 각각 3~4문장으로 재미있게 해석해 줘. 너무 무겁지 않게 트렌디한 말투를 사용해.
    2. 부스에 준비된 간식 리스트({snack_list_text}) 중 딱 1개를 선택해서 '오늘의 처방전'으로 추천해 줘. 
    3. 왜 그 간식을 추천했는지 사주 풀이와 자연스럽게 엮어서 1~2줄로 설명해 줘.

    [출력 형식]
    마크다운(Markdown)을 활용해서 글씨를 굵게 하거나 목록을 만들어 가독성 좋게 작성해 줘. 이모지도 적극적으로 사용해.
    """

    # 4. Gemini 모델 설정 (Flash 모델 사용, 시스템 명령어 주입)
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=system_prompt
    )

    # 5. 사용자 프롬프트
    user_prompt = f"이름: {name}\n사주 데이터: {saju_text}"

    # 6. 결과 생성 (창의성 조절을 위해 temperature 0.7 설정)
    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7
        )
    )

    # 7. 텍스트 결과만 반환
    return response.text
