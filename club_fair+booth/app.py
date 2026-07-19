import streamlit as st
import datetime
from saju_calculator import get_saju_data
from ai_agent_call import generate_report_with_snack

# ---------------------------------------------------------
# 1. 페이지 상태 초기화 (처음 접속했을 때 1페이지로 설정)
# ---------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 1

st.title("CWT Club Fair: Saju by the Generative AI & Snack for today")

# ==========================================
# [페이지 1] 사용자 정보 입력 화면
# ==========================================
if st.session_state.page == 1:
    st.write("Please fill below!")

    name = st.text_input("name", placeholder="ghent_university_student")

    col1, col2 = st.columns(2)
    with col1:
        calendar_type = st.radio("solar/lunar calander", ["solar", "lunar"])
        birth_date = st.date_input(
            "your birthday?",
            value=datetime.date(2000, 1, 1),
            min_value=datetime.date(1950, 1, 1),
            max_value=datetime.date.today()
        )

    with col2:
        time_unknown = st.checkbox("Don't know the exact time")
        if not time_unknown:
            birth_time = st.time_input("Birth Time", value=datetime.time(12, 0))
        else:
            birth_time = "unknown"

    # [버튼 클릭 시] 다음 페이지로 넘어가기 위한 작업
    if st.button("운세와 간식 처방받기"):
        if name:
            # 다음 페이지에서 쓸 수 있도록 입력받은 데이터를 주머니(session_state)에 저장
            st.session_state.name = name
            st.session_state.birth_date = birth_date

            # 페이지 번호를 2로 바꾸고 화면 전체 새로고침! (입력창들이 싹 사라집니다)
            st.session_state.page = 2
            st.rerun()
        else:
            st.error("Please fill the blank")

# ==========================================
# [페이지 2] 분석 로딩 및 결과 확인 화면
# ==========================================
elif st.session_state.page == 2:
    snacks = ["초코파이", "하리보 젤리", "비타민 음료", "사탕"]

    # 화면에 진입하자마자 로딩 스피너와 함께 분석 시작
    with st.spinner('AI가 사주를 분석하고 알맞은 간식을 고르고 있습니다...'):
        # 1. 주머니에 저장해둔 날짜(st.session_state.birth_date) 꺼내 쓰기
        y = st.session_state.birth_date.year
        m = st.session_state.birth_date.month
        d = st.session_state.birth_date.day

        saju_text = get_saju_data(y, m, d, 12, True)

        # 2. 주머니에 저장해둔 이름 꺼내서 AI 호출
        final_report = generate_report_with_snack(st.session_state.name, saju_text, snacks)

    # 분석이 끝나면 애니메이션과 함께 결과 출력
    st.balloons()
    st.success("처방이 완료되었습니다! 아래 결과를 확인하고 간식을 받아가세요.")
    st.info(final_report)

    # 3. 다음 사람을 위해 초기화하는 버튼
    st.write("---")
    if st.button("🔄 Next Person!"):
        st.session_state.page = 1  # 다시 1페이지로 돌리고
        st.rerun()  # 화면 새로고침!
