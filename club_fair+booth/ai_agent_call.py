import streamlit as st
import google.generativeai as genai

def generate_report_with_snack(name, saju_text, snacks):
    try:
        # 1. API 키 불러오기
        raw_api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=raw_api_key.strip())
        
        # 2. [핵심] 내 API 키로 쓸 수 있는 모델 자동 탐색
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # 'models/' 접두사를 제거하여 이름만 추출
                clean_name = m.name.replace("models/", "")
                available_models.append(clean_name)
                
        # 쓸 수 있는 모델이 아예 없다면 키 권한 문제
        if not available_models:
            return "🚨 이 API 키로는 구글 AI를 사용할 수 없습니다. Google AI Studio에서 'Create API key in a new project'로 키를 완전히 새로 발급받아 교체해 보세요."
            
        # 스캔된 목록 중 가장 첫 번째 모델을 자동으로 낚아채서 사용
        target_model = available_models[0]
        
        # 3. 간식 리스트 텍스트화 및 프롬프트 작성
        snack_list_text = ", ".join(snacks)
        
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
        
        # 4. 동적으로 찾은 모델로 실행
        model = genai.GenerativeModel(model_name=target_model)
        response = model.generate_content(
            combined_prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.7)
        )
        
        return response.text

    except Exception as e:
        # 에러가 나면 어떤 모델을 시도했는지 화면에 같이 출력해 줍니다.
        used_model = target_model if 'target_model' in locals() else '탐색 실패'
        error_msg = f"🚨 AI 서버 통신 에러\n\n- 시도한 모델: {used_model}\n- 상세 로그: {e}"
        return error_msg
