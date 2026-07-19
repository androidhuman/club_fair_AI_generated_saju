import streamlit as st
import google.generativeai as genai

def generate_report_with_snack(name, saju_text, snacks):
    try:
        # 1. API 키 불러오기 (공백 제거)
        raw_api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=raw_api_key.strip())
        
        # 2. 간식 리스트 텍스트화
        snack_list_text = ", ".join(snacks)
        
        # 3. 프롬프트 하나로 합치기 (에러 원천 차단)
        # 시스템 명령어와 사용자 데이터를 하나의 텍스트로 합쳐서 전달합니다.
        combined_prompt = f"""
        너는 20대 대학생들을 대상으로 유쾌하고 센스 있게 사주를 풀이해 주는 '동아리 부스 마스코트 역술가'야.
        
        [방문객 정보]
        이름: {name}
        사주 데이터: {saju_text}
        
        [임무]
        1. 제공된 사주 데이터를 바탕으로 사용자의 올해 운세, 학업운, 대인관계 등을 3~4문장으로 재미있게 해석해 줘. 너무 무겁지 않게 트렌디한 말투를 사용해.
        2. 부스에 준비된 간식 리스트({snack_list_text}) 중 딱 1개를 선택해서 '오늘의 처방전'으로 추천해 줘. 
        3. 왜 그 간식을 추천했는지 사주 풀이와 자연스럽게 엮어서 1~2줄로 설명해 줘.
        
        [출력 형식]
        마크다운(Markdown)을 활용해서 글씨를 굵게 하거나 목록을 만들어 가독성 좋게 작성해 줘. 이모지도 적극적으로 사용해.
        """
        
        # 4. 가장 안정적인 범용 모델(gemini-pro)로 변경하고, system_instruction 옵션 제거
        model = genai.GenerativeModel(model_name="gemini-pro")
        
        # 5. 결과 생성
        response = model.generate_content(
            combined_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7
            )
        )
        
        return response.text

    except Exception as e:
        error_msg = f"🚨 AI 서버와 통신하는 중 문제가 발생했습니다.\n\n(개발자용 에러 로그: {e})"
        return error_msg
